# Tibetan Font Toolkit

A practical open-source toolkit for diagnosing, documenting, and gradually improving Tibetan script rendering problems across fonts, platforms, and typesetting software.

一个用于诊断、记录和逐步改善藏文在字体、平台和排版软件中渲染问题的开源工具集。

---

## Project Status: Early Preview

This project is under active development.

The current tools are intended for testing, research, documentation, and community feedback. Please do **not** use them yet for production work, bulk font processing, commercial font repair, or important documents without manual verification.

The project may still change quickly, including script behavior, command-line options, test data, and documentation structure.

## 项目状态：早期预览版

本项目仍在持续完善中。

当前工具主要用于测试、研究、问题记录和社区反馈。暂不建议直接用于正式生产、批量处理字体、商业字体修复或重要文档；如需使用，请务必人工核验结果。

项目仍可能快速变化，包括脚本行为、命令参数、测试数据和文档结构。

---

## What This Project Tries to Solve

Tibetan script is a complex writing system. Consonants can stack vertically, vowel marks may appear above or below base letters, and proper rendering depends on Unicode handling, OpenType shaping, font tables, and application support.

In real use, Tibetan text may render differently in:

- Microsoft Word
- Adobe InDesign
- Google Docs
- Web browsers
- PDF export workflows
- Different operating systems and font engines

Common problems include:

- Stacked characters displaying incorrectly
- Vowel marks appearing in the wrong position
- Legacy fonts using Private Use Area characters instead of standard Unicode
- Missing or incomplete OpenType shaping tables
- Inconsistent behavior between editing software and exported PDF
- Color font tables causing unexpected black glyphs or export problems

This toolkit is intended to make these problems easier to inspect, reproduce, document, and eventually fix.

---

## Current Tools

The current early version includes several small Python utilities.

| Tool | File | Purpose |
|---|---|---|
| Font Diagnostician | `scripts/diagnose_font.py` | Read-only inspection of font tables, Unicode coverage, OpenType shaping features, and possible rendering risks |
| Tibetan Text Normalizer | `scripts/normalize_tibetan.py` | Normalize Tibetan text, whitespace, punctuation, selected legacy characters, and precomposed Tibetan characters |
| Test Page Generator | `scripts/generate_test_pages.py` | Generate simple HTML test pages for checking Tibetan rendering across fonts and platforms |

These tools are experimental and should be treated as inspection and testing helpers, not final production utilities.

---

## Installation

For now, installation is recommended only for testing.

```bash
git clone https://github.com/freepository/tibetan-font-toolkit-2023.git
cd tibetan-font-toolkit-2023
pip install -r requirements.txt
````

If you are not familiar with Python environments, it is safer to use a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Usage Examples

### Diagnose a Font

```bash
python scripts/diagnose_font.py /path/to/font.ttf --json report.json
```

This performs a read-only inspection of the font and writes a JSON report.

### Normalize Tibetan Text

```bash
python scripts/normalize_tibetan.py input.txt --output normalized.txt --stats
```

This reads a UTF-8 text file and writes a normalized output file.

### Generate a Rendering Test Page

```bash
python scripts/generate_test_pages.py --font /path/to/font.ttf --output tibetan_test_page.html
```

This generates an HTML page that can be opened in a browser to visually inspect Tibetan rendering behavior.

---

## Roadmap

Planned improvements include:

* Add reproducible sample text files in `examples/`
* Add before/after rendering case documentation
* Add pytest-based tests for the current scripts
* Add GitHub Actions CI
* Add more Tibetan and Sanskrit stack test cases
* Improve documentation for Word, InDesign, Google Docs, browser, and PDF workflows
* Add safer font analysis reports for non-programmers
* Investigate future repair utilities for specific font problems

---

## Why This Matters

Many Tibetan users, editors, publishers, designers, and researchers depend on correct Tibetan text rendering. However, Tibetan rendering problems are often difficult to explain and reproduce because the cause may involve several layers:

* Unicode text encoding
* Font glyph coverage
* OpenType `GSUB`, `GPOS`, and `GDEF` tables
* Application-specific shaping behavior
* PDF export behavior
* Legacy font encodings

This project aims to provide small, transparent, reproducible tools that help users and developers identify where a problem may be happening.

---

## Contributing

Contributions are welcome, especially:

* Real-world Tibetan rendering problems
* Problematic sample text
* Font compatibility reports
* Screenshots from different platforms
* Bug reports with software version information
* Test cases for rare Tibetan or Sanskrit stacks
* Improvements to scripts and documentation

Please see `CONTRIBUTING.md` for contribution guidelines.

---

## Safety Notes

This project is currently focused on diagnosis and documentation.

Before using any output from this toolkit in important work:

* Keep backups of original files
* Manually inspect all generated results
* Do not overwrite original documents or fonts
* Treat normalization output as a draft that requires review
* Test across the actual software you plan to use

---

## License

MIT License.

---

# 中文介绍

## 藏文字体工具包

Tibetan Font Toolkit 是一个用于诊断、记录和逐步改善藏文排版与字体渲染问题的开源工具集。

本项目关注的问题包括：

* 藏文上下叠字显示错位
* 元音符号位置异常
* 老旧字体使用私用区编码
* OpenType 排版表不完整
* Word、InDesign、Google Docs、浏览器和 PDF 导出结果不一致
* 彩色字体表导致黑块、导出异常或显示问题

---

## 当前状态

本项目目前是早期预览版，仍在持续完善。

当前脚本主要用于测试、研究和问题记录。暂不建议直接用于正式生产、批量处理字体或重要文档。使用结果必须人工核验。

---

## 当前工具

| 工具        | 文件                               | 用途                                    |
| --------- | -------------------------------- | ------------------------------------- |
| 字体诊断器     | `scripts/diagnose_font.py`       | 只读检查字体表、Unicode 覆盖、OpenType 排版特性和潜在风险 |
| 藏文文本规范化工具 | `scripts/normalize_tibetan.py`   | 规范化藏文文本、空格、标点、部分旧编码和预组合字符             |
| 渲染测试页生成器  | `scripts/generate_test_pages.py` | 生成 HTML 测试页，用于观察不同字体和平台下的藏文显示效果       |

---

## 测试安装

```bash
git clone https://github.com/freepository/tibetan-font-toolkit-2023.git
cd tibetan-font-toolkit-2023
pip install -r requirements.txt
```

建议使用虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 使用示例

### 检查字体

```bash
python scripts/diagnose_font.py /path/to/font.ttf --json report.json
```

### 规范化藏文文本

```bash
python scripts/normalize_tibetan.py input.txt --output normalized.txt --stats
```

### 生成藏文渲染测试页

```bash
python scripts/generate_test_pages.py --font /path/to/font.ttf --output tibetan_test_page.html
```

---

## 后续计划

后续计划包括：

* 增加 `examples/` 示例文本
* 增加典型问题的 before/after 文档
* 增加 pytest 测试
* 增加 GitHub Actions 自动测试
* 补充更多藏文和梵文叠字测试案例
* 补充 Word、InDesign、Google Docs、浏览器和 PDF 的兼容性说明
* 为非程序员用户生成更易读的诊断报告
* 研究特定字体问题的安全修复工具

---

## 参与贡献

欢迎提交：

* 真实藏文显示问题
* 问题文本样本
* 字体兼容性报告
* 不同平台截图
* 软件版本信息
* 罕见叠字测试案例
* 脚本和文档改进

请参考 `CONTRIBUTING.md`。

---

## 重要提醒

本项目当前主要用于诊断和记录问题。

在正式使用前，请务必：

* 保留原始文件备份
* 人工检查所有输出结果
* 不要覆盖原始字体或重要文档
* 将规范化结果视为草稿
* 在实际使用的软件中重新测试

---

Maintained by `freepository`.

```
```
