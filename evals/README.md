# Evals

Ten prompts that exercise specific, documented behaviors from `SKILL.md` —
not "does it make a nice deck" but "does it follow the rule it's supposed to
follow." Each file has the prompt, what a correct run does, and what a
failure concretely looks like, so a bad run is falsifiable rather than a
vibe.

These aren't automated (they require a model in the loop), but they're
written narrowly enough that a human — or a model grading transcripts — can
score them in under a minute each.

| # | Eval | Behavior under test |
|---|------|----------------------|
| 01 | [internal-update-inference](01-internal-update-inference.md) | Deck-type inference from weak signals |
| 02 | [client-proposal-footer](02-client-proposal-footer.md) | Deck-type inference sets footer + cap |
| 03 | [exec-summary-cap](03-exec-summary-cap.md) | Inference picks the tightest matching cap |
| 04 | [question-cap](04-question-cap.md) | Never asks more than 2 questions, never asks what's already stated |
| 05 | [plan-before-build](05-plan-before-build.md) | States a plan and waits, unless the request is unambiguous |
| 06 | [missing-stat](06-missing-stat.md) | Writes `[NEEDS INPUT]` instead of inventing a number |
| 07 | [overflow-cap](07-overflow-cap.md) | Flags cap overage before generating, doesn't silently cut |
| 08 | [slop-check-gate](08-slop-check-gate.md) | Won't deliver past a HIGH/MEDIUM finding |
| 09 | [batched-feedback](09-batched-feedback.md) | Collects revisions before editing, applies once |
| 10 | [file-versioning](10-file-versioning.md) | Never overwrites a prior output |
