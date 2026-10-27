"""Candidate staging contracts exercised through the real command-line scripts."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAGED = "candidates/2026-10-26/draft.md"
CANDIDATE = {
    "type": "candidate",
    "status": "draft",
    "candidate_type": "principle",
    "source_entries": "[journal/2026-10-25.md]",
    "persona": "Coach",
    "session_id": "weekly-2026-10-26",
}
PROJECT = """---
title: A committed project
status: active
horizon: 0-6mo
serves: [goal:staged-goal]
created: 2026-10-01
target_date: 2026-12-01
last_reviewed: 2026-10-26
last_moved: 2026-10-26
ended_on:
---
"""


class CandidateStagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.corpus = Path(self.temp.name)

    def write(self, rel, text):
        path = self.corpus / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def candidate(self, rel=STAGED, changes=None, omit=()):
        fields = {**CANDIDATE, **(changes or {})}
        for name in omit:
            fields.pop(name)
        text = "---\n" + "\n".join(f"{k}: {v}" for k, v in fields.items())
        return self.write(rel, text + "\n---\n\n# Candidate for human review\n")

    def run_script(self, name, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / name), *map(str, args)],
            capture_output=True, text=True, encoding="utf-8", check=False,
        )

    def validate(self):
        return self.run_script("validate.py", "--corpus", self.corpus)

    def assert_invalid(self, result, field):
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(field, result.stdout)
        self.assertEqual(result.stderr, "")

    def test_valid_staging_skips_active_artifact_fields_and_reference_checks(self):
        # Treating drafts as principles/goals/habits/evidence would reject these.
        for kind in ("principle", "goal", "habit", "evidence"):
            self.candidate(
                f"candidates/2026-10-26/{kind}.md",
                {"candidate_type": kind, "kind": "revealed",
                 "serves": "[goal:uncommitted]", "related": "[principle:uncommitted]"},
            )
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("4 file(s) validated", result.stdout)
        self.assertIn("0 warning(s)", result.stdout)

    def test_missing_provenance_fails(self):
        for field in ("source_entries", "persona", "session_id"):
            with self.subTest(field=field):
                self.candidate(omit=(field,))
                self.assert_invalid(self.validate(), field)

    def test_empty_or_malformed_provenance_fails(self):
        cases = {
            "source_entries": ("", "[]", '[""]', '[" "]', "null", "journal/entry.md",
                               '[journal/entry.md, ""]', "[null]"),
            "persona": ("", '" "', "[]", "[Coach]", "null", "~"),
            "session_id": ("", '" "', "[]", "[session]", "null", "~"),
        }
        for field, values in cases.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    self.candidate(changes={field: value})
                    self.assert_invalid(self.validate(), field)

    def test_named_external_sources_need_not_exist_in_corpus(self):
        self.candidate(changes={"source_entries": '["external-notes/interview.md"]'})
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("1 file(s) validated", result.stdout)

    def test_candidate_inline_sources_reject_malformed_syntax(self):
        for value in (
            "[journal/entry.md", "[journal/entry.md] garbage", "[[]",
            "[[journal/entry.md]]", "[{source: journal/entry.md}]",
            "[source: journal/entry.md]", "[*source]", "[!tag source]",
            '["journal/entry.md]', "['journal/entry.md]",
            '["journal/entry.md" garbage]', '["one.md" "two.md"]',
            '["one.md\', two.md]', '["bad\\q.md"]',
        ):
            with self.subTest(value=value):
                self.candidate(changes={"source_entries": value})
                self.assert_invalid(self.validate(), "source_entries")

    def test_candidate_scalar_provenance_rejects_malformed_quotes(self):
        for field in ("persona", "session_id"):
            for value in ('"Coach', "'weekly", '"Coach" trailing', "{}"):
                with self.subTest(field=field, value=value):
                    self.candidate(changes={field: value})
                    self.assert_invalid(self.validate(), field)

    def test_candidate_quoted_source_punctuation_and_comments_are_valid(self):
        for sources in (
            '["notes/first, second [draft] #1.md", \'notes/it\'\'s "quoted".md\'] # sources',
            '["session: weekly-01; response: first", "notes/{context}.md"]',
            '["notes/\\"quoted\\" #1.md"] # escaped quotes',
        ):
            with self.subTest(sources=sources):
                self.candidate(changes={"source_entries": sources})
                result = self.validate()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_legacy_active_artifact_list_parsing_remains_unchanged(self):
        self.write("projects/committed.md", PROJECT.replace("[goal:staged-goal]", "[vision"))
        self.write("vision.md", "---\nstatus: draft\nhorizon: 3-5yr\ncreated: 2026-10-26\n"
                   "last_reviewed: 2026-10-26\nended_on:\nsupersedes: []\n---\n")
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_candidate_schema_requires_type_kind_and_draft_status(self):
        for field in ("type", "candidate_type", "status"):
            with self.subTest(field=field, value="missing"):
                self.candidate(omit=(field,))
                self.assert_invalid(self.validate(), field)
        for field, value in (("type", "goal"), ("type", "[]"),
                             ("candidate_type", "vision"), ("candidate_type", "[]"),
                             ("status", "active"), ("status", "met"), ("status", "[]")):
            with self.subTest(field=field, value=value):
                self.candidate(changes={field: value})
                self.assert_invalid(self.validate(), field)

    def test_candidate_requires_a_valid_dated_staging_directory(self):
        for rel in ("candidates/draft.md", "candidates/not-a-date/draft.md",
                    "candidates/2026-02-30/draft.md", "candidates/2026-1-1/draft.md",
                    "candidates/2026-10-26/nested/draft.md"):
            with self.subTest(path=rel):
                path = self.candidate(rel)
                self.assert_invalid(self.validate(), "candidates/YYYY-MM-DD/")
                path.unlink()

    def test_dated_readme_cannot_bypass_provenance_checks(self):
        self.write("candidates/2026-10-26/README.md", "# A draft without provenance\n")
        self.assert_invalid(self.validate(), "source_entries")

    def test_staging_root_readme_is_only_structure(self):
        self.write("candidates/README.md", "# Candidate staging instructions\n")
        self.candidate()
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("1 file(s) validated", result.stdout)

    def test_candidate_marker_cannot_bypass_active_artifact_validation(self):
        self.write("goals/draft.md", PROJECT.replace("horizon: 0-6mo", "horizon: 6-24mo")
                   .replace("serves: [goal:staged-goal]", "serves: []")
                   .replace("status: active", "status: draft\ntype: candidate")
                   + "\n## Success criteria (falsifiable)\n- [ ] A measure\n")
        self.assert_invalid(self.validate(), "candidates/YYYY-MM-DD/")

    def test_staged_goal_does_not_resolve_an_active_project_reference(self):
        self.candidate("candidates/2026-10-26/staged-goal.md", {"candidate_type": "goal"})
        self.write("projects/committed.md", PROJECT)
        self.assert_invalid(self.validate(), "ref 'goal:staged-goal' does not resolve")

    def test_active_reference_cannot_traverse_into_staging(self):
        self.candidate("candidates/2026-10-26/staged-goal.md", {"candidate_type": "goal"})
        for slug in ("../candidates/2026-10-26/staged-goal",
                     "..\\candidates\\2026-10-26\\staged-goal"):
            with self.subTest(slug=slug):
                self.write("projects/committed.md", PROJECT.replace("goal:staged-goal", f"goal:{slug}"))
                self.assert_invalid(self.validate(), "does not resolve")

    def test_staged_active_looking_content_does_not_change_coherence(self):
        self.write("projects/committed.md", PROJECT)
        self.write("areas/health.md", "---\nstatus: active\nlast_reviewed: 2026-10-26\n---\n")
        baseline = self.run_script("coherence.py", self.corpus, "--today", "2026-10-26")
        self.assertEqual(baseline.returncode, 0, baseline.stdout + baseline.stderr)
        self.assertIn("Orphans:        1", baseline.stdout)
        self.assertIn("Starved areas:  1", baseline.stdout)
        self.assertIn("0 active goal(s)", baseline.stdout)
        for kind in ("goal", "principle", "habit", "evidence"):
            self.candidate(f"candidates/2026-10-26/staged-{kind}.md", {
                "candidate_type": kind, "status": "active", "domain": "health",
                "kind": "revealed", "date": "2026-10-26", "last_reviewed": "2020-01-01",
            })
        result = self.run_script("coherence.py", self.corpus, "--today", "2026-10-26")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, baseline.stdout)

    def test_coherence_references_cannot_traverse_into_staging(self):
        (self.corpus / "principles" / "core").mkdir(parents=True)
        for kind, active_dir, slug in (
            ("goal", "projects", "../candidates/2026-10-26/staged"),
            ("principle", "goals", "../../candidates/2026-10-26/staged"),
        ):
            for separator in ("/", "\\"):
                with self.subTest(kind=kind, separator=separator):
                    ref = f"{kind}:" + slug.replace("/", separator)
                    active = self.write(f"{active_dir}/committed.md", f"---\nstatus: active\nserves: [{ref}]\n---\n")
                    baseline = self.run_script("coherence.py", self.corpus, "--today", "2026-10-26")
                    self.assertEqual(baseline.returncode, 0, baseline.stdout + baseline.stderr)
                    self.assertIn("Orphans:        1", baseline.stdout)
                    staged = self.candidate("candidates/2026-10-26/staged.md", {
                        "candidate_type": kind, "status": "active",
                    })
                    result = self.run_script("coherence.py", self.corpus, "--today", "2026-10-26")
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    # Even invalid active-looking drafts cannot satisfy an upward link.
                    try:
                        self.assertEqual(result.stdout, baseline.stdout)
                    finally:
                        active.unlink()
                        staged.unlink()

    def test_active_artifact_required_fields_still_fail(self):
        self.candidate()
        self.write("goals/committed.md", "---\nstatus: active\n---\n")
        self.assert_invalid(self.validate(), "missing required field 'target_date'")


if __name__ == "__main__":
    unittest.main()
