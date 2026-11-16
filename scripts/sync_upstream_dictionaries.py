"""Fetch upstream dictionaries, build a review candidate and prepare the paired msime patch.

No arguments prepares tmp/upstream-sync-<unique>/ using remote HEADs and the
pinned builder. --apply RUN --msime-commit COMMIT applies a reviewed run after
the paired msime change has merged. No commits, pushes, merges or releases.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import update_rime_ice_only as audit

ROOT = Path(__file__).resolve().parents[1]
MSIME_URL = "https://github.com/metasequoiaime/msime.git"
CHANGED_GROUPS = ("rime-ice-supplement", "rime-wanxiang")
COMPARE_INPUTS = ("sources/pinyin/rime-ice.txt", "sources/pinyin/single-chars.txt",
                  "sources/pinyin/places.txt", "custom/words.txt", "sources/english/rime-ice-en.txt",
                  "sources/english/scowl-words.txt", "custom/english.txt")
SYNC_BEGIN = "<!-- upstream-sync:begin -->"
SYNC_END = "<!-- upstream-sync:end -->"


def run(args: list[str], cwd: Path | None = None, *, env: dict | None = None) -> bytes:
    print("+ " + " ".join(map(str, args)), flush=True)
    result = subprocess.run(list(map(str, args)), cwd=cwd, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        message = result.stdout.decode("utf-8", errors="replace")
        raise ValueError(f"Command failed ({result.returncode}): {args[0]}\n{message[-12000:]}")
    return result.stdout


def git(repo: Path, *args: str) -> bytes:
    return run(["git", "-C", str(repo), *args])


def checkout(url: str, ref: str, target: Path, *, local: Path | None = None) -> str:
    if target.exists():
        raise ValueError(f"Checkout destination already exists: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if ref.startswith("-") or not ref:
        raise ValueError("Git refs must not be empty or start with '-'")
    if local and local.is_dir():
        run(["git", "clone", "--shared", "--no-checkout", str(local), str(target)])
        git(target, "remote", "set-url", "origin", url)
        if subprocess.run(["git", "-C", str(target), "cat-file", "-e", ref + "^{commit}"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
            git(target, "fetch", "--depth=1", "origin", ref)
            ref = "FETCH_HEAD"
    else:
        target.mkdir(parents=True)
        git(target, "init")
        git(target, "remote", "add", "origin", url)
        git(target, "fetch", "--depth=1", "origin", ref)
        ref = "FETCH_HEAD"
    git(target, "-c", "core.autocrlf=false", "checkout", "--detach", ref)
    return git(target, "rev-parse", "HEAD").decode().strip()


def replace_block(text: str, block: str) -> str:
    if text.count(SYNC_BEGIN) != text.count(SYNC_END) or text.count(SYNC_BEGIN) > 1:
        raise ValueError("Malformed upstream-sync NOTICE markers")
    rendered = SYNC_BEGIN + "\n" + block.rstrip() + "\n" + SYNC_END
    if SYNC_BEGIN in text:
        return re.sub(re.escape(SYNC_BEGIN) + r".*?" + re.escape(SYNC_END),
                      lambda _: rendered, text, flags=re.S)
    return text.rstrip() + "\n\n" + rendered + "\n"


def update_lock(lock: dict, files: dict[str, bytes], ice_commit: str, wanxiang_commit: str,
                wanxiang_repository: str | None = None, removed: tuple[str, ...] = ()) -> dict:
    lock = copy.deepcopy(lock)
    recorded = {e["path"] for e in lock["files"]}
    for path in removed:
        if not path.startswith("sources/pinyin/wanxiang/") or path not in recorded or path in files:
            raise ValueError(f"Cannot remove {path}: only recorded Wanxiang files can be dropped")
    lock["files"] = [e for e in lock["files"] if e["path"] not in removed]
    lock["upstreams"]["rime-ice-supplement"]["commit"] = ice_commit
    lock["upstreams"]["rime-wanxiang"]["commit"] = wanxiang_commit
    if wanxiang_repository:
        previous = lock["upstreams"]["rime-wanxiang"]["repository"]
        if not audit.repository_change_allowed("rime-wanxiang", previous, wanxiang_repository):
            raise ValueError("Unsupported Wanxiang repository change")
        lock["upstreams"]["rime-wanxiang"]["repository"] = wanxiang_repository
    entries = {e["path"]: e for e in lock["files"]}
    for path, data in files.items():
        if path not in entries:
            raise ValueError(f"New upstream path requires coordinated builder changes: {path}")
        entries[path].update(size=len(data), sha256=audit.digest(data))
    return lock


def row_diff(before: bytes, after: bytes) -> dict:
    def rows(data):
        return {tuple(parts[:2]): parts[2:] for line in data.decode("utf-8-sig").splitlines()
                if line.strip() and not line.lstrip().startswith("#")
                for parts in [line.split("\t")]}
    old, new = rows(before), rows(after)
    return {"added": len(new.keys() - old.keys()), "removed": len(old.keys() - new.keys()),
            "weights_changed": sum(old[key] != new[key] for key in old.keys() & new.keys()),
            "old_rows": len(old), "new_rows": len(new)}


def candidate_copy(source: Path, target: Path) -> None:
    # Explicit data directories avoid recursively copying tmp, .git or build caches.
    target.mkdir()
    for name in ("sources", "custom", "curation", "packs", "scripts"):
        shutil.copytree(source / name, target / name, ignore=shutil.ignore_patterns("__pycache__"))
    for name in ("upstream.lock.json", "builder.lock.json", "NOTICE.md", "README.md", "AGENTS.md", ".gitattributes"):
        shutil.copyfile(source / name, target / name)


def license_snapshot(repo: Path, old_commit: str, output: Path, name: str,
                     previous_repository: str | None = None) -> dict:
    new_license = git(repo, "show", "HEAD:LICENSE")
    if subprocess.run(["git", "-C", str(repo), "cat-file", "-e", old_commit + "^{commit}"],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
        git(repo, "fetch", "--depth=1", previous_repository or "origin", old_commit)
    old_license = git(repo, "show", old_commit + ":LICENSE")
    (output / (name + "-LICENSE")).write_bytes(new_license)
    if old_license != new_license:
        (output / (name + "-previous-LICENSE")).write_bytes(old_license)
        raise ValueError(f"{name} LICENSE changed; inspect the saved license files before adapting the sync process")
    return {"sha256": audit.digest(new_license), "unchanged_from": old_commit}


def notice_block(lock: dict, generator: str, licenses: dict, removed: tuple[str, ...] = ()) -> str:
    ice = lock["upstreams"]["rime-ice-supplement"]["commit"]
    wx = lock["upstreams"]["rime-wanxiang"]["commit"]
    wx_repository = lock["upstreams"]["rime-wanxiang"]["repository"].removesuffix(".git")
    wx_project = wx_repository.rsplit("/", 1)[-1]
    dropped = ("；上游已不收的 " + "、".join(f"`{Path(p).name}`" for p in removed) + " 已从本仓删除") if removed else ""
    return (
        "## 当前自动同步的上游快照\n\n"
        "本节由同步脚本生成，记录当前源文件的上游提交；前文的逐文件说明须在同一次改动中人工核对，"
        "不一致时以本节和 `upstream.lock.json` 为准。\n\n"
        f"- 万象：作者 amzxyz，[{wx_project}]({wx_repository}/tree/{wx}/dicts)，"
        f"提交 `{wx}`。按 CC BY 4.0 使用，保留 RIME-LMDG 来源署名；"
        f"本仓已登记的词表逐字节复制，未修改其内容{dropped}。\n"
        f"- rime-ice 中英文补充表：[iDvel/rime-ice](https://github.com/iDvel/rime-ice/tree/{ice})，"
        f"提交 `{ice}`，GPL-3.0。由干净的 msime 提交 `{generator}` 的 `rime-ice-supplement` "
        "生成器生成；输入与完整去重集合见表头。词条取自新上游，权重为生成器输出，"
        "万象对齐仍由构建器 reweight 阶段完成。\n"
        "- `rime-ice.txt`、`single-chars.txt` 和基础英文表保留原有历史修正及来源提交；"
        "此次同步不把它们重建为上游原表，也不自动迁入无注音或不支持的读音。\n"
        "- 差集由 `scripts/update_rime_ice_only.py` 重新生成，完整输入摘要见 "
        "`sources/pinyin/rime-ice-only/manifest.json`。\n"
        f"- 万象 LICENSE SHA-256：`{licenses['rime-wanxiang']['sha256']}`；"
        f"rime-ice LICENSE SHA-256：`{licenses['rime-ice']['sha256']}`。"
        "两份许可证与此前固定上游提交逐字节相同；完整文本随同步报告保存。\n"
    )


def prepare(args) -> Path:
    lock = json.loads((ROOT / "upstream.lock.json").read_text(encoding="utf-8"))
    original = audit.load_inputs(ROOT, lock)
    parent = args.output.resolve() if args.output else ROOT / "tmp"
    parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="upstream-sync-", dir=parent))
    print(f"RUN_DIRECTORY={work}", flush=True)
    report = {"version": 1, "status": "preparing", "base_notice_sha256": audit.digest((ROOT / "NOTICE.md").read_bytes()),
              "base_generation_inputs": {p: audit.digest((ROOT / p).read_bytes()) for p in COMPARE_INPUTS},
              "base_builder_commit": json.loads(
        (ROOT / "builder.lock.json").read_text())["msime_commit"], "base_inputs": lock,
        "sync_script_sha256": audit.digest(Path(__file__).read_bytes())}
    try:
        ice_repo, wx_repo, msime = work / "rime-ice", work / "wanxiang", work / "msime"
        ice = checkout(lock["upstreams"]["rime-ice-supplement"]["repository"], args.rime_ice_ref, ice_repo)
        wx_repository = getattr(args, "wanxiang_repository", audit.WANXIANG_DATA_REPOSITORY)
        wx = checkout(wx_repository, args.wanxiang_ref, wx_repo)
        generator = checkout(MSIME_URL, report["base_builder_commit"], msime, local=args.msime)
        report["resolved_commits"] = {"rime-ice": ice, "rime-wanxiang": wx, "msime": generator}
        license_dir = work / "licenses"
        license_dir.mkdir()
        licenses = {
            "rime-ice": license_snapshot(ice_repo, lock["upstreams"]["rime-ice-supplement"]["commit"], license_dir, "rime-ice"),
            "rime-wanxiang": license_snapshot(wx_repo, lock["upstreams"]["rime-wanxiang"]["commit"], license_dir, "rime-wanxiang",
                                               lock["upstreams"]["rime-wanxiang"]["repository"]),
        }
        files = {}
        required = sorted(Path(p).name for p in original if p.startswith("sources/pinyin/wanxiang/"))
        available = sorted(p.name for p in (wx_repo / "dicts").glob("*.dict.yaml"))
        missing = sorted(set(required) - set(available))
        allowed_removals = sorted(set(getattr(args, "remove_wanxiang", None) or ()))
        report["wanxiang_structure"] = {"required": required, "available": available,
                                        "missing": missing, "removed": allowed_removals}
        if set(allowed_removals) - set(missing):
            raise ValueError("--remove-wanxiang names files that are not missing upstream: " +
                             ", ".join(sorted(set(allowed_removals) - set(missing))))
        if set(missing) - set(allowed_removals):
            raise ValueError("Required Wanxiang files missing upstream: " +
                             ", ".join(sorted(set(missing) - set(allowed_removals))) +
                             "; coordinated msime path-contract migration required (details in report.json); "
                             "pass --remove-wanxiang NAME for each file reviewed for removal")
        removed = tuple(f"sources/pinyin/wanxiang/{name}" for name in allowed_removals)
        report["removed_files"] = list(removed)
        for path in original:
            if path.startswith("sources/pinyin/wanxiang/") and path not in removed:
                upstream_file = wx_repo / "dicts" / Path(path).name
                if not upstream_file.is_file():
                    raise ValueError(f"Required Wanxiang file missing upstream: {upstream_file.name}; path-contract migration required")
                files[path] = upstream_file.read_bytes()
        expected = {Path(p).name for p in files}
        extras = sorted(p.name for p in (wx_repo / "dicts").glob("*.dict.yaml")
                        if p.name not in expected | {"abbrev.dict.yaml", "t9_abbrev.dict.yaml", "en.dict.yaml"})
        if extras:
            raise ValueError("Unregistered Wanxiang dictionaries need review and builder support: " + ", ".join(extras))
        dictionary = work / "dictionary"
        candidate_copy(ROOT, dictionary)
        build_dir = args.build_cache.resolve() if getattr(args, "build_cache", None) else work / "build"
        build_env = dict(os.environ, CARGO_TARGET_DIR=str(build_dir))
        build_log = run(["cargo", "build", "--locked", "--release", "-p", "msime-dict-builder"], msime, env=build_env)
        (work / "build.log").write_bytes(build_log)
        exe = build_dir / "release" / ("msime-dict-build.exe" if os.name == "nt" else "msime-dict-build")
        generated = work / "generated"
        log = run([str(exe), "rime-ice-supplement", "--upstream", str(ice_repo),
                   "--dictionary", str(dictionary), "--repository", str(msime), "--out", str(generated)])
        (work / "generator.log").write_bytes(log)
        generator_report = json.loads((generated / "upstream-update.json").read_text(encoding="utf-8"))
        if generator_report["commit"] != ice or generator_report["generator_commit"] != generator:
            raise ValueError("Generator report does not match clean, pinned checkouts")
        for scheme, name in (("pinyin", "rime-ice-supplement.txt"), ("english", "rime-ice-en-supplement.txt")):
            data = (generated / name).read_bytes()
            if b"-dirty" in data.splitlines()[0]:
                raise ValueError("Generator emitted a dirty provenance header")
            files[f"sources/{scheme}/{name}"] = data
        candidate_lock = update_lock(lock, files, ice, wx, wx_repository, removed)
        for path, data in files.items():
            (dictionary / path).write_bytes(data)
        for path in removed:
            (dictionary / path).unlink()
        (dictionary / "upstream.lock.json").write_bytes(audit.encode_json(candidate_lock))
        block = notice_block(candidate_lock, generator, licenses, removed)
        notice = replace_block((ROOT / "NOTICE.md").read_text(encoding="utf-8"), block)
        (dictionary / "NOTICE.md").write_bytes(notice.encode("utf-8"))
        verified_inputs = audit.load_inputs(dictionary, candidate_lock)
        outputs, manifest = audit.generate(verified_inputs, candidate_lock)
        for path, data in outputs.items():
            (dictionary / path).parent.mkdir(parents=True, exist_ok=True)
            (dictionary / path).write_bytes(data)
        # Generate only the paired upstream-reference/licensing change, not a builder upgrade.
        source_lock_path = msime / "resources/dictionary-sources.lock.json"
        source_lock = json.loads(source_lock_path.read_text(encoding="utf-8"))
        for name in CHANGED_GROUPS:
            if source_lock["references"][name] != lock["upstreams"][name]:
                raise ValueError(f"Pinned builder and dictionary disagree on {name}")
            source_lock["references"][name] = candidate_lock["upstreams"][name]
        source_lock_path.write_bytes(audit.encode_json(source_lock))
        paired_block = block + "\n本节为待发布上游更新；前文随已发布词库保留的历史来源说明继续适用。\n"
        for path in ("resources/licenses/msime-engine-dictionary-NOTICE.md", "resources/licenses/web-engine-NOTICE.md"):
            target = msime / path
            target.write_bytes(replace_block(target.read_text(encoding="utf-8"), paired_block).encode("utf-8"))
        patch = git(msime, "diff", "--binary", "--", "resources/dictionary-sources.lock.json", "resources/licenses")
        (work / "msime.patch").write_bytes(patch)
        report.update(status="candidate-ready", generator=generator_report, licenses=licenses,
                      target_upstreams={name: candidate_lock["upstreams"][name] for name in audit.GROUPS},
                      diff={p: row_diff(original[p], data) for p, data in files.items() if "/wanxiang/" not in p},
                      wanxiang_changed=[p for p, data in files.items() if "/wanxiang/" in p and original[p] != data],
                      combined_missing_unique_words=manifest["combined_missing_unique_words"],
                      candidate_files={p: audit.digest((dictionary / p).read_bytes()) for p in
                                       sorted(set([*files, *COMPARE_INPUTS, "NOTICE.md", "upstream.lock.json", *outputs]))})
        summary = ("# 上游词库同步候选\n\n"
                   f"rime-ice：`{ice}`\n\n万象：`{wx}`\n\n生成器：`{generator}`\n\n"
                   "`dictionary/` 是候选数据；`generated/` 保存生成器报告和拒绝词音；"
                   "`licenses/` 保存原始许可；`report.json` 列出增删和权重变化；"
                   "`msime.patch` 是先行提交到 msime 的引用与许可改动。\n\n"
                   "先审核候选，将 msime.patch 应用于基于最新 develop 的干净分支并合并配套 PR。"
                   "若其间还有 dict-builder 改动，按 AGENTS 先单独升级旧 builder pin。"
                   "再用合并提交运行 `python scripts/sync_upstream_dictionaries.py --apply <本目录> "
                   "--msime-commit <合并提交>`；脚本验证 develop 可达性、引用和构建器变更边界后更新本仓。\n\n"
                   "合入前仍须在本仓 PR 分支运行 Release built dictionaries（publish=false），"
                   "先填 msime PR 分支试跑，合并 msime 后留空再试跑，并通过 Eval gate 和 check-curation。"
                   "此脚本不创建、提交、推送或合并 PR，不发布 Release。\n")
        (work / "README.md").write_bytes(summary.encode("utf-8"))
    except Exception as error:
        report.update(status="failed", error=str(error))
        raise
    finally:
        (work / "report.json").write_bytes(audit.encode_json(report))
    return work


def apply_candidate(args) -> None:
    work = args.apply.resolve()
    report = json.loads((work / "report.json").read_text(encoding="utf-8"))
    if report.get("version") != 1 or report["status"] != "candidate-ready":
        raise ValueError("Only a completed candidate can be applied")
    if not args.msime_commit or not re.fullmatch(r"[0-9a-f]{40}", args.msime_commit):
        raise ValueError("--apply requires --msime-commit with the full merged commit")
    lock = json.loads((ROOT / "upstream.lock.json").read_text(encoding="utf-8"))
    audit.load_inputs(ROOT, lock)
    if lock != report["base_inputs"]:
        raise ValueError("Local upstream lock changed since preparation; regenerate the candidate")
    if audit.digest((ROOT / "NOTICE.md").read_bytes()) != report["base_notice_sha256"]:
        raise ValueError("Local NOTICE changed since preparation; regenerate the candidate")
    for path, digest in report["base_generation_inputs"].items():
        if path not in COMPARE_INPUTS or audit.digest((ROOT / path).read_bytes()) != digest:
            raise ValueError(f"Generator comparison input changed: {path}; regenerate the candidate")
    for path, digest in report["candidate_files"].items():
        if Path(path).is_absolute() or ".." in Path(path).parts:
            raise ValueError("Invalid candidate file path")
        if audit.digest((work / "dictionary" / path).read_bytes()) != digest:
            raise ValueError(f"Candidate changed since preparation: {path}; regenerate it")
    validation = Path(tempfile.mkdtemp(prefix="validate-msime-", dir=work))
    merged = validation / "msime"
    checkout(MSIME_URL, args.msime_commit, merged, local=args.msime)
    shallow = git(merged, "rev-parse", "--is-shallow-repository").decode().strip() == "true"
    git(merged, "fetch", *(["--unshallow"] if shallow else []), "origin", "develop")
    git(merged, "merge-base", "--is-ancestor", args.msime_commit, "FETCH_HEAD")
    base_pin = json.loads((ROOT / "builder.lock.json").read_text())["msime_commit"]
    if base_pin != report["base_builder_commit"]:
        raise ValueError("Builder pin changed since preparation; regenerate the candidate")
    git(merged, "merge-base", "--is-ancestor", base_pin, args.msime_commit)
    prior = git(merged, "diff", "--name-only", base_pin, args.msime_commit + "^", "--", "crates/dict-builder")
    if prior.strip():
        raise ValueError("Intervening dict-builder changes require a separate builder-pin upgrade first")
    changed_paths = git(merged, "diff", "--name-only", args.msime_commit + "^", args.msime_commit).decode().splitlines()
    if any(p != "resources/dictionary-sources.lock.json" and not p.startswith("resources/licenses/") for p in changed_paths):
        raise ValueError("Merged msime commit contains unrelated changes; expected the paired references/licensing PR")
    msime_lock = json.loads((merged / "resources/dictionary-sources.lock.json").read_text(encoding="utf-8"))
    candidate_lock = json.loads((work / "dictionary/upstream.lock.json").read_text(encoding="utf-8"))
    for name, reference in candidate_lock["upstreams"].items():
        actual = msime_lock.get("mozc") if name == "mozc" else msime_lock["references"].get(name)
        if actual != reference:
            raise ValueError(f"Merged builder reference disagrees with candidate: {name}")
    removed = frozenset(report.get("removed_files", ()))
    candidate_lock, writes = audit.import_plan(ROOT, work / "dictionary", lock, removed)
    outputs, _ = audit.generate(audit.load_inputs(work / "dictionary", candidate_lock), candidate_lock)
    writes.update(outputs)
    writes["builder.lock.json"] = audit.encode_json({"msime_commit": args.msime_commit})
    writes.update({path: None for path in removed})
    # All network and validation steps complete before touching this checkout.
    backup = Path(tempfile.mkdtemp(prefix="before-apply-", dir=work))
    written = []
    try:
        for path, data in writes.items():
            if data is None:
                target = ROOT / path
                if target.exists():
                    saved = backup / path
                    saved.parent.mkdir(parents=True, exist_ok=True)
                    saved.write_bytes(target.read_bytes())
                    written.append(path)
                    target.unlink()
                continue
            target = ROOT / path
            if target.is_file() and target.read_bytes() == data:
                continue
            saved = backup / path
            saved.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                saved.write_bytes(target.read_bytes())
            target.parent.mkdir(parents=True, exist_ok=True)
            written.append(path)
            target.write_bytes(data)
    except Exception:
        for path in reversed(written):
            saved, target = backup / path, ROOT / path
            if saved.exists():
                target.write_bytes(saved.read_bytes())
            else:
                target.unlink(missing_ok=True)
        raise
    print(f"Applied {len(written)} files. Backups: {backup}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rime-ice-ref", default="HEAD", help="remote ref or full commit; defaults to upstream default branch")
    parser.add_argument("--wanxiang-ref", default="wanxiang", help="data repository ref or full commit; default: wanxiang")
    parser.add_argument("--wanxiang-repository", default=audit.WANXIANG_DATA_REPOSITORY,
                        choices=(audit.WANXIANG_DATA_REPOSITORY, audit.WANXIANG_CONFIG_REPOSITORY),
                        help="dictionary source; config repository is only for reproducing historical snapshots")
    parser.add_argument("--remove-wanxiang", action="append", default=[], metavar="NAME",
                        help="recorded Wanxiang file (e.g. lianxiang.dict.yaml) reviewed for removal because "
                             "upstream no longer has it; repeat per file. Requires the paired builder change")
    parser.add_argument("--msime", type=Path, default=ROOT.parent / "msime", help="optional local clone used as an object cache")
    parser.add_argument("--output", type=Path, help="parent for a fresh, unique candidate directory; default: tmp/")
    parser.add_argument("--build-cache", type=Path, help="optional Cargo target cache to reuse compilation between runs")
    parser.add_argument("--apply", type=Path, metavar="RUN", help="apply a reviewed candidate after paired msime merge")
    parser.add_argument("--msime-commit", help="merged msime commit required by --apply")
    args = parser.parse_args(argv)
    try:
        if args.apply:
            apply_candidate(args)
        else:
            if args.msime_commit:
                raise ValueError("--msime-commit is only used with --apply")
            work = prepare(args)
            print(f"Candidate ready: {work}")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
