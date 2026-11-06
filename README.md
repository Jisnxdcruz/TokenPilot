# TokenPilot

TokenPilot is an open-source agent skill that helps AI assistants use fewer tokens without giving up accuracy, reasoning, or task completion.

## Problem

Long conversations and agent workflows waste tokens in predictable ways: whole files are re-read when one section would do, earlier turns are restated, the same instructions are repeated, outputs carry preambles and recaps, and tool calls are made that add nothing. The cost grows with every turn, and the context window fills up faster than it needs to.

Cutting tokens naively causes its own problems. A summary that drops a version number, or a shortened answer that skips a step, costs more in rework than it saved. TokenPilot is built around that trade-off.

## Features

- **Context management**: state blocks for long tasks, history summarization that keeps decisions and exact identifiers, and handoff notes.
- **Prompt optimization**: finds repeated instructions and compresses filler without removing constraints.
- **Tool-use efficiency**: search before read, targeted line ranges, batched lookups, and no repeated verification.
- **Code-generation efficiency**: targeted edits instead of full-file rewrites, and no restating unchanged code.
- **Output length control**: answer first, expand on request.
- **Safeguards**: exact preservation of commands, paths, and error messages, and no unmeasured savings claims.
- **Validator script**: checks SKILL.md frontmatter, naming, length limits, and referenced files.
- **Estimator script**: rough before/after token comparison, clearly labeled as an estimate.
- **Benchmark protocol**: a method for measuring real token and quality changes.

## Repository layout

```
TokenPilot/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .gitignore
├── skills/
│   └── token-optimizer/
│       ├── SKILL.md                  # Core instructions (loaded on activation)
│       ├── references/               # Detailed guidance (loaded on demand)
│       ├── scripts/
│       │   ├── validate_skill.py     # Structural validation
│       │   └── estimate_tokens.py    # Heuristic token estimate
│       └── examples/
│           ├── before.md
│           └── after.md
└── tests/
    ├── test_skill.py                 # Standard-library test suite
    └── BENCHMARKS.md                 # Measurement protocol
```

## Installation

### Claude Code

Copy the skill into a Claude Code skills directory.

Personal (available in all projects):

```bash
git clone https://github.com/jisnxdcruz/TokenPilot.git
mkdir -p ~/.claude/skills
cp -r TokenPilot/skills/token-optimizer ~/.claude/skills/
```

Project-only (checked into one repository):

```bash
mkdir -p .claude/skills
cp -r /path/to/TokenPilot/skills/token-optimizer .claude/skills/
```

Restart Claude Code or start a new session so the skill is discovered. Check that it appears in the skills list.

### Claude.ai

Skill support in Claude.ai depends on your plan and the current feature set. If your account has custom skill upload:

1. Zip the skill folder so `token-optimizer/SKILL.md` is at the root of the archive: `cd TokenPilot/skills && zip -r token-optimizer.zip token-optimizer`
2. Upload the zip in the skills section of your settings.
3. Enable the skill and start a new conversation.

If your account does not offer skill upload, paste the contents of `SKILL.md` into a project's custom instructions or a conversation's first message. Note that this costs tokens on every turn, which is the opposite of what the skill is for, so prefer a native skill install when available.

### Other agents

Any agent that supports the Agent Skills format (a directory with a `SKILL.md` file containing YAML frontmatter) can load this skill. Check your agent's documentation for the skill directory location.

## Usage

Once installed, the skill activates when a task matches its description, such as a long conversation, a multi-step task, a request to shorten output, or a request to save tokens. You can also ask for it directly:

> Use the token-optimizer skill to summarize this thread. Keep every decision, file path, and open question.

Validate a skill after editing it:

```bash
python3 skills/token-optimizer/scripts/validate_skill.py skills/token-optimizer
```

Compare two versions of a text file (estimate only):

```bash
python3 skills/token-optimizer/scripts/estimate_tokens.py --compare before.md after.md
```

See `skills/token-optimizer/examples/` for a before/after example.

## Supported agents

| Agent | Status |
|---|---|
| Claude Code | Supported. Installed by copying the skill directory. |
| Claude.ai | Supported where custom skill upload is available. Otherwise, use custom instructions as a fallback. |
| Other Agent Skills-compatible agents | Expected to work. Not individually tested. |

Testing across clients is still limited. If you test TokenPilot in another agent, please open an issue with your results.

## Measured results

None yet. TokenPilot makes no token-savings claim. To measure, follow `tests/BENCHMARKS.md`, then open a pull request that adds results with the model, task set, and quality data.

## Limitations

- The token estimator is a heuristic. It does not use any model's tokenizer.
- The validator checks structure, not content quality or whether the skill triggers correctly in a given client.
- Activation depends on the client's skill-matching logic and on the description text. It is not guaranteed.
- Summarization can lose information. The skill tries to keep exact values, but you should check summaries of anything critical.
- The skill changes how the model writes and reads. It cannot change the client's own context handling or billing.

## Contributing

See `CONTRIBUTING.md`. Please keep changes tested, measured, and free of unsupported claims.

## License

MIT. See `LICENSE`.