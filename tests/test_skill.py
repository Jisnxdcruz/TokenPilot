"""Tests for the token-optimizer skill and its scripts. Standard library only.

Run from the repository root:
    python -m unittest discover -s tests -v
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "token-optimizer"
SCRIPTS = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS))

import validate_skill  # noqa: E402
import estimate_tokens  # noqa: E402


class StructureTests(unittest.TestCase):
    def test_required_files_exist(self):
        for rel in [
            "README.md", "LICENSE", "CONTRIBUTING.md", "CHANGELOG.md", ".gitignore",
            "skills/token-optimizer/SKILL.md",
            "skills/token-optimizer/references/context-management.md",
            "skills/token-optimizer/references/prompt-optimization.md",
            "skills/token-optimizer/references/token-efficiency.md",
            "skills/token-optimizer/examples/before.md",
            "skills/token-optimizer/examples/after.md",
        ]:
            with self.subTest(path=rel):
                self.assertTrue((ROOT / rel).is_file(), f"missing {rel}")

    def test_no_empty_placeholder_files(self):
        for path in ROOT.rglob("*"):
            if path.is_file() and ".git" not in path.parts:
                with self.subTest(path=str(path.relative_to(ROOT))):
                    self.assertGreater(path.stat().st_size, 0, "empty file")

    def test_scripts_directory_has_real_scripts(self):
        scripts = sorted(p.name for p in SCRIPTS.glob("*.py"))
        self.assertEqual(scripts, ["estimate_tokens.py", "validate_skill.py"])


class FrontmatterTests(unittest.TestCase):
    def test_repo_skill_is_valid(self):
        self.assertEqual(validate_skill.validate(SKILL_DIR), [])

    def test_description_is_specific_about_activation(self):
        fields, _, err = validate_skill.parse_frontmatter((SKILL_DIR / "SKILL.md").read_text())
        self.assertIsNone(err)
        self.assertIn("Use when", fields["description"])
        self.assertLessEqual(len(fields["description"]), validate_skill.MAX_DESC)

    def test_parse_rejects_missing_delimiter(self):
        _, _, err = validate_skill.parse_frontmatter("name: x\n")
        self.assertIsNotNone(err)

    def test_parse_rejects_unclosed_frontmatter(self):
        _, _, err = validate_skill.parse_frontmatter("---\nname: x\n")
        self.assertIsNotNone(err)


class ValidatorRuleTests(unittest.TestCase):
    def make_skill(self, name_dir: str, frontmatter: str, body: str = "# Body\n") -> Path:
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, True)
        d = tmp / name_dir
        d.mkdir()
        (d / "SKILL.md").write_text(f"---\n{frontmatter}\n---\n{body}")
        return d

    def test_valid_minimal_skill(self):
        d = self.make_skill("my-skill", "name: my-skill\ndescription: Does a thing. Use when needed.")
        self.assertEqual(validate_skill.validate(d), [])

    def test_name_must_match_directory(self):
        d = self.make_skill("other-dir", "name: my-skill\ndescription: Does a thing.")
        self.assertTrue(any("must match directory" in e for e in validate_skill.validate(d)))

    def test_name_rejects_uppercase_and_underscores(self):
        for bad in ["My-Skill", "my_skill", "-leading", "trailing-", "double--hyphen"]:
            with self.subTest(name=bad):
                d = self.make_skill(bad, f"name: {bad}\ndescription: Does a thing.")
                self.assertTrue(any("must use lowercase" in e for e in validate_skill.validate(d)))

    def test_name_length_limit(self):
        long_name = "a" * 65
        d = self.make_skill(long_name, f"name: {long_name}\ndescription: Does a thing.")
        self.assertTrue(any("max is 64" in e for e in validate_skill.validate(d)))

    def test_description_required(self):
        d = self.make_skill("my-skill", "name: my-skill")
        self.assertTrue(any("'description' is required" in e for e in validate_skill.validate(d)))

    def test_description_length_limit(self):
        desc = "x" * 1025
        d = self.make_skill("my-skill", f"name: my-skill\ndescription: {desc}")
        self.assertTrue(any("max is 1024" in e for e in validate_skill.validate(d)))

    def test_body_line_limit(self):
        body = "\n".join(f"line {i}" for i in range(520)) + "\n"
        d = self.make_skill("my-skill", "name: my-skill\ndescription: Does a thing.", body)
        self.assertTrue(any("keep it under 500" in e for e in validate_skill.validate(d)))

    def test_missing_referenced_file_is_reported(self):
        d = self.make_skill(
            "my-skill",
            "name: my-skill\ndescription: Does a thing.",
            "See `references/nope.md` for details.\n",
        )
        self.assertTrue(any("missing file: references/nope.md" in e for e in validate_skill.validate(d)))

    def test_missing_skill_md(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, True)
        self.assertTrue(any("missing required file" in e for e in validate_skill.validate(tmp)))


class EstimateTokensTests(unittest.TestCase):
    def test_estimate_is_positive_and_scales(self):
        short = estimate_tokens.estimate("hello world")
        long = estimate_tokens.estimate("hello world " * 100)
        self.assertGreater(short["estimate"], 0)
        self.assertGreater(long["estimate"], short["estimate"])

    def test_empty_text(self):
        self.assertEqual(estimate_tokens.estimate("")["estimate"], 0)

    def test_cli_compare_runs(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, True)
        a, b = tmp / "a.md", tmp / "b.md"
        a.write_text("word " * 200)
        b.write_text("word " * 100)
        out = subprocess.run(
            [sys.executable, str(SCRIPTS / "estimate_tokens.py"), "--compare", str(a), str(b)],
            capture_output=True, text=True, check=True,
        ).stdout
        self.assertIn("change:", out)
        self.assertIn("-", out.split("change:")[1])

    def test_validator_cli_exit_codes(self):
        ok = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate_skill.py"), str(SKILL_DIR)],
            capture_output=True, text=True,
        )
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)


class ExamplesTests(unittest.TestCase):
    def test_after_is_shorter_than_before(self):
        before = estimate_tokens.estimate((SKILL_DIR / "examples/before.md").read_text())["estimate"]
        after = estimate_tokens.estimate((SKILL_DIR / "examples/after.md").read_text())["estimate"]
        self.assertLess(after, before)

    def test_after_preserves_critical_details(self):
        after = (SKILL_DIR / "examples/after.md").read_text()
        for critical in ["auth/login.py", "ex=SESSION_TTL", "config/settings.py", "line 104"]:
            with self.subTest(detail=critical):
                self.assertIn(critical, after)


if __name__ == "__main__":
    unittest.main()