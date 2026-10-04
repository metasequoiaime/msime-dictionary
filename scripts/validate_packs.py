"""Validate importable professional dictionary packs.

The checks mirror the Settings dictionary import rules closely enough to catch bad pull requests before users discover them at import time. The validator also checks each Chinese character pronunciation against pinyin/SingleCharsAllV1.txt and the single-character lines of pinyin/RimeIceSupplementV1.txt, rejects entries the released pinyin dictionary already ships (pinyin/BaseDictIceV1.txt, pinyin/RimeIceSupplementV1.txt and custom/words.txt, the inputs msime-dict-build uses for msime-pinyin.db), enforces the pack directory name, weight ranges, pack count and file size limits the project and the msime.app pack list rely on, and checks the format of custom/translations.txt.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = REPOSITORY_ROOT / "packs"
PINYIN_ROOT = REPOSITORY_ROOT / "pinyin"
UNLICENSED_ROOT = REPOSITORY_ROOT / "unlicensed"
# The pinyin inputs of the released msime-pinyin.db, besides pinyin/SingleCharsAllV1.txt (msime-dict-build main.rs, Stage::Quanpin and Stage::CustomWords). A pack entry already in one of them is a duplicate.
SHIPPED_PINYIN_SOURCES = (
    PINYIN_ROOT / "BaseDictIceV1.txt",
    PINYIN_ROOT / "RimeIceSupplementV1.txt",
    PINYIN_ROOT / "PlacesSupplementV1.txt",
    REPOSITORY_ROOT / "custom" / "words.txt",
)
# Excluded from releases for licensing (msime-dict-build licensing.rs); an overlap with them is reported as a note only.
UNRELEASED_PINYIN_SOURCES = (
    UNLICENSED_ROOT / "BaseDictAllV1Part1.txt",
    UNLICENSED_ROOT / "BaseDictAllV1Part2.txt",
)
# Single-character readings: the character table plus the single-character lines of the rime-ice supplement, which carry readings the table lacks (for example 宕 tan).
SINGLE_CHARACTER_SOURCE = PINYIN_ROOT / "SingleCharsAllV1.txt"
SUPPLEMENT_SOURCE = PINYIN_ROOT / "RimeIceSupplementV1.txt"
# CJK Unified Ideographs, Extension A to I, and the CJK Compatibility Ideographs blocks, as assigned in Unicode 16.0 (checked against Python 3.14 unicodedata). Python's re has no \p{Unified_Ideograph}, so the ranges are spelled out.
HAN_RE = re.compile(
    "["
    "\u3400-\u4dbf"  # Extension A
    "\u4e00-\u9fff"  # CJK Unified Ideographs
    "\uf900-\ufa6d\ufa70-\ufad9"  # CJK Compatibility Ideographs
    "\U00020000-\U0002a6df"  # Extension B
    "\U0002a700-\U0002b739"  # Extension C
    "\U0002b740-\U0002b81d"  # Extension D
    "\U0002b820-\U0002cea1"  # Extension E
    "\U0002ceb0-\U0002ebe0"  # Extension F
    "\U0002ebf0-\U0002ee5d"  # Extension I
    "\U0002f800-\U0002fa1d"  # CJK Compatibility Ideographs Supplement
    "\U00030000-\U0003134a"  # Extension G
    "\U00031350-\U000323af"  # Extension H
    "]"
)
PINYIN_RE = re.compile(r"[a-z]+(?:'[a-z]+)*")
ENGLISH_KEY_RE = re.compile(r"[a-z]+(?:[-'][a-z]+)*")
# msime.app lists the directories directly under packs/ by name; lowercase ASCII keeps the URL and the sort order predictable.
PACK_NAME_RE = re.compile(r"[a-z0-9_]+")
# The weight range custom/words.txt uses.
QUANPIN_WEIGHT_RANGE = (1, 10000)
# The weights in use today: custom/english.txt uses 1, the existing pack uses 10. The Settings importer gives a line without a weight 10000, so the weight is required.
ENGLISH_WEIGHT_RANGE = (1, 10)
# msime-web shared/official-packs.ts: MAX_PACKS directories are read per sweep (the rest are not listed), and a word list above MAX_COUNTED_BYTES is listed without an entry count.
MAX_PACKS = 40
MAX_COUNTED_BYTES = 2 * 1024 * 1024


def data_lines(path: Path, *, comments: bool) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    text = path.read_text(encoding="utf-8-sig")
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        if comments and line.startswith("#"):
            continue
        result.append((line_number, line))
    return result


def load_character_pronunciations() -> dict[str, set[str]]:
    pronunciations: dict[str, set[str]] = defaultdict(set)
    for source in (SINGLE_CHARACTER_SOURCE, SUPPLEMENT_SOURCE):
        if not source.exists():
            continue
        for _, line in data_lines(source, comments=True):
            fields = line.split("\t")
            if len(fields) >= 2 and len(fields[0]) == 1:
                pronunciations[fields[0]].add(fields[1])
    return pronunciations


def weight_error(weight: str, bounds: tuple[int, int]) -> str | None:
    low, high = bounds
    # str.isdigit() also accepts non-ASCII digits such as '²' or '١٢', which int() rejects or the importer's i64 parse refuses.
    if not (weight.isascii() and weight.isdigit()):
        return "weight must be a non-negative integer"
    if not low <= int(weight) <= high:
        return f"weight {weight} is outside {low}..{high}"
    return None


def validate_quanpin(
    path: Path, pronunciations: dict[str, set[str]]
) -> tuple[list[str], set[tuple[str, str]], set[str]]:
    errors: list[str] = []
    entries: set[tuple[str, str]] = set()
    words: set[str] = set()
    for line_number, line in data_lines(path, comments=False):
        fields = line.split("\t")
        if len(fields) != 3:
            errors.append(f"{path}:{line_number}: expected word<TAB>pinyin<TAB>weight")
            continue
        word, pinyin, weight = (field.strip() for field in fields)
        syllables = pinyin.split("'")
        han_characters = HAN_RE.findall(word)
        if not word:
            errors.append(f"{path}:{line_number}: empty word")
        if not PINYIN_RE.fullmatch(pinyin):
            errors.append(f"{path}:{line_number}: invalid full pinyin {pinyin!r}")
        problem = weight_error(weight, QUANPIN_WEIGHT_RANGE)
        if problem:
            errors.append(f"{path}:{line_number}: {problem}")
        if len(han_characters) != len(syllables):
            errors.append(
                f"{path}:{line_number}: {len(han_characters)} Han characters but "
                f"{len(syllables)} pinyin syllables"
            )
        if pronunciations and len(han_characters) == len(syllables):
            for character, syllable in zip(han_characters, syllables):
                allowed = pronunciations.get(character)
                if allowed and syllable not in allowed:
                    errors.append(
                        f"{path}:{line_number}: {character!r} is not annotated as {syllable!r} "
                        f"in SingleCharsAllV1.txt or the single characters of RimeIceSupplementV1.txt"
                    )
        entry = (word, pinyin)
        if entry in entries:
            errors.append(f"{path}:{line_number}: duplicate candidate {entry!r}")
        entries.add(entry)
        words.add(word)
    return errors, entries, words


def validate_english(path: Path) -> tuple[list[str], set[tuple[str, str]], set[str]]:
    errors: list[str] = []
    entries: set[tuple[str, str]] = set()
    displays: set[str] = set()
    for line_number, line in data_lines(path, comments=False):
        fields = line.split("\t")
        if len(fields) not in (2, 3):
            errors.append(f"{path}:{line_number}: expected key<TAB>display<TAB>weight")
            continue
        key, display = (field.strip() for field in fields[:2])
        if not ENGLISH_KEY_RE.fullmatch(key):
            errors.append(f"{path}:{line_number}: invalid lowercase English key {key!r}")
        if not display:
            errors.append(f"{path}:{line_number}: empty display")
        if len(fields) == 2:
            errors.append(f"{path}:{line_number}: missing weight (the importer would use 10000)")
        else:
            problem = weight_error(fields[2].strip(), ENGLISH_WEIGHT_RANGE)
            if problem:
                errors.append(f"{path}:{line_number}: {problem}")
        entry = (key, display)
        if entry in entries:
            errors.append(f"{path}:{line_number}: duplicate candidate {entry!r}")
        entries.add(entry)
        displays.add(display)
    return errors, entries, displays


def validate_translations(path: Path, *, allow_override: bool) -> tuple[list[str], set[str]]:
    """With allow_override (custom/translations.txt), a later line may give an existing source a new gloss, as the build keeps the last line and check-words allows; only a repeated source and gloss is an error. Packs keep one line per source."""
    errors: list[str] = []
    sources: set[str] = set()
    pairs: dict[tuple[str, str], int] = {}
    for line_number, line in data_lines(path, comments=True):
        fields = line.split("\t")
        if len(fields) != 2:
            errors.append(f"{path}:{line_number}: expected source<TAB>gloss")
            continue
        source, gloss = (field.strip() for field in fields)
        if not source or not gloss:
            errors.append(f"{path}:{line_number}: source and gloss must be non-empty")
        if (source, gloss) in pairs:
            errors.append(
                f"{path}:{line_number}: duplicate translation {source!r} -> {gloss!r} "
                f"(line {pairs[(source, gloss)]})"
            )
        elif source in sources and not allow_override:
            errors.append(f"{path}:{line_number}: duplicate translation source {source!r}")
        pairs.setdefault((source, gloss), line_number)
        sources.add(source)
    return errors, sources


def find_overlaps(
    entries: set[tuple[str, str]], sources: tuple[Path, ...]
) -> dict[tuple[str, str], list[str]]:
    """Where each of `entries` appears in `sources`, as path:line locations."""
    overlaps: dict[tuple[str, str], list[str]] = defaultdict(list)
    for source in sources:
        if not source.exists():
            continue
        for line_number, line in data_lines(source, comments=True):
            fields = line.split("\t")
            if len(fields) >= 2 and (fields[0], fields[1]) in entries:
                overlaps[(fields[0], fields[1])].append(
                    f"{source.relative_to(REPOSITORY_ROOT)}:{line_number}"
                )
    return overlaps


def validate_pack(
    pack: Path, pronunciations: dict[str, set[str]]
) -> tuple[list[str], set[tuple[str, str]]]:
    if not PACK_NAME_RE.fullmatch(pack.name):
        return [f"{pack}: directory name must match {PACK_NAME_RE.pattern}"], set()
    required = {
        "quanpin.txt": pack / "quanpin.txt",
        "english.txt": pack / "english.txt",
        "translations.txt": pack / "translations.txt",
        "README.md": pack / "README.md",
    }
    missing = [name for name, path in required.items() if not path.exists()]
    if missing:
        return [f"{pack}: missing required files: {', '.join(missing)}"], set()

    pinyin_errors, pinyin_entries, chinese_words = validate_quanpin(
        required["quanpin.txt"], pronunciations
    )
    english_errors, english_entries, english_displays = validate_english(
        required["english.txt"]
    )
    translation_errors, translation_sources = validate_translations(
        required["translations.txt"], allow_override=False
    )
    errors = pinyin_errors + english_errors + translation_errors

    for word_list in sorted(pack.glob("*.txt")):
        size = word_list.stat().st_size
        if size > MAX_COUNTED_BYTES:
            errors.append(
                f"{word_list}: {size} bytes is above the {MAX_COUNTED_BYTES} bytes msime.app counts"
            )

    for word in sorted(chinese_words - translation_sources):
        errors.append(f"{pack}: Chinese candidate has no translation: {word!r}")
    for display in sorted(english_displays - translation_sources):
        errors.append(f"{pack}: English candidate has no translation: {display!r}")

    print(
        f"{pack.name}: {len(pinyin_entries)} Chinese candidates, "
        f"{len(english_entries)} English candidates, {len(translation_sources)} translations"
    )
    return errors, pinyin_entries


def main() -> int:
    if not PACKS_ROOT.exists():
        print(f"Pack directory does not exist: {PACKS_ROOT}", file=sys.stderr)
        return 1
    pronunciations = load_character_pronunciations()
    errors: list[str] = []
    root_translations = REPOSITORY_ROOT / "custom" / "translations.txt"
    if root_translations.exists():
        root_errors, root_sources = validate_translations(root_translations, allow_override=True)
        errors.extend(root_errors)
        print(f"custom translations: {len(root_sources)} entries")
    packs = sorted(path for path in PACKS_ROOT.iterdir() if path.is_dir())
    if not packs:
        print(f"No packs found in {PACKS_ROOT}", file=sys.stderr)
        return 1
    if len(packs) > MAX_PACKS:
        errors.append(f"{PACKS_ROOT}: {len(packs)} packs, msime.app lists at most {MAX_PACKS}")
    pack_entries: dict[str, set[tuple[str, str]]] = {}
    for pack in packs:
        pack_errors, pack_entries[pack.name] = validate_pack(pack, pronunciations)
        errors.extend(pack_errors)

    # One pass over the large base files for all packs together.
    candidates = set().union(*pack_entries.values())
    shipped = find_overlaps(candidates, SHIPPED_PINYIN_SOURCES)
    unreleased = find_overlaps(candidates, UNRELEASED_PINYIN_SOURCES)
    for name, entries in pack_entries.items():
        for word, pinyin in sorted(entries & shipped.keys()):
            errors.append(
                f"{name}: candidate already ships in the pinyin dictionary: {word}\t{pinyin} "
                f"({', '.join(shipped[(word, pinyin)])})"
            )
        for word, pinyin in sorted(entries & unreleased.keys()):
            print(
                f"note: {name}: {word}\t{pinyin} is also in "
                f"{', '.join(unreleased[(word, pinyin)])}, which releases exclude"
            )
    if errors:
        print("\nValidation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    if not pronunciations:
        print("Validation OK (base-dictionary pronunciation checks skipped)")
    else:
        print("Validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
