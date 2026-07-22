# 05 — Plan before build

**Behavior under test:** a plan is stated and approval is awaited, except when the request is unambiguous and the source is already structured (SKILL.md, Step 1).

## Prompt A (should wait for approval)

> "Make a deck out of our Q3 results — figure out what matters most."

## Prompt B (should skip the wait)

> "Turn this doc's five sections into five slides, one each, in order." (pasted doc with five clearly labeled sections)

## Expected behavior

- **A:** states a compact plan (deck type, audience, footer, slide-by-slide one-liners) and stops, waiting for approval before drafting body copy.
- **B:** still states the plan, but proceeds straight into building without waiting — the request already resolved the only ambiguity (structure).
- In both cases, the plan never includes drafted slide body copy — only titles plus one line each.

## What failure looks like

- **A:** skips straight to a rendered .pptx with no plan shown first.
- **B:** stops and waits for approval on a request that left nothing to confirm.
- Either case: the "plan" is actually full slide text, not a structural outline.
