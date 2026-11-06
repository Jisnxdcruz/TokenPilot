# Prompt Optimization

## Detect repeated instructions

Repetition shows up in three places:

1. **Across turns**: the same rule restated every message. Fix: state it once in the system or project instructions, or in the state block.
2. **Within one prompt**: the same constraint phrased two ways. Fix: merge into one sentence.
3. **Across files**: the same convention documented in several README or config files. Fix: keep one canonical file and link to it.

When two instructions conflict, do not pick one silently. Name the conflict and ask which applies.

## Compression patterns

| Verbose | Compressed |
|---|---|
| "Please make sure that you always remember to use TypeScript strict mode." | "Use TypeScript strict mode." |
| "I would like you to write the output in the form of a bulleted list." | "Output: bulleted list." |
| "Do not include any unnecessary commentary or extra explanation." | "No commentary." |

Compression must not remove a constraint. "Use TypeScript" and "use strict mode" are two constraints; keep both.

## Structure for efficiency

- Put the task first, then constraints, then context, then the output format.
- Use labeled sections only when the prompt is long enough that a reader would otherwise lose track.
- Replace long background with a link or a reference to a file the agent can read on demand.

## Examples: keep them minimal

One example that shows the format is usually enough. Add a second example only when the first could be misread. Mark examples clearly so they are not treated as additional requirements.

## Checklist before sending a prompt

- Is every instruction stated once?
- Does each sentence add a constraint or a fact?
- Is any required detail (version, path, exact string) copied verbatim?
- Would removing any sentence change the result? If yes, keep it.