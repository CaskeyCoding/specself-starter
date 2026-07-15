# Getting Started — The Foundation Session

Run this **once**, with your agent, to seed your life OS. Budget ~60–90 minutes.
You don't need to finish in one sitting — the corpus is meant to be revised
forever. The goal here is a first honest draft of each horizon, not perfection.

> **Agent:** read [`AGENTS.md`](AGENTS.md) and all of [`steering/`](steering/)
> before you begin. Run this as an interview in the **Intake** then **Journalist**
> voice (see `personas/`). Ask one question at a time. Write only *candidate*
> drafts the human edits — author nothing as committed. Honor the one rule.

**See the system alive first, if your checkout has it.** The full repo (not every
generated kit ships this) includes an `examples/` folder: a small, **fictional**
persona (Sam Rivers) worked end to end, one principle with its evidence, a goal
laddering to a vision, a project, and a weekly review with the coherence check
actually run. If present, read it once to see how the horizons connect before you
build your own. (It's clearly-labeled fiction, zero real corpus.) If your kit
doesn't include it, the five passes below walk you through the same shape live.

## Before you start

1. Decide your storage: private repo (recommended) or local-only. See
   [`steering/privacy.md`](steering/privacy.md). If private repo, run
   `bash scripts/set-privacy-mode.sh --private` — it flips the `.gitignore`
   rules and creates `.specself-allow-corpus` for you, so the privacy guard
   (below) lets you version your corpus. (Manual fallback: delete the
   `your-life/**` rules from `.gitignore` between the marker comments AND
   create an empty `.specself-allow-corpus` file at the repo root yourself.)
2. Skim [`steering/methodology.md`](steering/methodology.md) so the horizons and
   the two axes aren't a surprise mid-session.

## The privacy guard (your corpus stays yours)

The kit ships a deterministic guard that refuses to commit your private
`your-life/` corpus or anything secret-shaped. It runs two ways, both calling the
same script (`.claude/hooks/guard-corpus-commit.sh`):

- **In Claude Code** — a `PreToolUse` hook in
  [`.claude/settings.json`](.claude/settings.json) blocks any `git commit`/`git push`
  that includes corpus or a secret, in-session.
- **In any git client** — install the pre-commit fallback once:

  ```bash
  pip install pre-commit && pre-commit install
  ```

  Then every `git commit` runs the same guard with no agent in the loop. This is the
  authoritative gate; the Claude hook is the convenience.

The guard checks file **paths**, not git's ignore status, so editing `.gitignore`
cannot bypass it (it catches the accidental un-ignore). Secret shapes are always
blocked.

**Private-repo users:** if you deliberately keep your whole life in a PRIVATE repo
and want it versioned, create an empty `.specself-allow-corpus` file at the repo
root (step 1 above). The guard then lets your corpus through while still blocking
secrets. Without that file it assumes a public remote and protects your corpus by
default.

## The session: a 20-question interview, then five passes of output

The agent runs this in two stages. First, it asks you the kit's fixed 20-question
bank (`personas/intake/foundation-questions.yaml`), one question at a time, in
the **Intake** voice, moving through seven phases from how you decide down to
where you're headed. That interview is how the material gets gathered; the
passes below are the **output structure** the agent synthesizes your 20 answers
into afterward, in the **Journalist** voice, drafting a few artifacts per pass
under `your-life/` using the matching `templates/`. Keep drafts short and true;
you'll deepen them over the coming weeks.

### The instrument: 20 questions, seven phases

The agent asks each question in order and does not skip or reorder. If an answer
stays abstract (the question's `thin_signal` describes what that looks like: "it
depends," a category instead of an instance, a deflection to circumstance), the
agent probes **once** with the paired follow-up to press for the specific story,
then moves on regardless of what comes back. The phases, in order:

1. **Operating System** (how you actually decide, not how you think you decide).
2. **Load-Bearing Values** (the stances that cost you something real, and the
   ones you quietly bent on).
3. **Life Chapters** (where your adult life actually divides, and which
   chapters you've never quite left).
4. **Domain Audit** (work, money, relationships, health, learning: what's
   working, what's neglected, what's slow-building).
5. **Failure Modes** (your most reliable way of failing, and where you're
   coasting right now).
6. **Energy and Operating Conditions** (the real conditions behind your best
   work, what drains you, and what you're honoring out of momentum rather than
   choice).
7. **Trajectory** (the five-year version you'd be proud of, and the bet you
   haven't made).

### Pass 1 — Principles (H5), revealed first
From the *evidence* in your Operating System, Load-Bearing Values, and Failure
Modes answers, the agent proposes 3–5 **candidate** `revealed` principles as
actionable rules ("when X, I do Y, even when it costs Z"), each citing the
specific answers it drew from. You rewrite them in your words. Anything you
*want* to be true but can't back with a story goes in `aspirational.md`, tagged
`aspirational`. **Protect that gap.**

### Pass 2 — Vision (H4)
Drawing on your Life Chapters and Trajectory answers: "Where is this person in
five years if the principles hold and the work compounds?" One page,
present-tense, concrete. Not a resume, a portrait. Draft to
`your-life/vision.md`.

### Pass 3 — Areas (H2)
From your Domain Audit and Energy answers: the standing roles you maintain
indefinitely, health, money, a relationship, your craft, learning. For each, the
agent names the **standard** ("what good looks like") and how you'd know it's
slipping. These rarely "complete," they're the roles you keep. Draft to
`your-life/areas/`.

### Pass 4 — Goals (H3)
From the unresolved domains and the Trajectory answers: the finite outcomes for
the next 6-24 months. For each: a falsifiable success criterion (a date and a
measure), and a `serves:` link up to the vision or a principle. If a goal serves
nothing above it, question it now.

### Pass 5 — Projects (H1) & first habits
From Failure Modes and Energy: the concrete projects you're driving *right now*
that ladder up to those goals, and 1–3 habits worth tracking. Your Energy answer
about momentum-only commitments becomes a **drop** candidate here, not a project
to add. Capacity is a coherence constraint, not a wish list.

Every candidate the agent drafts is exactly that: a candidate. It never authors
your record; you edit or discard everything it proposes.

## Close — first coherence pass

Run the [coherence check](steering/coherence.md) on what you just created:

- Does every project serve a goal? Every goal serve the vision or a principle?
- Is any area already starved? Is any goal already fighting a principle?
- Are there too many `active` projects to actually move?

End with the **one** sharpest question the agent found. Sit with it. Don't resolve
it tonight — note it for your first weekly review.

## After the foundation session

You're live. From here it's the loop:

- **Daily:** `/capture` or `/daily` — 2 minutes, raw.
- **Weekly:** `/weekly` — cluster, coherence-check, candidates.
- **Monthly+:** `/monthly`, `/quarterly`, `/annual` — synthesize, falsify, prune.

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
