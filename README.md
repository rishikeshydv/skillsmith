# Presentation Skill Generator

An Agent Skill that builds *other* skills. Give it your logo, a couple of decks that turned out right, and a few answers — it interviews you, then hands back a custom, installable presentation skill for your company: correct branding, sensible slide limits, and your team's actual voice, out of the box.

Built on the open [Agent Skills](https://agentskills.io) standard.

## Why

Non-technical employees waste iterations formatting decks because the model doesn't know their brand or house style. This generator captures that once, per company, so every employee's "make this into slides" comes out right the first time.

## What it produces

```
your-company-presentations/
├── SKILL.md      # the generated skill — brand-aware, capped questions, slide limits, anti-slop checks
├── brand.yaml     # your colors, fonts, logo, slide caps, voice rules
└── assets/        # logo, fonts if custom
```

Relies on Anthropic's public `pptx` skill for rendering mechanics — this only handles the company layer on top.

## Usage

1. Upload `presentation-skill-generator.skill` under **Customize → Skills**.
2. Start a chat: *"Set up branded slide generation for my company."*
3. Upload your logo + 1-3 example decks, answer a few questions, confirm the extracted brand summary.
4. Download the resulting `.skill` file.
5. Upload **that** file — Team/Enterprise: org owner uploads it under **Organization settings → Skills** for everyone; Pro/Max: each person adds it individually.

The generator doesn't install anything for you — step 5 is manual.

## Repo layout

```
skill/presentation-skill-generator/   the generator itself
docs/                                 notes on the org rollout & maintenance loop
```
