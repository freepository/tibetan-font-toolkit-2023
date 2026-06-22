#!/usr/bin/env python3
"""Tibetan Font Toolkit — Tibetan Text Normalizer

Normalizes Tibetan Unicode text by:
- Fixing abnormal whitespace (narrow no-break space, etc.)
- Replacing legacy PUA characters with standard Unicode
- Decomposing precomposed characters (U+0F73, U+0F75–U+0F79)
- Standardizing tsheg and shad punctuation
- Adding dotted circle (U+25CC) to orphaned combining marks

Usage:
    python scripts/normalize_tibetan.py input.txt --output normalized.txt

References:
    - Unicode Standard, Tibetan Block U+0F00–U+0FFF
    - Microsoft OpenType Tibetan Shaping
    - W3C Tibetan Layout Requirements
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# Legacy PUA to Unicode mapping (common in old Tibetan fonts)
PUA_TO_UNICODE = {
    0xE0F0: "\u0F00",  # ༀ (Om)
    0xE0F1: "\u0F01",  # ༁
    0xE0F2: "\u0F02",  # ༂
    0xE0F3: "\u0F03",  # ༃
    # Add more as discovered from specific legacy fonts
}

# Precomposed characters that should be decomposed
PRECOMPOSED_DECOMPOSITION = {
    # U+0F73 ཱི = U+0F71 ཱ + U+0F72 ི
    "\u0F73": "\u0F71\u0F72",
    # U+0F75 ཱུ = U+0F71 ཱ + U+0F74 ུ
    "\u0F75": "\u0F71\u0F74",
    # U+0F76 ྲྀ = U+0FB2 ྲ + U+0F80 ྀ
    "\u0F76": "\u0FB2\u0F80",
    # U+0F77 ཷ = U+0FB2 ྲ + U+0F71 ཱ + U+0F80 ྀ
    "\u0F77": "\u0FB2\u0F71\u0F80",
    # U+0F78 ླྀ = U+0FB3 ླ + U+0F80 ྀ
    "\u0F78": "\u0FB3\u0F80",
    # U+0F79 ཹ = U+0FB3 ླ + U+0F71 ཱ + U+0F80 ྀ
    "\u0F79": "\u0FB3\u0F71\u0F80",
    # U+0F81 ཱྀ = U+0F71 ཱ + U+0F80 ྀ
    "\u0F81": "\u0F71\u0F80",
}

# Whitespace normalization
WHITESPACE_MAP = str.maketrans({
    "\u00A0": " ",   # NO-BREAK SPACE → SPACE
    "\u2000": " ",   # EN QUAD → SPACE
    "\u2001": " ",   # EM QUAD → SPACE
    "\u2002": " ",   # EN SPACE → SPACE
    "\u2003": " ",   # EM SPACE → SPACE
    "\u2004": " ",   # THREE-PER-EM SPACE → SPACE
    "\u2005": " ",   # FOUR-PER-EM SPACE → SPACE
    "\u2006": " ",   # SIX-PER-EM SPACE → SPACE
    "\u2007": " ",   # FIGURE SPACE → SPACE
    "\u2008": " ",   # PUNCTUATION SPACE → SPACE
    "\u2009": " ",   # THIN SPACE → SPACE
    "\u200A": " ",   # HAIR SPACE → SPACE
    "\u202F": " ",   # NARROW NO-BREAK SPACE → SPACE
    "\u205F": " ",   # MEDIUM MATHEMATICAL SPACE → SPACE
    "\u3000": " ",   # IDEOGRAPHIC SPACE → SPACE
})

# Shad punctuation standardization
SHAD_VARIANTS = str.maketrans({
    "\u0F0D": "\u0F0D",  # ། (shad) — keep
    "\u0F0E": "\u0F0E",  # ༎ (nyis shad) — keep
    "\u0F0F": "\u0F0D",  # ༏ (tsheg shad) → shad
    "\u0F10": "\u0F0D",  # ༐ (nyis tsheg shad) → shad
    "\u0F11": "\u0F0D",  # ༑ (rin chen spungs shad) → shad (conservative)
})

# Combining marks that need a base character
TIBETAN_COMBINING_MARKS = frozenset(
    "\u0F71\u0F72\u0F73\u0F74\u0F75\u0F76\u0F77\u0F78\u0F79\u0F7A\u0F7B\u0F7C\u0F7D\u0F7E\u0F7F\u0F80\u0F81\u0F82\u0F83\u0F84\u0F86\u0F87\u0F8D\u0F8E\u0F8F\u0F90\u0F91\u0F92\u0F93\u0F94\u0F95\u0F96\u0F97\u0F99\u0F9A\u0F9B\u0F9C\u0F9D\u0F9E\u0F9F\u0FA0\u0FA1\u0FA2\u0FA3\u0FA4\u0FA5\u0FA6\u0FA7\u0FA8\u0FA9\u0FAA\u0FAB\u0FAC\u0FAD\u0FAE\u0FAF\u0FB0\u0FB1\u0FB2\u0FB3\u0FB4\u0FB5\u0FB6\u0FB7\u0FB8\u0FB9\u0FBA\u0FBB\u0FBC\u0FBE\u0FBF\u0FC0\u0FC1\u0FC2\u0FC3\u0FC4\u0FC5\u0FC6\u0FC7\u0FC8\u0FC9\u0FCA\u0FCB\u0FCC\u0FCE\u0FCF"
)


def normalize(text: str) -> str:
    """Apply full Tibetan text normalization pipeline."""
    # Step 1: Replace PUA characters
    result = []
    for ch in text:
        code = ord(ch)
        if code in PUA_TO_UNICODE:
            result.append(PUA_TO_UNICODE[code])
        else:
            result.append(ch)
    text = "".join(result)

    # Step 2: Normalize whitespace
    text = text.translate(WHITESPACE_MAP)
    # Collapse multiple spaces
    while "  " in text:
        text = text.replace("  ", " ")

    # Step 3: Decompose precomposed characters
    for composed, decomposed in PRECOMPOSED_DECOMPOSITION.items():
        text = text.replace(composed, decomposed)

    # Step 4: Standardize shad variants
    text = text.translate(SHAD_VARIANTS)

    # Step 5: Add dotted circle to orphaned combining marks at line starts
    lines = text.split("\n")
    fixed_lines = []
    for line in lines:
        if line and line[0] in TIBETAN_COMBINING_MARKS:
            line = "\u25CC" + line
        fixed_lines.append(line)
    text = "\n".join(fixed_lines)

    # Step 6: Fix orphaned combining marks after spaces
    text = text.replace(" \u0F71", " \u25CC\u0F71")
    text = text.replace(" \u0F72", " \u25CC\u0F72")
    text = text.replace(" \u0F74", " \u25CC\u0F74")

    return text


def main():
    ap = argparse.ArgumentParser(
        description="Normalize Tibetan Unicode text: fix whitespace, decompose precomposed chars, standardize punctuation."
    )
    ap.add_argument("input", help="Input text file (UTF-8)")
    ap.add_argument("--output", "-o", help="Output file (default: stdout)")
    ap.add_argument("--stats", action="store_true", help="Print normalization statistics")
    args = ap.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    original = input_path.read_text(encoding="utf-8")
    normalized = normalize(original)

    if args.stats:
        print(f"Original length:  {len(original)} chars", file=sys.stderr)
        print(f"Normalized length: {len(normalized)} chars", file=sys.stderr)
        print(f"Changes made: {len(original) != len(normalized) or original != normalized}", file=sys.stderr)

    if args.output:
        Path(args.output).write_text(normalized, encoding="utf-8")
        print(f"Written: {args.output}")
    else:
        print(normalized)


if __name__ == "__main__":
    main()
