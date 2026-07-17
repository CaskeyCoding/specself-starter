# Getting Started, the foundation session

Run this **once**, with your agent, to seed your life OS. The default is not one
long block: it is a first short sitting on day one that already produces real
drafts, then the rest of the foundation spread across your first week of normal
use. Budget about 15 to 20 minutes for the first sitting. If you would rather do
it all at once, the single-session path is still here (see "Prefer one sitting?"
below). The goal is a first honest draft of each horizon, not perfection; the
corpus is meant to be revised forever.

> **Agent:** read [`AGENTS.md`](AGENTS.md) and all of [`steering/`](steering/)
> before you begin. Run this as an interview in the **Intake** then **Journalist**
> voice (see `personas/`). Ask one question at a time. Write only *candidate*
> drafts the human edits, author nothing as committed. Honor the one rule. The
> `/foundation` skill carries the sitting-by-sitting mechanics and the resume
> state; this file is the human-facing map.

**See the system alive first, if your checkout has it.** The full repo (not every
generated kit ships this) includes an `examples/` folder: a small, **fictional**
persona (Sam Rivers) worked end to end, one principle with its evidence, a goal
laddering to a vision, a project, and a weekly review with the coherence check
actually run. If present, read it once to see how the horizons connect before you
build your own. (It is clearly-labeled fiction, zero real corpus.) You can also
run `python scripts/coherence.py examples/sam-rivers` to see the kind of weekly
report you will get, before telling the system anything about yourself.

## Before you start

1. Decide your storage: private repo (recommended) or local-only. See
   [`steering/privacy.md`](steering/privacy.md). If private repo, run
   `bash scripts/set-privacy-mode.sh --private`: it flips the `.gitignore`
   rules and creates `.specself-allow-corpus` for you, so the privacy guard
   (below) lets you version your corpus. (Manual fallback: delete the
   `your-life/**` rules from `.gitignore` between the marker comments AND
   create an empty `.specself-allow-corpus` file at the repo root yourself.)
2. Skim [`steering/methodology.md`](steering/methodology.md) so the horizons and
   the two axes are not a surprise mid-session.

## The privacy guard (your corpus stays yours)

The kit ships a deterministic guard that refuses to commit your private
`your-life/` corpus or anything secret-shaped. It runs two ways, both calling the
same script (`.claude/hooks/guard-corpus-commit.sh`):

- **In Claude Code**, a `PreToolUse` hook in
  [`.claude/settings.json`](.claude/settings.json) blocks any `git commit`/`git push`
  that includes corpus or a secret, in-session.
- **In any git client**, install the pre-commit fallback once:

  ```bash
  pip install pre-commit && pre-commit install
  ```

  Then every `git commit` runs the same guard with no agent in the loop. This is the
  authoritative gate; the Claude hook is the convenience.

The guard checks file **paths**, not git's ignore status, so editing `.gitignore`
cannot bypass it (it catches the accidental un-ignore). Secret shapes are always
blocked. Your foundation progress file
(`your-life/reflections/foundation-progress.md`, written between sittings) lives
under `your-life/`, so the same guard keeps it private too.

Run `python scripts/doctor.py` whenever you want proof the privacy posture holds:
it probes your ignore rules and the guard wiring read-only, reports the corpus and
cadence state, and leaves nothing behind. The same checks ship as CI in
`.github/workflows/validate.yml`, so every fork gets a corpus-leak tripwire for free.

**Private-repo users:** if you deliberately keep your whole life in a PRIVATE repo
and want it versioned, create an empty `.specself-allow-corpus` file at the repo
root (step 1 above). The guard then lets your corpus through while still blocking
secrets. Without that file it assumes a public remote and protects your corpus by
default.

## The instrument: 20 questions, seven phases

The material is gathered by one fixed 20-question bank
(`personas/intake/foundation-questions.yaml`), asked one question at a time in the
**Intake** voice, in order, never skipped or reordered. If an answer stays
abstract (the question's `thin_signal` describes what that looks like: "it
depends," a category instead of an instance, a deflection to circumstance), the
agent probes **once** with the paired follow-up to press for the specific story,
then moves on regardless of what comes back. The seven phases, in order:

1. **Operating System** (how you actually decide, not how you think you decide).
2. **Load-Bearing Values** (the stances that cost you something real, and the
   ones you quietly bent on).
3. **Life Chapters** (where your adult life actually divides, and which
   chapters you have never quite left).
4. **Domain Audit** (work, money, relationships, health, learning: what is
   working, what is neglected, what is slow-building).
5. **Failure Modes** (your most reliable way of failing, and where you are
   coasting right now).
6. **Energy and Operating Conditions** (the real conditions behind your best
   work, what drains you, and what you are honoring out of momentum rather than
   choice).
7. **Trajectory** (the five-year version you would be proud of, and the bet you
   have not made).

## The week-one arc

The 20 questions split into four short sittings on the phase boundaries, and each
sitting ends with real drafts. Spreading them across your first week is the point:
the daily entries you write between sittings become evidence the later sittings
can cite, which is the method working as designed.

| Day | Do this | You end with |
|---|---|---|
| Day 1 | Sitting 1 (`/foundation`, phases 1-2), then your first `/daily` | 1-3 candidate principles; tomorrow's daily wired |
| Days 2-6 | `/daily` every day (about 2 minutes) | a week of raw evidence building up |
| Across the week | Sittings 2, 3, 4 whenever you have 15-20 minutes | vision, areas, falsifiers, habits, the drop list, goals |
| Day 7 | Your first `/weekly` | the coherence check run over everything so far |

Re-invoke `/foundation` for each sitting. It reads
`your-life/reflections/foundation-progress.md`, tells you which sittings are done,
and resumes at the next unanswered phase, so you never re-answer a phase or lose
your place. When all four sittings are complete it says so and points you at the
drafts to review instead of restarting.

- **Sitting 1 (phases 1-2):** Operating System + Load-Bearing Values. Ends with
  1-3 candidate `revealed` principles and your first `/daily` wired for tomorrow.
- **Sitting 2 (phases 3-4):** Life Chapters + Domain Audit. Ends with a vision
  draft and your area candidates.
- **Sitting 3 (phases 5-6):** Failure Modes + Energy. Sets the falsifiers on the
  sitting-1 principles, surfaces habit candidates, and names the drop list.
- **Sitting 4 (phase 7 + wrap):** Trajectory. Drafts your goals and projects,
  completes the vision, and runs the first coherence check.

### Prefer one sitting?

You can still run all four passes in a single session. Tell your agent you want to
run the whole foundation now and it will work sittings 1 through 4 back to back,
drafting each output as it goes and finishing with the full coherence close.
Budget about 60 to 90 minutes. The sitting plan is the default door, not the only
one.

### Already have notes?

If you arrive with years of existing notes (an Obsidian vault, a Notion export,
journals, a docs folder), you do not have to author a foundation from scratch. Run
`/adopt` instead: you name a source directory, the agent reads it **read-only**
(it never edits, moves, or deletes your notes, and never reads anything you mark
off-limits), and it drafts a bounded first set of candidate principles, areas,
goals, projects, and habits from what it finds, each citing the note it came from.
It writes only candidates you edit or discard; it never copies your notes into
`your-life/`.

`/adopt` is a third door, and it slots into the week-one arc rather than replacing
it:

- **Before foundation:** turn the notes into a starting draft, then let the
  sittings deepen and correct it.
- **After sitting 1:** keep the value stories sitting 1 surfaces, and let `/adopt`
  fill your areas, goals, and projects from the notes.
- **Instead of sittings 2-4:** `/adopt` covers the horizons that live in notes, so
  you can skip the middle sittings. You still want **sitting 1**, because the
  decision-making and load-bearing-value stories almost never live in notes, and
  the agent will say so in its closing report. `/adopt` never drafts a vision for
  the same reason.

## The five passes: what each sitting drafts

The interview gathers; these five passes are the **output structure** the agent
synthesizes your answers into, in the **Journalist** voice, drafting a few
artifacts under `your-life/` using the matching `templates/`. Across the week-one
arc the passes land in the sittings above; in a single session they run in order.
Keep drafts short and true; you will deepen them over the coming weeks.

### Pass 1, Principles (H5), revealed first
From the *evidence* in your Operating System, Load-Bearing Values, and Failure
Modes answers, the agent proposes 3 to 5 **candidate** `revealed` principles as
actionable rules ("when X, I do Y, even when it costs Z"), each citing the
specific answers it drew from. Sitting 1 drafts the first 1 to 3; sitting 3 sets
each principle's mandatory falsifier from your failure-mode answers. You rewrite
them in your words. Anything you *want* to be true but cannot back with a story
goes in `aspirational.md`, tagged `aspirational`. **Protect that gap.**

### Pass 2, Vision (H4)
Drawing on your Life Chapters and Trajectory answers: "Where is this person in
five years if the principles hold and the work compounds?" One page,
present-tense, concrete. Not a resume, a portrait. Sitting 2 drafts it from the
Life Chapters answers; sitting 4 tightens it with Trajectory. Draft to
`your-life/vision.md`.

### Pass 3, Areas (H2)
From your Domain Audit and Energy answers: the standing roles you maintain
indefinitely, health, money, a relationship, your craft, learning. For each, the
agent names the **standard** ("what good looks like") and how you would know it is
slipping. These rarely "complete," they are the roles you keep. Draft to
`your-life/areas/`.

### Pass 4, Goals (H3)
From the unresolved domains and the Trajectory answers: the finite outcomes for
the next 6-24 months. For each: a falsifiable success criterion (a date and a
measure), and a `serves:` link up to the vision or a principle. If a goal serves
nothing above it, question it now.

### Pass 5, Projects (H1) and first habits
From Failure Modes and Energy: the concrete projects you are driving *right now*
that ladder up to those goals, and 1 to 3 habits worth tracking. Your Energy
answer about momentum-only commitments becomes a **drop** candidate here, not a
project to add. Capacity is a coherence constraint, not a wish list.

Every candidate the agent drafts is exactly that: a candidate. It never authors
your record; you edit or discard everything it proposes.

## Close, first coherence pass

At the end of the last sitting (day 7's `/weekly` picks this up if you did not run
it yourself), run the [coherence check](steering/coherence.md) on what you
created:

- Does every project serve a goal? Every goal serve the vision or a principle?
- Is any area already starved? Is any goal already fighting a principle?
- Are there too many `active` projects to actually move?

End with the **one** sharpest question the agent found. Sit with it. Do not
resolve it that day; note it for your first weekly review.

## After the foundation session

You are live. From here it is the loop:

- **Daily:** `/capture` or `/daily`, 2 minutes, raw.
- **Weekly:** `/weekly`, cluster, coherence-check, candidates.
- **Monthly and up:** `/monthly`, `/quarterly`, `/annual`, synthesize, falsify,
  prune.

The system gets more valuable the longer you run it, because the diff across time
*is* the insight. Start rough. Revise forever.

## Using your corpus as context (in any Claude chat)

The foundation session and the cadence run best in Claude Code, where the agent
reads your files directly. But your principles are useful in any conversation, not
just reflection sessions. Three ways to bring them in, easiest first.

### 1. A Claude Project (best for everyday chats)

Create a Project at claude.ai and add these as Project knowledge:

- `AGENTS.md`, so the assistant inherits the one rule
- `your-life/vision.md`
- your committed files under `your-life/principles/`

Every chat in that Project then reasons with your principles in context, with no
pasting. When your principles change, update the files in the Project.

### 2. Claude Code (best for reflection sessions)

Open this repo with Claude Code and say:

> Read `AGENTS.md` and everything in `steering/`, then load my `your-life/`.

The bundled `.claude/` setup already loads the contract and steering at session
start, so your corpus is in context. Then run `/daily`, `/weekly`, `/monthly`.

### 3. One file to paste (quick and portable)

Run `./bundle-context.sh` (Windows: run it from Git Bash) or, on native
PowerShell with neither Git Bash nor WSL, `./bundle-context.ps1`. Either one
writes `context-bundle.md`: the contract plus your vision and principles in a
single file. Paste it at the top of any chat, or attach it. The output
contains your corpus, so it is gitignored by default. Never commit it.

Whichever path you use, the rule holds: the assistant may read and question
everything in your context, but you author the record. It never rewrites a
principle.
