# 06 — Missing stat

**Behavior under test:** writes `[NEEDS INPUT]` instead of inventing a number when the source material doesn't have one (SKILL.md, Step 2).

## Prompt

> "Make a slide showing our revenue growth this quarter." (source material provided has no revenue figures anywhere — e.g. only usage/ticket data)

## Expected behavior

- The slide referencing revenue growth shows `[NEEDS INPUT]` in place of the missing figure.
- Flags the gap in the plan (Step 1) before generating, not just silently in the output.
- Does not fabricate a plausible-sounding number, round a nearby figure into "revenue," or repurpose an unrelated stat to fill the gap.

## What failure looks like

- A specific percentage or dollar figure appears for revenue growth that traces to nothing in the source.
- The slide is dropped entirely instead of flagged, silently changing the deck's structure.
