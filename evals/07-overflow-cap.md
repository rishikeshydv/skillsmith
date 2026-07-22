# 07 — Overflow cap

**Behavior under test:** flags a cap overage before generating rather than silently cutting or silently exceeding it (SKILL.md, Step 1 and Step 2).

## Prompt

> "Turn this 20-page report into a client deck." (source material clearly supports 18-20 distinct slides; deck type infers to `client_proposal`, cap 12)

## Expected behavior

- The plan states the overage explicitly (e.g. "source supports ~18 slides, cap is 12") before generating anything.
- Proposes a resolution — cut detail, move sections to an appendix, or ask the user what to prioritize — rather than picking silently.
- Final deck respects the cap unless the user explicitly approves exceeding it.

## What failure looks like

- Delivers a 18-slide deck against a 12-slide cap with no comment.
- Silently drops 6 slides' worth of content without saying what was cut or why.
- Asks a vague "how long should this be?" instead of naming the specific cap and the specific overage.
