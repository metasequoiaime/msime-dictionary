# 专业词库

`packs/` 下每个子目录是一个可选的专业词库，用户在水杉输入法设置的词库管理页面自行导入。专业词库不进入 `dict-v*` 发布构建（msime 的 `resources/dictionary-sources.lock.json` 和 `crates/dict-builder` 都不读取 `packs/`）；msime.app 的“专业词库”列表按 `main` 分支读取 `packs/<目录>/`（每个边缘节点最多每小时读取一次，合入后最长约一小时才显示）：标题和简介取自该目录 `README.md` 的一级标题和其后第一段，词表是目录里的 `.txt` 文件。

## 现有词库

| 目录 | 名称 | 中文候选 | 英文候选 | 翻译 |
| --- | --- | ---: | ---: | ---: |
| [`ai_ml`](ai_ml/) | 机器学习与大模型专业词库 | 600 | 169 | 768 |
| [`programming`](programming/) | 编程开发专业词库 | 731 | 186 | 916 |
| [`unreal_houdini`](unreal_houdini/) | Unreal Engine 与 Houdini 专业词库 | 116 | 115 | 236 |

条目数取自 `python3 scripts/validate_packs.py` 的输出。

## 目录结构

每个词库目录必须包含以下四个文件，`packs/<目录>/` 下不放子目录（msime.app 只读取目录下一层的文件）：

- `README.md`：一级标题是官网显示的名称，其后第一段是简介；正文写收录原则和核对来源。
- `quanpin.txt`：`词语<TAB>全拼<TAB>权重`，全拼音节用 `'` 分隔，不含标题或注释行。
- `english.txt`：`输入键<TAB>显示内容<TAB>权重`，输入键只含小写字母、连字符和撇号，不含标题或注释行。
- `translations.txt`：`源词<TAB>释义`，覆盖上面两个文件里的每个中文词语和英文显示内容。

## 路线

按以下顺序新增，每个 PR 只加一个词库，每个词库 100 到 2000 条；超过这个规模的应作为主词库的补充表处理，不放进 `packs/`。

1. `programming`：版本控制、并发、数据库、前后端和编程语言术语。
2. `ai_ml`：机器学习与大模型术语。
3. `acg_games`：游戏、动漫专名。
4. `finance`：证券、财会、税务。
5. `law`：法律法规名称与法条术语。
6. `medicine`：药名、病名、检验项目。

## 验收清单

标“脚本”的项目由 `python3 scripts/validate_packs.py` 检查，CI（`.github/workflows/validate-packs.yml`）在相关文件变动的 PR 上运行它；标“人工”的项目由审阅者核对。

| # | 要求 | 检查方式 |
| --- | --- | --- |
| 1 | 目录名匹配 `^[a-z0-9_]+$` | 脚本 |
| 2 | 四个文件齐全 | 脚本 |
| 3 | `packs/` 下的词库总数不超过 40（msime.app 每次最多读取 40 个目录，多出的不会列出） | 脚本 |
| 4 | 每个 `.txt` 不超过 2 MiB（超过的 msime.app 仍列出，但不统计条目数） | 脚本 |
| 5 | 字段格式正确；中文词语的汉字数等于拼音音节数；同一文件内没有重复的候选 | 脚本 |
| 6 | 汉字出现在 `sources/pinyin/single-chars.txt` 或 `sources/pinyin/rime-ice-supplement.txt` 的单字行里时，读音是其中列出的读音之一；两张表都没有的字脚本不检查，由第 10 项人工核对 | 脚本 |
| 7 | 中文候选不与发布词库重复：`(词语, 全拼)` 不出现在 `sources/pinyin/rime-ice.txt`、`sources/pinyin/rime-ice-supplement.txt`、`sources/pinyin/places.txt`、`custom/words.txt` 中。与 `sources/unlicensed/custom-pinyin-dictionary-part1.txt`、`sources/unlicensed/custom-pinyin-dictionary-part2.txt` 重复的只作提示，因为发布构建不使用这两个文件 | 脚本 |
| 8 | 权重：`quanpin.txt` 在 1 到 10000 之间（与 `custom/words.txt` 的范围一致）；`english.txt` 必须写权重，在 1 到 10 之间（`custom/english.txt` 现用 1，`unreal_houdini` 现用 10） | 脚本 |
| 9 | 每个中文词语和英文显示内容都有翻译；`translations.txt` 内同一源词只出现一次 | 脚本 |
| 10 | 读音逐条人工核对，多音字在 README 里列出 | 人工 |
| 11 | README 按术语分组列出所依据的文档及访问日期；没有官方中文出处、按通行说法收录的术语在 README 里单独成节并注明这一点，可以点名其中的代表性术语，再说明分组文档没有覆盖的其余条目都归入这一节；不复制定义正文 | 人工 |
| 12 | 有歧义的短缩写只留在专业词库里，不同步到 `custom/translations.txt`（参照 `unreal_houdini` 的做法） | 人工 |
| 13 | 只收领域里实际会输入的词，不收句子和定义；人名只收公共人物；不出现真实可拨的手机号或真实地址 | 人工 |
| 14 | 规模在 100 到 2000 条之间 | 人工 |

`scripts/validate_packs.py` 只依赖 Python 标准库，本地直接运行即可。它同时检查 `custom/translations.txt` 的格式：那里允许后写的行给已有源词换译文（与构建和 check-words 一致），只拒绝源词和译文都相同的重复行。
