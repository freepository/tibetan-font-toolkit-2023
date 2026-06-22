# Tibetan Font Toolkit

A practical open-source toolkit for diagnosing, documenting, and resolving Tibetan script rendering problems across fonts, platforms, and typesetting software.

**English** | [中文介绍](#中文介绍)

---

## What This Project Provides

Tibetan Font Toolkit provides small, focused utilities and reproducible test data for a real-world problem: **Tibetan stacked characters and complex glyph combinations frequently render incorrectly** in modern software.

### Current Tools (v0.1.0)

| Tool | File | Purpose |
|------|------|---------|
| **Font Diagnostician** | `scripts/diagnose_font.py` | Read-only audit of OpenType tables, Unicode coverage, shaping features, and color tables |
| **Text Normalizer** | `scripts/normalize_tibetan.py` | Fix whitespace, decompose precomposed chars, standardize punctuation, replace legacy PUA |
| **Test Page Generator** | `scripts/generate_test_pages.py` | Generate HTML test pages with Tibetan text samples for cross-platform validation |

### Test Data

- `examples/sample_tibetan_text.txt` — Representative Tibetan text samples
- `examples/before_after.md` — Documented rendering problems and fixes
- `examples/rendering-cases.md` — Platform-specific rendering case studies

### Engineering

- `tests/` — pytest test suite for all scripts
- `.github/workflows/test.yml` — CI running tests on every push
- `requirements.txt` — Declared Python dependencies

---

## Quick Start

```bash
# Clone
git clone https://github.com/freepository/tibetan-font-toolkit-2023.git
cd tibetan-font-toolkit-2023

# Install dependencies
pip install -r requirements.txt

# Run font diagnosis
python scripts/diagnose_font.py /path/to/your/font.ttf --json report.json

# Normalize Tibetan text
python scripts/normalize_tibetan.py input.txt --output normalized.txt --stats

# Generate HTML test page
python scripts/generate_test_pages.py --font /path/to/your/font.ttf --output test.html

# Run tests
pytest
```

---

## Why This Matters

Tibetan script is a complex writing system where consonants stack vertically, vowel marks attach above and below, and syllable boundaries determine line-breaking. These features require correct OpenType shaping (`GSUB`, `GPOS`, `GDEF`) and proper Unicode handling.

**Common problems this toolkit addresses:**

- Stacked character display issues (上下叠字错位)
- Left-right structural glyph problems (左右结构异常)
- Vowel marks rendering in wrong positions
- Legacy fonts using Private Use Area (PUA) instead of standard Unicode
- Color font tables (`SVG`, `COLR/CPAL`) causing black glyphs or export failures
- InDesign, Word, Google Docs, and browser rendering inconsistencies

---

## Project Status

- ✅ Core diagnostic scripts implemented and tested
- ✅ Unicode normalization pipeline working
- ✅ HTML test page generator with embedded font support
- ✅ pytest test suite
- ✅ GitHub Actions CI
- 🔄 Expanding test case library (community contributions welcome)
- 🔄 Font repair utilities (planned for v0.2.0)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. We welcome:

- Bug reports with specific fonts and software versions
- Additional test cases for rare Tibetan/Sanskrit stacks
- Platform-specific rendering documentation
- Pull requests for new diagnostic tools

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## 中文介绍

### 藏文字体工具包

一个用于诊断、记录和解决藏文在不同字体、平台和排版软件中渲染问题的开源工具集。

### 当前提供的工具 (v0.1.0)

| 工具 | 文件 | 用途 |
|------|------|------|
| **字体诊断器** | `scripts/diagnose_font.py` | 只读审计 OpenType 表、Unicode 覆盖、排版特性、彩色表 |
| **文本规范化** | `scripts/normalize_tibetan.py` | 修复空格、分解预组合字符、标准化标点、替换旧编码 |
| **测试页生成** | `scripts/generate_test_pages.py` | 生成 HTML 测试页，用于跨平台字体渲染验证 |

### 快速开始

```bash
pip install -r requirements.txt
python scripts/diagnose_font.py /path/to/font.ttf --json report.json
python scripts/normalize_tibetan.py input.txt --output normalized.txt --stats
python scripts/generate_test_pages.py --font /path/to/font.ttf --output test.html
pytest
```

### 解决的问题

- 上下叠字显示错位
- 左右结构异常
- 元音标记位置错误
- 老旧字体使用私用区编码而非标准 Unicode
- 彩色字体表导致黑块或导出失败
- InDesign、Word、Google Docs 和浏览器渲染不一致

### 参与贡献

欢迎提交 Issue 和 Pull Request！详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

*Maintained by [freepository](https://github.com/freepository) — Tibetan Font Toolkit v0.1.0*
