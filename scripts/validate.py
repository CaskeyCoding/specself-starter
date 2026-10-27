#!/usr/bin/env python3
"""Validate a your-life/ (or examples/) corpus against templates/README.md.

Stdlib only. Infers each artifact's type from its path, parses the simple
frontmatter subset the templates use (key: value, inline [a, b] lists), and
checks required fields, status enums, serves:/supersedes:/related: refs,
revealed-principle evidence, goal success criteria, and ended_on vs a
terminal status. Staged candidates have separate draft/provenance checks and
never participate in active-artifact checks. Errors exit 1; warnings print but
exit 0.
"""
import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

DATED_ITEM_RE = re.compile(r"^-\s*\d{4}-\d{2}-\d{2}\b")

REQUIRED_FIELDS = {
    "principle": {"title", "status", "kind", "domain", "confidence", "serves",
                  "created", "last_reviewed", "ended_on", "supersedes"},
    "goal": {"title", "status", "horizon", "serves", "created", "target_date",
             "last_reviewed", "ended_on"},
    "project": {"title", "status", "horizon", "serves", "created", "target_date",
                "last_reviewed", "last_moved", "ended_on"},
    "area": {"title", "status", "horizon", "serves", "created", "last_reviewed", "ended_on"},
    "habit": {"title", "status", "cadence", "serves", "created", "last_reviewed", "ended_on"},
    "vision": {"status", "horizon", "created", "last_reviewed", "ended_on", "supersedes"},
    "aspirational": {"status", "created", "last_reviewed", "ended_on"},
    "decision": {"title", "status", "date", "supersedes", "superseded_by"},
    "evidence": {"type", "date", "domain", "related"},
    "journal": {"date", "tier"},
    "review": {"date", "tier", "period"},
}

STATUS_ENUMS = {
    "principle": {"draft", "active", "contested", "retired"},
    "goal": {"draft", "active", "contested", "met", "retired"},
    "project": {"draft", "active", "contested", "shipped", "abandoned", "retired"},
    "area": {"draft", "active", "contested", "retired"},
    "habit": {"draft", "active", "lapsed", "retired"},
    "vision": {"draft", "active", "contested", "retired"},
    "aspirational": {"draft", "active", "contested", "retired"},
    "decision": {"proposed", "accepted", "superseded"},
}

TERMINAL_STATUSES = {"met", "shipped", "abandoned", "retired", "superseded"}
SINGLETONS = {"vision", "aspirational"}
WARN_EMPTY_SERVES_TYPES = {"goal", "project", "habit"}
SUCCESS_CRITERIA_HEADING = "## Success criteria (falsifiable)"
EVIDENCE_HEADING = "## Evidence"
STALE_DAYS = 90
CANDIDATE_TYPES = {"principle", "goal", "habit", "evidence"}
CANDIDATE_LOCATION = "candidates/YYYY-MM-DD/<slug>.md"
# Candidate values support plain text, quoted text, and flat inline lists.
# Quoted text may contain punctuation that would otherwise delimit a value.
CANDIDATE_SCALAR = r'''(?:"(?:[^"\\]|\\.)*"|'(?:[^']|'')*'|[^\s\[\]{},'"#][^\[\]{},'"#]*)'''
CANDIDATE_VALUE_RE = re.compile(
    rf"(?P<value>\[\s*(?:{CANDIDATE_SCALAR}(?:\s*,\s*{CANDIDATE_SCALAR})*)?\s*\]|{CANDIDATE_SCALAR})\s*(?:#.*)?"
)


def parse_candidate_value(value):
    """Parse the supported flat subset without repairing malformed syntax."""
    match = CANDIDATE_VALUE_RE.fullmatch(value.strip())
    if match is None:
        return None
    value = match.group("value").strip()
    is_list = value.startswith("[")
    tokens = re.findall(CANDIDATE_SCALAR, value[1:-1]) if is_list else [value]
    decoded = []
    for token in tokens:
        token = token.strip()
        if token.startswith('"'):
            try:
                decoded.append(json.loads(token))
            except ValueError:
                return None
        elif token.startswith("'"):
            decoded.append(token[1:-1].replace("''", "'"))
        else:
            # Mapping/alias/tag syntax is outside this flat text subset.
            if token[:1] in "&*!|>@`" or re.search(r":(?:\s|$)", token):
                return None
            decoded.append(token)
    return decoded if is_list else decoded[0]


def strip_comment(value):
    """Drop a trailing ' # ...' comment, respecting simple quoting."""
    in_quote = None
    for i, ch in enumerate(value):
        if ch in ("'", '"'):
            in_quote = None if in_quote == ch else (in_quote or ch)
        elif ch == "#" and in_quote is None:
            return value[:i]
    return value


def parse_frontmatter(text, candidate=False):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}, text
    fields = {}
    for raw in lines[1:end]:
        if ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        key = key.strip()
        if not key or not (key[0].isalpha() or key[0] == "_"):
            continue
        if candidate:
            fields[key] = parse_candidate_value(value)
            continue
        value = strip_comment(value).strip()
        if value.startswith("["):
            inner = value if value.endswith("]") else value + "]"
            inner = inner[1:-1].strip()
            items = [it.strip().strip('"').strip("'") for it in inner.split(",")] if inner else []
            fields[key] = [it for it in items if it]
        else:
            fields[key] = value.strip('"').strip("'")
    return fields, "\n".join(lines[end + 1:])


def infer_type(rel_path):
    parts = rel_path.parts
    if ".sensitive" in parts:
        return None
    if parts[0] == "candidates":
        # Only the staging root's index is structural. A draft named README.md
        # inside a dated directory must still supply provenance.
        return None if parts == ("candidates", "README.md") else "candidate"
    if rel_path.name in ("README.md", ".gitkeep"):
        return None
    # Persisted coherence reports (reviews/coherence/YYYY-MM-DD.md) are
    # machine-derived observations, not a validated artifact type
    # (persisted-coherence spec). Ignore the directory so the validator never
    # treats a regenerable report as a corpus artifact to check.
    if parts[:2] == ("reviews", "coherence"):
        return None
    if len(parts) == 1 and rel_path.name == "vision.md":
        return "vision"
    if len(parts) == 1 and rel_path.name == "aspirational.md":
        return "aspirational"
    by_top = {
        "principles": "principle", "goals": "goal", "areas": "area",
        "projects": "project", "habits": "habit", "decisions": "decision",
        "journal": "journal", "reviews": "review",
    }
    if parts[0] in by_top:
        return by_top[parts[0]]
    if parts[:2] == ("reflections", "evidence"):
        return "evidence"
    return None


def extract_section(body, heading):
    lines = body.splitlines()
    start = next((i + 1 for i, l in enumerate(lines) if l.strip() == heading), None)
    if start is None:
        return None
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[start:end]


def resolve_ref(ref, corpus):
    if ref in SINGLETONS:
        return (corpus / f"{ref}.md").is_file()
    if ":" not in ref:
        return False
    kind, slug = ref.split(":", 1)
    # References name artifact basenames, never paths. In particular, an
    # active artifact cannot use ../ to resolve a staged candidate.
    if not slug or "/" in slug or "\\" in slug:
        return False
    if kind in ("goal", "area", "project", "habit"):
        return (corpus / f"{kind}s" / f"{slug}.md").is_file()
    if kind == "principle":
        pdir = corpus / "principles"
        return pdir.is_dir() and any(pdir.glob(f"*/{slug}.md"))
    if kind == "decision":
        ddir = corpus / "decisions"
        return ddir.is_dir() and any(ddir.glob(f"{slug}-*.md"))
    return False


def nonempty_provenance(value):
    """Require text, excluding blank values and YAML null spellings."""
    return isinstance(value, str) and value.strip().lower() not in ("", "null", "~")


def check_candidate(rel, fields, errors):
    """Validate staging metadata only; a candidate is not a committed artifact."""
    loc = str(rel)
    dated_path = len(rel.parts) == 3 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", rel.parts[1])
    if dated_path:
        try:
            date.fromisoformat(rel.parts[1])
        except ValueError:
            dated_path = False
    if not dated_path:
        errors.append(f"{loc}: candidate must be staged at {CANDIDATE_LOCATION} with a valid date")

    if fields.get("type") != "candidate":
        errors.append(f"{loc}: candidate type must be 'candidate'")
    if fields.get("status") != "draft":
        errors.append(f"{loc}: candidate status must be 'draft'")
    candidate_type = fields.get("candidate_type")
    if not isinstance(candidate_type, str) or candidate_type not in CANDIDATE_TYPES:
        errors.append(f"{loc}: candidate_type must be principle | goal | habit | evidence")

    sources = fields.get("source_entries")
    if not isinstance(sources, list) or not sources or not all(nonempty_provenance(s) for s in sources):
        errors.append(f"{loc}: source_entries must be a nonempty inline list of source names or paths")
    for key in ("persona", "session_id"):
        if not nonempty_provenance(fields.get(key)):
            errors.append(f"{loc}: {key} must be nonempty provenance text")


def check_file(path, rel, atype, corpus, today, errors, warnings):
    loc = str(rel)
    fields, body = parse_frontmatter(
        path.read_text(encoding="utf-8-sig"), candidate=(atype == "candidate")
    )
    if atype == "candidate":
        check_candidate(rel, fields, errors)
        return
    if fields.get("type") == "candidate":
        errors.append(f"{loc}: candidate must be staged at {CANDIDATE_LOCATION}")

    for f in sorted(REQUIRED_FIELDS.get(atype, set())):
        if f not in fields:
            errors.append(f"{loc}: missing required field '{f}'")

    status = fields.get("status")
    if atype in STATUS_ENUMS and status is not None and status not in STATUS_ENUMS[atype]:
        enum = " | ".join(sorted(STATUS_ENUMS[atype]))
        errors.append(f"{loc}: status '{status}' not in {atype} enum ({enum})")

    for key in ("serves", "supersedes", "related"):
        value = fields.get(key)
        refs = value if isinstance(value, list) else ([value] if value else [])
        for ref in refs:
            if ref and not resolve_ref(ref, corpus):
                errors.append(f"{loc}: {key} ref '{ref}' does not resolve")

    if atype == "principle" and fields.get("kind") == "revealed":
        section = extract_section(body, EVIDENCE_HEADING)
        if section is None or not any(DATED_ITEM_RE.match(l.strip()) for l in section):
            errors.append(f"{loc}: revealed principle has no dated item under '{EVIDENCE_HEADING}'")

    if atype == "goal":
        section = extract_section(body, SUCCESS_CRITERIA_HEADING)
        if section is None or not any(l.strip().startswith(("- [ ]", "- [x]", "- [X]")) for l in section):
            errors.append(f"{loc}: no checkbox under '{SUCCESS_CRITERIA_HEADING}'")

    if "ended_on" in fields and status is not None:
        ended_on = fields.get("ended_on", "")
        terminal = status in TERMINAL_STATUSES
        if terminal and not ended_on:
            errors.append(f"{loc}: ended_on empty while status '{status}' is terminal")
        elif not terminal and ended_on:
            errors.append(f"{loc}: ended_on set while status '{status}' is non-terminal")

    if atype in WARN_EMPTY_SERVES_TYPES and isinstance(fields.get("serves"), list) and not fields["serves"]:
        warnings.append(f"{loc}: empty serves:")

    last_reviewed = fields.get("last_reviewed")
    if last_reviewed:
        try:
            lr = datetime.strptime(last_reviewed, "%Y-%m-%d").date()
            if (today - lr).days > STALE_DAYS:
                warnings.append(f"{loc}: last_reviewed {last_reviewed} is more than {STALE_DAYS} days old")
        except ValueError:
            pass


def validate(corpus):
    errors, warnings, count = [], [], 0
    today = date.today()
    for path in sorted(corpus.rglob("*.md")):
        rel = path.relative_to(corpus)
        atype = infer_type(rel)
        if atype is None:
            continue
        count += 1
        check_file(path, rel, atype, corpus, today, errors, warnings)
    return errors, warnings, count


def main():
    parser = argparse.ArgumentParser(description="Validate a SpecSelf corpus against templates/README.md.")
    parser.add_argument("--corpus", default="your-life", help="corpus root (default: your-life)")
    args = parser.parse_args()

    corpus = Path(args.corpus)
    if not corpus.is_dir():
        print(f"ERROR: corpus path '{corpus}' is not a directory")
        return 1

    errors, warnings, count = validate(corpus)
    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")

    if errors:
        print(f"FAIL: {len(errors)} error(s) across {count} file(s) in {corpus}")
        return 1

    print(f"OK: {count} file(s) validated in {corpus}, 0 error(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
