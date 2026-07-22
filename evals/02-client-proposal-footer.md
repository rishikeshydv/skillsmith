# 02 — Client proposal footer

**Behavior under test:** deck-type inference sets both the cap and the footer requirement together.

## Prompt

> "Turn this pricing doc into a deck for the prospect call on Thursday." (with a pasted doc)

## Expected behavior

- Infers `client_proposal` from "prospect."
- Plan states the `client_proposal` cap and `Footer: yes`.
- Built deck carries the brand's `client_facing_text` on every slide except the title.
- Runs `slop_check.py --client-facing` (or `--deck-type client_proposal`, which defaults client-facing on) before delivering.

## What failure looks like

- Deck ships without the confidentiality footer.
- Runs the checker with `--internal`, suppressing the footer check entirely.
- Treats "prospect call" as ambiguous and asks an audience question it didn't need to ask.
