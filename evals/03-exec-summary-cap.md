# 03 — Exec summary cap

**Behavior under test:** inference picks the tightest matching cap when a request could plausibly fit more than one deck type.

## Prompt

> "I need to walk the board through where Q3 landed before Thursday's steerco."

## Expected behavior

- Infers `exec_summary` from "board" / "steerco" — the tightest cap of the three deck types.
- If the source material is much larger than the cap allows, says so before generating rather than silently cutting (see eval 07) — but doesn't ask a clarifying question just because the source is long; it states the plan and flags the overage inline.
- Plan reflects the `exec_summary` cap, not `default`.

## What failure looks like

- Falls through to `default` because "board" isn't a literal keyword match, instead of recognizing the intent.
- Produces a 10-slide deck when the exec cap is 5, without flagging it first.
