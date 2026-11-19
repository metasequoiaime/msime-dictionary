"""Validate the pinyin-next seed dictionaries under sources/pinyin-next/packs/.

Each pack is sources/pinyin-next/packs/<domain>/<name>.txt: UTF-8 without BOM, LF line endings, ending with a newline. It starts with a "#" header whose first line is "# msime pinyin-next pack: <name>", which has a "# source:" line, and whose last line is "# word<TAB>pinyin<TAB>weight"; no comment lines follow the header. Every other line is word<TAB>pinyin<TAB>weight: the word is Han characters only, the pinyin has one lowercase syllable per character separated by "'", and the same (word, pinyin) appears once per file.

Readings and weights follow sources/pinyin-next/base: a (word, pinyin) pair that base has keeps the base weight, any other pair has weight 10. Each syllable of a pair base does not have must be a reading sources/pinyin/single-chars.txt (or a single-character line of sources/pinyin/rime-ice-supplement.txt) lists for that character; pairs copied from base are trusted as base has them.

Uses the Python standard library only. Exit status 1 when any check fails.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = REPOSITORY_ROOT / "sources" / "pinyin-next" / "packs"
BASE_ROOT = REPOSITORY_ROOT / "sources" / "pinyin-next" / "base"
SINGLE_CHARACTER_SOURCES = (
    REPOSITORY_ROOT / "sources" / "pinyin" / "single-chars.txt",
    REPOSITORY_ROOT / "sources" / "pinyin" / "rime-ice-supplement.txt",
)
HAN_RE = re.compile(
    "["
    "㐀-䶿一-鿿豈-舘並-龎"
    "\U00020000-\U0002a6df\U0002a700-\U0002b739\U0002b740-\U0002b81d\U0002b820-\U0002cea1"
    "\U0002ceb0-\U0002ebe0\U0002ebf0-\U0002ee5d\U0002f800-\U0002fa1d\U00030000-\U0003134a\U00031350-\U000323af"
    "]+"
)
PINYIN_RE = re.compile(r"[a-z]+(?:'[a-z]+)*")
COLUMNS_HEADER = "# word\tpinyin\tweight"
NEW_WORD_WEIGHT = 10


def load_base() -> dict[tuple[str, str], int]:
    base: dict[tuple[str, str], int] = {}
    for path in sorted(BASE_ROOT.glob("*.txt")):
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("#"):
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) == 3 and parts[2].isdigit():
                    base[(parts[0], parts[1])] = int(parts[2])
    return base


def load_single_readings() -> dict[str, set[str]]:
    readings: dict[str, set[str]] = {}
    for path in SINGLE_CHARACTER_SOURCES:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("#"):
                    continue
                parts = line.rstrip("\r\n").split("\t")
                if len(parts) >= 2 and len(parts[0]) == 1:
                    readings.setdefault(parts[0], set()).add(parts[1])
    return readings


def check_pack(path: Path, base: dict[tuple[str, str], int], single: dict[str, set[str]]) -> tuple[list[str], int]:
    errors: list[str] = []
    rel = path.relative_to(REPOSITORY_ROOT).as_posix()
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        errors.append(f"{rel}: starts with a UTF-8 BOM")
    if b"\r" in raw:
        errors.append(f"{rel}: contains CR; use LF line endings")
    if not raw.endswith(b"\n"):
        errors.append(f"{rel}: does not end with a newline")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        return errors + [f"{rel}: not UTF-8 ({error})"], 0
    lines = text.replace("\r\n", "\n").split("\n")
    if lines and lines[-1] == "":
        lines.pop()

    header_end = 0
    while header_end < len(lines) and lines[header_end].startswith("#"):
        header_end += 1
    header = lines[:header_end]
    expected_first = f"# msime pinyin-next pack: {path.stem}"
    if not header or header[0] != expected_first:
        errors.append(f"{rel}:1: first line must be {expected_first!r}")
    if not any(line.startswith("# source:") for line in header):
        errors.append(f"{rel}: header has no '# source:' line")
    if not header or header[-1] != COLUMNS_HEADER:
        errors.append(f"{rel}:{header_end}: last header line must be {COLUMNS_HEADER!r}")

    seen: set[tuple[str, str]] = set()
    count = 0
    for number, line in enumerate(lines[header_end:], start=header_end + 1):
        where = f"{rel}:{number}"
        if line.startswith("#"):
            errors.append(f"{where}: comment after the header")
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            errors.append(f"{where}: expected word<TAB>pinyin<TAB>weight")
            continue
        word, pinyin, weight_text = parts
        count += 1
        if not HAN_RE.fullmatch(word):
            errors.append(f"{where}: word {word!r} must be Han characters only")
            continue
        if not PINYIN_RE.fullmatch(pinyin):
            errors.append(f"{where}: pinyin {pinyin!r} must be lowercase syllables separated by \"'\"")
            continue
        syllables = pinyin.split("'")
        if len(syllables) != len(word):
            errors.append(f"{where}: {word} has {len(word)} characters but {len(syllables)} syllables")
            continue
        if (word, pinyin) in seen:
            errors.append(f"{where}: duplicate {word}\t{pinyin}")
        seen.add((word, pinyin))
        if not weight_text.isdigit():
            errors.append(f"{where}: weight {weight_text!r} is not a non-negative integer")
            continue
        weight = int(weight_text)
        base_weight = base.get((word, pinyin))
        if base_weight is not None:
            if weight != base_weight:
                errors.append(f"{where}: {word}\t{pinyin} is in base with weight {base_weight}, not {weight}")
            continue
        if weight != NEW_WORD_WEIGHT:
            errors.append(f"{where}: {word}\t{pinyin} is not in base, so its weight must be {NEW_WORD_WEIGHT}, not {weight}")
        for char, syllable in zip(word, syllables):
            allowed = single.get(char)
            if allowed is None:
                errors.append(f"{where}: {char} in {word} is not in the single-character tables")
            elif syllable not in allowed:
                errors.append(f"{where}: {char} in {word} read {syllable}, expected one of {sorted(allowed)}")
    return errors, count


def main() -> int:
    errors: list[str] = []
    for path in sorted(PACKS_ROOT.rglob("*")):
        rel = path.relative_to(PACKS_ROOT)
        if path.is_dir():
            if len(rel.parts) > 1:
                errors.append(f"{path.relative_to(REPOSITORY_ROOT).as_posix()}: packs are one directory deep (<domain>/<name>.txt)")
            continue
        if len(rel.parts) != 2 or path.suffix != ".txt":
            errors.append(f"{path.relative_to(REPOSITORY_ROOT).as_posix()}: expected sources/pinyin-next/packs/<domain>/<name>.txt")
    packs = sorted(path for path in PACKS_ROOT.glob("*/*.txt") if path.is_file())
    base = load_base()
    single = load_single_readings()
    for path in packs:
        pack_errors, count = check_pack(path, base, single)
        errors.extend(pack_errors)
        print(f"{path.relative_to(PACKS_ROOT).as_posix()}: {count} entries")
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    print(f"{len(packs)} packs, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
