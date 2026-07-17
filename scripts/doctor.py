#!/usr/bin/env python3
"""SpecSelf doctor: prove the kit's guarantees hold, any time.

One command a new forker runs whenever they want proof the privacy posture is
intact and to see the single next step. Stdlib only, Windows + POSIX, same
conventions as scripts/validate.py and scripts/coherence.py.

Five checks:

  1. Privacy posture: your-life/** content is gitignored (probed via
     `git check-ignore` on a filename that is never created on disk, so the
     script leaves nothing behind), your-life/.sensitive/ is ignored, and the
     pre-commit guard script is reachable. In deliberate private-repo mode
     (`.specself-allow-corpus` present, or SPECSELF_ALLOW_CORPUS=1) the corpus
     is versioned on purpose, so only .sensitive-ignored and guard-reachable
     are required; the mode is named in the PASS line.
  2. Guard wiring: .claude/settings.json wires the PreToolUse guard hook and the
     SessionStart overdue nudge, the referenced scripts exist, and the
     .pre-commit-config.yaml fallback references the same guard. Assessed by
     reading files only; the fallback install state is reported, never changed
     (this script never runs `pre-commit install`).
  3. Corpus health: scripts/validate.py exit status over your-life/.
  4. Cadence state (report only, never flips the exit code): newest journal,
     review, and coherence artifacts, and which review tier is overdue. Ports
     the overdue.sh / overdue.ps1 "more than one period behind" rule; those
     scripts surface overdue state and exit 0, and check 4 inherits that.
  5. One closing line: the single next step (a foundation sitting, /adopt,
     /weekly, or /daily) derived from what exists, mirroring the
     foundation-progress resume semantics.

Exit 0 when the guarantee checks (1, 2, 3) all pass, 1 otherwise. Check 4 is a
state readout and check 5 is guidance; neither changes the exit code. The script
never writes anything and never executes a hook.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parents[1]

# Paths that are NEVER created on disk; used only as check-ignore probes.
CORPUS_PROBE = "your-life/principles/core/__doctor_probe__.md"
SENSITIVE_PROBE = "your-life/.sensitive/__doctor_probe__.md"

STRUCTURE_NAMES = {"README.md", ".gitkeep"}


# ---------------------------------------------------------------------------
# Subprocess helpers (no shell; explicit args; run from the kit root so the
# script works both "from the kit dir" and via `python scripts/doctor.py` at
# the repo root).
# ---------------------------------------------------------------------------

def run_git(args):
    try:
        proc = subprocess.run(
            ["git", *args], cwd=str(KIT_ROOT),
            capture_output=True, text=True,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError:
        return None, "", "git not found on PATH"


def run_python(args):
    proc = subprocess.run(
        [sys.executable, *args], cwd=str(KIT_ROOT),
        capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def is_ignored(path):
    """True if git ignores `path`. rc 0 = ignored, 1 = not ignored, None/128 =
    git unavailable or error (treated as not-verifiable)."""
    rc, _out, _err = run_git(["check-ignore", "-q", path])
    return rc == 0, rc


# ---------------------------------------------------------------------------
# Result plumbing
# ---------------------------------------------------------------------------

class Result:
    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.passed = True
        self.summary = ""
        self.hints = []

    def fail(self, summary, hint=None):
        self.passed = False
        self.summary = summary
        if hint:
            self.hints.append(hint)

    def ok(self, summary):
        self.summary = summary

    def render(self):
        status = "PASS" if self.passed else "FAIL"
        lines = [f"{status}  Check {self.number} {self.name}: {self.summary}"]
        for h in self.hints:
            lines.append(f"      hint: {h}")
        return lines


# ---------------------------------------------------------------------------
# Check 1: privacy posture
# ---------------------------------------------------------------------------

def check_privacy():
    r = Result(1, "privacy posture")
    allow_corpus = (
        (KIT_ROOT / ".specself-allow-corpus").is_file()
        or os.environ.get("SPECSELF_ALLOW_CORPUS") == "1"
    )

    sensitive_ignored, sens_rc = is_ignored(SENSITIVE_PROBE)
    corpus_ignored, corp_rc = is_ignored(CORPUS_PROBE)
    guard = KIT_ROOT / ".claude" / "hooks" / "guard-corpus-commit.sh"
    guard_reachable = guard.is_file()

    if sens_rc is None:
        r.fail(
            "cannot verify (git not found on PATH)",
            "install git so the doctor can probe your ignore rules.",
        )
        return r

    problems = []
    if not sensitive_ignored:
        problems.append("your-life/.sensitive/ is NOT gitignored")
        r.hints.append(
            "restore the '**/.sensitive/' rule in .gitignore; the escape hatch "
            "must never be committable."
        )
    if not allow_corpus and not corpus_ignored:
        problems.append("your-life/** corpus content is NOT gitignored")
        r.hints.append(
            "restore the 'your-life/**' block in .gitignore, or run "
            "scripts/set-privacy-mode.sh --private for a deliberate private repo."
        )
    if not guard_reachable:
        problems.append(".claude/hooks/guard-corpus-commit.sh is missing")
        r.hints.append("the pre-commit guard script is gone; restore it from the kit.")

    if problems:
        r.passed = False
        r.summary = "; ".join(problems)
        return r

    mode = "private mode (corpus versioned deliberately)" if allow_corpus else "public mode"
    if allow_corpus:
        r.ok(
            f"{mode}; .sensitive/ ignored and the pre-commit guard is reachable "
            "(secrets stay blocked either way)."
        )
    else:
        r.ok(
            f"{mode}; your-life/** corpus and .sensitive/ are gitignored and the "
            "pre-commit guard is reachable."
        )
    return r


# ---------------------------------------------------------------------------
# Check 2: guard wiring (read-only)
# ---------------------------------------------------------------------------

def _hook_commands(block):
    """Yield each hook command string from a settings.json hook block list."""
    for entry in block or []:
        for hook in entry.get("hooks", []):
            cmd = hook.get("command")
            if isinstance(cmd, str):
                yield cmd


def check_guard_wiring():
    r = Result(2, "guard wiring")
    settings_path = KIT_ROOT / ".claude" / "settings.json"

    if not settings_path.is_file():
        r.fail(
            ".claude/settings.json is missing",
            "restore .claude/settings.json so the PreToolUse guard and SessionStart nudge wire up.",
        )
        return r
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, OSError) as exc:
        r.fail(
            f".claude/settings.json is not valid JSON ({exc.__class__.__name__})",
            "fix the JSON in .claude/settings.json.",
        )
        return r

    hooks = settings.get("hooks", {})
    pretool_cmds = list(_hook_commands(hooks.get("PreToolUse")))
    session_cmds = list(_hook_commands(hooks.get("SessionStart")))

    problems = []
    if not any("guard-corpus-commit-hook.sh" in c for c in pretool_cmds):
        problems.append("PreToolUse guard hook not wired in settings.json")
    if not any("overdue.sh" in c for c in session_cmds):
        problems.append("SessionStart overdue nudge not wired in settings.json")

    # Referenced scripts must exist.
    referenced = {
        ".claude/hooks/guard-corpus-commit-hook.sh": KIT_ROOT / ".claude" / "hooks" / "guard-corpus-commit-hook.sh",
        ".claude/hooks/guard-corpus-commit.sh": KIT_ROOT / ".claude" / "hooks" / "guard-corpus-commit.sh",
        "scripts/overdue.sh": KIT_ROOT / "scripts" / "overdue.sh",
    }
    for rel, path in referenced.items():
        if not path.is_file():
            problems.append(f"referenced script missing: {rel}")

    # Pre-commit fallback config must reference the same guard.
    precommit_cfg = KIT_ROOT / ".pre-commit-config.yaml"
    if not precommit_cfg.is_file():
        problems.append(".pre-commit-config.yaml fallback is missing")
    elif "guard-corpus-commit.sh" not in precommit_cfg.read_text(encoding="utf-8-sig"):
        problems.append(".pre-commit-config.yaml does not reference the guard")

    if problems:
        r.passed = False
        r.summary = "; ".join(problems)
        r.hints.append(
            "the corpus guard is not fully wired; restore .claude/settings.json, "
            "the hook scripts, and .pre-commit-config.yaml from the kit."
        )
        return r

    # Install state of the pre-commit fallback: report, never install.
    if shutil.which("pre-commit"):
        install_note = "pre-commit is on PATH; activate the fallback with 'pre-commit install'."
    else:
        install_note = "activate the fallback with 'pip install pre-commit && pre-commit install'."
    r.ok(
        "settings.json wires the PreToolUse guard and SessionStart nudge, the hook "
        f"scripts exist, and the pre-commit fallback is configured. {install_note}"
    )
    return r


# ---------------------------------------------------------------------------
# Check 3: corpus health
# ---------------------------------------------------------------------------

def check_corpus_health():
    r = Result(3, "corpus health")
    validate = KIT_ROOT / "scripts" / "validate.py"
    if not validate.is_file():
        r.fail("scripts/validate.py is missing", "restore scripts/validate.py from the kit.")
        return r
    rc, out, _err = run_python([str(validate), "--corpus", "your-life"])
    tail = out.strip().splitlines()[-1] if out.strip() else ""
    if rc == 0:
        r.ok(f"scripts/validate.py passes over your-life/. {tail}")
    else:
        r.fail(
            f"scripts/validate.py reports errors over your-life/. {tail}",
            "run 'python scripts/validate.py' and fix the reported errors.",
        )
    return r


# ---------------------------------------------------------------------------
# Check 4: cadence state (report only; ports overdue.sh / overdue.ps1)
# ---------------------------------------------------------------------------

WEEK_RE = re.compile(r"^(\d{4})-W(\d{2})")
QUARTER_RE = re.compile(r"^(\d{4})-Q([1-4])")
MONTH_RE = re.compile(r"^(\d{4})-(0[1-9]|1[0-2])")
YEAR_RE = re.compile(r"^(\d{4})")
DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")


def _newest_review_tokens(reviews_dir):
    """Return {tier: newest_token} scanning review filenames, mirroring overdue.sh."""
    latest = {"weekly": None, "quarterly": None, "monthly": None, "annual": None}
    if not reviews_dir.is_dir():
        return latest
    for f in sorted(reviews_dir.iterdir()):
        if not f.is_file():
            continue
        base = f.name
        m = WEEK_RE.match(base)
        if m:
            tok = f"{m.group(1)}-W{m.group(2)}"
            if latest["weekly"] is None or tok > latest["weekly"]:
                latest["weekly"] = tok
            continue
        m = QUARTER_RE.match(base)
        if m:
            tok = f"{m.group(1)}-Q{m.group(2)}"
            if latest["quarterly"] is None or tok > latest["quarterly"]:
                latest["quarterly"] = tok
            continue
        m = MONTH_RE.match(base)
        if m:
            tok = f"{m.group(1)}-{m.group(2)}"
            if latest["monthly"] is None or tok > latest["monthly"]:
                latest["monthly"] = tok
            continue
        m = YEAR_RE.match(base)
        if m:
            tok = m.group(1)
            if latest["annual"] is None or tok > latest["annual"]:
                latest["annual"] = tok
    return latest


def _newest_dated(directory):
    """Newest YYYY-MM-DD stem in a directory (journal or coherence). None if empty."""
    if not directory.is_dir():
        return None
    newest = None
    for f in sorted(directory.iterdir()):
        if not f.is_file():
            continue
        m = DATE_RE.match(f.stem)
        if m and (newest is None or f.stem > newest):
            newest = f.stem
    return newest


def _overdue_tiers(latest, today):
    """Which tiers are more than one period behind, per overdue.sh's diff > 1 rule."""
    overdue = []
    iso = today.isocalendar()
    now_gyear, now_week = iso[0], iso[1]

    if latest["weekly"]:
        m = WEEK_RE.match(latest["weekly"])
        ly, lw = int(m.group(1)), int(m.group(2))
        now_monday = date.fromisocalendar(now_gyear, now_week, 1)
        latest_monday = date.fromisocalendar(ly, lw, 1)
        if (now_monday - latest_monday).days // 7 > 1:
            overdue.append(f"weekly (latest {latest['weekly']})")

    if latest["monthly"]:
        ly, lm = latest["monthly"].split("-")
        now_idx = today.year * 12 + today.month
        latest_idx = int(ly) * 12 + int(lm)
        if now_idx - latest_idx > 1:
            overdue.append(f"monthly (latest {latest['monthly']})")

    if latest["quarterly"]:
        ly, lq = latest["quarterly"].split("-Q")
        now_q = (today.month - 1) // 3 + 1
        now_idx = today.year * 4 + now_q
        latest_idx = int(ly) * 4 + int(lq)
        if now_idx - latest_idx > 1:
            overdue.append(f"quarterly (latest {latest['quarterly']})")

    if latest["annual"]:
        if today.year - int(latest["annual"]) > 1:
            overdue.append(f"annual (latest {latest['annual']})")

    return overdue


def check_cadence(today):
    """Report-only. Returns (Result, cadence_state dict). Never fails."""
    r = Result(4, "cadence state")
    reviews_dir = KIT_ROOT / "your-life" / "reviews"
    journal_dir = KIT_ROOT / "your-life" / "journal"
    coherence_dir = reviews_dir / "coherence"

    latest = _newest_review_tokens(reviews_dir)
    newest_journal = _newest_dated(journal_dir)
    newest_coherence = _newest_dated(coherence_dir)
    overdue = _overdue_tiers(latest, today)

    have_any_review = any(latest.values())
    state = {
        "latest_reviews": latest,
        "newest_journal": newest_journal,
        "newest_coherence": newest_coherence,
        "overdue": overdue,
        "have_any_review": have_any_review,
    }

    if not have_any_review and newest_journal is None and newest_coherence is None:
        r.ok("no cadence artifacts yet; the loop begins once you start writing.")
        return r, state

    parts = []
    parts.append(f"newest journal: {newest_journal or 'none'}")
    review_bits = [f"{tier} {tok}" for tier, tok in latest.items() if tok]
    parts.append("newest reviews: " + (", ".join(review_bits) if review_bits else "none"))
    parts.append(f"newest coherence: {newest_coherence or 'none'}")
    if overdue:
        parts.append("overdue: " + "; ".join(overdue))
    else:
        parts.append("overdue: none")
    r.ok(". ".join(parts) + ".")
    return r, state


# ---------------------------------------------------------------------------
# Check 5: the single next step (mirrors foundation-progress resume semantics)
# ---------------------------------------------------------------------------

SITTING_HEADER_RE = re.compile(r"^##\s+Sitting\s+(\d+)\b(.*)$")


def _corpus_has_content():
    """True if any authored corpus artifact exists under your-life/ (anything
    beyond committed structure and the foundation-progress checklist)."""
    corpus = KIT_ROOT / "your-life"
    if not corpus.is_dir():
        return False
    progress = corpus / "reflections" / "foundation-progress.md"
    for path in corpus.rglob("*.md"):
        if path.name in STRUCTURE_NAMES:
            continue
        if path == progress:
            continue
        return True
    return False


def _next_incomplete_sitting():
    """Lowest-numbered sitting not yet completed in foundation-progress.md, or
    None if the file is absent or all sittings are complete. Mirrors the
    foundation skill's resume read: a sitting block with 'Completed:' is done;
    'Not yet run' (or no Completed line) is pending."""
    progress = KIT_ROOT / "your-life" / "reflections" / "foundation-progress.md"
    if not progress.is_file():
        return None, False  # (next sitting, file present)
    text = progress.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    # Split into sitting blocks.
    blocks = {}
    current = None
    for line in lines:
        m = SITTING_HEADER_RE.match(line)
        if m:
            current = int(m.group(1))
            blocks[current] = {"header": m.group(2).strip(), "body": []}
            continue
        if current is not None:
            blocks[current]["body"].append(line)
    if not blocks:
        return None, True
    for number in sorted(blocks):
        body = "\n".join(blocks[number]["body"])
        completed = re.search(r"^-\s*Completed:\s*\S", body, re.MULTILINE)
        if not completed:
            return number, True
    return None, True  # all complete


def _sitting_phase_label(number):
    return {
        1: "sitting 1 (Operating System + Load-Bearing Values)",
        2: "sitting 2 (Life Chapters + Domain Audit)",
        3: "sitting 3 (Failure Modes + Energy)",
        4: "sitting 4 (Trajectory + wrap)",
    }.get(number, f"sitting {number}")


def next_step(cadence_state):
    """Return the single next-step line (no PASS/FAIL; guidance only)."""
    next_sitting, progress_present = _next_incomplete_sitting()

    if progress_present:
        if next_sitting is not None:
            return f"Next: run /foundation to resume {_sitting_phase_label(next_sitting)}."
        # Foundation complete; move into the loop.
        return _loop_step(cadence_state)

    # No progress file.
    if _corpus_has_content():
        return _loop_step(cadence_state)
    return (
        "Next: run /foundation (sitting 1) to seed your stack, or /adopt if you "
        "arrive with existing notes."
    )


def _loop_step(cadence_state):
    if not cadence_state["have_any_review"]:
        return "Next: run /weekly for your first weekly review."
    weekly_overdue = any(o.startswith("weekly") for o in cadence_state["overdue"])
    if weekly_overdue:
        return "Next: run /weekly; your weekly review is overdue."
    return "Next: run /daily to capture today, then /weekly at the end of the week."


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="SpecSelf doctor: prove the kit's privacy guarantees hold and show the next step."
    )
    parser.add_argument(
        "--today", default=None,
        help="override today's date (YYYY-MM-DD) for deterministic cadence checks; default date.today().",
    )
    args = parser.parse_args()

    if args.today:
        try:
            today = datetime.strptime(args.today, "%Y-%m-%d").date()
        except ValueError:
            print(f"ERROR: --today '{args.today}' is not YYYY-MM-DD")
            return 1
    else:
        today = date.today()

    print(f"SpecSelf doctor ({KIT_ROOT.name})")
    print("")

    guarantees = [check_privacy(), check_guard_wiring(), check_corpus_health()]
    cadence_result, cadence_state = check_cadence(today)

    for r in guarantees:
        for line in r.render():
            print(line)
    for line in cadence_result.render():
        print(line)

    print("")
    print(next_step(cadence_state))
    print("")

    failed = [r for r in guarantees if not r.passed]
    if failed:
        names = ", ".join(f"check {r.number}" for r in failed)
        print(f"FAIL: {len(failed)} guarantee check(s) failing ({names}).")
        return 1
    print("OK: all guarantee checks pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
