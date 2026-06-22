#!/usr/bin/env python3
"""Tibetan Font Toolkit — Rendering Test Page Generator

Generates HTML test pages with Tibetan text samples for cross-platform
font rendering validation. Tests stacked characters, combining marks,
and complex syllable structures.

Usage:
    python scripts/generate_test_pages.py --font "MyFont.ttf" --output test_page.html

Dependencies:
    pip install fontTools
"""
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
from datetime import datetime


# Tibetan test strings covering common rendering cases
TEST_CASES = [
    {
        "name": "Basic Consonants + Tsheg",
        "text": "\u0F40\u0F0B\u0F56\u0F0B\u0F42\u0F0B\u0F58\u0F0B\u0F46\u0F0B\u0F51\u0F0B\u0F54\u0F0B\u0F62\u0F0B\u0F63",
        "description": "Basic Tibetan consonants separated by tsheg (syllable marker)",
    },
    {
        "name": "Stacked Characters (Subjoined)",
        "text": "\u0F40\u0F9A\u0F0B\u0F56\u0FB2\u0F0B\u0F42\u0FB7\u0F0B\u0F58\u0FAD\u0F0B\u0F46\u0F9F\u0F0B\u0F51\u0FB1",
        "description": "Consonants with subjoined letters (yata, rata, lata, vata)",
    },
    {
        "name": "Vowel Marks (Above)",
        "text": "\u0F40\u0F72\u0F0B\u0F56\u0F7A\u0F0B\u0F42\u0F7B\u0F0B\u0F58\u0F7C\u0F0B\u0F46\u0F80\u0F0B\u0F51\u0F81",
        "description": "Vowel marks: i, e, o, u, ai, reversed i",
    },
    {
        "name": "Vowel Marks (Below)",
        "text": "\u0F40\u0F71\u0F0B\u0F56\u0F74\u0F0B\u0F42\u0F71\u0F72\u0F0B\u0F58\u0F71\u0F74\u0F0B\u0F46\u0F75",
        "description": "Vowel marks below: a-chung, u, i+u, a+u, o",
    },
    {
        "name": "Precomposed Characters (Legacy)",
        "text": "\u0F40\u0F73\u0F0B\u0F56\u0F75\u0F0B\u0F42\u0F76\u0F0B\u0F58\u0F77\u0F0B\u0F46\u0F78\u0F0B\u0F51\u0F79\u0F0B\u0F54\u0F81",
        "description": "Precomposed vowel characters (should be decomposed by modern shapers)",
    },
    {
        "name": "Sanskrit/Tantra Stacks",
        "text": "\u0F68\u0F9F\u0FB5\u0F71\u0F72\u0F0B\u0F68\u0FA1\u0FB1\u0F74\u0F0B\u0F68\u0F9C\u0FB7\u0F71\u0F7C",
        "description": "Complex Sanskrit stacks with multiple subjoined letters and vowels",
    },
    {
        "name": "Punctuation Marks",
        "text": "\u0F0D\u0F0E\u0F0F\u0F10\u0F11\u0F14\u0F34\u0F3F\u0FBE\u0FBF\u0F0B\u0F85",
        "description": "Tibetan punctuation: shad, nyis shad, tsheg, yig mgo, etc.",
    },
    {
        "name": "Numbers",
        "text": "\u0F20\u0F21\u0F22\u0F23\u0F24\u0F25\u0F26\u0F27\u0F28\u0F29\u0F0B\u0F2A\u0F2B\u0F2C\u0F2D\u0F2E\u0F2F",
        "description": "Tibetan digits and half digits",
    },
    {
        "name": "Dotted Circle Test",
        "text": "\u25CC\u0F71\u25CC\u0F72\u25CC\u0F74\u25CC\u0F7A\u25CC\u0F7C\u25CC\u0F80\u25CC\u0F82\u25CC\u0F83",
        "description": "Combining marks on dotted circle (U+25CC) — tests mark positioning",
    },
    {
        "name": "Long Pecha Sample",
        "text": "\u0F68\u0F44\u0F0B\u0F56\u0F62\u0F0B\u0F42\u0F72\u0F42\u0F0B\u0F56\u0F66\u0F0B\u0F63\u0F7C\u0F42\u0F0B\u0F62\u0F92\u0FB1\u0F74\u0F44\u0F0B\u0F56\u0F5E\u0F72\u0F0B\u0F42\u0FB2\u0F74\u0F56\u0F0B\u0F56\u0F66\u0F0B\u0F63\u0F7C\u0F42\u0F0D",
        "description": "A complete Tibetan sentence for paragraph-level testing",
    },
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="bo">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tibetan Font Rendering Test — {font_name}</title>
    <style>
        @font-face {{
            font-family: 'TestFont';
            src: url('data:font/ttf;base64,{font_b64}') format('truetype');
            font-display: swap;
        }}
        body {{
            font-family: 'TestFont', 'Noto Sans Tibetan', 'Microsoft Himalaya', sans-serif;
            margin: 40px;
            line-height: 2;
            background: #fafafa;
        }}
        h1 {{ color: #333; border-bottom: 2px solid #0F4C81; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; font-size: 1.1em; }}
        .test-case {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }}
        .tibetan-text {{
            font-size: 24px;
            color: #222;
            margin: 10px 0;
            padding: 10px;
            background: #f5f5f5;
            border-radius: 4px;
            word-wrap: break-word;
        }}
        .description {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        .codepoints {{
            font-family: monospace;
            font-size: 0.8em;
            color: #888;
            margin-top: 5px;
        }}
        .meta {{
            color: #999;
            font-size: 0.85em;
            margin-top: 40px;
            border-top: 1px solid #ddd;
            padding-top: 10px;
        }}
        .pass {{
            color: #2e7d32;
            font-weight: bold;
        }}
        .fail {{
            color: #c62828;
            font-weight: bold;
        }}
        .warn {{
            color: #f57c00;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h1>📝 Tibetan Font Rendering Test</h1>
    <p><strong>Font:</strong> {font_name}</p>
    <p><strong>Generated:</strong> {timestamp}</p>
    <p><strong>Test Cases:</strong> {case_count}</p>

    {test_cases_html}

    <div class="meta">
        <p>Generated by Tibetan Font Toolkit</p>
        <p>For issues, visit: <a href="https://github.com/freepository/tibetan-font-toolkit-2023">github.com/freepository/tibetan-font-toolkit-2023</a></p>
    </div>
</body>
</html>
"""


def generate_test_case_html(case: dict, index: int) -> str:
    """Generate HTML for a single test case."""
    codepoints = " ".join(f"U+{ord(c):04X}" for c in case["text"])
    return f"""
    <div class="test-case">
        <h2>#{index + 1} {case['name']}</h2>
        <div class="tibetan-text">{case['text']}</div>
        <div class="description">{case['description']}</div>
        <div class="codepoints">{codepoints}</div>
    </div>
    """


def generate_html(font_path: Path | None) -> str:
    """Generate complete HTML test page."""
    font_b64 = ""
    font_name = "System Default"

    if font_path and font_path.exists():
        font_data = font_path.read_bytes()
        font_b64 = base64.b64encode(font_data).decode("ascii")
        font_name = font_path.name

    test_cases_html = "\n".join(
        generate_test_case_html(case, i) for i, case in enumerate(TEST_CASES)
    )

    return HTML_TEMPLATE.format(
        font_name=font_name,
        font_b64=font_b64,
        timestamp=datetime.now().isoformat(),
        case_count=len(TEST_CASES),
        test_cases_html=test_cases_html,
    )


def main():
    ap = argparse.ArgumentParser(
        description="Generate HTML test page for Tibetan font rendering validation."
    )
    ap.add_argument("--font", help="Path to font file to embed (optional)")
    ap.add_argument("--output", "-o", default="tibetan_test_page.html", help="Output HTML file")
    ap.add_argument("--json", action="store_true", help="Also output test cases as JSON")
    args = ap.parse_args()

    font_path = Path(args.font) if args.font else None
    html = generate_html(font_path)

    output_path = Path(args.output)
    output_path.write_text(html, encoding="utf-8")
    print(f"Generated: {output_path}")

    if args.json:
        json_path = output_path.with_suffix(".json")
        json_path.write_text(
            json.dumps({
                "generated": datetime.now().isoformat(),
                "font": font_path.name if font_path else None,
                "test_cases": TEST_CASES,
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Generated: {json_path}")


if __name__ == "__main__":
    main()
