# 04 — Question cap

**Behavior under test:** never more than 2 questions, and never asking what the request already states (SKILL.md, Step 1).

## Prompt

> "Make a deck for our client kickoff next week — here's the scope doc." (pasted doc clearly names the client, timeline, and deliverables)

## Expected behavior

- Asks at most 2 questions total, and only ones whose answers would actually change the deck (e.g. length, if the source is unusually thin or thick for the cap).
- Does not ask who the client is, what the deadline is, or anything the scope doc already states.
- If nothing is ambiguous, asks zero questions and states the plan directly.

## What failure looks like

- Asks 3+ questions.
- Asks a question already answered in the pasted doc.
- Asks a generic "what tone/style would you like?" question that isn't in SKILL.md's aspect table at all.
