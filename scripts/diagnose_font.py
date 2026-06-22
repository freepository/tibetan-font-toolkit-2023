#!/usr/bin/env python3
"""Tibetan Font Toolkit — Font Diagnostic Script

A read-only font diagnostic tool for Tibetan and complex-script fonts.
Checks OpenType tables, Unicode coverage, shaping features, and color tables.

Usage:
    python scripts/diagnose_font.py /path/to/font.ttf --json report.json

Dependencies:
    pip install fontTools
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET

try:
    from fontTools.ttLib import TTFont
except ImportError:
    print("Error: fontTools not installed. Run: pip install fontTools", file=sys.stderr)
    sys.exit(1)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_unicode(rec):
    try:
        return rec.toUnicode()
    except Exception as e:
        return f"<decode-error {type(e).__name__}: {e}>"


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
    except Exception as e:
        report["open_error"] = f"{type(e).__name__}: {e}"
        report["risks"].append("ttfont_open_failed")
        return report

    report["sfntVersion"] = repr(font.sfntVersion)
    report["tables"] = list(font.keys())
    report["glyph_count"] = len(font.getGlyphOrder())

    # name table
    if "name" in font:
        names = []
        lang_counter = Counter()
        for rec in font["name"].names:
            lang_counter[f"p{rec.platformID}-e{rec.platEncID}-l0x{rec.langID:04X}"] += 1
            if rec.nameID in {1, 2, 3, 4, 5, 6, 16, 17}:
                names.append({
                    "nameID": rec.nameID,
                    "platformID": rec.platformID,
                    "platEncID": rec.platEncID,
                    "langID": f"0x{rec.langID:04X}",
                    "value": safe_unicode(rec),
                })
        report["name"] = {"key_records": names, "language_record_counts": dict(lang_counter)}
        for nid in [1, 2, 4, 6]:
            if not font["name"].getName(nid, 3, 1, 0x0409):
                report["risks"].append(f"missing_windows_english_nameID_{nid}")
        if not any(r.platformID == 3 and r.platEncID == 1 and r.langID == 0x0804 for r in font["name"].names):
            report["risks"].append("missing_windows_simplified_chinese_names")

    # cmap
    if "cmap" in font:
        cmap_tables = []
        all_codes = set()
        for st in font["cmap"].tables:
            cmap_tables.append({
                "platformID": st.platformID,
                "platEncID": st.platEncID,
                "format": st.format,
                "entries": len(st.cmap),
            })
            all_codes.update(st.cmap.keys())
        tibetan = [c for c in all_codes if 0x0F00 <= c <= 0x0FFF]
        pua = [c for c in all_codes if 0xE000 <= c <= 0xF8FF]
        report["cmap"] = {
            "tables": cmap_tables,
            "tibetan_codepoints": len(tibetan),
            "pua_codepoints": len(pua),
            "has_dotted_circle_U25CC": 0x25CC in all_codes,
        }
        if pua and len(pua) > len(tibetan):
            report["risks"].append("pua_heavy_possible_legacy_encoding")
        if not tibetan:
            report["risks"].append("no_tibetan_unicode_codepoints")
        if 0x25CC not in all_codes:
            report["risks"].append("missing_dotted_circle_U25CC")

    # GSUB/GPOS
    for tag in ["GSUB", "GPOS"]:
        if tag not in font:
            report["risks"].append(f"missing_{tag}")
            continue
        table = font[tag].table
        features = []
        if getattr(table, "FeatureList", None):
            for fr in table.FeatureList.FeatureRecord:
                features.append({"tag": fr.FeatureTag, "lookups": list(fr.Feature.LookupListIndex)})
        lookup_types = Counter()
        if getattr(table, "LookupList", None):
            for lookup in table.LookupList.Lookup:
                lookup_types[str(lookup.LookupType)] += 1
        report[tag] = {"features": features, "lookup_type_counts": dict(lookup_types)}

    # GDEF
    if "GDEF" in font:
        gdef = font["GDEF"].table
        class_defs = getattr(getattr(gdef, "GlyphClassDef", None), "classDefs", None)
        if class_defs:
            report["GDEF"] = {"glyph_class_counts": dict(Counter(map(str, class_defs.values())))}
        else:
            report["GDEF"] = {"glyph_class_counts": {}}
            report["risks"].append("gdef_no_glyph_class_def")
    else:
        report["risks"].append("missing_GDEF")

    # SVG
    if "SVG " in font:
        svg_report = {"doc_count": len(font["SVG "].docList), "docs": [], "fill_counts": Counter(), "multi_path_docs": 0, "parse_errors": 0}
        for doc in font["SVG "].docList:
            item = {"startGlyphID": doc.startGlyphID, "endGlyphID": doc.endGlyphID, "chars": len(doc.data), "compressed": bool(doc.compressed)}
            try:
                root = ET.fromstring(doc.data)
                paths = root.findall(".//{http://www.w3.org/2000/svg}path")
                item["path_count"] = len(paths)
                fills = [(p.get("fill") if p.get("fill") is not None else "<none>") for p in paths]
                item["fills_sample"] = fills[:10]
                svg_report["fill_counts"].update(fills)
                if len(paths) > 1:
                    svg_report["multi_path_docs"] += 1
                if any(f in {"currentColor", "context-fill", "<none>"} for f in fills):
                    report["risks"].append(f"svg_risky_fill_gid_{doc.startGlyphID}_{doc.endGlyphID}")
            except Exception as e:
                item["parse_error"] = f"{type(e).__name__}: {e}"
                svg_report["parse_errors"] += 1
            svg_report["docs"].append(item)
        svg_report["fill_counts"] = dict(svg_report["fill_counts"])
        report["SVG"] = svg_report
        if svg_report["multi_path_docs"]:
            report["risks"].append("svg_multi_path_docs_present")

    # COLR/CPAL
    report["color_tables"] = {tag: (tag in font) for tag in ["SVG ", "COLR", "CPAL", "sbix", "CBDT", "CBLC"]}
    if "COLR" in font and "CPAL" not in font:
        report["risks"].append("COLR_without_CPAL_ignored_by_spec")

    # metrics
    metrics = {}
    if "head" in font:
        metrics["unitsPerEm"] = font["head"].unitsPerEm
    if "hhea" in font:
        metrics["hhea"] = {"ascent": font["hhea"].ascent, "descent": font["hhea"].descent, "lineGap": font["hhea"].lineGap}
    if "OS/2" in font:
        os2 = font["OS/2"]
        metrics["OS/2"] = {"sTypoAscender": os2.sTypoAscender, "sTypoDescender": os2.sTypoDescender, "sTypoLineGap": os2.sTypoLineGap, "usWinAscent": os2.usWinAscent, "usWinDescent": os2.usWinDescent}
    report["metrics"] = metrics

    font.close()
    report["risks"] = sorted(set(report["risks"]))
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Diagnose Tibetan/complex-script fonts for OpenType table integrity, Unicode coverage, and rendering risks."
    )
    ap.add_argument("font", help="Path to font file (.ttf, .otf, .woff, etc.)")
    ap.add_argument("--json", dest="json_path", help="Write JSON report to file")
    args = ap.parse_args(argv)
    report = diagnose(Path(args.font))
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_path:
        Path(args.json_path).write_text(text, encoding="utf-8")
    print(text)
    return 0 if "open_error" not in report else 2


if __name__ == "__main__":
    raise SystemExit(main())
