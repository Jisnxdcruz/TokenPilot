# Contributing to TokenPilot

Thanks for helping. Please keep changes small, tested, and honest about what they do.

## Ground rules

1. **Correctness over brevity.** A change that saves tokens but lowers accuracy will not be merged.
2. **No unmeasured claims.** Do not add token-savings percentages to docs unless they come from a reproducible benchmark run described in `tests/BENCHMARKS.md`. Include the model, task set, and quality criteria.
3. **No copied implementations.** If you adapt ideas from another project, credit it and confirm its license allows it.
4. **No placeholder files.** Every file should contain working content.
5. **No unnecessary dependencies.** Scripts use the Python standard library.
6. **No secrets.** Never commit API keys, tokens, or private data.

## Development setup

```bash
git clone https://github.com/<your-username>/TokenPilot.git
cd TokenPilot
python3 -m unittest discover -s tests -v
python3 skills/token-optimizer/scripts/validate_skill.py skills/token-optimizer
```

Python 3.9 or newer is required.

## Making changes

- Keep `SKILL.md` under 500 lines. Move detail into `references/`.
- Keep the `description` field under 1024 characters and specific about when to use the skill.
- If you add a file path to `SKILL.md`, the validator will check that it exists.
- Add a test for any new validator rule or script behavior.
- Add an entry under `[Unreleased]` in `CHANGELOG.md`.

## Pull requests

1. Fork the repository and create a branch.
2. Run the tests and the validator. Both must pass.
3. Describe what changed and why. For behavioral changes to the skill, include a before/after example.
4. Keep one logical change per pull request.

## Reporting issues

Include the agent or client you used (for example, Claude Code or Claude.ai), the skill version, the task, and the observed versus expected behavior.