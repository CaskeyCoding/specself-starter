"""Delegate checks to a local kit; display capture/review guidance read-only.

The installed package deliberately contains no corpus or kit data. Locate a
checkout from the corpus, working directory, or editable/source installation.
"""
import argparse
from pathlib import Path
import subprocess
import sys


TIERS = ("daily", "weekly", "monthly", "quarterly", "annual")
COHERENCE_OPTIONS = {
    "today": "date override (YYYY-MM-DD)",
    "starvation-days": "evidence window in days",
    "stale-days": "staleness window in days",
    "stalled-days": "project movement window in days",
    "project-ceiling": "active-project capacity ceiling",
    "goal-ceiling": "active-goal capacity ceiling",
    "promotion-evidence-count": "dated evidence count for a promotion candidate",
    "write": "persist a derived coherence report to DIR (explicit opt-in)",
    "tier": "tier label for a persisted coherence report",
}


def build_parser():
    parser = argparse.ArgumentParser(
        prog="specself", description="Local tools for a SpecSelf kit checkout.",
        allow_abbrev=False,
    )
    commands = parser.add_subparsers(dest="command", required=True)
    descriptions = {
        "doctor": "check kit guarantees, corpus health, cadence, and next step",
        "coherence": "run the existing six-check coherence report",
        "capture": "show capture instructions and template, without writing",
        "review": "show cadence guidance and a review template, without writing",
    }
    for name, description in descriptions.items():
        command = commands.add_parser(
            name, help=description, description=description, allow_abbrev=False,
        )
        command.add_argument("corpus", nargs="?", help="corpus directory (default: your-life)")
        command.add_argument("--corpus", dest="corpus_option", metavar="DIR", help="alternative to the positional corpus")
        if name == "doctor":
            command.add_argument("--today", help="date override (YYYY-MM-DD)")
        elif name == "coherence":
            for option, help_text in COHERENCE_OPTIONS.items():
                command.add_argument("--" + option, help=help_text + "; passed to scripts/coherence.py")
            command.epilog = "Defaults and check semantics are owned by scripts/coherence.py."
        else:
            command.add_argument(
                "--dry-run", action="store_true",
                help="explicit read-only preview (also the default)",
            )
            if name == "review":
                command.add_argument("--tier", choices=TIERS, default="weekly", help="review tier (default: weekly)")
    return parser


def find_kit(corpus):
    """Prefer the corpus's kit, then cwd's kit, then a source installation."""
    for start in (corpus.resolve(), Path.cwd().resolve(), Path(__file__).resolve().parent):
        for root in (start, *start.parents):
            if all((root / relative).is_file() for relative in (
                "scripts/doctor.py", "scripts/coherence.py", "steering/cadence.md",
                "templates/journal-entry.md",
            )):
                return root
    raise FileNotFoundError(
        "no SpecSelf kit checkout found; run from a kit checkout or point --corpus "
        "to a corpus inside one. The installed package does not bundle kit data."
    )


def show_guidance(kit, corpus, command, tier=None):
    if command == "capture":
        sources = (".claude/commands/capture.md", "templates/journal-entry.md")
    else:
        template = "journal-entry.md" if tier == "daily" else f"review-{tier}.md"
        sources = ("steering/cadence.md", f"templates/{template}")
    # Load only the bounded kit resources, never the corpus. Load everything
    # before printing so a missing template cannot look like a complete preview.
    documents = [(relative, (kit / relative).read_text(encoding="utf-8-sig")) for relative in sources]
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(f"Read-only {command} preview for {corpus}" + (f" ({tier})" if tier else ""))
    print("No files were created or changed. The instructions below describe a human-led session;")
    print("this command displays them without executing the workflow. Template paths use your-life/")
    print("as a placeholder for the selected corpus. The human decides and commits.\n")
    for relative, content in documents:
        print(f"--- {relative} ---")
        print(content.rstrip())
        print()
    return 0


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.corpus is not None and args.corpus_option is not None:
        parser.error("choose either positional corpus or --corpus, not both")
    corpus = Path(args.corpus_option or args.corpus or "your-life")
    try:
        kit = None
        if args.command == "doctor" and args.corpus is None and args.corpus_option is None:
            # Match doctor's historical kit-relative default from any cwd.
            kit = find_kit(Path.cwd())
            corpus = kit / "your-life"
        if ".sensitive" in corpus.parts or ".sensitive" in corpus.resolve().parts:
            print("ERROR: .sensitive/ is a private escape hatch and cannot be a corpus", file=sys.stderr)
            return 1
        if not corpus.is_dir():
            print(f"ERROR: corpus path '{corpus}' is not a directory", file=sys.stderr)
            return 1
        kit = kit or find_kit(corpus)
        if args.command in ("capture", "review"):
            return show_guidance(kit, corpus, args.command, getattr(args, "tier", None))
        script = kit / "scripts" / f"{args.command}.py"
        if args.command == "doctor":
            # doctor's historical default is relative to its own kit root.
            # Normalize the caller-selected corpus for that script convention.
            try:
                doctor_corpus = corpus.resolve().relative_to(kit)
            except ValueError:
                doctor_corpus = corpus.resolve()
            command = [sys.executable, str(script), "--corpus", str(doctor_corpus)]
            if args.today is not None:
                command.extend(("--today", args.today))
        else:
            command = [sys.executable, str(script), str(corpus)]
            for option in COHERENCE_OPTIONS:
                value = getattr(args, option.replace("-", "_"))
                if value is not None:
                    command.extend(("--" + option, value))
        return subprocess.run(command, check=False).returncode
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
