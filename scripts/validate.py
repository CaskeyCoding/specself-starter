#!/usr/bin/env python3
"""Validate a your-life/ (or examples/) corpus against templates/README.md.

Stdlib only. Infers each artifact's type from its path, parses the simple
frontmatter subset the templates use (key: value, inline [a, b] lists), and
checks required fields, status enums, serves:/supersedes:/related: refs,
revealed-principle evidence, goal success criteria, and ended_on vs a
terminal status. Errors exit 1; warnings print but exit 0.
"""
import argparse
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


def strip_comment(value):
    """Drop a trailing ' # ...' comment, respecting simple quoting."""
    in_quote = None
    for i, ch in enumerate(value):
        if ch in ("'", '"'):
            in_quote = None if in_quote == ch else (in_quote or ch)
        elif ch == "#" and in_quote is None:
            return value[:i]
    return value


def parse_frontmatter(text):
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
    if ".sensitive" in parts or rel_path.name in ("README.md", ".gitkeep"):
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
    if kind in ("goal", "area", "project", "habit"):
        return (corpus / f"{kind}s" / f"{slug}.md").is_file()
    if kind == "principle":
        pdir = corpus / "principles"
        return pdir.is_dir() and any(pdir.glob(f"*/{slug}.md"))
    if kind == "decision":
        ddir = corpus / "decisions"
        return ddir.is_dir() and any(ddir.glob(f"{slug}-*.md"))
    return False


def check_file(path, rel, atype, corpus, today, errors, warnings):
    loc = str(rel)
    fields, body = parse_frontmatter(path.read_text(encoding="utf-8-sig"))

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
