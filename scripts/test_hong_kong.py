"""用合成数据验证输入、生成表和报告之间的校验关系。"""

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import check_hong_kong as check


class HongKongValidation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.data = self.root / 'sources/hong-kong'
        for name in check.INPUT_PATHS:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('合成输入\n')
        self.commit = 'a' * 40
        (self.data / 'landsd-readings.tsv').write_text(
            '# msime 仓库提交 ' + self.commit + "\n示例街\t示例街\tsi lai gaai\tshi'li'jie\n")
        report = {'input_names': 1, 'ready': ['示例街'], 'pending': [], 'unsupported': [],
                  'counts': {'ready': 1, 'pending': 0, 'unsupported': 0}}
        (self.data / 'audit.json').write_text(json.dumps(report))
        self.manifest = {
            'files': [self.record(path, self.data) for path in ['landsd-place-names.geojson', 'landsd-street-names.json', 'CSDI-terms.txt']],
            'generated': {**self.record('landsd-readings.tsv', self.data), 'msime_commit': self.commit,
                          'rows': 1, 'counts': report['counts'], 'audit_sha256': check.measure(self.data / 'audit.json')[1],
                          'inputs': [self.record(path, self.root) for path in sorted(check.INPUT_PATHS)]},
        }
        self.save()

    def record(self, path, root):
        size, digest = check.measure(root / path)
        return {'path': path, 'size': size, 'sha256': digest}

    def save(self):
        (self.data / 'sources.json').write_text(json.dumps(self.manifest))

    def validate(self):
        with patch.object(check, 'ROOT', self.root), patch.object(check, 'DATA', self.data), contextlib.redirect_stdout(io.StringIO()):
            check.main()

    def test_consistent_generation_passes(self):
        self.validate()

    def test_each_changed_generation_input_is_rejected(self):
        for name in sorted(check.INPUT_PATHS):
            with self.subTest(name=name):
                path = self.root / name
                original = path.read_bytes()
                path.write_text('已修改输入\n')
                with self.assertRaises(AssertionError):
                    self.validate()
                path.write_bytes(original)

    def test_updated_snapshot_digest_cannot_hide_stale_generation(self):
        name = 'landsd-street-names.json'
        (self.data / name).write_text('新的快照\n')
        self.manifest['files'] = [self.record(entry['path'], self.data) for entry in self.manifest['files']]
        self.save()
        with self.assertRaisesRegex(AssertionError, '生成输入已变化'):
            self.validate()

    def test_missing_or_duplicate_input_record_is_rejected(self):
        inputs = self.manifest['generated']['inputs']
        inputs[-1] = inputs[0]
        self.save()
        with self.assertRaisesRegex(AssertionError, '清单不完整'):
            self.validate()

    def test_modified_table_and_report_are_rejected(self):
        for name in ['landsd-readings.tsv', 'audit.json']:
            with self.subTest(name=name):
                path = self.data / name
                original = path.read_bytes()
                path.write_text('损坏输出\n')
                with self.assertRaises(AssertionError):
                    self.validate()
                path.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
