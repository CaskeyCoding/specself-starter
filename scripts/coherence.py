#!/usr/bin/env python3
"""Run the six coherence checks (steering/coherence.md) against a SpecSelf corpus.

Stdlib only. `steering/coherence.md` is the spec this script implements; read it
before changing check semantics. Coherence is advisory by design ("report the
gaps as questions, never as edits" -- coherence.md line 6), so this script never
exits 1 for a finding, only for a genuine usage error (bad corpus path, bad
--today). It prints a deterministic report and always returns 0 on a clean run.

What each of the six checks does, and where its numbers come from:

1. Orphan (upward) -- active projects need a `serves:` link to an active goal;
   active goals need `serves:` to include `vision` or a `principle:`. An empty
   `serves:` is flagged either way per coherence.md line 37 ("a mistake or a
   deliberate orphan -- flag it either way"), as a finding, not an error.

2. Contradiction -- coherence.md gives NO mechanical rule for this (section
   "2. Contradiction check" is a single sentence plus a worked-example finding;
   detecting semantic conflict between a goal/project and a principle requires
   reading the prose, which is exactly the judgment coherence.md reserves for
   the human/agent session, not a script). Any keyword/heuristic match here
   would be an invented rule, not one sourced from the doc, so this check is
   deliberately NOT implemented; the report says so and defers to persona
   review (see AGENTS.md / personas/skeptic.md).

3. Starvation (downward) -- flags an active `area` with zero dated `evidence`
   records (reflections/evidence/*.md, `domain:` field) in the last N days.
   coherence.md never states N as a rule; its own worked example uses "3
   weeks" / "21d" (lines 61-62, 96), so 21 days is this script's default,
   overridable via --starvation-days. Note the mechanical limitation: this
   only works when an area's file basename matches a `schemas/enums.yaml`
   domain value (true for `health` in examples/sam-rivers; an area like
   `side-business` has no domain-enum counterpart and will never show
   evidence under this check).

4. Capacity -- coherence.md (line 65) says only "realistic bandwidth," with no
   number anywhere in the kit. The two ceilings (--project-ceiling,
   --goal-ceiling) are therefore this SCRIPT's own convention, not sourced
   from the doc -- said plainly here and in --help so nobody mistakes the
   default for a documented rule. What coherence.md's own worked example (line
   68-69, 97) *does* give mechanically is "stalled": active projects with no
   movement. Projects (only) carry `last_moved:`; a project not moved in
   --stalled-days is "stalled," and the capacity line reports both counts,
   mirroring "(7 active projects, 5 stalled)".

5. Staleness -- an active/non-terminal artifact whose `last_reviewed` is older
   than --stale-days is flagged "recommend contested." Default 90 days mirrors
   validate.py's STALE_DAYS and lines up with steering/cadence.md's quarterly
   tier (the doc's own "primary pruning tier," ~90 days apart) -- the closest
   mechanical stand-in for "past its cadence" (coherence.md line 73) without
   re-deriving free-text evidence dates. `vision` and `aspirational` are
   deliberately EXCLUDED: their cadence is annual (cadence.md), so a flat
   90-day/"recommend contested" verdict would misfire on a singleton that is
   working exactly as designed.

6. Revealed/aspirational drift -- two mechanical proxies, since coherence.md
   (line 81-82) asks for "new evidence" without defining how much:
   (a) a `kind: revealed` principle with no dated item under its own
       `## Evidence` section within --stale-days is flagged as a
       drift-from-revealed candidate (evidence stopped accumulating);
   (b) an `aspirational.md` entry (an H2 section with `- domain:` and
       `- added:` bullets) with at least --promotion-evidence-count dated
       `evidence` records of the same domain, dated on/after its `added:`
       date, is flagged a promotion candidate. That count is NOT sourced from
       coherence.md either (only a corpus's own aspirational entry states its
       personal promotion bar, e.g. examples/sam-rivers's "four consecutive
       weeks" -- that is corpus content, not steering, so it is not hardcoded
       here); it is a tunable flag with a documented default.

Determinism: pass --today YYYY-MM-DD to fix "now" for the two date-relative
checks (staleness, starvation, staleness-based drift); omitting it defaults to
date.today(), which makes two runs on different days differ by design.

Usage:
    python scripts/coherence.py examples/sam-rivers --today 2026-07-15
    python scripts/coherence.py your-life
"""
import argparse
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Frontmatter parsing -- mirrors scripts/validate.py's parser (copied, not
# imported, so the two scripts stay independently runnable/deployable; keep
# in sync by hand if validate.py's frontmatter subset ever changes).
# ---------------------------------------------------------------------------

DATED_ITEM_RE = re.compile(r"^-\s*(\d{4}-\d{2}-\d{2})\b")
EVIDENCE_HEADING = "## Evidence"
TERMINAL_STATUSES = {"met", "shipped", "abandoned", "retired", "superseded"}


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
    """Subset of validate.py's infer_type -- only the types the six checks need."""
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


def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def as_list(value):
    if isinstance(value, list):
        return value
    return [value] if value else []


# ---------------------------------------------------------------------------
# Corpus loading
# ---------------------------------------------------------------------------

def load_corpus(corpus):
    """Return {artifact_type: [(rel_path, fields, body), ...]}, sorted for determinism."""
    records = {}
    for path in sorted(corpus.rglob("*.md")):
        rel = path.relative_to(corpus)
        atype = infer_type(rel)
        if atype is None:
            continue
        fields, body = parse_frontmatter(path.read_text(encoding="utf-8-sig"))
        records.setdefault(atype, []).append((rel, fields, body))
    return records


def principle_exists(corpus, slug):
    pdir = corpus / "principles"
    return pdir.is_dir() and any(pdir.glob(f"*/{slug}.md"))


# ---------------------------------------------------------------------------
# Check 1: Orphan (upward)
# ---------------------------------------------------------------------------

def check_orphans(records, corpus):
    findings = []
    for rel, fields, _body in records.get("project", []):
        if fields.get("status") != "active":
            continue
        slug = rel.stem
        serves = as_list(fields.get("serves"))
        if not serves:
            findings.append(f"project:{slug} -> empty serves: (mistake or deliberate orphan)")
            continue
        resolved = False
        for ref in serves:
            if ref.startswith("goal:"):
                gslug = ref.split(":", 1)[1]
                gpath = corpus / "goals" / f"{gslug}.md"
                if gpath.is_file():
                    gfields, _ = parse_frontmatter(gpath.read_text(encoding="utf-8-sig"))
                    if gfields.get("status") == "active":
                        resolved = True
                        break
        if not resolved:
            findings.append(f"project:{slug} -> serves {serves} resolves to no active goal")

    for rel, fields, _body in records.get("goal", []):
        if fields.get("status") != "active":
            continue
        slug = rel.stem
        serves = as_list(fields.get("serves"))
        if not serves:
            findings.append(f"goal:{slug} -> empty serves: (mistake or deliberate orphan)")
            continue
        resolved = any(ref == "vision" and (corpus / "vision.md").is_file() for ref in serves) or any(
            ref.startswith("principle:") and principle_exists(corpus, ref.split(":", 1)[1]) for ref in serves
        )
        if not resolved:
            findings.append(f"goal:{slug} -> serves {serves} resolves to no vision/principle")

    return sorted(findings)


# ---------------------------------------------------------------------------
# Check 3: Starvation (downward)
# ---------------------------------------------------------------------------

def check_starvation(records, corpus, today, window_days):
    evidence_by_domain = {}
    for _rel, fields, _body in records.get("evidence", []):
        d = parse_date(fields.get("date"))
        if d is None:
            continue
        evidence_by_domain.setdefault(fields.get("domain"), []).append(d)

    cutoff = today - timedelta(days=window_days)
    findings = []
    for rel, fields, _body in records.get("area", []):
        if fields.get("status") != "active":
            continue
        slug = rel.stem
        recent = [d for d in evidence_by_domain.get(slug, []) if d >= cutoff]
        if not recent:
            findings.append(f"area:{slug} -> 0 dated evidence (domain '{slug}') in {window_days}d")
    return sorted(findings)


# ---------------------------------------------------------------------------
# Check 4: Capacity
# ---------------------------------------------------------------------------

def check_capacity(records, today, project_ceiling, goal_ceiling, stalled_days):
    active_projects = [(rel, f) for rel, f, _b in records.get("project", []) if f.get("status") == "active"]
    active_goals = [(rel, f) for rel, f, _b in records.get("goal", []) if f.get("status") == "active"]

    stalled = []
    for rel, fields in active_projects:
        lm = parse_date(fields.get("last_moved"))
        if lm is None or (today - lm).days > stalled_days:
            stalled.append(rel.stem)
    stalled.sort()

    over = len(active_projects) > project_ceiling or len(active_goals) > goal_ceiling
    detail = (
        f"{len(active_projects)} active project(s) (ceiling {project_ceiling}), "
        f"{len(stalled)} stalled (no last_moved in {stalled_days}d), "
        f"{len(active_goals)} active goal(s) (ceiling {goal_ceiling})"
    )
    return over, detail, stalled


# ---------------------------------------------------------------------------
# Check 5: Staleness
# ---------------------------------------------------------------------------

# vision/aspirational deliberately excluded -- annual cadence, see module docstring.
STALENESS_TYPES = ("principle", "goal", "project", "area", "habit")


def check_staleness(records, today, stale_days):
    findings = []
    for atype in STALENESS_TYPES:
        for rel, fields, _body in records.get(atype, []):
            status = fields.get("status")
            if status in TERMINAL_STATUSES:
                continue
            lr = parse_date(fields.get("last_reviewed"))
            if lr is None:
                continue
            age = (today - lr).days
            if age > stale_days:
                findings.append(
                    f"{atype}:{rel.stem} -> last_reviewed {fields.get('last_reviewed')} "
                    f"({age}d old, > {stale_days}d); recommend contested"
                )
    return sorted(findings)


# ---------------------------------------------------------------------------
# Check 6: Revealed/aspirational drift
# ---------------------------------------------------------------------------

def parse_aspirational_entries(path):
    """Parse aspirational.md's H2 entries. Assumes each candidate is an H2
    heading (its slug) followed by `- domain: X` / `- added: YYYY-MM-DD`
    bullets, per examples/sam-rivers's shape. The `## Graduated` section is
    skipped (those have already been promoted, not candidates)."""
    if not path.is_file():
        return []
    entries = []
    current = None
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("## "):
            if current:
                entries.append(current)
            heading = line[3:].strip()
            current = None if heading.lower() == "graduated" else {"slug": heading, "domain": None, "added": None}
            continue
        if current is None:
            continue
        m = re.match(r"-\s*domain:\s*(\S+)", line.strip())
        if m:
            current["domain"] = m.group(1)
        m = re.match(r"-\s*added:\s*(\S+)", line.strip())
        if m:
            current["added"] = m.group(1)
    if current:
        entries.append(current)
    return entries


def check_drift(records, corpus, today, stale_days, promotion_evidence_count):
    findings = []
    cutoff = today - timedelta(days=stale_days)

    for rel, fields, body in records.get("principle", []):
        if fields.get("kind") != "revealed" or fields.get("status") in TERMINAL_STATUSES:
            continue
        section = extract_section(body, EVIDENCE_HEADING)
        dated = []
        for line in section or []:
            m = DATED_ITEM_RE.match(line.strip())
            if m:
                d = parse_date(m.group(1))
                if d:
                    dated.append(d)
        if not any(d >= cutoff for d in dated):
            findings.append(
                f"principle:{rel.stem} -> revealed, no dated evidence in {stale_days}d; "
                f"drift-from-revealed candidate"
            )

    evidence_records = records.get("evidence", [])
    for entry in parse_aspirational_entries(corpus / "aspirational.md"):
        if not entry["domain"] or not entry["added"]:
            continue
        added = parse_date(entry["added"])
        if added is None:
            continue
        matches = 0
        for _rel, fields, _body in evidence_records:
            if fields.get("domain") != entry["domain"]:
                continue
            d = parse_date(fields.get("date"))
            if d and d >= added:
                matches += 1
        if matches >= promotion_evidence_count:
            findings.append(
                f"aspirational:{entry['slug']} -> {matches} dated evidence entries "
                f"(domain {entry['domain']}) since {entry['added']}; promotion candidate"
            )

    return sorted(findings)


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def build_report(corpus, records, today, args):
    orphans = check_orphans(records, corpus)
    starved = check_starvation(records, corpus, today, args.starvation_days)
    over_capacity, capacity_detail, _stalled = check_capacity(
        records, today, args.project_ceiling, args.goal_ceiling, args.stalled_days
    )
    stale = check_staleness(records, today, args.stale_days)
    drift = check_drift(records, corpus, today, args.stale_days, args.promotion_evidence_count)

    lines = [f"Coherence - {today.isoformat()} ({corpus})", ""]

    lines.append(f"Orphans:        {len(orphans)}")
    lines.extend(f"  {f}" for f in orphans)

    lines.append("Contradictions: not mechanically checkable, deferred to persona review "
                 "(see script docstring / personas/skeptic.md)")

    lines.append(f"Starved areas:  {len(starved)}")
    lines.extend(f"  {f}" for f in starved)

    lines.append(f"Over-capacity:  {'yes' if over_capacity else 'no'} ({capacity_detail})")

    lines.append(f"Stale:          {len(stale)}")
    lines.extend(f"  {f}" for f in stale)

    lines.append(f"Drift:          {len(drift)}")
    lines.extend(f"  {f}" for f in drift)

    lines.append("")
    lines.append(
        "Mechanical findings only; ranking the single sharpest question is a "
        "persona judgment call (steering/coherence.md) that this script does not attempt."
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Run the six coherence checks from steering/coherence.md against a SpecSelf corpus."
    )
    parser.add_argument("corpus", nargs="?", default="your-life", help="corpus root (default: your-life)")
    parser.add_argument(
        "--today", default=None,
        help="override today's date (YYYY-MM-DD) for deterministic, reproducible runs; default date.today()",
    )
    parser.add_argument(
        "--starvation-days", type=int, default=21,
        help="starvation window in days (default 21 = coherence.md's own worked example, '3 weeks'/'21d')",
    )
    parser.add_argument(
        "--stale-days", type=int, default=90,
        help="staleness window in days for goal/project/principle/area/habit (default 90, "
             "~one quarterly cadence tier per steering/cadence.md; mirrors validate.py's STALE_DAYS)",
    )
    parser.add_argument(
        "--stalled-days", type=int, default=7,
        help="a project with no last_moved in this many days counts as 'stalled' for the capacity "
             "check (default 7, matching coherence.md's own worked example: 'Last week ... zero movement')",
    )
    parser.add_argument(
        "--project-ceiling", type=int, default=3,
        help="active-project capacity ceiling. NOT sourced from coherence.md (it names no number, only "
             "'realistic bandwidth') -- this is this script's own tunable convention, override freely",
    )
    parser.add_argument(
        "--goal-ceiling", type=int, default=3,
        help="active-goal capacity ceiling. Same caveat as --project-ceiling: not doc-sourced.",
    )
    parser.add_argument(
        "--promotion-evidence-count", type=int, default=3,
        help="dated evidence entries (matching domain, since the aspirational entry's 'added' date) "
             "needed to flag a promotion candidate. Not sourced from coherence.md; tune per corpus.",
    )
    args = parser.parse_args()

    corpus = Path(args.corpus)
    if not corpus.is_dir():
        print(f"ERROR: corpus path '{corpus}' is not a directory")
        return 1

    if args.today:
        today = parse_date(args.today)
        if today is None:
            print(f"ERROR: --today '{args.today}' is not YYYY-MM-DD")
            return 1
    else:
        today = date.today()

    records = load_corpus(corpus)
    print(build_report(corpus, records, today, args))
    return 0


if __name__ == "__main__":
    sys.exit(main())
