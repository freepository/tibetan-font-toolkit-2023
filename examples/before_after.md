# Tibetan Rendering Before/After Notes

This file records simple examples of text normalization and rendering checks.

## Example 1: Precomposed Tibetan Vowels

Some Tibetan vowels have precomposed Unicode forms. Modern text processing often works better when these are decomposed into their component marks.

| Case | Text | Notes |
|---|---|---|
| Before | `ཀཱི` | Contains U+0F73 |
| After | `ཀཱི` | Decomposed into U+0F71 U+0F72 |

## Example 2: Orphaned Combining Marks

Combining marks without a visible base can render unpredictably. The normalizer may add U+25CC dotted circle for inspection.

| Case | Text | Notes |
|---|---|---|
| Before | `ཱ` | Combining mark alone |
| After | `◌ཱ` | Dotted circle added for visual diagnosis |

## Notes

These examples are for testing and documentation only. Always verify results manually before using normalized text in important documents.
