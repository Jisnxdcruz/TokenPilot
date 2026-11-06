#!/usr/bin/env python3
"""Validate a SKILL.md skill directory against the Agent Skills format rules.

Checks:
  - SKILL.md exists and starts with YAML frontmatter delimited by '---'
  - Required fields 'name' and 'description' are present and non-empty
  - name: max 64 chars, lowercase letters/digits/hyphens, no leading/trailing hyphen,
    matches the directory name
  - description: max 1024 chars
  - body is under 500 lines
  - relative paths to references/, scripts/, examples/, assets/ mentioned in SKILL.md exist

Standard library only. Exit code 0 when valid, 1 when errors are found.

Usage:
    python scripts/validate_skill.py path/to/skill-dir
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PATH_RE = re.compile(r"\b((?:references|scripts|examples|assets)/[A-Za-z0-9_./-]+)")
MAX_NAME = 64
MAX_DESC = 1024
MAX_BODY_LINES = 500


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str, str | None]:
    """Return (fields, body, error). Supports simple single-line 'key: value' pairs."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text, "SKILL.md must start with '---' frontmatter delimiter"
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None, text, "frontmatter is missing closing '---' delimiter"
    fields: dict[str, str] = {}
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith((" ", "\t")):
            return None, "", "nested or continued YAML values are not supported; use single-line values"
        if ":" not in raw:
            return None, "", f"invalid frontmatter line: {raw!r}"
        key, _, value = raw.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    body = "\n".join(lines[end + 1 :])
    return fields, body, None


def validate(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"missing required file: {skill_md}"]

    fields, body, err = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    if err:
        return [err]

    name = fields.get("name", "")
    description = fields.get("description", "")

    if not name:
        errors.append("frontmatter field 'name' is required")
    else:
        if len(name) > MAX_NAME:
            errors.append(f"name is {len(name)} chars; max is {MAX_NAME}")
        if not NAME_RE.match(name):
            errors.append(
                f"name {name!r} must use lowercase letters, digits, and single hyphens, "
                "without leading or trailing hyphens"
            )
        if name != skill_dir.name:
            errors.append(f"name {name!r} must match directory name {skill_dir.name!r}")

    if not description:
        errors.append("frontmatter field 'description' is required")
    elif len(description) > MAX_DESC:
        errors.append(f"description is {len(description)} chars; max is {MAX_DESC}")

    body_lines = body.count("\n") + 1 if body.strip() else 0
    if body_lines > MAX_BODY_LINES:
        errors.append(f"SKILL.md body is {body_lines} lines; keep it under {MAX_BODY_LINES}")

    for ref in sorted(set(PATH_RE.findall(body))):
        ref_clean = ref.rstrip(".")
        if not (skill_dir / ref_clean).exists():
            errors.append(f"SKILL.md references missing file: {ref_clean}")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 1
    skill_dir = Path(argv[1]).resolve()
    if not skill_dir.is_dir():
        print(f"error: not a directory: {skill_dir}")
        return 1
    errors = validate(skill_dir)
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        print(f"\n{len(errors)} error(s) found.")
        return 1
    print(f"OK: {skill_dir.name} is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))