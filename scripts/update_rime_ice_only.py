"""Refresh the word-spelling difference between reviewed rime-ice and Wanxiang inputs.

Default: regenerate the audit files from this checkout. --check never writes.
--from-reviewed imports the three upstream groups from a reviewed dictionary
checkout, including their lock records and NOTICE, before regenerating the audit.
--sync-upstream delegates fetching and candidate generation to the companion
sync_upstream_dictionaries.py script. Neither command publishes releases.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = "sources/pinyin/rime-ice-only"
GROUPS = ("rime-ice", "rime-ice-supplement", "rime-wanxiang")
ICE_FILES = ("rime-ice", "rime-ice-supplement")
WANXIANG_CONFIG_REPOSITORY = "https://github.com/amzxyz/rime-wanxiang.git"
WANXIANG_DATA_REPOSITORY = "https://github.com/amzxyz/rime-wanxiang-data.git"


def repository_change_allowed(name: str, previous: str, updated: str) -> bool:
    return previous == updated or (name == "rime-wanxiang" and
                                   previous == WANXIANG_CONFIG_REPOSITORY and
                                   updated == WANXIANG_DATA_REPOSITORY)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encode_json(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def selected_entries(lock: dict) -> dict[str, dict]:
    entries = {}
    for entry in lock["files"]:
        if entry["upstream"] not in GROUPS:
            continue
        path = entry["path"]
        # Import only known source paths, never arbitrary paths from a manifest.
        allowed = path in {
            "sources/pinyin/rime-ice.txt",
            "sources/pinyin/rime-ice-supplement.txt",
            "sources/english/rime-ice-en-supplement.txt",
        } or (path.startswith("sources/pinyin/wanxiang/")
              and Path(path).name == path.removeprefix("sources/pinyin/wanxiang/")
              and path.endswith(".dict.yaml"))
        if not allowed or ".." in Path(path).parts or path in entries:
            raise ValueError(f"Unexpected or duplicate upstream path: {path}")
        expected = ("rime-wanxiang" if "/wanxiang/" in path else
                    "rime-ice" if path.endswith("/rime-ice.txt") else "rime-ice-supplement")
        if entry["upstream"] != expected:
            raise ValueError(f"{path}: expected upstream {expected}")
        entries[path] = entry
    for stem in ICE_FILES:
        if f"sources/pinyin/{stem}.txt" not in entries:
            raise ValueError(f"Missing lock entry for {stem}")
    return entries


def load_inputs(root: Path, lock: dict) -> dict[str, bytes]:
    inputs = {}
    for path, entry in selected_entries(lock).items():
        data = (root / path).read_bytes()
        if len(data) != entry["size"] or digest(data) != entry["sha256"]:
            raise ValueError(f"{path}: bytes disagree with upstream.lock.json")
        inputs[path] = data
    actual = {p.relative_to(root).as_posix()
              for p in (root / "sources/pinyin/wanxiang").glob("*.dict.yaml")}
    recorded = {p for p in inputs if p.startswith("sources/pinyin/wanxiang/")}
    if not actual or actual != recorded:
        raise ValueError("Wanxiang directory and lock file lists disagree")
    return inputs


def import_plan(root: Path, reviewed: Path, current: dict,
                removed: frozenset[str] = frozenset()) -> tuple[dict, dict[str, bytes]]:
    """Plan an import; `removed` lists Wanxiang paths the reviewed run explicitly dropped."""
    candidate = json.loads((reviewed / "upstream.lock.json").read_text(encoding="utf-8"))
    old_entries, new_entries = selected_entries(current), selected_entries(candidate)
    if any(not p.startswith("sources/pinyin/wanxiang/") or p not in old_entries
           or (reviewed / p).exists() for p in removed):
        raise ValueError("Only recorded Wanxiang files absent from the reviewed checkout can be removed")
    if old_entries.keys() - removed != new_entries.keys():
        raise ValueError("Upstream file paths changed; use the cross-repository path-contract process")
    for name in current["upstreams"].keys() | candidate["upstreams"].keys():
        if name not in GROUPS and candidate["upstreams"].get(name) != current["upstreams"].get(name):
            raise ValueError(f"Reviewed checkout also changes unrelated upstream {name}")
    inputs = load_inputs(reviewed, candidate)
    notice = (reviewed / "NOTICE.md").read_bytes()
    for name in GROUPS:
        reference = candidate["upstreams"][name]
        commit = reference["commit"]
        if (len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit)
                or not repository_change_allowed(name, current["upstreams"][name]["repository"],
                                                  reference["repository"])):
            raise ValueError(f"Invalid commit or changed repository for {name}")
        if commit not in notice.decode("utf-8"):
            raise ValueError(f"Reviewed NOTICE.md must document the full {name} commit")
    merged = copy.deepcopy(current)
    for name in GROUPS:
        merged["upstreams"][name] = candidate["upstreams"][name]
    merged["files"] = [new_entries.get(entry["path"], entry) for entry in merged["files"]
                       if entry["path"] not in removed]
    writes = dict(inputs)
    writes["NOTICE.md"] = notice
    if merged != current:
        writes["upstream.lock.json"] = encode_json(merged)
    return merged, writes


def generate(inputs: dict[str, bytes], lock: dict) -> tuple[dict[str, bytes], dict]:
    wanxiang = set()
    wanxiang_rows = 0
    comparison_paths = sorted(p for p in inputs if p.startswith("sources/pinyin/wanxiang/"))
    for path in comparison_paths:
        body = False
        for lineno, line in enumerate(inputs[path].decode("utf-8-sig").splitlines(), 1):
            if line.strip() == "...":
                body = True
                continue
            if not body or not line.strip() or line.lstrip().startswith("#"):
                continue
            fields = line.split("\t")
            if len(fields) < 2 or not fields[0]:
                raise ValueError(f"{path}:{lineno}: invalid dictionary row")
            wanxiang.add(fields[0])
            wanxiang_rows += 1
        if not body:
            raise ValueError(f"{path}: missing YAML data marker")
    outputs = {}
    manifest = {
        "version": 1,
        "comparison": "Exact word spelling; no reading, weight, Unicode or script normalization; no curation",
        "generator": {"path": "scripts/update_rime_ice_only.py",
                      "sha256": digest(Path(__file__).read_bytes())},
        "upstreams": {name: lock["upstreams"][name] for name in GROUPS},
        "inputs": [],
        "wanxiang": {"files": len(comparison_paths), "rows": wanxiang_rows,
                     "unique_words": len(wanxiang)},
        "sources": {},
    }
    union = set()
    for stem in ICE_FILES:
        path = f"sources/pinyin/{stem}.txt"
        comparison_paths.append(path)
        rows = []
        words = set()
        total_rows = 0
        for lineno, line in enumerate(inputs[path].decode("utf-8-sig").splitlines(), 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            fields = line.split("\t")
            if len(fields) != 3 or not fields[0] or not fields[1]:
                raise ValueError(f"{path}:{lineno}: expected word, pinyin and integer weight")
            word, pinyin, weight = fields
            weight = int(weight)
            total_rows += 1
            words.add(word)
            if word not in wanxiang:
                rows.append((word, pinyin, weight, lineno))
        rows.sort(key=lambda row: (-row[2], row[0], row[1], row[3]))
        ordered_words = list(dict.fromkeys(row[0] for row in rows))
        union.update(ordered_words)
        header = (f"# Generated by scripts/update_rime_ice_only.py; source: {path}\n"
                  "# Exact word-spelling difference against all sources/pinyin/wanxiang/*.dict.yaml\n"
                  "# Source licenses/attribution: ../../../NOTICE.md; input hashes/commits: manifest.json\n"
                  "# word\tpinyin\toriginal_weight\tsource_line\n")
        entries = header + "".join(f"{w}\t{p}\t{v}\t{n}\n" for w, p, v, n in rows)
        outputs[f"{OUTPUT}/{stem}-only-entries.txt"] = entries.encode("utf-8")
        outputs[f"{OUTPUT}/{stem}-only-words.txt"] = "".join(w + "\n" for w in ordered_words).encode("utf-8")
        manifest["sources"][stem] = {
            "input_rows": total_rows, "input_unique_words": len(words),
            "missing_rows": len(rows), "missing_unique_words": len(ordered_words),
        }
    for path in sorted(comparison_paths):
        manifest["inputs"].append({"path": path, "size": len(inputs[path]), "sha256": digest(inputs[path])})
    manifest["combined_missing_unique_words"] = len(union)
    manifest["outputs"] = [{"path": path, "size": len(data), "sha256": digest(data)}
                           for path, data in sorted(outputs.items())]
    outputs[f"{OUTPUT}/manifest.json"] = encode_json(manifest)
    return outputs, manifest


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--sync-upstream" in argv:
        import sync_upstream_dictionaries
        argv.remove("--sync-upstream")
        return sync_upstream_dictionaries.main(argv)
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail if audit outputs are missing or stale; never write")
    mode.add_argument("--from-reviewed", type=Path, metavar="CHECKOUT",
                      help="import reviewed dictionary checkout inputs, related lock entries and NOTICE.md")
    args = parser.parse_args(argv)
    try:
        lock = json.loads((ROOT / "upstream.lock.json").read_text(encoding="utf-8"))
        inputs = load_inputs(ROOT, lock)
        writes = {}
        if args.from_reviewed:
            lock, writes = import_plan(ROOT, args.from_reviewed.resolve(), lock)
            inputs = {path: data for path, data in writes.items() if path.startswith("sources/")}
        outputs, manifest = generate(inputs, lock)
        writes.update(outputs)
        changed = [path for path, data in writes.items()
                   if not (ROOT / path).is_file() or (ROOT / path).read_bytes() != data]
        if args.check:
            if changed:
                print("Stale or missing audit outputs:\n" + "\n".join(changed))
                return 1
        else:
            # Validate and render every input/output before changing any file.
            for path in changed:
                target = ROOT / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(writes[path])
        for stem, stats in manifest["sources"].items():
            print(f"{stem}: {stats['missing_unique_words']} missing words / {stats['missing_rows']} rows")
        print(f"Combined: {manifest['combined_missing_unique_words']} words; {len(changed)} files {'stale' if args.check else 'updated'}")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
