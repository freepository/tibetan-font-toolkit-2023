from pathlib import Path
import importlib.util


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "normalize_tibetan.py"


spec = importlib.util.spec_from_file_location("normalize_tibetan", MODULE_PATH)
normalize_tibetan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(normalize_tibetan)


def test_decomposes_precomposed_vowel():
    assert normalize_tibetan.normalize("ཀ\u0F73") == "ཀ\u0F71\u0F72"


def test_normalizes_common_whitespace():
    assert normalize_tibetan.normalize("བཀྲ\u00A0ཤིས") == "བཀྲ ཤིས"


def test_adds_dotted_circle_to_initial_combining_mark():
    assert normalize_tibetan.normalize("\u0F71") == "\u25CC\u0F71"


def test_replaces_known_legacy_pua_character():
    assert normalize_tibetan.normalize("\uE0F0") == "\u0F00"
