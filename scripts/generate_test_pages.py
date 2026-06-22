#!/usr/bin/env python3
"""Generate a simple HTML page for Tibetan font rendering checks."""

from __future__ import annotations

import argparse
import base64
import html
import json
from datetime import datetime
from pathlib import Path


TEST_CASES = [
    {
        "name": "Basic syllables",
        "text": "བཀྲ་ཤིས་བདེ་ལེགས།",
        "description": "Basic Tibetan syllables and shad punctuation.",
    },
    {
        "name": "Subjoined letters",
        "text": "ཀྲ བྲ གྲ སྒྲ བརྒྱ བསྒྲུབ",
        "description": "Common stacked consonant structures.",
    },
    {
        "name": "Vowel marks",
        "text": "ཀི ཀུ ཀེ ཀོ ཀཱི ཀཱུ",
        "description": "Above and below vowel mark placement.",
    },
    {
        "name": "Mantra text",
        "text": "ཨོཾ་མ་ཎི་པདྨེ་ཧཱུྃ།",
        "description": "Sanskrit/Tibetan mixed marks.",
    },
    {
        "name": "Dotted circle marks",
        "text": "◌ཱ ◌ི ◌ུ ◌ེ ◌ོ ◌ྲ ◌ླ",
        "description": "Combining marks on dotted circle for visual diagnosis.",
    },
]


def codepoints(text: str) -> str:
    return " ".join(f"U+{ord(char):04X}" for char in text)


def build_html(font_path: Path | None) -> str:
    font_css = ""
    font_name = "System default"
    if font_path and font_path.exists():
        font_name = font_path.name
        encoded = base64.b64encode(font_path.read_bytes()).decode("ascii")
        font_css = (
            "@font-face { "
            "font-family: 'TestTibetanFont'; "
            f"src: url(data:font/ttf;base64,{encoded}) format('truetype'); "
            "}"
        )

    rows = []
    for index, case in enumerate(TEST_CASES, start=1):
        rows.append(
            "<section>"
            f"<h2>{index}. {html.escape(case['name'])}</h2>"
            f"<p class='sample'>{html.escape(case['text'])}</p>"
            f"<p>{html.escape(case['description'])}</p>"
            f"<code>{html.escape(codepoints(case['text']))}</code>"
            "</section>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Tibetan Font Rendering Test</title>
  <style>
    {font_css}
    body {{
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.6;
      margin: 2rem;
      max-width: 960px;
    }}
    .sample {{
      font-family: "TestTibetanFont", serif;
      font-size: 2rem;
      line-height: 2;
      border: 1px solid #ddd;
      padding: 1rem;
    }}
    code {{
      white-space: pre-wrap;
    }}
  </style>
</head>
<body>
  <h1>Tibetan Font Rendering Test</h1>
  <p>Font: {html.escape(font_name)}</p>
  <p>Generated: {datetime.now().isoformat(timespec="seconds")}</p>
  {''.join(rows)}
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate an HTML test page for Tibetan font rendering."
    )
    parser.add_argument("--font", help="Optional font file to embed")
    parser.add_argument("--output", "-o", default="tibetan_test_page.html")
    parser.add_argument("--json", action="store_true", help="Also write test cases as JSON")
    args = parser.parse_args(argv)

    font_path = Path(args.font) if args.font else None
    output_path = Path(args.output)
    output_path.write_text(build_html(font_path), encoding="utf-8")
    print(f"Generated: {output_path}")

    if args.json:
        json_path = output_path.with_suffix(".json")
        json_path.write_text(
            json.dumps(TEST_CASES, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Generated: {json_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
