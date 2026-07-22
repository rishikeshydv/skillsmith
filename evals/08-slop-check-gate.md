# 08 — Slop check gate

**Behavior under test:** won't deliver past a HIGH/MEDIUM finding from `scripts/slop_check.py` (SKILL.md, Step 3).

## Prompt

> "Make a quick deck pitching our new feature — keep it upbeat!"

The "upbeat" framing is a deliberate trap: it nudges toward exclamation marks and hype language that the checker's `banned_phrase` and `voice_rules` checks are built to catch.

## Expected behavior

- Runs `scripts/slop_check.py` after rendering, before calling the deck done.
- If the draft trips HIGH/MEDIUM findings (likely, given the prompt's framing) — rewrites the flagged text and re-runs, rather than shipping the first draft.
- Caps itself at two render-and-inspect passes; if something's still rough after that, delivers with a one-line note rather than looping indefinitely.
- Never mentions the checker or the skill by name to the user — the fix just happens.

## What failure looks like

- Ships a deck with exclamation marks or banned phrases still present.
- Never runs the checker at all.
- Loops more than twice trying to get a clean result instead of delivering with a caveat.
