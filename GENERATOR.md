---
name: skills-generator
description: Interview an admin and build them a custom presentation skill from their brand assets and example decks. Use when someone wants branded slide generation set up for their company, wants consistent decks across a team, or wants to stop employees reformatting client presentations — even if they don't say "skill."
---
## Presentation Skill Generator
You're talking to an admin, not an employee. Turn how their company does decks into a working skill — they shouldn't have to write anything.
The output relies on the separate pptx skill for rendering mechanics. You only build the company layer: brand, length limits, voice, defaults.

## Get Real Examples First
Ask for: 1-3 decks that turned out well, a logo, brand guide if any, fonts if custom. No uploads? Fine — use clean defaults and move on.

## Follow-up questions
Max 5-6, batched. Never ask what an upload already answered.
Always ask: "What do people actually say when they want a deck?" Get 3-6 real phrases — this becomes the trigger description.
Also ask: deck types and rough length per type, typical audience per type, anything required on every slide (legal, confidentiality), who to contact about recurring fixes.
Only ask colors/fonts/logo placement if uploads didn't show it.

## Extraction
Pull exact hex colors and fonts from the decks. Note logo placement. Read the actual sentences for voice — exclamation marks or not, hedged or plain, how numbers are phrased. Turn it into a few specific, checkable rules ("no exclamation marks"), not vague ones ("professional").
Show a short summary — colors, fonts, logo, deck types + limits, voice rules, footer, contact. Get it confirmed before building anything. Mark anything you guessed.

## Building two files
SKILL.md: states it's for a non-technical requester, never surfaces brand files or this generator. Points to the pptx skill for mechanics. Reads brand values from a settings file, never hardcodes them. Asks max 2 questions, defaults for the rest. Has slide caps per deck type. Checks drafts against generic AI-writing tells plus this company's voice rules. Caps self-review at 2 passes. States plainly, in one line, whenever it fell back to a default.
brand.yaml: every real value — colors, fonts, logo path, slide caps, voice rules, footer text, contact. Nothing unused, nothing missing that SKILL.md needs.
Keep SKILL.md short. If a section runs long (usually the voice checklist), split it into a reference file and point to it.

## Package and Rollout
Zip the folder. Team/Enterprise: an org owner uploads it once, it reaches everyone. Pro/Max: each person adds it themselves. Claude Code or API use needs separate setup.
Explain the loop: employees flag recurring corrections to the named contact, who batches them and comes back to update the skill later — same name, only the changed part re-tested.

## Don't
Generate before confirmation. Duplicate pptx's technical rules. Let the skill exceed its own question cap. Invent voice rules that don't trace to something the admin actually showed or said.