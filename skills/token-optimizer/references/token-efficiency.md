# Token Efficiency

## Where tokens go

Typical sources of waste, in rough order of impact on long agent sessions:

1. Re-reading whole files when one section is needed
2. Re-sending full history or full prior outputs
3. Repeating instructions or background each turn
4. Unnecessary tool calls, including verification of facts already confirmed
5. Long preambles, recaps, and unrequested extra sections
6. Full-file rewrites when a targeted edit would do

## Tool use

- Batch independent lookups into one step.
- Use search before read.
- Request only the fields you need from structured output.
- Cache results you will reuse within the task (in the state block, not by re-fetching).

## Output length

- Answer first. Expand on request.
- For code edits, show the changed hunk with a line reference, not the whole file.
- For analysis, use a short summary plus the detail the user asked for.

## Measuring honestly

Do not claim savings without measurement. To measure:

1. Pick a fixed set of representative tasks.
2. Run each task with the same model, with and without the skill.
3. Record input and output tokens from the API or usage report, not from estimates.
4. Score output quality with the same criteria in both runs (for example, a checklist of required facts, or tests passing).
5. Report both token change and quality change. A token reduction that lowers quality is not a win.

`scripts/estimate_tokens.py` gives a rough character-based estimate for quick comparisons. It is not a substitute for the API's token counts.

## Trade-offs

- Less output is cheaper, but a missing step costs more in rework. Optimize for total cost to a correct result.
- Summaries save tokens on future turns but can lose detail. Keep verbatim anchors for anything exact.