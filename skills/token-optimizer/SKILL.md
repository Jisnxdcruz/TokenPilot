---
name: token-optimizer
description: Reduces unnecessary token use in long conversations, multi-step agent tasks, and code generation while preserving accuracy. Use when context is growing large, when the user asks to shorten output or save tokens, when summarizing long threads, when a task involves many tool calls or large files, or when instructions are being repeated across turns.
---

# Token Optimizer

## Purpose

Spend tokens where they improve the result. Cut repetition, bulk, and waste. Never cut reasoning, verification, or details the task depends on.

**Core rule: correctness outranks brevity.** If a shorter answer would be less accurate, complete, or safe, use the longer one.

## When to activate

Apply this skill when any of these hold:

- The conversation is long and earlier turns restate context already settled.
- The user asks for shorter answers, a summary, or lower cost.
- A multi-step task risks re-reading the same files or repeating the same tool calls.
- Generated code or documents are much longer than the request needs.
- Instructions, constraints, or background are repeated in several places.

Do not activate it for short, single-step tasks where optimization would add overhead without saving anything.

## Principles

1. **Read selectively.** Open the section of a file that answers the question, not the whole file, unless the whole file is needed. Use search (grep, headings, line ranges) first.
2. **Reference, don't restate.** Point to a decision already made ("using the schema from step 2") instead of pasting it again.
3. **Deduplicate instructions.** When a rule appears more than once, keep one authoritative copy. Flag conflicts instead of silently picking one.
4. **Match output length to the request.** Answer the question first. Add detail only when it changes what the user should do.
5. **Batch tool calls.** Combine independent reads or lookups into one step. Skip calls whose results you already have.
6. **Compress history with care.** When summarizing, keep decisions, constraints, open questions, file paths, identifiers, numbers, and error messages verbatim. Drop pleasantries, abandoned drafts, and superseded attempts.
7. **Prefer deterministic tools for mechanical work.** Use a script for counting, parsing, validation, or formatting rather than reasoning through it token by token.

## Context management

- Keep a short running state block for long tasks: goal, decisions made, files touched, open items, and known constraints. Update it instead of rereading the full history.
- When context is large, restate only what the next step needs.
- Do not carry forward outputs that have been superseded. Note only their final result.
- Details: `references/context-management.md`.

## Prompt optimization

- Write instructions once, in the most specific place they apply.
- Remove filler ("Please make sure to", "It is important that you") and hedges that add no constraint.
- Use short, imperative sentences. Use lists when items are parallel; use prose for reasoning.
- Keep examples minimal: one representative example beats five similar ones.
- Details: `references/prompt-optimization.md`.

## Tool-use efficiency

- Before a tool call, check whether the answer is already in context.
- Prefer targeted queries (a specific line range, a grep pattern, a field filter) over full dumps.
- Stop when the question is answered. Do not verify facts that were just confirmed.
- Never skip a call that is needed for correctness, such as reading a file before editing it.

## Code-generation efficiency

- Generate only the changed parts when editing an existing file, unless the user needs the whole file.
- Do not restate unchanged code in explanations. Name the function or line instead.
- Omit boilerplate the user did not ask for, but keep error handling that the task requires.
- Keep comments that explain non-obvious intent. Remove comments that restate the code.

## Output length

- Lead with the answer or the artifact.
- Skip preambles ("Great question") and closing recaps that repeat the body.
- Use the minimum formatting that makes the response clear.
- Expand when the user asks for detail, when the topic is risky, or when a shorter form would omit a needed step.

## Accuracy and safety safeguards

- Never drop constraints, edge cases, warnings, or safety-relevant details to save tokens.
- Never compress a quoted requirement, error message, command, or identifier. Copy it exactly.
- If you summarize and something important was left out, say what was omitted and offer to expand.
- Do not claim a specific percentage of token savings unless it was measured with the same model, task, and quality criteria. Say "estimated" when using the heuristic script.
- When optimization and accuracy conflict, choose accuracy and state the trade-off briefly.

## Examples

Inefficient:

> Sure! I'd be happy to help with that. So, as I mentioned earlier, the config file is config.yaml, and as I said before, the port should be 8080. Here is the full file again for your reference: [400 lines]. Let me know if you want any changes!

Optimized:

> Port is set to 8080 in `config.yaml` (line 12). The only change needed is line 47: replace `timeout: 30` with `timeout: 60`.

More examples: `examples/before.md` and `examples/after.md`.

## Reference files

- `references/context-management.md`: state blocks, history summarization, and handoffs.
- `references/prompt-optimization.md`: instruction deduplication and compression patterns.
- `references/token-efficiency.md`: tool use, output length, and measurement guidance.