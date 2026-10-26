"""CLI contracts exercised through real processes and disposable corpora."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = "examples/sam-rivers"


def run_python(*args, cwd=ROOT):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, *map(str, args)], cwd=cwd, env=env,
        capture_output=True, text=True, encoding="utf-8", timeout=30,
    )


def cli(*args, cwd=ROOT):
    return run_python("-m", "specself", *args, cwd=cwd)


def snapshot(root):
    """Include names, directories, and file bytes, excluding the privacy hatch."""
    result = {}
    for directory, children, files in os.walk(root):
        children[:] = [name for name in children if name != ".sensitive"]
        for name in children + files:
            path = Path(directory) / name
            rel = path.relative_to(root).as_posix()
            result[rel] = (
                hashlib.sha256(path.read_bytes()).hexdigest()
                if path.is_file() else None
            )
    return result


class CliTests(unittest.TestCase):
    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_help_lists_the_four_commands(self):
        result = cli("--help")
        self.assert_success(result)
        for command in ("doctor", "coherence", "capture", "review"):
            self.assertIn(command, result.stdout)

    def test_unknown_command_is_a_usage_error(self):
        result = cli("unknown")
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage:", result.stderr)
        self.assertIn("invalid choice", result.stderr)

    def test_every_command_accepts_both_corpus_forms(self):
        for command in ("doctor", "coherence", "capture", "review"):
            for corpus_args in ((EXAMPLE,), ("--corpus", EXAMPLE)):
                with self.subTest(command=command, corpus_args=corpus_args):
                    self.assert_success(cli(command, *corpus_args))

    def test_missing_corpus_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "missing"
            for command in ("doctor", "coherence", "capture", "review"):
                with self.subTest(command=command):
                    result = cli(command, missing)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("not a directory", result.stdout + result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
            self.assertFalse(missing.exists())

    def test_two_corpus_arguments_are_rejected(self):
        for command in ("doctor", "coherence", "capture", "review"):
            with self.subTest(command=command):
                result = cli(command, EXAMPLE, "--corpus", "your-life")
                self.assertEqual(result.returncode, 2)
                self.assertIn("usage:", result.stderr)

    def test_default_doctor_matches_direct_script(self):
        direct = run_python("scripts/doctor.py", "--today", "2026-07-15")
        wrapped = cli("doctor", "--today", "2026-07-15")
        self.assert_success(direct)
        self.assertEqual(wrapped.returncode, direct.returncode)
        self.assertEqual(wrapped.stdout, direct.stdout)
        self.assertEqual(wrapped.stderr, direct.stderr)
        self.assertIn("passes over your-life/", wrapped.stdout)

    def test_doctor_uses_selected_corpus_for_health_and_cadence(self):
        result = cli("doctor", EXAMPLE, "--today", "2026-07-15")
        self.assert_success(result)
        self.assertIn(str(Path(EXAMPLE)), result.stdout)
        self.assertIn("newest journal:", result.stdout)
        self.assertNotIn("Next: run /foundation", result.stdout)

    def test_default_doctor_preserves_kit_relative_corpus_from_subdirectory(self):
        direct = run_python(ROOT / "scripts" / "doctor.py", "--today", "2026-07-15", cwd=ROOT / "scripts")
        wrapped = cli("doctor", "--today", "2026-07-15", cwd=ROOT / "scripts")
        self.assert_success(direct)
        self.assertEqual(wrapped.returncode, direct.returncode, wrapped.stderr)
        self.assertEqual(wrapped.stdout, direct.stdout)
        self.assertEqual(wrapped.stderr, direct.stderr)

    def test_coherence_matches_direct_output_and_options(self):
        options = (
            "--today", "2026-07-15", "--starvation-days", "5",
            "--stale-days", "10", "--stalled-days", "2",
            "--project-ceiling", "0", "--goal-ceiling", "0",
            "--promotion-evidence-count", "1",
        )
        direct = run_python("scripts/coherence.py", EXAMPLE, *options)
        wrapped = cli("coherence", EXAMPLE, *options)
        self.assert_success(direct)
        self.assertEqual(wrapped.returncode, direct.returncode)
        self.assertEqual(wrapped.stdout, direct.stdout)
        self.assertEqual(wrapped.stderr, direct.stderr)

    def test_delegated_date_error_preserves_status_and_output(self):
        for command in ("doctor", "coherence"):
            with self.subTest(command=command):
                corpus_args = ("--corpus", EXAMPLE) if command == "doctor" else (EXAMPLE,)
                direct = run_python(f"scripts/{command}.py", *corpus_args, "--today", "bad-date")
                wrapped = cli(command, EXAMPLE, "--today", "bad-date")
                self.assertEqual(direct.returncode, 1)
                self.assertEqual(wrapped.returncode, direct.returncode)
                self.assertEqual(wrapped.stdout, direct.stdout)

    def test_coherence_explicit_write_preserves_the_derived_report(self):
        with tempfile.TemporaryDirectory() as temporary:
            direct_dir = Path(temporary) / "direct"
            wrapped_dir = Path(temporary) / "wrapped"
            options = ("--today", "2026-07-15", "--tier", "monthly")
            direct = run_python("scripts/coherence.py", EXAMPLE, *options, "--write", direct_dir)
            wrapped = cli("coherence", EXAMPLE, *options, "--write", wrapped_dir)
            self.assert_success(direct)
            self.assert_success(wrapped)
            self.assertEqual(wrapped.stdout, direct.stdout)
            self.assertEqual(
                (wrapped_dir / "2026-07-15.md").read_bytes(),
                (direct_dir / "2026-07-15.md").read_bytes(),
            )

    def test_doctor_preserves_validation_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            corpus = Path(temporary)
            (corpus / "goals").mkdir()
            (corpus / "goals" / "invalid.md").write_text("# Missing required frontmatter\n", encoding="utf-8")
            direct = run_python("scripts/doctor.py", "--corpus", corpus)
            wrapped = cli("doctor", corpus)
            self.assertEqual(direct.returncode, 1)
            self.assertEqual(wrapped.returncode, direct.returncode)
            self.assertEqual(wrapped.stdout, direct.stdout)
            self.assertIn("FAIL  Check 3 corpus health", wrapped.stdout)

    def test_private_escape_hatch_cannot_be_selected_as_corpus(self):
        with tempfile.TemporaryDirectory() as temporary:
            sensitive = Path(temporary) / ".sensitive"
            sensitive.mkdir()
            for command in ("doctor", "coherence", "capture", "review"):
                with self.subTest(command=command):
                    result = cli(command, sensitive)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("private escape hatch", result.stderr)

    def test_capture_and_every_review_tier_are_read_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            corpus = Path(temporary) / "corpus"
            shutil.copytree(ROOT / EXAMPLE, corpus)
            before = snapshot(corpus)
            for dry_run in ((), ("--dry-run",)):
                result = cli("capture", corpus, *dry_run)
                self.assert_success(result)
                self.assertIn("Read-only", result.stdout)
                self.assertIn(".claude/commands/capture.md", result.stdout)
                self.assertIn("## Captures", result.stdout)
                for tier in ("daily", "weekly", "monthly", "quarterly", "annual"):
                    with self.subTest(tier=tier, dry_run=dry_run):
                        result = cli("review", corpus, "--tier", tier, *dry_run)
                        self.assert_success(result)
                        self.assertIn("Read-only", result.stdout)
                        self.assertIn("steering/cadence.md", result.stdout)
                        self.assertIn(f"tier: {tier}", result.stdout)
                self.assertEqual(snapshot(corpus), before)

    def test_default_review_is_weekly_and_default_corpus_is_your_life(self):
        result = cli("review")
        self.assert_success(result)
        self.assertIn("your-life", result.stdout)
        self.assertIn("tier: weekly", result.stdout)

    def test_sensitive_only_corpus_still_needs_foundation(self):
        with tempfile.TemporaryDirectory() as temporary:
            corpus = Path(temporary)
            sensitive = corpus / ".sensitive"
            sensitive.mkdir()
            (sensitive / "private.md").write_bytes(b"\xff\xfe\x00")
            result = cli("doctor", corpus)
            self.assert_success(result)
            self.assertIn("Next: run /foundation", result.stdout)

    def test_candidate_only_corpus_still_needs_foundation(self):
        with tempfile.TemporaryDirectory() as temporary:
            corpus = Path(temporary)
            candidates = corpus / "candidates" / "2026-10-26"
            candidates.mkdir(parents=True)
            (candidates / "draft.md").write_text(
                "---\ntype: candidate\nstatus: draft\ncandidate_type: principle\n"
                'source_entries: ["session:fixture#answer-1"]\npersona: journalist\n'
                "session_id: fixture-01\n---\n# Candidate\nUncommitted idea.\n",
                encoding="utf-8",
            )
            result = cli("doctor", corpus)
            self.assert_success(result)
            self.assertIn("Next: run /foundation", result.stdout)


if __name__ == "__main__":
    unittest.main()
