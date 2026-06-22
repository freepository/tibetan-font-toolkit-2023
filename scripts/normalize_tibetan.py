#!/usr/bin/env python3
"""Normalize Tibetan Unicode text for inspection and testing."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PUA_TO_UNICODE = {
    0xE0F0: "\u0F00",
    0xE0F1: "\u0F01",
    0xE0F2: "\u0F02",
    0xE0F3: "\u0F03",
}

PRECOMPOSED_DECOMPOSITION = {
    "\u0F73": "\u0F71\u0F72",
    "\u0F75": "\u0F71\u0F74",
    "\u0F76": "\u0FB2\u0F80",
    "\u0F77": "\u0FB2\u0F71\u0F80",
    "\u0F78": "\u0FB3\u0F80",
    "\u0F79": "\u0FB3\u0F71\u0F80",
    "\u0F81": "\u0F71\u0F80",
}

WHITESPACE_MAP = str.maketrans({
    "\u00A0": " ",
    "\u2000": " ",
    "\u2001": " ",
    "\u2002": " ",
    "\u2003": " ",
    "\u2004": " ",
    "\u2005": " ",
    "\u2006": " ",
    "\u2007": " ",
    "\u2008": " ",
    "\u2009": " ",
    "\u200A": " ",
    "\u202F": " ",
    "\u205F": " ",
    "\u3000": " ",
})

SHAD_VARIANTS = str.maketrans({
    "\u0F0F": "\u0F0D",
    "\u0F10": "\u0F0D",
    "\u0F11": "\u0F0D",
})

TIBETAN_COMBINING_MARKS = frozenset(
    "\u0F71\u0F72\u0F73\u0F74\u0F75\u0F76\u0F77\u0F78\u0F79"
    "\u0F7A\u0F7B\u0F7C\u0F7D\u0F80\u0F81\u0F82\u0F83"
    "\u0F90\u0F91\u0F92\u0F93\u0F94\u0F95\u0F96\u0F97"
    "\u0F99\u0F9A\u0F9B\u0F9C\u0F9D\u0F9E\u0F9F"
    "\u0FA0\u0FA1\u0FA2\u0FA3\u0FA4\u0FA5\u0FA6\u0FA7\u0FA8\u0FA9"
    "\u0FAA\u0FAB\u0FAC\u0FAD\u0FAE\u0FAF\u0FB0\u0FB1\u0FB2\u0FB3"
    "\u0FB4\u0FB5\u0FB6\u0FB7\u0FB8\u0FB9"
)


def normalize(text: str) -> str:
    """Apply a conservative Tibetan text normalization pipeline."""
    chars = []
    for ch in text:
        chars.append(PUA_TO_UNICODE.get(ord(ch), ch))
    text = "".join(chars)

    text = text.translate(WHITESPACE_MAP)
    while "  " in text:
        text = text.replace("  ", " ")

    for composed, decomposed in PRECOMPOSED_DECOMPOSITION.items():
        text = text.replace(composed, decomposed)

    text = text.translate(SHAD_VARIANTS)

    fixed_lines = []
    for line in text.split("\n"):
        if line and line[0] in TIBETAN_COMBINING_MARKS:
            line = "\u25CC" + line
        fixed_lines.append(line)
    text = "\n".join(fixed_lines)

    for mark in ("\u0F71", "\u0F72", "\u0F74", "\u0F7A", "\u0F7C", "\u0F80"):
        text = text.replace(" " + mark, " \u25CC" + mark)

    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Normalize Tibetan Unicode text for testing and inspection."
    )
    parser.add_argument("input", help="Input UTF-8 text file")
    parser.add_argument("--output", "-o", help="Output file; defaults to stdout")
    parser.add_argument("--stats", action="store_true", help="Print basic statistics")
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        return 2

    original = input_path.read_text(encoding="utf-8")
    normalized = normalize(original)

    if args.output:
        Path(args.output).write_text(normalized, encoding="utf-8")
    else:
        print(normalized, end="" if normalized.endswith("\n") else "\n")

    if args.stats:
        print(f"Original length: {len(original)}", file=sys.stderr)
        print(f"Normalized length: {len(normalized)}", file=sys.stderr)
        print(f"Changed: {original != normalized}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
