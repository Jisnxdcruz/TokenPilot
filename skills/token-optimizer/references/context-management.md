# Context Management

## State block

For tasks spanning many turns, maintain a compact state block and update it each step:

GOAL: <one sentence>
DECIDED: <decision> (reason, if non-obvious)
FILES: <path> (what changed or what was learned)
OPEN: <unresolved question or next action>
CONSTRAINTS: <requirements the output must satisfy>

Rewrite the block instead of appending to it. Remove items that are resolved.

## Summarizing long history

When compressing earlier conversation, preserve:

- Decisions and their reasons
- Requirements, constraints, and acceptance criteria
- File paths, identifiers, versions, URLs, and commands (verbatim)
- Error messages and their causes, and what fixed them
- Open questions and who owns them

Drop:

- Greetings, acknowledgements, and filler
- Superseded drafts and abandoned approaches (keep one line saying why they were abandoned, if that prevents a repeat)
- Duplicated content that appears in a file already referenced

## Handoffs between sessions or agents

Write a handoff note with the state block plus the exact next step. The receiving agent should not need the full history to continue.

## Reading large files

1. Locate the relevant section (headings, grep for symbols or keywords).
2. Read that range with a line window.
3. Expand the window only if the first read is insufficient.

Read the whole file only when the task needs global understanding (for example, a full refactor or a security review).

## Pitfalls

- Summaries that paraphrase exact values (a version number, a flag name) cause subtle errors. Keep those verbatim.
- Over-aggressive pruning can remove the reason a decision was made, leading to it being reversed later. Keep the reason.