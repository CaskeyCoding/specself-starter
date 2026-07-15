---
title: Launch paid, not free-to-play
status: accepted
date: 2026-02-18
supersedes: []
superseded_by:
---

> **FICTIONAL EXAMPLE:** not a real person, not real corpus. Part of the `examples/`
> worked corpus (persona: Sam Rivers). See [`examples/README.md`](../../README.md).

# ADR-001: Launch paid, not free-to-play

`goal:launch-paid-game-v1` already assumed a paid launch when it was written in
January. This ADR is the moment that assumption got seriously tested and formally
reaffirmed, in writing, before the store page price field could no longer be changed
without confusing anyone who'd already wishlisted.

## Context

Building the store page in February forced a real decision: the price field has to
hold something before the page goes live. A friend in the dev-meetup Discord relaunched
their own game free-to-play with cosmetic add-ons that same week and their wishlist
count visibly jumped, which was enough to make me second-guess a plan I'd been
building toward for a month. The store page draft (2026-02-27) could not go up
without this settled first.

## Options considered

### Option A: Free-to-play with cosmetic purchases

- Pros: lower barrier to install, matches what just worked for a friend, larger top
  of funnel.
- Cons: needs a live-ops loop (cosmetics, a shop, ongoing content) I have no capacity
  to run solo without either crunching or letting the game go stale. Also close to
  the "dark-pattern monetization" the vision explicitly rules out: cosmetic shops
  drift there without deliberate restraint I don't currently have bandwidth to
  enforce. Rejected on capacity and on the vision's own terms, not on principle
  alone.

### Option B: Paid, fixed price at launch

- Pros: one clean transaction, no live-ops tail, a price is a forcing function for a
  real ship date (exactly what `principle:ship-before-its-ready` needs: a free demo
  with no purchase moment lets "almost done" drift indefinitely). Matches the
  `goal:launch-paid-game-v1` success criteria as already written.
- Cons: smaller top of funnel than free, no cosmetic-shop safety net if unit sales
  come in low. Accepted, since the smaller, honest funnel is the trade the vision
  already said I'd make.

## Decision

Launch at a fixed price, $14. No free tier, no cosmetic shop, no live-ops loop.

## Consequences

This locks the store page's price field for real starting with the 2026-02-27 draft,
and closes off F2P tooling work I would otherwise have been tempted to start instead
of cutting the tutorial. It keeps `goal:launch-paid-game-v1`'s success criteria
meaningful as written: "100 paid units" only means something if paid was never in
question. What I'll watch: wishlist-to-purchase conversion in the first week after
launch, since a fixed price with no funnel de-risking (no demo-to-cosmetic bridge)
means that number carries more weight than it would under Option A.
