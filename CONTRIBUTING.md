# Contributing to Tibetan Font Toolkit

Thank you for your interest in contributing! This project addresses a niche but important problem: reproducible tools for Tibetan script rendering and font compatibility.

## How to Contribute

### Reporting Issues

When reporting a font rendering issue, please include:

1. **Font file name and version** (or link if freely available)
2. **Software and version** where the problem occurs (e.g., Adobe InDesign 2024, Microsoft Word 365, Chrome 120)
3. **Operating system** (macOS 14, Windows 11, etc.)
4. **Specific Tibetan text** that triggers the problem (Unicode text preferred)
5. **Expected vs. actual behavior** (screenshots or descriptions)
6. **Output of `diagnose_font.py`** if applicable

### Submitting Test Cases

Add new test cases to `examples/` or `tests/fixtures/`:

- Use UTF-8 encoding
- Include both the Tibetan text and a description of what it tests
- Note any platform-specific behavior

### Code Contributions

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Add or update tests in `tests/`
5. Ensure all tests pass: `pytest`
6. Submit a Pull Request with a clear description

### Code Style

- Python: follow PEP 8
- Scripts should be self-contained and accept `--help`
- All font-modifying tools must have a `--dry-run` option or be read-only by default
- Document dependencies in `requirements.txt`

## Development Setup

```bash
git clone https://github.com/freepository/tibetan-font-toolkit-2023.git
cd tibetan-font-toolkit-2023
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pytest
```

## Areas We Need Help

- [ ] More Tibetan/Sanskrit test strings for rare stacks
- [ ] Windows-specific rendering documentation
- [ ] Additional font table parsers (AAT, Graphite)
- [ ] InDesign-specific troubleshooting guides
- [ ] Browser/webfont compatibility matrix
- [ ] Documentation in Tibetan language

## Code of Conduct

Be respectful and constructive. This project serves a global community including Tibetan users, font makers, and document creators. Prioritize accuracy over speed, and always cite sources when making claims about OpenType behavior or platform compatibility.
