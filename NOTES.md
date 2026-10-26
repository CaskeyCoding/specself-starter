# SS-1 / SS-3 foundation slice

Scope: the task's four-command CLI and candidate staging, on
`feature/ss-1-ss-3-foundation`, starting at `7708548`. No push or PR.

Implementation plan:

- Delegate doctor/coherence to their existing scripts, adding corpus selection
  to doctor without changing its defaults. Test actual subprocess behavior.
- Expose capture and review as read-only instruction/template previews. Test
  example-corpus success and unchanged corpus files, including all review tiers.
- Validate staged candidate provenance separately; preserve active checks and
  exclude staging from active references/coherence/onboarding. Test temporary
  corpora with valid drafts, missing provenance, and broken active artifacts.
- Align agent instructions with staging, verify module and installed entry points,
  run the required direct-script checks, review the diff, and commit locally.

Small choices made where the task leaves room:

- Capture/review print the existing command, template, and cadence contract;
  they do not conduct a session or save content. `--dry-run` is explicit but is
  also their default behavior. Weekly is the default review tier.
- The package is a wrapper for a kit checkout: scripts and session materials
  remain plain files in that checkout, rather than bundled copies that can drift.
  Python runtime code and tests use only the standard library. Setuptools is
  build tooling only; there are no runtime package dependencies.
- Staged files use `type: candidate`, `status: draft`, `candidate_type`,
  `source_entries` (a nonempty inline list), `persona`, and `session_id`.
  Sources are citations, not an instruction to ingest or copy source notes.
- The git rule applies to corpus commits, not this requested engineering commit.
  Existing privacy guards remain authoritative: default ignored corpus content
  stays local until the human deliberately enables corpus versioning. No
  automatic staging, git commits, promotion, or ledger workflow is added.

## Local acceptance evidence

Run from the kit root after installing the wrapper into a local virtualenv:

```text
python -m pip install --no-deps -e .
python -m unittest discover -s tests -v
python scripts/coherence.py examples/sam-rivers
python scripts/validate.py --corpus examples/sam-rivers
python scripts/doctor.py
python -m specself --help
specself --help
python -m specself doctor examples/sam-rivers
python -m specself coherence examples/sam-rivers
python -m specself capture examples/sam-rivers --dry-run
python -m specself review examples/sam-rivers --dry-run
```

The fictional example has date-dependent staleness warnings; these are advisory
and exit zero. Candidate negative fixtures must exit nonzero.

Verification on 2026-10-26 against the final working diff over `7708548`:

- `python -m unittest discover -s tests -v`: 35 tests passed.
- Both required direct example scripts exited zero; validation reported 13
  files, zero errors, and seven existing staleness warnings. Default doctor
  passed all guarantee checks.
- Built and installed a regular wheel into the ignored `.venv/` using
  `.venv/Scripts/python.exe -m pip install --no-deps .` (then force-reinstalled
  after the reviewed doctor fix). Installed code bytes matched `src/specself/cli.py`.
- Both installed entry points passed help and all four commands against Sam
  Rivers. All four console commands also passed from a temporary external
  working directory with an absolute corpus path. Default doctor passed from
  `scripts/`; unknown console subcommands exited 2 with usage.
- Independent code review's malformed-list and doctor working-directory
  findings were reproduced, fixed, and re-reviewed with no remaining blockers.
  Disclosure review found no personal corpus, credentials, or NDA material.

| Criterion | Evidence | Boundary / limitation | Grade |
|---|---|---|---|
| SS-1 module and installed commands, unknown usage | `test_cli.py`: help, unknown-command, every-command tests; regular-wheel checks above | Real Python and console subprocesses; installed wrapper requires a kit checkout | Adequate |
| SS-1 existing behavior and options | `test_cli.py`: direct-output, default-doctor, subdirectory, date-error, validation-failure, explicit-write tests | Exact stdout/exit parity and persisted derived-report bytes | Strong |
| SS-1 capture/review previews | `test_capture_and_every_review_tier_are_read_only` | Real corpus snapshots unchanged for default and dry-run, all five tiers; no session automation claimed | Adequate |
| SS-3 provenance and dated draft schema | `test_candidates.py`: missing, empty, malformed, quoted-source, dated-path, schema and README cases | Real temporary files and validator exits; citations are not dereferenced | Strong |
| SS-3 staging excluded from active corpus | `test_candidates.py`: active-field, active-reference, traversal and coherence tests; candidate-only doctor test | Actual validation, reports and onboarding guidance; staged data cannot satisfy active references | Strong |
| SS-3 agent write/commit boundary | `AGENTS.md`, session skill/template review, candidate template | Policy encoded and conflicting instructions updated; no automatic git writer or promotion added | Adequate |

Strong grades use observed failing regressions followed by passing checks; no
mutation campaign was run. The final commit containing these notes identifies
the verified implementation. No user corpus was changed, pushed, or published.
