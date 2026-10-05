# 水杉输入法词库

水杉输入法（[msime](https://github.com/metasequoiaime/msime)）词库的源数据仓库：这里只放文本源数据，由 msime 的构建器 `msime-dict-build` 构建成本仓 `dict-v*` Release 中的数据库与模型；构建脚本和生成的数据库都不放在这里。

- 想加一个词、一个英文单词或一条候选窗翻译：见[贡献词条](#贡献词条)。
- 想做一个按需导入的专业词库：见[专业词库](#专业词库)和 [packs/README.md](packs/README.md)。
- 维护者发布新词库：见[发布](#发布)。

## 目录

```
sources/                                  msime 构建器经 --dictionary 读取的全部输入，按输入方案分目录
  pinyin/                                 拼音词库 -> msime-pinyin.db
    rime-ice.txt                          雾凇拼音（rime-ice）的全拼词条，经本项目修正 -> msime-pinyin.db
    rime-ice-supplement.txt               rime-ice 新提交中相对 rime-ice.txt 新增的词条（本项目生成的补充表）-> msime-pinyin.db
    places.txt                            行政区划全称与简称中缺失或权重偏低的词条（本项目生成的补充表）-> msime-pinyin.db
    single-chars.txt                      单字读音与字频 -> msime-pinyin.db；msime-stroke.db 的权重
  wubi/                                   五笔词库 -> msime-wubi.db
    wubi86-jidian.txt                     86 版五笔（rime-wubi86-jidian，另补了 rime-wubi 的词条）-> wubi86 表
    wubi86-supplement.txt                 86 表没有、98 表或拼音高频二字词里有的词组，编码按 86 词组规则推出（本项目生成的补充表）-> wubi86 表
    wubi98.txt                            98 版五笔主表（98wubi-tables 的 98五笔含词表-【单义】.txt 原样改名，UTF-16LE）-> wubi98 表
    wubi98-fcitx.txt                      Fcitx5 table-extra 的 98 五笔表，作补充（tables/wubi98.txt 原样改名）-> wubi98 表
  english/                                英文词库 -> msime-english.db
    rime-ice-en.txt                       雾凇的英文词表 -> msime-english.db
    rime-ice-en-supplement.txt            rime-ice 新提交中相对 rime-ice-en.txt 新增的纯 ASCII 单词（本项目生成的补充表）-> msime-english.db
    scowl-words.txt                       SCOWL 60 级英文词表中 rime-ice 英文词表与 custom/english.txt 没有、且有 Google 词频的词（本项目生成的补充表）-> msime-english.db
    google-word-counts.txt                Google 英文词频，作排序权重 -> msime-english.db
  cantonese/                              粤拼方案 -> msime-cantonese.db
    jyut6ping3.chars.dict.yaml            单字与粤拼 -> msime-cantonese.db
    jyut6ping3.words.dict.yaml            词语与粤拼 -> msime-cantonese.db
    essay-cantonese.txt                   字词频率（以上三个是 rime-cantonese 原样）-> msime-cantonese.db
    hkcancor-word-counts.txt              香港粤语语料库的词频，给 essay 没收的词加权（本项目生成）-> msime-cantonese.db
  zhuyin/                                 注音方案 -> msime-zhuyin.db
    tsi.csv                               词语、词频与注音（libchewing-data 原样）-> msime-zhuyin.db
    word.csv                              单字与注音（libchewing-data 原样）-> msime-zhuyin.db
    mcbopomofo-supplement.txt             由 McBopomofo 数据转换的补充词语（本项目转换，不是原样）-> msime-zhuyin.db
    phrase.occ                            McBopomofo 的词语出现次数，给 tsi.csv 没计数的词加权（McBopomofo 原样）-> msime-zhuyin.db
  stroke/                                 笔画方案（rime-stroke 原样）-> msime-stroke.db
    stroke.dict.yaml                      字与笔顺码 -> msime-stroke.db
  japanese/                               日文方案（Mozc OSS 词库原样）-> msime-japanese.dat
    dictionary00.txt … dictionary09.txt   读音、上下文 ID、代价与词语 -> msime-japanese.dat
    id.def                                上下文 ID 与词性标签 -> msime-japanese.dat
    connection_single_column.txt          连接代价矩阵 -> msime-japanese.dat
    dictionary_filter.tsv                 要从基础词库删去的词条（读音与词语的正则）-> msime-japanese.dat
    aux_dictionary.tsv                    沿用已有词条上下文 ID 与代价的新词 -> msime-japanese.dat
    places.tsv、words.tsv                 Mozc dictionary_manual 的人工词表（读音、词语、词性）-> msime-japanese.dat
    README.txt                            上游说明与许可 -> msime-mozc_dictionary_oss_README.txt
    LICENSE                               Mozc 仓库根目录的许可证（Google BSD 与词典条款）-> msime-mozc_LICENSE.txt
  korean/                                 韩文方案（libhangul 原样）
    hanja.txt                             韩文音节与汉字 -> msime 引擎内嵌的 Hanja 表（不是 Release 附件）
  unlicensed/                             没有再分发授权的文件，发布构建不使用，只供 --include-unlicensed 的本地完整构建
    custom-pinyin-dictionary-part1.txt    CustomPinyinDictionary 与雾凇合并的全量词库（第 1 部分）-> 只进完整构建的 msime-pinyin.db
    custom-pinyin-dictionary-part2.txt    同上（第 2 部分）-> 只进完整构建的 msime-pinyin.db
    single-char-whitelist.txt             单字白名单，来源没有记录 -> 只在完整构建中过滤单字
    oaldpe-words.txt                      从 oaldpe.mdx 提取的英文词形列表 -> 只进完整构建的 msime-english.db
custom/                                   人工维护的数据，唯一接受投稿的目录（只追加）
  words.txt                               中文词条 -> msime-pinyin.db
  translations.txt                        候选窗翻译 -> msime-english.db
  english.txt                             英文词条 -> msime-english.db
  names.txt                               人名（没有任何构建或网站读取）
packs/                                    用户按需导入的专业词库，不进入构建
  README.md                               专业词库的说明与验收清单
  ai_ml/                                  机器学习与大模型
  programming/                            编程开发
  unreal_houdini/                         Unreal Engine 与 Houdini
scripts/
  validate_packs.py                       专业词库与 custom/translations.txt 的本地检查
.github/
  workflows/                              CI 与发布 workflow，见下文
  dependabot.yml
README.md                                 本文件
NOTICE.md                                 各文件的上游、提交、许可与已知问题
AGENTS.md                                 给代码代理的维护约束
CHANGELOG.md                              已冻结，只作历史记录
```

**目录约定**：`sources/` 放 msime 构建器经 `--dictionary` 读取的输入，由本仓 Git 提交固定，上游原样文件和派生文件另由根目录 `upstream.lock.json` 按 SHA-256 固定；粤拼、注音（`tsi.csv`、`word.csv`、`phrase.occ`）、笔画、日文、韩文的上游原样文件保留上游的文件名；本项目生成或修正的文件，以及上游文件名不是 ASCII 或会和别的文件同名的上游原样文件（`wubi98.txt`、`wubi98-fcitx.txt`，上游原文件名见 `NOTICE.md`），用小写、连字符分隔、说明来源的名字（如 `rime-ice-supplement.txt`、`mcbopomofo-supplement.txt`），不带版本后缀，因为内容由提交固定。`custom/` 是唯一接受投稿的地方，只追加。`packs/` 是可选的专业词库，不进入构建。

所有数据文件按字节保存：`upstream.lock.json` 按大小和 SHA-256 固定上游原样文件与派生文件，CI 由 `scripts/check_upstream.py` 检查，msime 构建器读取时再校验一遍，并要求记录的上游提交等于 msime 锁文件和许可证写明的提交；所以不要格式化、转换编码或换行符、排序或去重，仓库的 `.gitattributes`（`* -text`）关闭了换行转换。各文件的上游与许可见 [NOTICE.md](NOTICE.md)，逐文件的格式见[文件格式](#文件格式)。

## 源文件与发布产物

下表依据 msime develop 上发布构建器 `crates/dict-builder` 的 `main.rs`、`licensing.rs` 和各语言模块。“主命令”指 `msime-dict-build --cache … --out …`，“languages”指 `msime-dict-build languages`，发布 workflow 两者都运行。

| 源文件 | 读取它的构建阶段 | 产物 | 发布状态 |
| --- | --- | --- | --- |
| `sources/pinyin/single-chars.txt` | 主命令 Quanpin；languages 的笔画词库用它的字频 | `msime-pinyin.db`；`msime-stroke.db` 的权重 | 进入 |
| `sources/pinyin/rime-ice.txt` | 主命令 Quanpin；其中读错的行由 ReadingCorrections（在 CustomWords 之后）删除，清单是 msime 的 `resources/dictionary-sources/pinyin-reading-corrections.txt`，见 `NOTICE.md`「上游状态与已知数据问题」 | `msime-pinyin.db` | 进入 |
| `sources/pinyin/rime-ice-supplement.txt` | 主命令 Quanpin | `msime-pinyin.db` | 进入 |
| `sources/pinyin/places.txt` | 主命令 PlacesSupplement（在 CustomWords 之前）：没有的词插入，已有且权重更低的调高到这里的权重，已有且权重更高的不变 | `msime-pinyin.db` | 进入 |
| `custom/words.txt` | 主命令 CustomWords：没有的词插入，已有且权重更低的调高到这里的权重，已有且权重更高的不变 | `msime-pinyin.db` | 进入 |
| `sources/unlicensed/custom-pinyin-dictionary-part1.txt`、`sources/unlicensed/custom-pinyin-dictionary-part2.txt` | 只在 `--include-unlicensed` 的完整构建中读取 | — | 被 `licensing.rs` 排除：合并自 CustomPinyinDictionary，该快照没有声明许可；发布构建改用 `sources/pinyin/rime-ice.txt` |
| `sources/unlicensed/single-char-whitelist.txt` | 只在完整构建中读取 | — | 被 `licensing.rs` 排除：来源没有记录 |
| `sources/wubi/wubi86-jidian.txt` | 主命令 Wubi | `msime-wubi.db` 的 `wubi86` 表 | 进入 |
| `sources/wubi/wubi86-supplement.txt` | 主命令 Wubi，在 `wubi86-jidian.txt` 之后并入；同一编码下排在原有词条之后 | `msime-wubi.db` 的 `wubi86` 表 | 进入 |
| `sources/wubi/wubi98.txt`、`sources/wubi/wubi98-fcitx.txt` | 主命令 Wubi98：以主表为准，补充表中重复的（编码、词语）去掉 | `msime-wubi.db` 的 `wubi98` 表 | 进入 |
| `sources/english/rime-ice-en.txt`、`sources/english/rime-ice-en-supplement.txt` | 主命令 English，只保留全部由 ASCII 字母组成的显示词；同一个词的每种大小写各占一行：SCOWL 只收了大写形式的（Wikipedia、Ukraine）大写在前，其余全小写的在前 | `msime-english.db` | 进入 |
| `sources/english/scowl-words.txt` | 主命令 English，与上一行的词表合并；SCOWL 的许可声明同时写入该库的 `source_notices` 表。这些词有英译中释义，但不进中译英释义的候选 | `msime-english.db` | 进入（`dict-v` 发布附 `msime-scowl_Copyright.txt`） |
| `sources/english/google-word-counts.txt` | 主命令 English，作为排序权重 | `msime-english.db` | 进入 |
| `custom/english.txt` | 主命令 English | `msime-english.db` | 进入 |
| `sources/unlicensed/oaldpe-words.txt` | 只在完整构建中读取 | — | 被 `licensing.rs` 排除：提取自商业词典 |
| `custom/translations.txt` | 主命令 CustomTranslations，覆盖由 ECDICT 生成的释义 | `msime-english.db` | 进入 |
| `sources/cantonese/` 下 4 个文件 | languages；`hkcancor-word-counts.txt` 只作排序权重 | `msime-cantonese.db` | 进入 |
| `sources/zhuyin/` 下 4 个文件 | languages；`phrase.occ` 只作排序权重 | `msime-zhuyin.db` | 进入 |
| `sources/stroke/stroke.dict.yaml` | languages | `msime-stroke.db` | 进入 |
| `sources/japanese/dictionary00.txt` … `dictionary09.txt`、`id.def`、`connection_single_column.txt` | 主命令 JapaneseModel | `msime-japanese.dat` | 进入 |
| `sources/japanese/dictionary_filter.tsv` | 主命令 JapaneseModel，按 Mozc `gen_filtered_dictionary.py` 删去基础词库中完全匹配的行 | `msime-japanese.dat` | 进入 |
| `sources/japanese/aux_dictionary.tsv`、`places.tsv`、`words.tsv` | 主命令 JapaneseModel，按 Mozc `gen_aux_dictionary.py --strict` 生成补充词条：aux 行复制基准词条的上下文 ID 与代价再加偏移，词表行按词性取同词性词条代价的中位数，基础词库已有的跳过 | `msime-japanese.dat` | 进入 |
| `sources/japanese/README.txt` | 主命令 JapaneseModel，原样复制 | `msime-mozc_dictionary_oss_README.txt` | 进入 |
| `sources/japanese/LICENSE` | 主命令 JapaneseModel，原样复制 | `msime-mozc_LICENSE.txt` | 进入 |
| `sources/korean/hanja.txt` | `msime-dict-build hanja`，发布 workflow 不运行 | msime 源码里的 `crates/engine/src/korean/hanja.tsv`，由引擎用 `include_str!` 内嵌 | 不是 Release 附件 |
| `custom/names.txt` | 无 | — | 没有消费方：构建器不读，官网投稿也不写它 |
| `packs/` | 不进入构建 | msime.app 按本仓 `main` 读取并列出（官网缓存约一小时），用户在设置里导入 | 不进入 Release |

几点补充：

- `msime-pinyin.db` 构建完的全拼表同时是 `msime-bigram.bin`、`msime-trigram.bin` 的词表，ECDICT 释义的中文权重也从它读取，所以改动它的输入也会改变 n-gram 模型和 `msime-english.db` 的释义。
- 有些输入不在本仓：ECDICT、zhwiki 语料、msime `resources/dictionary-sources/` 下的快捷短语（进入 `msime-pinyin.db`）以及 emoji、颜文字和符号（构成 `msime-others.db`），还有 msime `resources/licenses/` 下的许可证文本。
- `licensing.rs` 排除的输入记录在每个 Release 的 manifest 里（`licensing.excluded_inputs`），发布 workflow 会断言 `licensing.includes_unlicensed_inputs` 为 `false`。

## 贡献词条

有两种途径：

- **官网提交**：在 [msime.app](https://msime.app) 的词条提交页填写中文词语、英文单词或候选窗翻译。人名也按词语提交。服务端以 `community-words/<时间戳>` 分支按批开 Pull Request，维护者审核后合入。
- **直接提 Pull Request**：在 `custom/words.txt`、`custom/translations.txt` 或 `custom/english.txt` 的末尾追加行。不要修改、删除或重排已有的行。

三个文件的格式：

| 文件 | 每行 | 说明 |
| --- | --- | --- |
| `custom/words.txt` | `词<TAB>全拼<TAB>权重` | 全拼音节用 `'` 分隔，如 `未来可期	wei'lai'ke'qi	5000` |
| `custom/translations.txt` | `源词<TAB>译文` | 源词含 U+3400 及以上的字符（汉字）时是中译英，否则是英译中；`#` 开头是注释。同一源词写了多行时，构建取最后一行 |
| `custom/english.txt` | `编码<TAB>显示词<TAB>权重` | 编码是输入的小写字母，显示词是上屏的写法，同一编码可以有多个显示词 |

**权重**：新词条的权重必须落在所在文件现有条目的范围内，CI 按文件当前内容计算这个范围。`custom/words.txt` 目前是 1 到 10000，大多数历史条目写的是 `1`。想让一个词在整句里更容易胜出，就参照基础词库里同量级的真实词取值（例如 `扛不住` 在 `sources/pinyin/rime-ice.txt` 里是 2430），不要为了靠前填一个极大值。`custom/english.txt` 目前只有 `1`：有 Google 词频的英文词按词频排序，没有词频的才用这里的权重，而且排在所有有词频的词之后。这个范围普通 Pull Request 无法放宽，确实需要时先开 Issue。

**重复**：已经在发布词库里的词（同词同拼音）不应再写进 `custom/words.txt`，check-words 会拒绝它在比对库里找到的重复。比对库是 check-words 运行时找到的本仓最新一次 `dict-v` release 的 `msime-pinyin.db` 和 `msime-english.db`，按该 release 自带的 `msime-SHA256SUMS.txt` 校验，所以已经发布的源数据（包括 `sources/pinyin/rime-ice-supplement.txt`、`sources/english/rime-ice-en-supplement.txt`）里的词都会被拦下，每次发版后自动跟上，不需要改 workflow。`custom/words.txt` 现有的 9 行（刘汝佳、断连、堪堪、判空、属于是、云风、扛把子、推流、合入）与发布输入里的词重复，其中扛把子（100 → 10000）、推流（689 → 3855）、合入（100 → 3855）三行抬高了已发布词的权重，另外 6 行的权重不高于已有值（5 行更低，断连相等），不起作用。按只追加规则这些行保留不删。

### CI

本仓有 5 个 workflow（`.github/workflows/`）：

| workflow | 触发 | 检查什么 |
| --- | --- | --- |
| `check-words.yml` | Pull Request 改动 `custom/words.txt`、`custom/translations.txt`、`custom/english.txt` | 用 msime 固定提交（`MSIME_COMMIT`）的 `msime-dict-build check-words`，即构建所用的解析器：只能追加；每行能按构建的规则解析（词语的全拼须是 `'` 分隔的小写字母并能映射到全拼表）；词语和英文的权重在文件现有范围内；不与本次改动、所在文件或比对库重复（比对库是运行时找到的最新 `dict-v` release 的 `msime-pinyin.db` 和 `msime-english.db`，按该 release 的 `msime-SHA256SUMS.txt` 校验）。翻译可以给已有源词换一个译文，完全相同的一行算重复。结果写成 Pull Request 评论 |
| `validate-packs.yml` | Pull Request 改动 `packs/`、`custom/translations.txt`、`custom/words.txt`、它对照的 `sources/pinyin/`、`sources/unlicensed/` 文件、脚本或该 workflow | 运行 `python3 scripts/validate_packs.py`，见[专业词库](#专业词库) |
| `quality.yml` | 推送到 `main`、Pull Request、merge queue、手动 | actionlint 校验 workflow 与其中的 shell；Pull Request 上另做依赖审查（high 及以上失败） |
| `codeql.yml` | 每天定时 | CodeQL 分析 GitHub Actions workflow |
| `release-built-dictionaries.yml` | 推送到 `main` 且改动了 `sources/` 或 `custom/`；手动（可只构建不发布） | 用这次推送的提交构建 19 个附件，自动加修订号发布 `dict-v*` Release，说明列出源数据变更和每个附件的用途，见[发布](#发布) |

从 fork 发来的 Pull Request 拿到的是只读 token，check-words 不会发评论；同样的结果在该次运行的 job summary 里。维护者在 CI 之外再人工审核内容（包括敏感词）。

本地能跑的是 `python3 scripts/validate_packs.py`，只用 Python 标准库。check-words 需要 Rust 工具链和 msime 检出，本地一般不跑；要跑的话照 `check-words.yml` 的步骤，在 `MSIME_COMMIT` 上构建 `msime-dict-build` 后运行 `check-words`。

`sources/pinyin/`、`sources/wubi/`、`sources/english/` 下的基础词库来自第三方，不在里面加新词；其中本项目生成的补充表（`sources/pinyin/rime-ice-supplement.txt`、`sources/pinyin/places.txt`、`sources/english/rime-ice-en-supplement.txt`、`sources/english/scowl-words.txt`、`sources/wubi/wubi86-supplement.txt`、`sources/zhuyin/mcbopomofo-supplement.txt`、`sources/cantonese/hkcancor-word-counts.txt`）也不手工改，只用 msime 的生成器在原路径重新生成。候选窗翻译的修正写到 `custom/translations.txt`，不改 ECDICT。`sources/cantonese/`、`sources/zhuyin/`、`sources/stroke/`、`sources/japanese/`、`sources/korean/` 下的上游文件不在本仓修改，错误报给上游。具体约束见 [AGENTS.md](AGENTS.md)。

## 专业词库

| 词库 | 内容 |
| --- | --- |
| [`packs/ai_ml`](packs/ai_ml) | 机器学习与大模型 |
| [`packs/programming`](packs/programming) | 编程开发 |
| [`packs/unreal_houdini`](packs/unreal_houdini) | Unreal Engine、Houdini 和 Houdini Engine for Unreal |

专业词库不进入发布词库，用户在设置里导入后才作为用户词条生效，所以垂直领域的短缩写（`SOP`、`TOP`、`PCG`）不会干扰普通输入。msime.app 按本仓 `main` 读取 `packs/` 下的目录，合入后不需要发版，官网按边缘节点缓存，最长约一小时后显示。每个词库目录要有哪些文件、README 怎么写、验收清单见 [packs/README.md](packs/README.md)。

`python3 scripts/validate_packs.py` 检查：

- `packs/` 下每个目录名只用小写字母、数字和下划线，目录不超过 40 个（官网最多列出 40 个），每个目录都有 `quanpin.txt`、`english.txt`、`translations.txt`、`README.md`，单个词表不超过 2 MiB（超过时官网不统计条数）。
- `quanpin.txt` 每行 `词<TAB>全拼<TAB>权重`：汉字个数与音节数一致（CJK 基本区、扩展区和兼容区的汉字都算），字出现在 `sources/pinyin/single-chars.txt` 或 `sources/pinyin/rime-ice-supplement.txt` 的单字行里时，读音必须是其中列出的读音之一（两张表都没有的字不检查，由人工核对），权重在 1 到 10000 之间，同一词库内不重复。
- `english.txt` 每行 `编码<TAB>显示词<TAB>权重`：编码由小写字母组成，可含连字符和撇号，权重必填且在 1 到 10 之间，同一词库内不重复。
- 每个中文候选和英文候选在该词库的 `translations.txt` 里都有翻译，词库的翻译每个源词只写一行。
- 候选不能已经在发布的拼音词库输入里，即 `sources/pinyin/rime-ice.txt`、`sources/pinyin/rime-ice-supplement.txt`、`sources/pinyin/places.txt`、`custom/words.txt`；与 `sources/unlicensed/custom-pinyin-dictionary-part1.txt`、`sources/unlicensed/custom-pinyin-dictionary-part2.txt` 重复只打印提示，因为这两份不进入发布。
- `custom/translations.txt` 的格式：同一源词后面的行可以覆盖前面的译文，但源词和译文完全相同的行算重复。

## 发布

合入 `main` 的推送只要改动了 `sources/` 或 `custom/`，`release-built-dictionaries.yml` 就自动用这次推送的提交构建并发布一个新的 `dict-v*` Release，不需要先去 msime 改锁文件。只改 `packs/`、文档或 workflow 的合入不触发发布。

1. 版本号：在现有最高的 `dict-vX.Y.Z` 上加一个修订号（`dict-v2.0.6` 之后是 `dict-v2.0.7`）；算出的标签已经存在时失败，已发布的版本不可修改。发布的运行共用一个 concurrency 组，不会两次合入抢同一个版本号；GitHub 每组只保留一个排队的运行，短时间内连续合入时排在中间的运行会被取消，由最新的那次发布，它的说明列出自上一版以来的全部源数据提交。
2. 构建：检出这次推送的提交，用 msime `develop` 的 `msime-dict-build` 和 `msime-dict-build languages`，以 `--dictionary <检出目录>` 直接读取检出里的 `sources/` 与 `custom/`。workflow 检查 19 个附件齐全、两份校验和匹配、manifest 的 `licensing.includes_unlicensed_inputs` 与 `source.dirty` 都是 `false`，并且 `custom_dictionary_commit` 等于这次推送的提交。
3. 发布：`dict-vX.Y.Z` 标签打在这次推送的提交上，Release 标为 latest。Release 说明写明源数据提交、msime 构建器的分支和实际使用的提交、触发方式、自上一版以来改动 `sources/` 或 `custom/` 的提交（比较基点是上一版 manifest 的 `custom_dictionary_commit`，读不到时退回上一版的标签），以及下表每个附件的用途和谁使用它。
4. msime 各平台在 `resources/desktop-dictionary.lock.json` 和 `resources/language-dictionaries.lock.json` 里升级到新版本的 URL、大小和 SHA-256，下一个客户端版本随之带上新词库；check-words 的比对库在运行时自动取最新版本，不需要改。

手动运行（Actions 里的 Release built dictionaries → Run workflow）用于用新的构建器重建同一份源数据，或者只构建不发布的试跑：`version` 留空即自动加修订号，也可以填 `X.Y.Z`；`msime_ref` 默认 `develop`；`publish` 默认关闭，此时只把附件和说明预览上传为 workflow artifact，说明也写进 job summary。打开 `publish` 只能从 `main` 运行；手动指定的版本低于现有最高版本时，Release 不标为 latest。打开 `publish` 的手动运行和推送触发的发布共用一个 concurrency 组，组里只保留一个排队的运行，后来的会取消先排队的：手动发布还在排队时有新的合入推送，手动那次会被取消，改由推送的运行按默认参数（`develop`、自动版本号）发布；反过来手动运行也会取代排队中的推送运行（源数据不丢，只是换成手动指定的参数）。所以手动发布前先在 Actions 里确认没有排队中的发布运行，触发后确认它没有被取消。

msime 的 `resources/dictionary-sources.lock.json` 不固定本仓任何文件，msime 只消费本仓的 `dict-v` Release 附件。要复现某个版本，按它 manifest 的 `custom_dictionary_commit` 检出本仓、按 `source.commit` 检出 msime，再带 `--dictionary` 运行 `msime-dict-build`。

**某个改动进了哪个版本**：每个 Release 的 manifest（`msime-dictionary-manifest.json`）的 `custom_dictionary_commit` 是构建实际读取的本仓提交，Release 说明开头也写着它。由本 workflow 自动发布的版本，标签就打在这个提交上；`dict-v2.0.6` 及更早的版本是用旧 workflow 手动发布的，标签打在发布时的 `main` 上，不一定是读取的源数据（例如 `dict-v2.0.5` 的标签指向 `a4b790c`，而构建读取的是 `5926261`，之后合入的 `5bc9c77`（#42）不在其中）。所以统一按 manifest 判断一个提交是否已发布：

```sh
commit=$(gh release download dict-v2.0.5 -R metasequoiaime/msime-dictionary -p msime-dictionary-manifest.json -O - | jq -r .custom_dictionary_commit)
git merge-base --is-ancestor <改动的提交> "$commit" && echo 已包含
```

`dict-v*` Release 的 19 个附件：

| 附件 | 内容 |
| --- | --- |
| `msime-pinyin.db` | 普通话拼音主词库，以及快捷短语表；构建时按 msime 的读音纠错表删去已知的错误读音 |
| `msime-wubi.db` | 五笔 86 与五笔 98 的编码数据 |
| `msime-english.db` | 英文单词（含 SCOWL 60 级补充词表）与中英双向释义，库内附 SCOWL 版权声明 |
| `msime-others.db` | 表情、颜文字和符号（数据来自 msime 仓库） |
| `msime-japanese.dat` | 基于 Mozc 开源词典生成的日文词库，含 Mozc 的过滤表与 aux、地名、补充词表 |
| `msime-bigram.bin` | 二元语言模型，用于整句候选的上下文评分 |
| `msime-trigram.bin` | 三元语言模型，与二元模型一起参与整句候选排序 |
| `msime-cantonese.db` | 粤拼方案的音节、单字和词语词库，essay 没收的词按 HKCanCor 词频加权 |
| `msime-zhuyin.db` | 注音方案的音节、单字和词语词库，`tsi.csv` 没计数的词语按 McBopomofo `phrase.occ` 加权 |
| `msime-stroke.db` | 笔画方案的编码与候选词库 |
| `msime-mozc_dictionary_oss_README.txt` | 日文词库的来源与许可证说明，分发 `msime-japanese.dat` 时必须一并保留 |
| `msime-mozc_LICENSE.txt` | Mozc 仓库根目录的 `LICENSE`（`sources/japanese/LICENSE` 原文），含 README 里没有的 Google 三条款 BSD 版权声明与免责声明，分发 `msime-japanese.dat` 时必须一并保留 |
| `msime-scowl_Copyright.txt` | 英文词库所用 SCOWL 词表的版权与许可声明（msime `resources/licenses/scowl-aspell6-en-Copyright.txt` 原文），分发 `msime-english.db` 时必须一并保留 |
| `msime-rime_cantonese_LICENSE.txt` | 粤拼词库所用 rime-cantonese 数据的许可证，并附 HKCanCor 的署名与引用 |
| `msime-libchewing_data_LICENSE.txt` | 注音词库所用 libchewing-data 数据的许可证，并附 McBopomofo 补充表的 BSD 说明与 `phrase.occ` 的 MIT 许可全文 |
| `msime-rime_stroke_LICENSE.txt` | 笔画词库所用 rime-stroke 数据的许可证 |
| `msime-dictionary-manifest.json` | 机器可读的发布清单：格式兼容性、构建来源提交、上游引用、功能列表、10 个主产物的大小与 SHA-256、许可检查结果 |
| `msime-SHA256SUMS.txt` | 10 个主产物（主词库、模型、日文说明与 LICENSE、SCOWL 版权声明）和 manifest 的 SHA-256 |
| `msime-language-dictionaries-SHA256SUMS` | 语言词库及其许可证文本的 SHA-256 |

## 文件格式

除 `sources/wubi/wubi98.txt` 外都是 UTF-8 无 BOM。“结尾换行”指文件最后一行之后是否有换行符。

| 文件 | 编码 | 换行 | 文件头 | 每行 | 结尾换行 |
| --- | --- | --- | --- | --- | --- |
| `sources/pinyin/rime-ice.txt` | UTF-8 | CRLF | 1 行 `#` 注释 | `词<TAB>全拼<TAB>权重`，全拼音节用 `'` 分隔 | 有 |
| `sources/pinyin/rime-ice-supplement.txt` | UTF-8 | LF | 1 行 `#` 注释（上游提交与生成方式；其中的 `BaseDictIceV1` 是 `rime-ice.txt` 的旧名，见 `NOTICE.md`） | `词<TAB>全拼<TAB>权重`，也含单字行 | 有 |
| `sources/pinyin/places.txt` | UTF-8 | LF | 5 行 `#` 注释（生成器、上游提交、收录与读音规则、对照集合、字音表、权重下限与常用词封顶：同一全拼的其他词权重超过 `rime-ice.txt` 第 90 百分位时，地名权重降到比它低 1，不抢首位；权重为占位值的词不算，占位值是超过常用线的行中被超过 1% 的行共用的单个权重值，当前为 9999） | `词<TAB>全拼<TAB>权重`，按词和全拼排序 | 有 |
| `sources/unlicensed/custom-pinyin-dictionary-part1.txt` | UTF-8 | LF | 无 | `词<TAB>全拼<TAB>权重` | 有 |
| `sources/unlicensed/custom-pinyin-dictionary-part2.txt` | UTF-8 | CRLF | 无 | `词<TAB>全拼<TAB>权重`，权重都是 1；与 part1 是因 GitHub 单文件大小限制拆开的同一份词库 | 有 |
| `sources/pinyin/single-chars.txt` | UTF-8 | CRLF | 1 行 `#` 注释 | `字<TAB>全拼<TAB>权重` | 有 |
| `sources/unlicensed/single-char-whitelist.txt` | UTF-8 | LF | 无 | 一个字 | 有 |
| `sources/wubi/wubi86-jidian.txt` | UTF-8 | 混合：第 1–89271 行 LF，第 89272 行起 CRLF | 无 | `词<TAB>五笔编码<TAB>权重`；第 3835、51162、73916、78885 行多一个第 4 列 | 有 |
| `sources/wubi/wubi86-supplement.txt` | UTF-8 | LF | 5 行 `#` 注释（生成器、输入及其 SHA-256、收录规则、编码规则、对照集合与权重） | `词<TAB>五笔编码<TAB>权重`，按编码排序，同一编码内按权重从高到低 | 有 |
| `sources/wubi/wubi98.txt` | UTF-16LE，带 BOM | CRLF | 无 | `词<TAB>五笔编码`，没有权重，同一编码内按行序排列 | 有（UTF-16LE 的 CRLF） |
| `sources/wubi/wubi98-fcitx.txt` | UTF-8 | LF | 第 1–8 行是 Fcitx 码表头：`KeyCode=`、`Length=`、`Pinyin=`、`[Rule]` 及规则、`[Data]` | `五笔编码 词`，空格分隔 | 有 |
| `sources/english/rime-ice-en.txt` | UTF-8 | CRLF | 无；正文中有 1777 行被 `#` 注释掉的条目和 16 个空行 | `显示词 编码 [权重]`，空格分隔；显示词本身可含空格（如 `Dish Network DishNetwork`），51 行带权重 | 有 |
| `sources/english/rime-ice-en-supplement.txt` | UTF-8 | LF | 3 行 `#` 注释（其中的 `BaseDictIceEn.txt` 是 `rime-ice-en.txt` 的旧名，见 `NOTICE.md`） | `显示词<TAB>编码` | 有 |
| `sources/english/scowl-words.txt` | UTF-8 | LF | 9 行 `#` 注释（生成器、上游发布与提交、SCOWL 版权与许可声明、收录规则、对照集合、排除规则、排序方式、行序） | 一个显示词，全由 ASCII 字母组成，至少 3 个字母；按小写形式排序，同一个词的全小写形式在前 | 有 |
| `sources/english/google-word-counts.txt` | UTF-8 | LF | 无 | `词<TAB>次数` | 无 |
| `sources/unlicensed/oaldpe-words.txt` | UTF-8 | LF | 无 | 一个小写词形 | 有 |
| `sources/cantonese/jyut6ping3.chars.dict.yaml` | UTF-8 | LF | Rime YAML 头，到第 12 行 `...` 为止 | `字<TAB>粤拼[<TAB>百分比]`，粤拼带声调数字，第 3 列是该字各读音的使用比例，可省略 | 有 |
| `sources/cantonese/jyut6ping3.words.dict.yaml` | UTF-8 | LF | Rime YAML 头，到第 12 行 `...` 为止 | `词<TAB>粤拼`，音节用空格分隔 | 有 |
| `sources/cantonese/essay-cantonese.txt` | UTF-8 | LF | 无 | `字或词<TAB>次数` | 有 |
| `sources/cantonese/hkcancor-word-counts.txt` | UTF-8 | LF | 3 行 `#` 注释（生成器、上游提交与引用、计数规则） | `词<TAB>次数`，按次数降序、同次数按码位排序 | 有 |
| `sources/zhuyin/tsi.csv` | UTF-8 | LF | 4 行 `# dc:` 元数据 | `词,词频,注音`，音节用空格分隔 | 有 |
| `sources/zhuyin/word.csv` | UTF-8 | LF | 4 行 `# dc:` 元数据 | `字,频率,注音`，频率都是 0 | 有 |
| `sources/zhuyin/mcbopomofo-supplement.txt` | UTF-8 | LF | 2 行 `#` 中文注释（来源提交与转换方式） | `词,0,注音`，逗号分隔，相对 `tsi.csv` 去重 | 有 |
| `sources/zhuyin/phrase.occ` | UTF-8 | LF | 无 | `词 次数`，空格分隔（上游文档写的是 tab），含单字、注音符号与 0 次的行，按 C locale 排序 | 有 |
| `sources/stroke/stroke.dict.yaml` | UTF-8 | LF | Rime YAML 头，到第 24 行 `...` 为止 | `字<TAB>笔顺码`，笔顺码由 `h` 横、`s` 竖、`p` 撇、`n` 点、`z` 折组成；一个字可以有多行 | 有 |
| `sources/japanese/dictionary00.txt` … `dictionary09.txt` | UTF-8 | LF | 无 | `读音<TAB>左上下文<TAB>右上下文<TAB>代价<TAB>词语`；`dictionary09.txt` 有 62 行带第 6 列 `SPELLING_CORRECTION` | 有 |
| `sources/japanese/id.def` | UTF-8 | LF | 无 | `编号 标签`，空格分隔，标签内部用逗号分隔（如 `0 BOS/EOS,*,*,*,*,*,*`），共 2672 行 | 有 |
| `sources/japanese/connection_single_column.txt` | UTF-8 | LF | 第 1 行 `2672` 是矩阵维度 | 之后每行一个连接代价，共 2672² = 7139584 行 | 有 |
| `sources/japanese/README.txt` | UTF-8 | LF | — | 上游说明，含许可与署名要求 | 有 |
| `sources/japanese/LICENSE` | UTF-8 | LF | — | Mozc 仓库根目录的许可证：Google 三条款 BSD 文本，之后是 `src/data/dictionary*` 的 NAIST/ICOT 条款与冲绳辞书的公有领域声明 | 有 |
| `sources/japanese/dictionary_filter.tsv` | UTF-8 | LF | 1 行 `#` 列名 | `读音正则<TAB>词语正则` | 有 |
| `sources/japanese/aux_dictionary.tsv` | UTF-8 | LF | 1 行 `#` 列名 | `读音<TAB>词语<TAB>基准读音<TAB>基准词语<TAB>代价偏移` | 有 |
| `sources/japanese/places.tsv`、`sources/japanese/words.tsv` | UTF-8 | LF | 1 行 `#` 列名 | `读音<TAB>词语<TAB>词性`，词性是 `名詞`、`固有名詞`、`地名` 等 Mozc 别名 | 有 |
| `sources/korean/hanja.txt` | UTF-8 | LF | 26 行 `#` 注释（BSD 许可） | `韩文音节:汉字:训音` | 有 |
| `custom/words.txt` | UTF-8 | LF | 无 | `词<TAB>全拼<TAB>权重` | 有 |
| `custom/translations.txt` | UTF-8 | LF | `#` 注释行，开头和各分组前都有 | `源词<TAB>译文` | 有 |
| `custom/english.txt` | UTF-8 | LF | 无 | `编码<TAB>显示词<TAB>权重` | 无 |
| `custom/names.txt` | UTF-8 | LF | 无 | 一个人名 | 无 |

## 许可

本仓库**不对外提供统一的开源许可**：其中绝大部分词库并非本项目的作品，给整个仓库挂一份 LICENSE 等于替上游作者重新授权。逐项的来源与上游条款见 [NOTICE.md](NOTICE.md)，使用或再分发前请以对应上游的条款为准。本项目自建的部分（`custom/`、`packs/`、`scripts/`）以 GPL-3.0 提供。

## 历史

本仓库最初名为 MSIME-Dict，保存词库源数据和 Python 构建脚本，自定义词条在独立的 msime-customdict 中；2026-09-05 两者并入 MSIME-Engine。MSIME-Engine 被 msime 的 Rust 引擎和构建器取代后，源数据于 2026-09-30 以复制文件的方式回到这里（当时的 `cn/`、`en/` 取自 msime-engine [`e92a9c7`](https://github.com/metasequoiaime/msime-engine/tree/e92a9c7c64e262f30218ca9aaad5f40d0b18cf89/dictionary)，`custom/`、`packs/`、`scripts/validate_packs.py` 取自 msime-customdict [`b075c8e`](https://github.com/metasequoiaime/msime-customdict/tree/b075c8e3e71ab48b3c048c229289275b0d42b6d0)，早先的历史在这两个仓库中查阅），本仓库成为唯一的词库源数据仓库。
