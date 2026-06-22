#!/usr/bin/env python3
"""Read-only diagnostic checks for Tibetan and complex-script fonts."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from fontTools.ttLib import TTFont


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _feature_tags(font: TTFont, table_name: str) -> list[str]:
    if table_name not in font:
        return []
    table = font[table_name].table
    feature_list = getattr(table, "FeatureList", None)
    if not feature_list:
        return []
    return sorted({record.FeatureTag for record in feature_list.FeatureRecord})


def diagnose(path: Path) -> dict:
    report = {
        "path": str(path),
        "exists": path.exists(),
        "risks": [],
    }
    if not path.exists():
        report["risks"].append("file_missing")
        return report

    report["bytes"] = path.stat().st_size
    report["sha256"] = sha256(path)

    try:
        font = TTFont(path, lazy=False)
    except Exception as exc:
        report["open_error"] = f"{type(exc).__name__}: {exc}"
        report["risks"].append("ttfont_open_failed")
        return report

    try:
        report["tables"] = list(font.keys())
        report["glyph_count"] = len(font.getGlyphOrder())

        all_codes = set()
        cmap_tables = []
        if "cmap" in font:
            for subtable in font["cmap"].tables:
                cmap_tables.append({
                    "platformID": subtable.platformID,
                    "platEncID": subtable.platEncID,
                    "format": subtable.format,
                    "entries": len(subtable.cmap),
                })
                all_codes.update(subtable.cmap.keys())

        tibetan_codes = sorted(code for code in all_codes if 0x0F00 <= code <= 0x0FFF)
        pua_codes = sorted(code for code in all_codes if 0xE000 <= code <= 0xF8FF)
        report["cmap"] = {
            "tables": cmap_tables,
            "tibetan_codepoints": len(tibetan_codes),
            "pua_codepoints": len(pua_codes),
            "has_dotted_circle_U25CC": 0x25CC in all_codes,
        }

        if not tibetan_codes:
            report["risks"].append("no_tibetan_unicode_codepoints")
        if pua_codes and len(pua_codes) > len(tibetan_codes):
            report["risks"].append("pua_heavy_possible_legacy_encoding")
        if 0x25CC not in all_codes:
            report["risks"].append("missing_dotted_circle_U25CC")

        for table_name in ("GSUB", "GPOS"):
            features = _feature_tags(font, table_name)
            report[table_name] = {"present": table_name in font, "features": features}
            if table_name not in font:
                report["risks"].append(f"missing_{table_name}")

        report["GDEF"] = {"present": "GDEF" in font}
        if "GDEF" not in font:
            report["risks"].append("missing_GDEF")

        report["color_tables"] = {
            tag: tag in font for tag in ("SVG ", "COLR", "CPAL", "sbix", "CBDT", "CBLC")
        }
        if "COLR" in font and "CPAL" not in font:
            report["risks"].append("COLR_without_CPAL")

        metrics = {}
        if "head" in font:
            metrics["unitsPerEm"] = font["head"].unitsPerEm
        if "hhea" in font:
            metrics["hhea"] = {
                "ascent": font["hhea"].ascent,
                "descent": font["hhea"].descent,
                "lineGap": font["hhea"].lineGap,
            }
        if "OS/2" in font:
            os2 = font["OS/2"]
            metrics["OS/2"] = {
                "sTypoAscender": os2.sTypoAscender,
                "sTypoDescender": os2.sTypoDescender,
                "sTypoLineGap": os2.sTypoLineGap,
                "usWinAscent": os2.usWinAscent,
                "usWinDescent": os2.usWinDescent,
            }
        report["metrics"] = metrics
        report["risk_counts"] = dict(Counter(report["risks"]))
        report["risks"] = sorted(set(report["risks"]))
        return report
    finally:
        font.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Diagnose Tibetan and complex-script font rendering risks."
    )
    parser.add_argument("font", help="Path to .ttf, .otf, .woff, or .woff2 font file")
    parser.add_argument("--json", dest="json_path", help="Write report to JSON file")
    args = parser.parse_args(argv)

    report = diagnose(Path(args.font))
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_path:
        Path(args.json_path).write_text(output, encoding="utf-8")
    print(output)
    return 0 if "open_error" not in report else 2


if __name__ == "__main__":
    raise SystemExit(main())
