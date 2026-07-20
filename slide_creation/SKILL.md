---
name: slide-creation
description: Create presentations (.pptx) with correct branding, structure, and length on the first pass. Use whenever Company-X user asks to make, update, or export a deck, slides, or presentation — including phrasings like "turn this into slides," "make a deck for the client," "can you put this in a presentation," or "I need slides for tomorrow's call" — even if they don't mention branding or a template.
---
This skill produces personalized decks without the requester having to specify anything. The requester may be non-technical — never mention this skill, brand.yaml, or the rendering pipeline; just produce a correct deck.
Use the pptx skill's technical guidance (pptxgenjs setup, chart rules, QA process, image conversion) as the mechanical foundation. Everything below is what to do within that foundation for Company-X specifically.

## Brand Config
- Read brand.yaml in this skill's folder for exact colors, fonts, and logo paths.
Never guess or restate brand values from memory.

## Ask Little
- Ask at most 2 questions before generating, only if the answer changes the deck. Never ask something already stated in the request.
Aspect: Audience
Default: External client
Ask only when: request doesn't make it obvious

Aspect: Length
Default: See slide caps below
Ask only when: source material is unusually large or thin

Aspect: Deliverable
Default: .pptx
Ask only when: user says "just show me" (then render inline, don't export)

## Slide Length
- Unbounded length is the #1 way decks become bloated and expensive to fix. Cap by
deck type; if a cap would be exceeded, tell the user before generating rather than
quietly overflowing.
Internal status update: 6 slides max
Client proposal: 10–12 slides
Board/exec summary: 5 slides max, one number or decision per slide
- One idea per slide. If content doesn't fit the cap, cut detail or split into an
appendix — never shrink font size below 14pt body / 24pt title to force a fit.

## Anti-slop Checklist
Before rendering, check the drafted text against this list:
- No stock openers: "In today's fast-paced world," "Unlock the power of," "Let's dive in"
- No filler intensifiers: "truly," "seamlessly," "robust," "cutting-edge" used as decoration
- No claim, number, or stat that isn't traceable to the user's source material — if a number is needed and absent, mark it [NEEDS INPUT] rather than inventing one
- No content-free slides ("Thank You" slides with no next step; "Questions?" with nothing else)
Also check drafted text against voice_rules in brand.yaml.

## Producing the deck
- Draft slide-by-slide content from the source material, respecting the length cap.
- Build with pptxgenjs per the pptx skill's technical rules such as layout, colors, charts.
- Convert to images and run the verification checklist below

## Verification Checklist
- Logo present per spec, correctly sized, not stretched
- Brand colors and fonts applied exactly from brand.yaml
- No text overflow or cut-off content
- Slide count within the cap for this deck type
- Anti-slop checklist re-confirmed on final text
- Client-facing decks include the confidentiality footer: "Company-X — Confidential" on every slide except the title

## Note
If a brand asset fails to load or the request doesn't match a known deck type,
proceed with the closest reasonable default and say plainly, in one sentence,
what you approximated. Never block delivery over a missing nicety.

## Token Budget
- Draft content once from the source material before touching layout.
- Verification is capped at two render-and-inspect passes. If issues remain after two passes, deliver with a one-line note on what's still rough rather than looping indefinitely.
- Never paste full slide text back into the chat response — describe the deck in
- 1–2 sentences and deliver the file. The file is the deliverable, not the chat.

## File Versioning & Edits
When a request modifies an existing deck (add/remove/reorder a slide, edit content) rather than
creating a new one:
- Never overwrite the previous output file. Save the edited deck under an incremented filename
  (e.g. `clientname_v2.pptx` following `clientname_v1.pptx`). If the user didn't name the file,
  derive a base name from the deck topic and version it from v1.
- State in one sentence what changed and confirm the previous version is untouched, e.g.:
  "Added slide 4 (Pricing) — deck.pptx now has 7 slides; deck_v1.pptx (6 slides) is still available above."
- If asked to regenerate a PDF or image export after an edit, always rebuild it from the current
  .pptx — never assume an earlier PDF in the conversation still matches the deck's current state.
- Internally, edits should still be targeted (insert/duplicate the specific slide, edit only the
  changed slide's XML) per the pptx skill — this section only governs what gets saved and said,
  not how the edit is made.

## Feedback Loop
If the user corrects something and it seems likely to recur, mention once that Bikalpa (Head of AI) maintains this skill and can make the fix permanent.