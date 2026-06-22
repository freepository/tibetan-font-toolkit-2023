# Tibetan Rendering Test Cases

These cases are intended for manual comparison across fonts, browsers, editors, and PDF export workflows.

| Category | Sample | What to Check |
|---|---|---|
| Basic syllables | `བཀྲ་ཤིས།` | Clear consonant and vowel positioning |
| Subjoined letters | `ཀྲ བྲ གྲ སྒྲ` | Stacked consonants align vertically |
| Complex stack | `བསྒྲུབ` | Multi-letter stack remains readable |
| Mantra text | `ཨོཾ་མ་ཎི་པདྨེ་ཧཱུྃ།` | Sanskrit/Tibetan marks render correctly |
| Punctuation | `། ༎ ༄༅།` | Tibetan punctuation spacing and shape |
| Dotted circle | `◌ཱ ◌ི ◌ུ ◌ེ ◌ོ` | Combining mark positioning |

When reporting a rendering problem, include the font name, software version, operating system, screenshot, and the exact Unicode text.
