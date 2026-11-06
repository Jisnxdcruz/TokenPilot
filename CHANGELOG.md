# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-11-06

### Added
- `token-optimizer` skill (`skills/token-optimizer/SKILL.md`) with principles for context management, prompt compression, tool-use efficiency, code-generation efficiency, output length, and accuracy safeguards.
- Reference files: context management, prompt optimization, token efficiency and measurement.
- Before/after example of a debugging session.
- `scripts/validate_skill.py`: standard-library validator for frontmatter, naming, length limits, and referenced file paths.
- `scripts/estimate_tokens.py`: heuristic token estimator with a before/after comparison mode. Results are labeled as estimates.
- Test suite in `tests/` runnable with the standard library.
- Benchmark protocol in `tests/BENCHMARKS.md`. No savings figures are claimed in this release.