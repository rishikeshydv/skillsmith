# 09 — Batched feedback

**Behavior under test:** collects revisions before editing and applies them in one pass, rather than editing on the first note (SKILL.md, Step 4).

## Prompt sequence

1. "Can you bump the title font on slide 2?"
2. (a few seconds later, same message thread) "oh also slide 4's chart needs a legend, and can we cut slide 6 entirely"

## Expected behavior

- After message 1, asks once — "Anything else before I make these?" — rather than editing immediately.
- Once message 2 lands, reads back the full batch as a numbered list grouped by slide, and confirms before touching the file.
- Applies all three changes in a single pass with targeted edits (not a full regeneration).
- Reports what changed in one line, once, after the batch — not once per item.

## What failure looks like

- Edits slide 2 immediately after message 1, then edits again after message 2 (two rebuild passes instead of one).
- Regenerates the entire deck instead of touching only slides 2, 4, and 6.
- Never reads back a confirmation list before editing.
