---
name: slide-creation
description: Create presentations (.pptx) with correct branding, structure, and length on the first pass. Use whenever Company-X user asks to make, update, or export a deck, slides, or presentation — including phrasings like "turn this into slides," "make a deck for the client," "can you put this in a presentation," or "I need slides for tomorrow's call" — even if they don't mention branding or a template.
---

This skill produces personalized decks without the requester having to specify or supply anything. The requester may be non-technical — never mention this skill, brand.yaml, the check script, or the rendering pipeline. Never ask the user for a template, theme, or starter file. Just produce a correct deck.

Use the pptx skill's technical guidance (pptxgenjs setup, chart rules, image conversion, targeted XML edits) as the mechanical foundation. Everything below is what to do within that foundation for Company-X.

## Brand Config

`brand.yaml` at this skill's root is the single source of truth for colors, fonts, type sizes, logo, slide caps, footer text, and voice rules. Read it. Never guess or restate brand values from memory, and never duplicate them into this file.

## Step 1 — Plan Before Building

Produce a plan first, always. A wrong assumption caught here costs one line; caught after rendering it costs a full rebuild.

Infer the deck type from the request. This sets the cap and whether the footer applies:

| Signals | Deck type |
|---|---|
| standup, weekly, status, progress, sprint | `internal_update` |
| client, pitch, proposal, prospect, SOW | `client_proposal` |
| board, exec, leadership, QBR, steerco | `exec_summary` |
| anything else | `default` |

Ask at most 2 questions, and only when the answer changes the deck. Never ask what the request already states.

| Aspect | Default | Ask only when |
|---|---|---|
| Audience | External client | Deck type is ambiguous between internal and client-facing |
| Length | Cap for the inferred deck type | Source material is far larger or thinner than the cap fits |
| Deck type | Inferred from the table above | No signal matches and the cap materially differs |

If the user says "just show me," render inline and skip the .pptx export — that's a routing rule, not a question.

Then state the plan in one compact block and wait for approval:
Deck type: client_proposal (12 slides max) · Audience: external · Footer: yes
1. [title_slide]     Acme Q3 Proposal
2. [stat_callout]    42% of their support tickets are password resets
3. [two_column]      Current state vs proposed
4. [chart_takeaway]  Cost curve over 18 months
5. [bullets]         Implementation phases
6. [closing]         Decision needed by Aug 15
Flagged: no Q3 revenue figure in the source; slide 4 will show [NEEDS INPUT].

Slide titles plus one line each. Do not draft slide body copy at this stage — that's the content you'd throw away if the structure is wrong.

Skip the approval wait only when the request is unambiguous and the source is already structured (e.g. "turn this doc's five sections into five slides"). Still state the plan; just proceed straight into building.

## Step 2 — Build

- Draft content once from the source material, respecting the cap. One idea per slide.
- Define slide masters once per deck with pptxgenjs `defineSlideMaster()` — one master
  per archetype used, reading every color, font, size, and position from `brand.yaml`.
  Build slides against those masters. Never style a slide inline.
- Set font sizes explicitly on every master. Implicitly inherited sizes can't be
  verified mechanically and cost an extra visual pass.
- Respect `layout.density`. If a slide exceeds the bullet or word limits, it's the
  wrong archetype — convert it to `stat_callout`, `two_column`, or split it.
- Style charts from `layout.charts`. Never ship a bare chart; every chart slide uses
  `chart_takeaway` with the takeaway written as a sentence, not a label.
- Apply the logo and footer per the position and scope rules in `brand.yaml`.
- If a stat is needed and absent from the source, write `[NEEDS INPUT]`. Never invent one.

If content won't fit the cap, cut detail or move it to an appendix. Never shrink below
the minimums in `brand.yaml`, and never quietly overflow — say so before generating.

## Step 3 — Check

Run after every render, before delivering:
python "scripts/slop_check.py" <output.pptx> --deck-type <type> [--client-facing|--internal]

| Code | Meaning | Action |
|---|---|---|
| 0 | Clean | Deliver |
| 1 | HIGH/MEDIUM findings | Fix the text and re-run. Don't ship past a failing check. |
| 2 | Tool failure (line starts `SLOP_CHECK_TOOL_ERROR:`) | Not a content problem. Do not edit prose. Note it in one line and deliver. |

INFO findings are numeric claims surfaced for the traceability check below — they don't block.

The script covers banned phrases, empty and title-only slides, low-specificity slides, repeated title structure, exclamation marks, rhetorical-question titles, slide cap, font minimums, footer presence, and logo format/size/stretch. Don't re-check those by hand.

**Judgment checks the script can't do:**

- Every flagged number traces to the user's source material.
- Text matches the plain-numbers voice rule in `brand.yaml`.
- If this session produced more than one deck: do the openings and section titles sound interchangeable despite different source material? If so, revise the later one and let the source's own shape drive structure.
- Visually confirm no text overflow, and font sizes if the script reported unresolved runs.

Verification is capped at two render-and-inspect passes. If issues remain, deliver with a one-line note on what's still rough rather than looping.

## Step 4 — Handle Feedback in Batches

Revision loops are the most expensive part of deck work. One round of ten changes costs far less than ten rounds of one.

1. **Collect before editing.** If the user sends a partial list or is clearly still reading, ask once: "Anything else before I make these?" Then wait. Don't start editing on the first note.
2. **Read back the batch** as a numbered list, grouped by slide, and confirm before touching the file. Ambiguous items get resolved here, not after a rebuild.
3. **Apply in one pass.** Targeted edits — insert, duplicate, or edit only the affected slides, per the pptx skill. Never regenerate the whole deck for a subset of slides.
4. **Re-run the check once** on the finished result, not per change.
5. **Report in one line** what changed.

If an edit pushes the deck past its cap, say so before applying and ask what to cut. Don't silently overflow.

If the same correction recurs across sessions, mention once — without naming this skill — that the team that maintains our deck conventions can make the fix permanent, and who to send it to (`org.maintainer_contact` in `brand.yaml`).

## File Versioning

Never overwrite a previous output.

- First build: `<topic>_v1.pptx`. Each subsequent edit increments: `_v2`, `_v3`.
- Derive the base name from the deck topic if the user didn't name it.
- State what changed and confirm the prior version survives:

  > "Added slide 4 (Pricing) — acme_proposal_v2.pptx has 7 slides; acme_proposal_v1.pptx (6 slides) is still available above."

- Rebuild any PDF or image export from the current .pptx. Never assume an earlier export still matches.

## Token Discipline

- Plan once, draft once. The plan exists so the draft doesn't get thrown away.
- Never paste slide text back into chat. Describe the deck in 1–2 sentences and deliver the file — the file is the deliverable.
- Batch revisions. See Step 4.

## When Something's Missing

If a brand asset fails to load or the request matches no known deck type, proceed with the closest reasonable default and say plainly, in one sentence, what you approximated. Never block delivery over a missing nicety.