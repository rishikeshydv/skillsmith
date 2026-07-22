# 01 — Internal update inference

**Behavior under test:** deck-type inference from weak signals (SKILL.md, Step 1 table).

## Prompt

> "Can you put together slides for tomorrow's standup? Just want to walk through where the migration is at."

## Expected behavior

- Infers `internal_update` from "standup" — no follow-up question about audience.
- States the plan block with `Deck type: internal_update` and the matching cap from brand config.
- Footer marked "no" in the plan header, since `internal_update` decks aren't client-facing by default.
- Does not ask about branding, template, or which deck type — none of that changes given the signal.

## What failure looks like

- Asks "who is this for?" or "is this client-facing?" when "standup" already answers it.
- Defaults to `client_proposal` or applies the client footer anyway.
- Skips stating a plan and jumps straight to generating.
