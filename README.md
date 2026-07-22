# slide-creation

An Agent Skill that makes AI-generated `.pptx` decks look like someone made them on purpose — on the brand's colors, within a slide cap, in a voice that isn't generic AI slop — plus a deterministic checker that catches it when they don't.

## See it, don't take it on faith

Same source brief, two decks, both in [`examples/`](examples/):

- [`examples/source-brief.md`](examples/source-brief.md) — a fictional client brief with real numbers in it.
- [`examples/without-skill.pptx`](examples/without-skill.pptx) — what generic "make me a deck" output looks like: buzzwords, no footer, a JPEG logo, 15 slides against a 12-slide cap, a bare "Thank You!" closer.
- [`examples/with-skill.pptx`](examples/with-skill.pptx) — the same brief, built against [`brand.example.yaml`](brand.example.yaml) following this skill's rules.

Run the checker on both and the difference isn't a matter of taste:

```
$ python scripts/slop_check.py examples/without-skill.pptx --deck-type client_proposal --client-facing --brand brand.example.yaml
examples/without-skill.pptx: 45 findings across 15 slides
  [HIGH] slide 1  banned_phrase       phrase matching /Fast-Paced World/
  [HIGH] slide 2  banned_phrase       phrase matching /robust solution/
  [HIGH] slide 8  empty_slide         no extractable text at all
  [HIGH] slide -  slide_cap_exceeded  15 slides exceeds the cap of 12 for 'client_proposal'
  ...
-> 44 high/medium findings must be fixed before delivery.

$ python scripts/slop_check.py examples/with-skill.pptx --deck-type client_proposal --client-facing --brand brand.example.yaml
examples/with-skill.pptx: 13 findings across 6 slides
  [INFO] slide 2  numeric_claim_needs_source_check  '42%' — confirm this traces to the user's source material
  ...
-> Only low/info findings — review at your discretion.
```

Open both files. The clean one keeps the brief's actual numbers (42%, 1,201 tickets, $186,000 in savings); the sloppy one talks about "unlocking seamless support" and never mentions a single figure from the brief it was supposedly built from.

## The problem

Ask a model for "a deck" and you get plausible-looking slides that ignore your brand, your slide-count conventions, and your house style — every single time, because it has no memory of any of that between conversations. The fix isn't a better prompt; it's putting your conventions in a file the model reads, and a script that checks its output against that file instead of asking it to grade its own homework.

## Install

```
git clone https://github.com/rishikeshydv/skillsmith
cd skillsmith
pip install -r scripts/requirements.txt
cp brand.example.yaml brand.yaml   # then edit it — colors, caps, footer, voice rules
```

Point your agent (Claude, or anything that reads `SKILL.md`-style skill files) at this directory. It'll read `brand.yaml` and `SKILL.md` before building anything.

## Worked example

```
$ python scripts/slop_check.py my_deck.pptx --deck-type client_proposal --client-facing
my_deck.pptx: 2 findings across 8 slides
  [HIGH] slide 3  font_below_minimum  11pt on 'Q3 renewal risk by segment' is below the body minimum of 14pt
  [MEDIUM] slide 6  exclamation_mark  brand voice forbids exclamation marks

-> 2 high/medium findings must be fixed before delivery.
```

Exit code 0 means ship it; exit code 1 means something concrete needs fixing, named down to the slide and the phrase; exit code 2 means the tool itself broke (missing dependency, unreadable file) — not a content problem, don't touch the prose. `SKILL.md` describes the full build loop this plugs into: plan, build against `brand.yaml`, check, batch feedback, version files. The checker is Step 3 of that loop, not the whole thing.

## Why it's built this way

**Deterministic checks instead of asking the model to self-review.** "Does this deck follow the brand guidelines?" is a question the model that just wrote the deck is bad at answering honestly — it wrote confident-sounding slides, so it rates them as fine. A regex for banned phrases, an aspect-ratio comparison for a stretched logo, and a word count against a cap don't have that bias. `scripts/slop_check.py` only asks questions with a mechanically correct answer — font size, slide count, phrase match, footer presence — and leaves the genuinely judgment-based checks (does this number trace to the source, do two decks in one session sound too similar) to a short explicit list the model still has to do by hand. Splitting those apart is the actual design decision here, not the specific regexes.

**Config in YAML, not prose.** `brand.yaml` versus writing "our brand colors are..." into `SKILL.md` directly: a script can load and validate YAML; it can't parse a paragraph reliably, and neither can a model asked to "remember" it turn over turn. Keeping brand facts in structured config also means `SKILL.md` stays a set of rules that don't change per company, while `brand.yaml` is the only file a new team actually needs to edit.

**Planning before drafting.** `SKILL.md` requires a slide-by-slide outline — titles and one line each — before any slide body copy gets written, and a wait for approval unless the request is already unambiguous. The reasoning: a wrong structural assumption caught at the outline stage costs one line to fix; caught after the deck is fully drafted, it costs a full rebuild, because the draft and the structure are entangled once real copy exists. Cheap mistakes should get caught while they're still cheap.

## Repo layout

```
SKILL.md              the skill itself — read by your agent
brand.example.yaml    copy to brand.yaml and fill in your own values (gitignored)
scripts/
  slop_check.py        the checker
  requirements.txt
tests/
  fixtures/             ~19 small .pptx files, each built to trip one specific check
  test_slop_check.py
examples/
  source-brief.md
  with-skill.pptx
  without-skill.pptx
evals/                 10 prompts exercising SKILL.md's documented behaviors, with expected vs. failure
.github/workflows/     CI runs the test suite on every PR
```

## Tests

```
pip install -r scripts/requirements.txt pytest
pytest tests/
```

Every check in `slop_check.py` has a fixture built specifically to trip it, plus a shared clean deck used as the negative case. `tests/fixtures/generate_fixtures.py` and `examples/generate_examples.py` are the scripts that built the committed `.pptx` files — re-run them if you change what a fixture needs to contain.

## License

MIT — see [LICENSE](LICENSE).
