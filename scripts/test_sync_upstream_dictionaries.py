"""Test orchestration with local Git fixtures and a simulated external builder."""

import argparse
import contextlib
import copy
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import sync_upstream_dictionaries as sync
import update_rime_ice_only as audit


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, root, path, data):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data.encode() if isinstance(data, str) else data)

    def repository(self, path, files):
        path.mkdir(parents=True)
        self.quiet_git(path, "init")
        self.quiet_git(path, "config", "core.autocrlf", "false")
        for name, data in files.items():
            self.write(path, name, data)
        self.quiet_git(path, "add", "--", *files)
        self.quiet_git(path, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                       "commit", "-m", "test(sync): fixture")
        return self.quiet_git(path, "rev-parse", "HEAD").decode().strip()

    def quiet_git(self, path, *args):
        return subprocess.run(["git", "-C", str(path), *args], check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

    def test_remote_checkout_preserves_bytes_and_does_not_modify_original(self):
        source, target = self.root / "upstream", self.root / "checkout"
        content = b"fixture\r\nsecond\r\n"
        commit = self.repository(source, {"data.txt": content})
        with contextlib.redirect_stdout(io.StringIO()):
            actual = sync.checkout(str(source), "HEAD", target)
        self.assertEqual(actual, commit)
        self.assertEqual((target / "data.txt").read_bytes(), content)
        self.assertEqual(self.quiet_git(source, "status", "--porcelain"), b"")
        with self.assertRaises(ValueError):
            sync.checkout(str(source), "HEAD", target)

    def test_notice_block_replaces_only_owned_section(self):
        base = "historical attribution\n"
        first = sync.replace_block(base, "current snapshot")
        second = sync.replace_block(first, "new snapshot")
        self.assertTrue(second.startswith(base))
        self.assertNotIn("current snapshot", second)
        self.assertEqual(second.count(sync.SYNC_BEGIN), 1)
        with self.assertRaises(ValueError):
            sync.replace_block(sync.SYNC_BEGIN, "bad")

    def test_default_source_is_explicit_data_repository_and_wanxiang_branch(self):
        with patch.object(sync, "prepare", return_value=self.root) as prepare, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(sync.main([]), 0)
        args = prepare.call_args.args[0]
        self.assertEqual(args.wanxiang_repository, "https://github.com/amzxyz/rime-wanxiang-data.git")
        self.assertEqual(args.wanxiang_ref, "wanxiang")

    def test_only_known_configuration_to_data_repository_migration_is_allowed(self):
        self.assertTrue(audit.repository_change_allowed("rime-wanxiang", audit.WANXIANG_CONFIG_REPOSITORY,
                                                       audit.WANXIANG_DATA_REPOSITORY))
        self.assertFalse(audit.repository_change_allowed("rime-ice", audit.WANXIANG_CONFIG_REPOSITORY,
                                                        audit.WANXIANG_DATA_REPOSITORY))
        self.assertFalse(audit.repository_change_allowed("rime-wanxiang", audit.WANXIANG_DATA_REPOSITORY,
                                                        audit.WANXIANG_CONFIG_REPOSITORY))

    def test_license_migration_compares_with_original_repository(self):
        original, data = self.root / "original", self.root / "data"
        baseline = self.repository(original, {"LICENSE": "same license\n"})
        self.repository(data, {"LICENSE": "same license\n", "README.md": "new data repository\n"})
        output = self.root / "licenses"
        output.mkdir()
        with contextlib.redirect_stdout(io.StringIO()):
            result = sync.license_snapshot(data, baseline, output, "wanxiang", str(original))
        self.assertEqual(result["unchanged_from"], baseline)
        self.assertEqual((output / "wanxiang-LICENSE").read_bytes(), b"same license\n")

    def test_license_change_stops_and_saves_both_texts(self):
        repo = self.root / "upstream"
        old = self.repository(repo, {"LICENSE": b"original license\n"})
        self.write(repo, "LICENSE", b"changed license\n")
        self.quiet_git(repo, "add", "LICENSE")
        self.quiet_git(repo, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                       "commit", "-m", "test(sync): changed license")
        output = self.root / "licenses"
        output.mkdir()
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(ValueError):
            sync.license_snapshot(repo, old, output, "fixture")
        self.assertEqual((output / "fixture-LICENSE").read_bytes(), b"changed license\n")
        self.assertEqual((output / "fixture-previous-LICENSE").read_bytes(), b"original license\n")

    def test_diff_and_lock_update_preserve_historical_main_commit(self):
        before = b"# old\nkept\tpinyin\t1\nremoved\tpinyin\t2\n"
        after = b"# new\nkept\tpinyin\t3\nadded\tpinyin\t4\n"
        self.assertEqual(sync.row_diff(before, after),
                         {"added": 1, "removed": 1, "weights_changed": 1, "old_rows": 2, "new_rows": 2})
        original = {"upstreams": {name: {"commit": "1" * 40} for name in audit.GROUPS},
                    "files": [{"path": "sources/pinyin/rime-ice-supplement.txt", "size": 0, "sha256": "old"}]}
        revised = sync.update_lock(original, {"sources/pinyin/rime-ice-supplement.txt": after}, "2" * 40, "3" * 40)
        self.assertEqual(revised["upstreams"]["rime-ice"]["commit"], "1" * 40)
        self.assertEqual(revised["files"][0]["sha256"], audit.digest(after))
        self.assertEqual(original["files"][0]["sha256"], "old")
        with self.assertRaises(ValueError):
            sync.update_lock(original, {"unexpected.txt": b""}, "2" * 40, "3" * 40)

    def test_lock_update_drops_only_explicitly_removed_wanxiang_files(self):
        gone = "sources/pinyin/wanxiang/gone.dict.yaml"
        original = {"upstreams": {name: {"commit": "1" * 40} for name in audit.GROUPS},
                    "files": [{"path": gone, "size": 1, "sha256": "x"},
                              {"path": "sources/pinyin/rime-ice-supplement.txt", "size": 1, "sha256": "y"}]}
        revised = sync.update_lock(original, {}, "2" * 40, "3" * 40, removed=(gone,))
        self.assertEqual([e["path"] for e in revised["files"]], ["sources/pinyin/rime-ice-supplement.txt"])
        for bad in ("sources/pinyin/rime-ice-supplement.txt", "sources/pinyin/wanxiang/unknown.dict.yaml"):
            with self.assertRaises(ValueError):
                sync.update_lock(original, {}, "2" * 40, "3" * 40, removed=(bad,))

    def fixture(self):
        dictionary = self.root / "dictionary"
        ice_repo, wx_repo, msime_repo = [self.root / name for name in ("ice", "wx", "msime")]
        ice_commit = self.repository(ice_repo, {"LICENSE": "fixture GPL\n"})
        wx_data = "---\nname: fixture\n...\n已有词\tyi you ci\t10\n".encode()
        wx_commit = self.repository(wx_repo, {"LICENSE": "fixture CC\n", "dicts/test.dict.yaml": wx_data})
        sources = {
            "sources/pinyin/wanxiang/test.dict.yaml": wx_data,
            "sources/pinyin/rime-ice.txt": "已有词\tyi'you'ci\t10\n示例词\tshi'li'ci\t20\n".encode(),
            "sources/pinyin/rime-ice-supplement.txt": "旧示例词\tjiu'shi'li'ci\t1\n".encode(),
            "sources/english/rime-ice-en-supplement.txt": b"OldFixture\toldfixture\n",
        }
        lock = {"version": 1, "upstreams": {
            "rime-ice": {"repository": "https://github.com/iDvel/rime-ice.git", "commit": ice_commit},
            "rime-ice-supplement": {"repository": "https://github.com/iDvel/rime-ice.git", "commit": ice_commit},
            "rime-wanxiang": {"repository": "https://github.com/amzxyz/rime-wanxiang.git", "commit": wx_commit}},
            "files": []}
        for path, data in sources.items():
            group = "rime-wanxiang" if "/wanxiang/" in path else "rime-ice" if path.endswith("/rime-ice.txt") else "rime-ice-supplement"
            lock["files"].append({"path": path, "upstream": group, "size": len(data), "sha256": audit.digest(data)})
            self.write(dictionary, path, data)
        for p in sync.COMPARE_INPUTS:
            if not (dictionary / p).exists():
                self.write(dictionary, p, "# comparison fixture\n")
        for directory in ("curation", "packs", "scripts"):
            (dictionary / directory).mkdir(exist_ok=True)
        self.write(dictionary, "upstream.lock.json", audit.encode_json(lock))
        for name in ("README.md", "AGENTS.md", ".gitattributes"):
            self.write(dictionary, name, "fixture\n")
        self.write(dictionary, "NOTICE.md", f"historical {ice_commit} {wx_commit}\n")
        pin = self.repository(msime_repo, {
            "resources/dictionary-sources.lock.json": audit.encode_json({"references": copy.deepcopy(lock["upstreams"])}),
            "resources/licenses/msime-engine-dictionary-NOTICE.md": "published historical attribution\n",
            "resources/licenses/web-engine-NOTICE.md": "published historical attribution\n"})
        self.write(dictionary, "builder.lock.json", audit.encode_json({"msime_commit": pin}))
        return dictionary, ice_repo, wx_repo, msime_repo, pin

    def test_prepare_orchestrates_candidate_patch_and_provenance_without_changing_source(self):
        dictionary, ice_repo, wx_repo, msime_repo, pin = self.fixture()
        originals = {p: p.read_bytes() for p in dictionary.rglob("*") if p.is_file()}
        real_checkout, real_run = sync.checkout, sync.run
        captured = []

        def checkout(url, ref, target, **kwargs):
            source = msime_repo if url == sync.MSIME_URL else wx_repo if "wanxiang" in url else ice_repo
            return real_checkout(str(source), ref, target)

        def external(args, cwd=None, **kwargs):
            captured.append(args)
            if args[0] == "cargo":
                return b"simulated external compiler for orchestration test\n"
            if "rime-ice-supplement" in args:
                out = Path(args[args.index("--out") + 1])
                self.write(out, "rime-ice-supplement.txt", f"# generator {pin}\n新增示例词\txin'zeng'shi'li'ci\t30\n")
                self.write(out, "rime-ice-en-supplement.txt", f"# generator {pin}\nNewFixture\tnewfixture\n")
                ice_commit = self.quiet_git(ice_repo, "rev-parse", "HEAD").decode().strip()
                self.write(out, "upstream-update.json", audit.encode_json({"commit": ice_commit, "generator_commit": pin}))
                return b"simulated external generator\n"
            return real_run(args, cwd, **kwargs)

        args = argparse.Namespace(output=self.root / "runs", rime_ice_ref="HEAD", wanxiang_ref="HEAD", msime=msime_repo)
        with patch.object(sync, "ROOT", dictionary), patch.object(sync, "checkout", checkout), \
                patch.object(sync, "run", external), contextlib.redirect_stdout(io.StringIO()):
            work = sync.prepare(args)
        for p, data in originals.items():
            self.assertEqual(p.read_bytes(), data)
        self.assertEqual(self.quiet_git(msime_repo, "status", "--porcelain"), b"")
        report = json.loads((work / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "candidate-ready")
        self.assertEqual(report["diff"]["sources/pinyin/rime-ice-supplement.txt"]["added"], 1)
        self.assertTrue((work / "msime.patch").read_bytes())
        self.assertEqual((work / "dictionary/sources/pinyin/rime-ice.txt").read_bytes(),
                         originals[dictionary / "sources/pinyin/rime-ice.txt"])
        self.assertIn("新增示例词", (work / "dictionary" / audit.OUTPUT / "rime-ice-supplement-only-words.txt").read_text(encoding="utf-8"))
        self.assertTrue(any(a[:2] == ["cargo", "build"] for a in captured))
        apply_args = argparse.Namespace(apply=work, msime_commit="1" * 40, msime=msime_repo)
        main_file = work / "dictionary/sources/pinyin/rime-ice.txt"
        intact = main_file.read_bytes()
        main_file.write_bytes(b"tampered candidate")
        with patch.object(sync, "ROOT", dictionary), patch.object(sync, "checkout") as network, self.assertRaises(ValueError):
            sync.apply_candidate(apply_args)
        network.assert_not_called()
        main_file.write_bytes(intact)
        # Apply the actual generated patch in the local msime fixture, then merge
        # by creating the one references/licensing commit that apply requires.
        self.quiet_git(msime_repo, "apply", str(work / "msime.patch"))
        self.quiet_git(msime_repo, "add", "--", "resources/dictionary-sources.lock.json",
                       "resources/licenses/msime-engine-dictionary-NOTICE.md", "resources/licenses/web-engine-NOTICE.md")
        self.quiet_git(msime_repo, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                       "commit", "-m", "test(sync): paired references and licensing")
        self.quiet_git(msime_repo, "branch", "-M", "develop")
        apply_args.msime_commit = self.quiet_git(msime_repo, "rev-parse", "HEAD").decode().strip()
        real_write = Path.write_bytes
        fault = {"armed": True}

        def fail_one_write(path, data):
            if path == dictionary / "sources/pinyin/rime-ice-supplement.txt" and fault["armed"]:
                fault["armed"] = False
                raise OSError("simulated disk write failure")
            return real_write(path, data)

        with patch.object(sync, "ROOT", dictionary), patch.object(sync, "checkout", checkout), \
                patch.object(Path, "write_bytes", fail_one_write), contextlib.redirect_stdout(io.StringIO()), \
                self.assertRaises(OSError):
            sync.apply_candidate(apply_args)
        self.assertFalse(fault["armed"])
        for p, data in originals.items():
            self.assertEqual(p.read_bytes(), data)
        with patch.object(sync, "ROOT", dictionary), patch.object(sync, "checkout", checkout), \
                contextlib.redirect_stdout(io.StringIO()):
            sync.apply_candidate(apply_args)
        self.assertEqual(json.loads((dictionary / "builder.lock.json").read_text())["msime_commit"],
                         apply_args.msime_commit)
        self.assertEqual((dictionary / "sources/pinyin/rime-ice.txt").read_bytes(), intact)
        with patch.object(audit, "ROOT", dictionary), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(audit.main(["--check"]), 0)

    def test_apply_rejects_failed_candidate_before_network_or_writes(self):
        self.write(self.root, "report.json", audit.encode_json({"status": "failed"}))
        args = argparse.Namespace(apply=self.root, msime_commit="1" * 40)
        with patch.object(sync, "checkout") as checkout, self.assertRaises(ValueError):
            sync.apply_candidate(args)
        checkout.assert_not_called()


if __name__ == "__main__":
    unittest.main()
