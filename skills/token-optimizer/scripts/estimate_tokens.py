#!/usr/bin/env python3
"""Rough token estimate for text files, for quick before/after comparisons.

This is a heuristic (about 4 characters per token for English prose, with a word-based
cross-check). It does NOT use any model's tokenizer. Use the API's reported usage for
real measurements.

Usage:
    python scripts/estimate_tokens.py FILE [FILE ...]
    python scripts/estimate_tokens.py --compare BEFORE AFTER
"""
from __future__ import annotations

import sys
from pathlib import Path

CHARS_PER_TOKEN = 4.0
WORDS_PER_TOKEN = 0.75  # tokens ~= words / 0.75 for English prose


def estimate(text: str) -> dict[str, int]:
    chars = len(text)
    words = len(text.split())
    by_chars = round(chars / CHARS_PER_TOKEN)
    by_words = round(words / WORDS_PER_TOKEN)
    return {
        "chars": chars,
        "words": words,
        "estimate": round((by_chars + by_words) / 2),
    }


def read(path: str) -> str:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"not a file: {path}")
    return p.read_text(encoding="utf-8", errors="replace")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    if argv[1] == "--compare":
        if len(argv) != 4:
            print("usage: --compare BEFORE AFTER")
            return 1
        before = estimate(read(argv[2]))["estimate"]
        after = estimate(read(argv[3]))["estimate"]
        change = (after - before) / before * 100 if before else 0.0
        print(f"before: ~{before} tokens (estimated)")
        print(f"after:  ~{after} tokens (estimated)")
        print(f"change: {change:+.1f}% (estimated; verify with API usage counts)")
        return 0
    for path in argv[1:]:
        e = estimate(read(path))
        print(f"{path}: ~{e['estimate']} tokens (estimated), {e['words']} words, {e['chars']} chars")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))