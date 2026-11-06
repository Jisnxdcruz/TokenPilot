# Benchmark Protocol

TokenPilot makes no token-savings claim until results from this protocol exist. Results must be reproducible and must report quality alongside tokens.

## Principles

- Same model, same task, same quality criteria, with and without the skill.
- Use token counts reported by the API or the client's usage display, not estimates.
- Report quality changes as well as token changes. A reduction that lowers quality is a regression.
- Run each condition several times. Model output varies, so single runs are anecdotes.

## Task set

Use 8 to 12 representative tasks in at least three categories:

| Category | Example task | Quality check |
|---|---|---|
| Long-thread follow-up | Answer a question in a 40-turn conversation | Answer cites the correct earlier decision |
| Code edit | Change one function in a 400-line file | Diff applies and tests pass |
| Summarization | Summarize a 3,000-word meeting transcript | Lists every decision and action item from a key |
| Tool-heavy task | Find a bug across 5 files | Correct file and line identified |
| Short Q&A | Answer a factual question | Answer is correct and complete |

Write the expected facts or tests for each task before running anything.

## Procedure

1. Fix the model version and settings (temperature, max output tokens).
2. For each task, run baseline (no skill) and treatment (skill loaded), N times each. Start with N = 5.
3. Record: input tokens, output tokens, tool calls, wall-clock time, and the quality result.
4. Score quality blind when possible, using the checklist for that task.
5. Compute median token counts per condition and the quality pass rate per condition.

## Results template

Model: <model id>
Date: <YYYY-MM-DD>
Skill commit: <git sha>
N per cell: <n>

Task	Condition	Median input	Median output	Tool calls	Quality pass rate
...	baseline				
...	skill				

Publish the raw data alongside the summary so others can check the numbers.

## Reporting

A claim such as "reduced output tokens by X% on code-edit tasks" is allowed only when:

- The table above is included, with N and the model stated.
- Quality pass rates are equal or better in the skill condition, or the trade-off is stated plainly.
- The task set and checklists are published.