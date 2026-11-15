"""Exercise word-level comparison, provenance checks and reviewed imports."""

import copy
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import update_rime_ice_only as update


class RimeIceOnlyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.inputs = {
            "sources/pinyin/wanxiang/test.dict.yaml": "---\nname: test\n...\n已有词\tyǐ yǒu cí\t10\n混合词\tMixed\n".encode(),
            "sources/pinyin/rime-ice.txt": "# source\n已有词\tother\t99\n示例词\tshi'li'ci\t8\n另一词\tling'yi'ci\t20\n示例词\tother\t9\n".encode(),
            "sources/pinyin/rime-ice-supplement.txt": "示例词\tshi'li'ci\t7\n混合词\tother\t20\n".encode(),
            "sources/english/rime-ice-en-supplement.txt": b"Example\tExample\n",
        }
        self.lock = {
            "version": 1,
            "upstreams": {name: {"repository": "https://github.com/example/" + name,
                                 "commit": str(i + 1) * 40}
                          for i, name in enumerate(update.GROUPS)},
            "files": [],
        }
        for path, data in self.inputs.items():
            group = ("rime-wanxiang" if "/wanxiang/" in path else
                     "rime-ice" if path.endswith("/rime-ice.txt") else "rime-ice-supplement")
            self.lock["files"].append({"path": path, "upstream": group,
                                       "size": len(data), "sha256": update.digest(data)})
            self.write(self.root, path, data)
        self.write(self.root, "upstream.lock.json", update.encode_json(self.lock))
        self.notice = "\n".join(ref["commit"] for ref in self.lock["upstreams"].values()).encode()
        self.write(self.root, "NOTICE.md", self.notice)

    def write(self, root, path, data):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def test_word_match_ignores_reading_and_keeps_all_missing_source_rows(self):
        outputs, manifest = update.generate(self.inputs, self.lock)
        self.assertEqual(manifest["sources"]["rime-ice"]["missing_rows"], 3)
        self.assertEqual(manifest["combined_missing_unique_words"], 2)
        words = outputs[update.OUTPUT + "/rime-ice-only-words.txt"].decode().splitlines()
        self.assertEqual(words, ["另一词", "示例词"])
        rows = [line for line in outputs[update.OUTPUT + "/rime-ice-only-entries.txt"].decode().splitlines()
                if not line.startswith("#")]
        self.assertEqual(rows, ["另一词\tling'yi'ci\t20\t4", "示例词\tother\t9\t5", "示例词\tshi'li'ci\t8\t3"])
        self.assertEqual(manifest["sources"]["rime-ice-supplement"]["missing_unique_words"], 1)

    def test_missing_yaml_marker_and_bad_ice_rows_fail(self):
        for path, data in [
            ("sources/pinyin/wanxiang/test.dict.yaml", b"name: test\n"),
            ("sources/pinyin/rime-ice.txt", b"word\tpinyin\n"),
            ("sources/pinyin/rime-ice.txt", b"word\tpinyin\tnot-a-number\n"),
        ]:
            with self.subTest(path=path, data=data), self.assertRaises(ValueError):
                update.generate({**self.inputs, path: data}, self.lock)

    def test_changed_bytes_and_unrecorded_wanxiang_file_fail(self):
        self.assertEqual(update.load_inputs(self.root, self.lock), self.inputs)
        self.write(self.root, "sources/pinyin/wanxiang/extra.dict.yaml", b"...\n")
        with self.assertRaises(ValueError):
            update.load_inputs(self.root, self.lock)
        self.write(self.root, "sources/pinyin/rime-ice.txt", b"changed")
        with self.assertRaises(ValueError):
            update.load_inputs(self.root, self.lock)

    def test_check_detects_stale_output_without_writing(self):
        with patch.object(update, "ROOT", self.root), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(update.main([]), 0)
            self.assertEqual(update.main(["--check"]), 0)
            output = self.root / update.OUTPUT / "rime-ice-only-words.txt"
            output.write_bytes(b"stale")
            self.assertEqual(update.main(["--check"]), 1)
            self.assertEqual(output.read_bytes(), b"stale")

    def test_reviewed_import_validates_before_writes_and_includes_shared_english(self):
        candidate = self.root / "candidate"
        for path, data in self.inputs.items():
            self.write(candidate, path, data)
        self.write(candidate, "upstream.lock.json", update.encode_json(self.lock))
        self.write(candidate, "NOTICE.md", self.notice)
        merged, writes = update.import_plan(self.root, candidate, self.lock)
        self.assertEqual(merged, self.lock)
        self.assertIn("sources/english/rime-ice-en-supplement.txt", writes)
        self.write(candidate, "sources/pinyin/rime-ice.txt", b"invalid")
        with patch.object(update, "ROOT", self.root), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(update.main(["--from-reviewed", str(candidate)]), 1)
        self.assertEqual((self.root / "sources/pinyin/rime-ice.txt").read_bytes(),
                         self.inputs["sources/pinyin/rime-ice.txt"])
        self.assertFalse((self.root / update.OUTPUT).exists())

    def test_reviewed_import_rejects_path_changes(self):
        changed = copy.deepcopy(self.lock)
        changed["files"][0]["path"] = "sources/pinyin/wanxiang/renamed.dict.yaml"
        self.write(self.root / "candidate", "upstream.lock.json", update.encode_json(changed))
        with self.assertRaises(ValueError):
            update.import_plan(self.root, self.root / "candidate", self.lock)

    def test_reviewed_import_accepts_only_explicit_wanxiang_removal(self):
        gone = "sources/pinyin/wanxiang/gone.dict.yaml"
        data = b"---\nname: gone\n...\n"
        current = copy.deepcopy(self.lock)
        current["files"].append({"path": gone, "upstream": "rime-wanxiang", "size": len(data),
                                 "sha256": update.digest(data)})
        candidate = self.root / "candidate"
        for path, body in self.inputs.items():
            self.write(candidate, path, body)
        self.write(candidate, "upstream.lock.json", update.encode_json(self.lock))
        self.write(candidate, "NOTICE.md", self.notice)
        with self.assertRaises(ValueError):
            update.import_plan(self.root, candidate, current)
        merged, writes = update.import_plan(self.root, candidate, current, frozenset({gone}))
        self.assertNotIn(gone, [e["path"] for e in merged["files"]])
        self.assertNotIn(gone, writes)
        with self.assertRaises(ValueError):
            update.import_plan(self.root, candidate, current,
                               frozenset({gone, "sources/pinyin/rime-ice.txt"}))

    def test_reviewed_update_refreshes_sources_locks_notice_and_difference_together(self):
        candidate = self.root / "candidate"
        revised = dict(self.inputs)
        revised["sources/pinyin/rime-ice.txt"] += "新增示例词\txin'zeng'shi'li'ci\t30\n".encode()
        revised["sources/pinyin/wanxiang/test.dict.yaml"] += "另一词\tling yi ci\t20\n".encode()
        revised["sources/english/rime-ice-en-supplement.txt"] += b"Another\tAnother\n"
        revised_lock = copy.deepcopy(self.lock)
        for i, name in enumerate(update.GROUPS):
            revised_lock["upstreams"][name]["commit"] = str(i + 4) * 40
        for entry in revised_lock["files"]:
            data = revised[entry["path"]]
            entry.update(size=len(data), sha256=update.digest(data))
            self.write(candidate, entry["path"], data)
        revised_notice = "\n".join(ref["commit"] for ref in revised_lock["upstreams"].values()).encode()
        self.write(candidate, "NOTICE.md", revised_notice)
        self.write(candidate, "upstream.lock.json", update.encode_json(revised_lock))
        with patch.object(update, "ROOT", self.root), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(update.main(["--from-reviewed", str(candidate)]), 0)
            self.assertEqual(update.main(["--check"]), 0)
        for path, data in revised.items():
            self.assertEqual((self.root / path).read_bytes(), data)
        self.assertEqual(json.loads((self.root / "upstream.lock.json").read_text()), revised_lock)
        self.assertEqual((self.root / "NOTICE.md").read_bytes(), revised_notice)
        words = (self.root / update.OUTPUT / "rime-ice-only-words.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(words, ["新增示例词", "示例词"])


if __name__ == "__main__":
    unittest.main()
