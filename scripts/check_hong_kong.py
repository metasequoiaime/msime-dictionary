#!/usr/bin/env python3
"""核对香港官方名称快照、派生表与覆盖报告；来源不是 Git 仓库，单独固定下载摘要。"""

import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'sources/hong-kong'
INPUT_PATHS = {
    'sources/hong-kong/landsd-place-names.geojson',
    'sources/hong-kong/landsd-street-names.json',
    'sources/hong-kong/CSDI-terms.txt',
    'sources/cantonese/jyut6ping3.chars.dict.yaml',
    'sources/cantonese/jyut6ping3.words.dict.yaml',
    'sources/pinyin/single-chars.txt', 'sources/pinyin/rime-ice.txt',
    'sources/pinyin/rime-ice-supplement.txt', 'sources/pinyin/places.txt',
    'sources/opencc/TSCharacters.txt', 'sources/opencc/HKVariants.txt',
    'sources/opencc/TWVariants.txt',
    'curation/hong-kong-readings.tsv', 'curation/hong-kong-forms.tsv',
}


def measure(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def main():
    manifest = json.loads((DATA / 'sources.json').read_text())
    files = manifest['files']
    expected = {'landsd-place-names.geojson', 'landsd-street-names.json', 'CSDI-terms.txt'}
    assert len(files) == len(expected) and {f['path'] for f in files} == expected
    for entry in files:
        assert measure(DATA / entry['path']) == (entry['size'], entry['sha256']), entry['path']
    generated = manifest['generated']
    inputs = generated.get('inputs', [])
    assert len(inputs) == len(INPUT_PATHS) and {entry['path'] for entry in inputs} == INPUT_PATHS, '生成输入清单不完整'
    for entry in inputs:
        assert measure(ROOT / entry['path']) == (entry['size'], entry['sha256']), '生成输入已变化：' + entry['path']
    assert generated['path'] == 'landsd-readings.tsv'
    assert re.fullmatch('[a-f0-9]{40}', generated['msime_commit']), '生成器必须来自已提交工作区'
    table = DATA / generated['path']
    assert measure(table) == (generated['size'], generated['sha256'])
    assert table.read_text().splitlines()[0] == '# msime 仓库提交 ' + generated['msime_commit']
    rows = [line.split('\t') for line in table.read_text().splitlines() if line and not line.startswith('#')]
    assert len(rows) == generated['rows']
    assert len({tuple(row) for row in rows}) == len(rows)
    for row in rows:
        assert len(row) == 4
        for word, key, delimiter in [(row[0], row[2], ' '), (row[1], row[3], "'")]:
            assert all('\u3400' <= char <= '\u4dbf' or '\u4e00' <= char <= '\u9fff' or '\U00020000' <= char <= '\U000323af' for char in word), row
            assert len(word) >= 2 and len(word) == len(key.split(delimiter)), row
            assert all(re.fullmatch('[a-z]+', syllable) for syllable in key.split(delimiter)), row
    audit = DATA / 'audit.json'
    assert measure(audit)[1] == generated['audit_sha256']
    report = json.loads(audit.read_text())
    assert report['counts'] == generated['counts']
    assert not report['pending'], '有待审读音，不可发布'
    for kind in ['ready', 'pending', 'unsupported']:
        assert len(report[kind]) == report['counts'][kind]
    assert sum(report['counts'].values()) == report['input_names']
    assert {row[0] for row in rows} == set(report['ready'])
    assert all('reason' in row for row in report['unsupported'])
    print(f"OK: {len(rows)} 香港名称，{len(report['unsupported'])} 条有明确不支持原因，来源与派生摘要一致")


if __name__ == '__main__':
    main()
