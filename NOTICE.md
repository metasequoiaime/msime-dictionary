# 来源与授权说明

本仓库**不对外提供统一的开源许可**，因为其中绝大部分词库并非本项目的作品，而是从其他项目收集、合并、去重而来（见 [README](README.md)）。给整个仓库挂一份 LICENSE 等于替上游作者重新授权，因此这里改为逐项说明来源与上游条款。使用或再分发本仓库的数据时，请以对应上游的条款为准。

## 中文词库

| 文件 | 上游 | 上游许可 |
| --- | --- | --- |
| `sources/pinyin/rime-ice.txt` | [iDvel/rime-ice](https://github.com/iDvel/rime-ice)，对照提交 `9e66b0729083b37d217312294f6d516c8d7234be`（见下） | GPL-3.0 |
| `sources/pinyin/rime-ice-supplement.txt` | [iDvel/rime-ice](https://github.com/iDvel/rime-ice)，提交 `3aea6d3694fb3d94ec663641f021f788822897ad` 的 `cn_dicts/base.dict.yaml`、`ext.dict.yaml`、`8105.dict.yaml`、`others.dict.yaml`，排除 `rime-ice.txt` 已有的同词同音行 | GPL-3.0 |
| `sources/pinyin/places.txt` | [modood/Administrative-divisions-of-China](https://github.com/modood/Administrative-divisions-of-China)，提交 `c49d495b40ac73eb1a66f6eeae5f8fd10696f035` 的 `dist/provinces.csv`、`dist/cities.csv`、`dist/areas.csv`（原始数据来自国家统计局的统计用区划代码）。由 msime `crates/dict-builder` 的 `msime-dict-build places-supplement` 生成省、地、县三级区划的全称与去后缀简称，读音须由 `rime-ice.txt`、`rime-ice-supplement.txt` 证实，只收这两份文件没有、或权重不超过 10 且低于分层下限的词，这两份文件已有排名（权重大于 10）的词不抬升；这两份文件里同一全拼的其他词权重超过 `rime-ice.txt` 全部行权重的第 90 百分位（常用线，由生成器从数据算出）时，地名权重降到比该词低 1，不抢常用词的首位，比较时跳过权重为占位值的词（`rime-ice.txt` 里权重超过常用线的行中被超过 1% 的行共用的单个权重值，由生成器从数据算出，当前为 9999）；规则与对照文件的 SHA-256 写在文件头 | WTFPL（区划名称）；读音的证实与权重下限依据 rime-ice 的 `rime-ice.txt`、`rime-ice-supplement.txt`（GPL-3.0） |
| `sources/unlicensed/custom-pinyin-dictionary-part1.txt`、`sources/unlicensed/custom-pinyin-dictionary-part2.txt` | [wuhgit/CustomPinyinDictionary](https://github.com/wuhgit/CustomPinyinDictionary)（`2023-09-28(No.82)` 版）与 rime-ice 合并去重 | GPL-3.0 与**未声明**的混合 |
| `sources/pinyin/single-chars.txt` | [iDvel/rime-ice](https://github.com/iDvel/rime-ice)，读音以 [mozillazg/pinyin-data](https://github.com/mozillazg/pinyin-data) 校正 | GPL-3.0 + MIT |
| `sources/wubi/wubi86-jidian.txt` | [KyleBing/rime-wubi86-jidian](https://github.com/KyleBing/rime-wubi86-jidian) | Apache-2.0 |
| `sources/wubi/wubi86-jidian.txt` 新增词条来源 | [rime/rime-wubi](https://github.com/rime/rime-wubi)，提交 `152a0d3f3efe40cae216d1e3b338242446848d07` | LGPL-3.0 |
| `sources/wubi/wubi86-supplement.txt` | 本项目生成的补充表：由 msime `crates/dict-builder` 的 `wubi86-supplement` 子命令从本仓 `sources/wubi/wubi86-jidian.txt`、`sources/wubi/wubi98.txt`、`sources/wubi/wubi98-fcitx.txt` 和 `sources/pinyin/rime-ice.txt` 生成。词条取 86 表没有、而 98 表收录或 rime-ice 权重不低于 5000 的二字词，编码按 86 版词组规则由 86 表的单字全码推出 | GPL-3.0（词条依据 GPL-3.0 的 rime-ice、GPL-3.0-or-later 的 Fcitx 表与 Unlicense 的 98 五笔表；编码依据 Apache-2.0 的 jidian 单字码） |
| `sources/wubi/wubi98.txt` | [yanhuacuo/98wubi-tables](https://github.com/yanhuacuo/98wubi-tables)（98五笔小组），提交 `6b8b6fb9d3c34e0d5e3b17211e1f1c100e7eb697` 的 `98五笔含词表-【单义】.txt`（见下） | Unlicense |
| `sources/wubi/wubi98-fcitx.txt` | [fcitx/fcitx5-table-extra](https://github.com/fcitx/fcitx5-table-extra)，提交 `dbc7154a7f0b9fc04313160ae8066ed4d8cbc446` 的 `tables/wubi98.txt` | GPL-3.0-or-later（随仓库的 `LICENSES/GPL-3.0-or-later.txt`） |
| `sources/unlicensed/single-char-whitelist.txt` | **待确认**，见下方「待解决」 | **待确认** |

`sources/pinyin/rime-ice.txt` 的上游提交是后来补记的：此前它是唯一没有被记录提交的中文词库来源，没有办法判断树里那份是从哪个版本导出的。按 rime-ice `9e66b0729083b37d217312294f6d516c8d7234be` 比对，它的前身 `BaseDictIce.txt` 有 28185 条上游不存在的词条，另有 8328 条权重与上游不同。多出来的条目里既有上游没收的真词（地名、品牌），也有语料切分留下的碎片（例如「米高」「钟的」「之事」）。已确认的碎片在 msime-engine 的 `67fd083` 中从当时的 `cn/BaseDictIceV1.txt` 与 `cn/BaseDictAllV1Part1.txt`（即现在的 `sources/pinyin/rime-ice.txt` 与 `sources/unlicensed/custom-pinyin-dictionary-part1.txt`）删除，本仓库的这两个文件与 msime-engine `e92a9c7c64e262f30218ca9aaad5f40d0b18cf89` 的 `dictionary/cn/` 逐字节一致。这份文件的真实来源仍然没有查清，所以不要把它描述成「原样搬运」。

`sources/wubi/wubi98-fcitx.txt` 保留 Fcitx5 table-extra 的 UTF-8 原始表格式（表头、规则和数据区），构建器只读取数据区的 `编码 空格 词` 行，并与 98 五笔主表按“编码、词语”去重。该表补足主表没有的合法开源候选，例如 `ukuy` 的“冲凉”，同时保留 Fcitx 表中的完整候选集合，不把单个词条作为特殊补丁。

`sources/wubi/wubi98.txt` 与上游文件逐字节一致（SHA-256 `1b5a4c22eddae08d8e0e6aa8f926f92d45d6cdaa591e5cee0e8aad29271da1cc`，UTF-16LE 带 BOM、CRLF），没有改编码或换行。权利声明来自数据作者本人：上游仓库在 2024-01-20 的提交 `4dbcaa65` 加入 Unlicense，此前同一作者在 2021 年把这份表贡献给 [fcitx/fcitx5-table-extra](https://github.com/fcitx/fcitx5-table-extra)（`tables/wubi98.txt`，GPL-3.0-or-later 包内分发，Debian main 收录）。两份表 112584 条里只有 4 条不同，差异来自上游 2024-06-25 的拆分校正（`72a36bae`）。上游没有记录 GB2312/GBK 部分的单字编码与简码是怎样生成的，只能说它们依照 98 版五笔的编码规范；这里如实记下，不把它描述成独立生成。界面上称“98 五笔”，不使用“王码”“五笔字型”等商标。

## 英文词库

| 文件 | 上游 | 上游许可 |
| --- | --- | --- |
| `sources/english/rime-ice-en.txt` | [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | GPL-3.0 |
| `sources/english/rime-ice-en-supplement.txt` | [iDvel/rime-ice](https://github.com/iDvel/rime-ice)，提交 `3aea6d3694fb3d94ec663641f021f788822897ad` 的 `en_dicts/en.dict.yaml` 与 `en_ext.dict.yaml` 中相对 `rime-ice-en.txt` 新增的纯 ASCII 单词 | GPL-3.0 |
| `sources/english/scowl-words.txt` | [en-wl/wordlist](https://github.com/en-wl/wordlist)（SCOWL）发布 `rel-2026.02.25`（提交 `7e99edab8e32f9f9ea2b15f249ca8d4d67237410`）的 Aspell 英文词典 `aspell6-en-2026.02.25-0.tar.bz2`（SCOWL 60 级官方拼写检查词典）中 `en-common.cwl`、`en_US-wo_accents-only.cwl`、`en_GB-ise-wo_accents-only.cwl` 的纯字母词形（至少 3 个字母），排除 `rime-ice-en.txt`、`rime-ice-en-supplement.txt`、`custom/english.txt` 已有或被 rime-ice 注释掉的词、蔑称、只有大写形式且拼出中文词全拼的专名，以及没有 Google 词频的词；由 msime `crates/dict-builder` 的 `english-supplement` 子命令生成 | SCOWL 许可：可自由使用、复制、修改、分发和出售，条件是在所有副本中保留版权声明，并在随附文档中同时保留版权声明与许可声明。文件头照录了版权声明与许可声明；`dict-v` 发布把许可全文作为 `msime-scowl_Copyright.txt` 与 `msime-english.db` 一起附上；词典包 `Copyright` 全文收在 msime 的 `resources/licenses/scowl-aspell6-en-Copyright.txt`。60 级官方词典不涉及 UKACD 条款，也不用澳大利亚英语数据 |
| `sources/english/google-word-counts.txt` | [Google 1/3 million 词频表](https://www.norvig.com/ngrams/count_1w.txt) | 以来源页面说明为准 |
| `sources/unlicensed/oaldpe-words.txt` | 自 oaldpe.mdx 提取的词形列表 | 权利归词典出版方 |

`sources/pinyin/rime-ice-supplement.txt` 第 1 行文件头里的 `BaseDictIceV1`、`sources/english/rime-ice-en-supplement.txt` 第 3 行文件头里的 `BaseDictIceEn.txt` 是生成时对照文件的旧名，分别指现在的 `sources/pinyin/rime-ice.txt`、`sources/english/rime-ice-en.txt`。这两个文件按字节锁定，msime 里也没有它们的生成器，文件头作为历史陈述保留不改；下次补上生成器、在原路径重新生成时再改成新名。

## 粤拼、注音与笔画词库

| 文件 | 上游 | 上游许可 |
| --- | --- | --- |
| `sources/cantonese/jyut6ping3.chars.dict.yaml`、`sources/cantonese/jyut6ping3.words.dict.yaml`、`sources/cantonese/essay-cantonese.txt` | [rime/rime-cantonese](https://github.com/rime/rime-cantonese)，默认分支 `main` 提交 `259f0e48bba840c3a2e0d117539e96937f3d89bc`（上游每周发布的 `latest` Release 所在提交）的同名文件 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| `sources/cantonese/hkcancor-word-counts.txt` | [fcbond/hkcancor](https://github.com/fcbond/hkcancor)（香港粤语语料库 HKCanCor），提交 `39aeadf920e0b5ca93d0ad7792c59e740e7bdd65` 的 `data/utf8/` 下 58 个转写文件，由 msime `crates/dict-builder/src/hkcancor.rs` 统计成两字及以上汉字词的词频，只含词与次数 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)（上游 `data/LICENSE`） |
| `sources/zhuyin/tsi.csv`、`sources/zhuyin/word.csv` | [chewing/libchewing-data](https://github.com/chewing/libchewing-data)，提交 `c44e81aef24b06f1509f19e1be54c99812d0c43f` 的 `dict/chewing/tsi.csv`、`dict/chewing/word.csv` | [LGPL-2.1-or-later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html) |
| `sources/zhuyin/mcbopomofo-supplement.txt` | [openvanilla/McBopomofo](https://github.com/openvanilla/McBopomofo)，提交 `be6564acad6c4d3265c34a2e1a872d80f9db6068` 的 `Source/Data/BPMFMappings.txt`，转换为本仓 CSV 格式并排除 `tsi.csv` 已有组合 | BSD（上游说明多字词表源自 BSD 授权的 libtabe，并含修改） |
| `sources/zhuyin/phrase.occ` | [openvanilla/McBopomofo](https://github.com/openvanilla/McBopomofo)，提交 `be6564acad6c4d3265c34a2e1a872d80f9db6068` 的 `Source/Data/phrase.occ` | [MIT](https://github.com/openvanilla/McBopomofo/blob/be6564acad6c4d3265c34a2e1a872d80f9db6068/LICENSE.txt) |
| `sources/stroke/stroke.dict.yaml` | [rime/rime-stroke](https://github.com/rime/rime-stroke)，提交 `1e8fff9b9494ddec23b0cbc526bcfd8171a6fd48` 的 `stroke.dict.yaml` | [LGPL-3.0](https://www.gnu.org/licenses/lgpl-3.0.html) |

这七个文件与上游固定提交逐字节一致（UTF-8、LF），没有改编码、换行或内容：

| 文件 | SHA-256 |
| --- | --- |
| `sources/cantonese/jyut6ping3.chars.dict.yaml` | `9b053a594c80eae76545bcdd83239884a49b1ba48b89ca0ab9e8daac79f33013` |
| `sources/cantonese/jyut6ping3.words.dict.yaml` | `54d174ad2bb997e4a678b7b076b84e4dc5914481b32467cdea3b43e88b7d5474` |
| `sources/cantonese/essay-cantonese.txt` | `d08836175f598219f43c2f2f9e12e12711212dbefe08d57b2eddb7a9d9f22a5d` |
| `sources/zhuyin/tsi.csv` | `c889a1ac3ae1901b3f8f62748bc41b958f010bf995f7f88dbaf9e3494f341428` |
| `sources/zhuyin/word.csv` | `da55b8e599c1389bc486453554f3410cf9c621d0ffff0ce38855698d26b3892a` |
| `sources/zhuyin/phrase.occ` | `dcd11597090b2bef88fb385bdd567e235ccd916728c84b8d0d3f8069ccfc7b8d` |
| `sources/stroke/stroke.dict.yaml` | `b3e93dce89c185f45c3d6e189b86b3a8626913352cc85e1094c786579a665791` |

rime-cantonese 由粤语计算语言学基础建设组（[CanCLID](https://github.com/CanCLID)）开发和维护，按其 README，主体部分以 CC BY 4.0 发布（上游仓库的 `LICENSE-CC-BY`），拼写是香港语言学学会（LSHK）的[粤拼](https://www.lshk.org/jyutping)方案。上游另有按 ODbL 1.0 发布的 `jyut6ping3.maps.dict.yaml`，以及 `jyut6ping3.phrase.dict.yaml`、`jyut6ping3.lettered.dict.yaml`，这三个文件不收入本仓。上游默认分支是 `main`：`.github/workflows/fetch-upstream.yml` 每周把 [CanCLID/rime-cantonese-upstream](https://github.com/CanCLID/rime-cantonese-upstream) 的数据重建后推到 `main`，`release.yml` 从 `main` 打包并把 `latest` 标签移到 `main` 的最新提交；`master` 分支只有 2024-12-01 前的自动部署提交（“Deploying to master from @ rime/rime-cantonese@…”），之后不再更新，所以本仓改按 `main` 锁定。两个分支的 `LICENSE-CC-BY` 相同。

HKCanCor 是陆镜光（Luke Kang Kwong）整理的 1997–1998 年香港粤语对话与电台节目转写，按上游 `README.md` 与 `data/README`、`data/LICENSE` 以 CC BY 4.0 发布，要求引用：K. K. Luke and May L. Y. Wong (2015) The Hong Kong Cantonese Corpus: Design and Uses. Journal of Chinese Linguistics Monograph Series, 25, 312–333。本仓只收由它统计出的词频表 `sources/cantonese/hkcancor-word-counts.txt`，不收语料文本；转写文件由 msime 锁文件直接按上游提交固定。粤拼词库只用它给 `essay-cantonese.txt` 没收的词加权，换算方法见 msime `crates/dict-builder/src/cantonese.rs`。

McBopomofo 的 `phrase.occ` 是该项目在自己语料上统计的词语出现次数（上游 `Source/Data/README.md` 与 `AGENTS.md` 称之为 phrase frequency/occurrence data，`textpool.rc` 记着语料路径，语料本身不公开）；上游没有为数据单独声明许可，仓库根目录 `LICENSE.txt` 与 `README.markdown`“軟體授權”一节说明整个项目以 MIT 发布，Copyright (c) 2011-2026 Mengjuei Hsieh et al.。注音词库只用它给 `tsi.csv` 在任何读音下都没计数的词语加权。上游文档写它用 tab 分隔，实际文件用空格分隔，构建器两种都接受。

libchewing-data 的两个文件在文件头声明 `dc:rights,Copyright (c) 2025 libchewing Core Team` 与 `dc:license,LGPL-2.1-or-later`；上游仓库没有单独的许可证文件，许可以文件头为准。

rime-stroke 的上游仓库以 LGPL-3.0 发布（`LICENSE`）。`AUTHORS` 列出的作者是四季的風、雪齋、Kunki Chou 与宋天，并写明前三位的数据是依 CNS11643 全字库的授权声明（http://www.cns11643.gov.tw/AIDB/copyright.do）以 LGPL 再分发的。CNS11643 全字库网站以《政府資料開放授權條款－第1版》授权（见其[全字库授权](https://www.cns11643.gov.tw/pageView.jsp?ID=59)页），要求利用其资料时注明来源：數位發展部，CNS11643中文標準交換碼全字庫網站，https://www.cns11643.gov.tw 。按 `stroke.dict.yaml` 的文件头：主码表源自 CNS11643 中文标准交换码全字库网站（http://www.cns11643.gov.tw），由 Kunki Chou 整理；附码表源自北大中文论坛，由孙海峰、徐孟罗、唐捺之、谢振斌整理；至扩展 J 区的超集扩充数据来自宋天；Rime 输入方案由四季的風、雪齋、Kunki Chou 制作。

msime 用 `msime-dict-build languages` 把它们构建成 `msime-cantonese.db`、`msime-zhuyin.db`、`msime-stroke.db`，与桌面词库一起放在本仓库的 `dict-v*` Release；随产物分发的署名、改动说明与许可证全文在 msime 的 `resources/licenses/rime-cantonese-CC-BY-4.0.txt`（同时署名 HKCanCor）、`resources/licenses/libchewing-data-LGPL-2.1.txt`（同时收 McBopomofo 的 MIT 声明）、`resources/licenses/rime-stroke-LGPL-3.0.txt`，换上游提交时这些文件要一起改。`msime-stroke.db` 的排序权重取自 `sources/pinyin/single-chars.txt`。

## 日文与韩文词库

| 文件 | 上游 | 上游许可 |
| --- | --- | --- |
| `sources/japanese/dictionary00.txt` … `dictionary09.txt`、`sources/japanese/id.def`、`sources/japanese/connection_single_column.txt`、`sources/japanese/README.txt` | [google/mozc](https://github.com/google/mozc)，提交 `9fbd649bea4c5e99cd8ad5e487213b26a953a376` 的 `src/data/dictionary_oss/` 文件 | Mozc 仓库根目录 `LICENSE`：署名 Google Inc. 的三条款 BSD 文本适用于整个仓库，`src/data/dictionary*` 另附 IPAdic、ICOT 与冲绳辞书条款；后者与随附的 `README.txt` 所列条款相同 |
| `sources/japanese/aux_dictionary.tsv`、`sources/japanese/dictionary_filter.tsv`、`sources/japanese/places.tsv`、`sources/japanese/words.tsv` | [google/mozc](https://github.com/google/mozc)，同一提交 `9fbd649bea4c5e99cd8ad5e487213b26a953a376` 的 `src/data/dictionary_oss/aux_dictionary.tsv`、`src/data/dictionary_oss/dictionary_filter.tsv`、`src/data/dictionary_manual/places.tsv`、`src/data/dictionary_manual/words.tsv` | 与上一行相同：两份目录都在 `src/data/dictionary*` 之下 |
| `sources/japanese/LICENSE` | [google/mozc](https://github.com/google/mozc)，同一提交 `9fbd649bea4c5e99cd8ad5e487213b26a953a376` 的仓库根目录 `LICENSE`（git blob `15ef0f074d90c3856c3202a9ab1a8a349ae57570`） | 即上面两行所适用的许可文本本身 |
| `sources/korean/hanja.txt` | [libhangul/libhangul](https://github.com/libhangul/libhangul)，提交 `717409ce61524bb3d8426060a384822f21354c62` 的 `data/hanja/hanja.txt` | BSD-3-Clause |

`sources/japanese/` 与 `sources/korean/hanja.txt` 均逐字节保留上游文件。`msime-dict-build` 从 `sources/japanese/` 构建 `msime-japanese.dat`，并按 Mozc OSS 构建组装系统词典的方式使用后加的四个文件：`dictionary_filter.tsv` 从基础词库中删去匹配的行（`gen_filtered_dictionary.py`），`aux_dictionary.tsv`、`places.tsv`、`words.tsv` 生成补充词条（`gen_aux_dictionary.py`），`places.tsv` 与 `words.tsv` 来自 Mozc 的 `src/data/dictionary_manual/` 目录，保留上游文件名；从 `sources/korean/hanja.txt` 生成引擎内嵌的韩文 Hanja 表；日文词库发布时必须同时分发 `sources/japanese/README.txt`（附件名 `msime-mozc_dictionary_oss_README.txt`）与 `sources/japanese/LICENSE`：Google 三条款 BSD 文本要求的版权声明与免责声明不在这份 README 里，所以 Mozc 根目录的 `LICENSE` 逐字节收为 `sources/japanese/LICENSE`，作为 `msime-mozc_LICENSE.txt` 与 `msime-japanese.dat` 一起附在 `dict-v` 发布上；韩文数据的 BSD-3-Clause 文本见 msime 的 `resources/licenses/libhangul-hanja-BSD-3-Clause.txt`。更新任一上游提交时，需同步更新 msime 的锁文件、构建器路径和对应的许可证说明。

## 下游影响

发布构建的拼音词库 `msime-pinyin.db` 由 `sources/pinyin/single-chars.txt`、`sources/pinyin/rime-ice.txt`、`sources/pinyin/rime-ice-supplement.txt`、`sources/pinyin/places.txt` 与 `custom/words.txt` 构建，另含 msime 仓库自带的 `resources/dictionary-sources/mix/quick_phrases.txt` 快捷短语；`sources/unlicensed/custom-pinyin-dictionary-part1.txt`、`sources/unlicensed/custom-pinyin-dictionary-part2.txt`（含 CustomPinyinDictionary 的内容）不进入发布构建，见下方「发布构建不包含这些条目」。只有用 `--include-unlicensed` 做的本地完整构建才会读入这两份。中文数据主体来自 rime-ice（GPL-3.0），使用该数据库的前端本身以 GPL-3.0 分发，与 rime-ice 兼容，但**必须保留对 rime-ice 的署名**。

词库由 [msime](https://github.com/metasequoiaime/msime) 的 Rust 构建器 `crates/dict-builder`（`msime-dict-build`）构建并以本仓库的 `dict-v*` release 发布（数据库按 `msime-<内容>` 命名），随产物送到用户手上的署名在 msime 的 `resources/licenses/` 与 [MSIME-Windows](https://github.com/metasequoiaime/MSIME-Windows) 的 `THIRD_PARTY_NOTICES.txt` 里。改动本文件的来源表时，这些文件要一起改。

## 待解决

以下部分目前没有明确的再分发授权，需要与上游作者确认后才能补上：

- [wuhgit/CustomPinyinDictionary](https://github.com/wuhgit/CustomPinyinDictionary) 是 `sources/unlicensed/custom-pinyin-dictionary-part1.txt`、`sources/unlicensed/custom-pinyin-dictionary-part2.txt` 的主体。上游在 2026-09-30 的提交 `cf17f96af885cb818c2fad87184f383a52482351`（“Add License”）加入了 CC-BY-SA-4.0 许可，但本仓用的 `2023-09-28(No.82)` 快照早于这次加许可，许可是否覆盖这份快照没有确认，所以仍按未声明许可处理，继续排除在发布构建之外。
- `sources/unlicensed/single-char-whitelist.txt` 的来源没有记录。完整构建用它过滤单字条目，所以需要补上来源；在补上之前不要假定它可以再分发。
- `sources/unlicensed/oaldpe-words.txt` 提取自商业词典。词典本体曾以 `en/oaldpe.mdx` 放在本仓中，现已移除——构建只需要提取好的词形列表，不需要词典本体。提取脚本 `makecikudb/englishdb/extract_oaldpe_headwords.py` 已随旧的 Python 构建流程删除，需要时从 git 历史取回，自备 `.mdx` 作为参数运行。**注意移除只影响当前版本，词典本体仍留在 git 历史中。**改写历史会让所有 fork、clone 以及下游锁定的 commit 全部失效，因此暂不改写；是否改写单独决策。

### 发布构建不包含这些条目

上面这些条目**默认不进入构建产物**。判定写在 msime 的 `crates/dict-builder/src/licensing.rs` 里，`msime-dict-build` 每次运行都会打印它排除了什么、为什么排除、以及换用了什么替代输入：

| 排除的输入 | 替代 | 后果 |
| --- | --- | --- |
| `sources/unlicensed/custom-pinyin-dictionary-part1.txt`、`sources/unlicensed/custom-pinyin-dictionary-part2.txt` | `sources/pinyin/rime-ice.txt`（rime-ice，GPL-3.0） | 中文词库召回下降；rime-ice 是合并前的子集，构建不会失败 |
| `sources/unlicensed/single-char-whitelist.txt` | 无 | 不做过滤，`single-chars.txt` 里的单字全部收入 |
| `sources/unlicensed/oaldpe-words.txt` | 无 | 英文词表来自 `rime-ice-en.txt`、`sources/english/rime-ice-en-supplement.txt`、`sources/english/scowl-words.txt` 与 `custom/english.txt`，`sources/english/google-word-counts.txt` 提供词频 |

想构建完整词库（本地开发、评估召回率）用 `--include-unlicensed`，或设环境变量 `MSIME_DICT_INCLUDE_UNLICENSED=1`。**这样构建出来的产物不要附到 release 上。**

拿到上游的书面再分发许可之后，把对应条目从 `licensing.rs` 的 `UNLICENSED_INPUTS` 里移出，并在同一次改动里更新本文件。

### 上游状态与已知数据问题

以下各项不涉及再分发授权，记录在这里供更新上游或重新生成补充表时处理：

- [chewing/libchewing-data](https://github.com/chewing/libchewing-data) 的 GitHub 仓库已归档，仓库描述是 “Migrated to Codeberg”。`sources/zhuyin/tsi.csv`、`sources/zhuyin/word.csv` 仍按上面记录的 GitHub 提交锁定；Codeberg 上是否有更新的数据没有核实，换上游地址前要先核对。
- `sources/pinyin/rime-ice-supplement.txt` 生成时只排除了 `rime-ice.txt` 已有的同词同音行，没有对照 `sources/pinyin/single-chars.txt`：它的 8757 行单字中有 8740 对（字,拼音）与 `single-chars.txt` 重合，其中 725 对权重不同。msime 构建器把拼音词表逐行直接插入、不去重，这些单字在 `msime-pinyin.db` 里会出现两行。对候选排序的影响没有在引擎里测过。
- `sources/pinyin/rime-ice-supplement.txt` 沿用了 rime-ice `base.dict.yaml` 的容错读音，权重与正读相同，例如 `血型 xie'xing 94145`（正读 `血型 xue'xing 94145` 在 `sources/pinyin/rime-ice.txt`）。这是上游的行为，不是转换错误；是否在补充表里排除容错读音尚未决定。
- 发布拼音输入里有一批多音字读错的词条，例如「重」在“再次”“层”义下读 chong、「调」在“调整”义下读 tiao、「行」在“行列”“行业”义下读 hang，却被标成 zhong、diao、xing。错行留在按字节锁定的文件里不改，由 msime 构建器在构建时删除：清单在 msime 仓库的 `resources/dictionary-sources/pinyin-reading-corrections.txt`（每行 `词<TAB>错读<TAB>正读`），`msime-dict-build` 的 `reading-corrections` 阶段在全部拼音输入（含 `custom/words.txt`）并入之后删除每一条错读的全部行；某条错读一行也删不到（上游已改，条目过时），或删完后这个词没有正读的行，构建都会失败。清单目前 218 条，删除 218 行，分三类：
  - 本节早先记录的 24 条：`重采样 zhong'cai'yang`、`数据去重 shu'ju'qu'zhong`、`数组去重 shu'zu'qu'zhong`、`函数重载 han'shu'zhong'zai`、`可重入 ke'zhong'ru`、`可重入函数 ke'zhong'ru'han'shu`、`重入锁 zhong'ru'suo`、`重放攻击 zhong'fang'gong'ji`、`重签名 zhong'qian'ming`、`重编程 zhong'bian'cheng`、`重定时 zhong'ding'shi`、`末端重复 mo'duan'zhong'fu`、`重复精度高 zhong'fu'jing'du'gao`、`二十万军重入赣 er'shi'wan'jun'zhong'ru'gan`、`盛年不重来 sheng'nian'bu'zhong'lai`、`只缘妖雾又重来 zhi'yuan'yao'wu'you'zhong'lai`、`反调试 fan'diao'shi`（这 17 条的正读已在 `custom/words.txt` 末尾按错行权重补上），以及正读已在 `rime-ice-supplement.txt` 的 `调参 diao'can`、`调参侠`、`性能调优`、`数据库调优`、`重绘 zhong'hui`、`自动重连 zi'dong'zhong'lian`，和 `调优 diao'you`（10687，删除后正读 `调优 tiao'you` 9999 是这个词唯一的读音）。错行都在 `sources/pinyin/rime-ice.txt`。
  - rime-ice 自己改过读音的 182 条：错行在 `sources/pinyin/rime-ice.txt`，而 rime-ice 提交 `3aea6d3694fb3d94ec663641f021f788822897ad` 的 `cn_dicts/` 已没有这个读音、改收正读，正读随 `rime-ice-supplement.txt` 进入构建。只收按词义能判定的，例如 `重铬酸盐`、`重氮盐`、`重睑`、`重唇鱼` 的“重”读 chong，`重载列车`、`重钢结构`、`重装战士` 的“重”读 zhong，股价的 `回调`、`内调外养` 的“调”读 tiao，`行纪`、`首行缩进`、`太行路` 的“行”读 hang，`进行测量`、`时行感冒` 的“行”读 xing，`不长眼`、`徒长枝`、`长姐如母` 的“长”读 zhang，`三短一长`、`长上影线` 的“长”读 chang，`处理不了`、`上得了台面`、`了不了解吗` 的“了”读 liao。
  - 所有输入（包括 rime-ice `3aea6d3`）都只有错读的 12 条：`何日更重游`、`弃妾已去难重回`、`飞镜又重磨`、`两重心字罗衣`、`九重泉底龙知无`、`重楼翠阜出霜晓`（“重”读 chong），`行内元素`、`代码行数`、`单行注释`、`用品行业`、`文旅行业`、`直销行业服务网点设立管理办法`（“行”读 hang）。正读按错行的权重追加在 `custom/words.txt` 末尾。
  - 有歧义、没有处理的：`重设计 zhong'she'ji`（“重新设计”读 chong，“重视设计”读 zhong）、`重建设 zhong'jian'she`（同理）、`判重了 pan'zhong'le`（`rime-ice-supplement.txt`，“查重判定”读 chong，“判得重了”读 zhong）、`重配置 zhong'pei'zhi`、`重载版`、`重装上阵`、`重装秘术`、`霸者重装`、`重上君子堂`、`重鉴`；编程里的“回调”读 diao，所以 `出现回调`、`回调后`、`回调时`、`回调结束`、`快速回调` 两读都留着；`调侃儿 diao'kan'er`（《现代汉语词典》“说行话”义读 diào）、`改调解张`；`林花谢了春红`、`姓了`、`足了十人`；`全行`（“全银行”读 hang）、`修行业`；`增长睫毛`、`长恶不悛`、`长子线`、`张家长`（「张家长李家短」读 chang，「张＋家长」读 zhang；整句 `张家长李家短` 的错读已删除）、`甲长`（保甲的“甲长”读 zhang，龟鳖、甲壳类的“甲长”指背甲长度，读 chang）、`更无长物`（“长物”读 zhàng，rime-ice 新版改成的 chang 也不对）。人名、地名和品牌的读音无法从词义判定，也没有处理：`王行华`、`李时行`、`小西行长`、`徐行镇`、`刘行镇`、`曹行镇`、`高行中学`、`木村了`、`冯了性药酒`、`路学长`、`保长对应`、`快乐长门人`、`重野秀一`。`电子调速微型异步电动机通用技术条件`、`虢州岑二十七长史参三十韵` 两条错读只在 `rime-ice.txt` 里、不在 `--include-unlicensed` 构建换用的 `sources/unlicensed/custom-pinyin-dictionary-part1.txt`、`custom-pinyin-dictionary-part2.txt` 里，放进清单会让那种构建失败，权重都是 1，没有收。
  - 两读都对、不算错误的：单独的 `重载`（“再次加载”读 chong，“重载荷”读 zhong）、`调配`（调色调配读 tiao，人员调配读 diao）。

## 本项目自建部分

`custom/` 下的自定义词条、候选窗翻译覆盖、英文词条与人名，`packs/` 下的专业词库，以及 `scripts/validate_packs.py` 由本项目编写，依据 GPL-3.0 提供，与组织内其他仓库一致。
