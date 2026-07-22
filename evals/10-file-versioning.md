# 10 — File versioning

**Behavior under test:** never overwrites a previous output; increments version suffixes and confirms the prior version still exists (SKILL.md, File Versioning).

## Prompt sequence

1. "Make a deck on our Q3 roadmap."
2. "Add a slide on hiring plans."

## Expected behavior

- First build is saved as `<topic>_v1.pptx` with a topic name derived from the request.
- The second request produces `<topic>_v2.pptx` — a new file, not an overwrite of `_v1`.
- States what changed and explicitly confirms the prior version is still available, e.g. "`roadmap_v2.pptx` has 7 slides; `roadmap_v1.pptx` (6 slides) is still available above."
- The edit is targeted (inserts the new slide) rather than a full regeneration of the deck.

## What failure looks like

- The second file is also named `_v1.pptx` (silently overwriting the first).
- No mention of the prior version still being available.
- Any exported PDF/image from the first version is left stale after the .pptx changes, with no note that it needs regenerating.
