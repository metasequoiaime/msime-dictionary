# 来源与授权说明

本仓库**不对外提供统一的开源许可**，因为其中绝大部分词库并非本项目的作品，而是从其他项目收集、合并、去重而来（见 [README](README.md)）。给整个仓库挂一份 LICENSE 等于替上游作者重新授权，因此这里改为逐项说明来源与上游条款。使用或再分发本仓库的数据时，请以对应上游的条款为准。

## 中文词库

| 文件 | 上游 | 上游许可 |
| --- | --- | --- |
| `cn/BaseDictIceV1.txt` | [iDvel/rime-ice](https://github.com/iDvel/rime-ice)，对照提交 `9e66b0729083b37d217312294f6d516c8d7234be`（见下） | GPL-3.0 |
| `cn/BaseDictAllV1Part1.txt`、`cn/BaseDictAllV1Part2.txt` | [wuhgit/CustomPinyinDictionary](https://github.com/wuhgit/CustomPinyinDictionary)（`2023-09-28(No.82)` 版）与 rime-ice 合并去重 | GPL-3.0 与**未声明**的混合 |
| `cn/SingleCharsAllV1.txt` | [iDvel/rime-ice](https://github.com/iDvel/rime-ice)，读音以 [mozillazg/pinyin-data](https://github.com/mozillazg/pinyin-data) 校正 | GPL-3.0 + MIT |
| `cn/Wubi86.txt` | [KyleBing/rime-wubi86-jidian](https://github.com/KyleBing/rime-wubi86-jidian) | Apache-2.0 |
| `cn/Wubi98.txt` | [yanhuacuo/98wubi-tables](https://github.com/yanhuacuo/98wubi-tables)（98五笔小组），提交 `6b8b6fb9d3c34e0d5e3b17211e1f1c100e7eb697` 的 `98五笔含词表-【单义】.txt`（见下） | Unlicense |
| `cn/SingleCharWhitelist.txt` | **待确认**，见下方「待解决」 | **待确认** |

`cn/BaseDictIceV1.txt` 的上游提交是后来补记的：此前它是唯一没有被记录提交的中文词库来源，没有办法判断树里那份是从哪个版本导出的。按 rime-ice `9e66b0729083b37d217312294f6d516c8d7234be` 比对，它的前身 `BaseDictIce.txt` 有 28185 条上游不存在的词条，另有 8328 条权重与上游不同。多出来的条目里既有上游没收的真词（地名、品牌），也有语料切分留下的碎片（例如「米高」「钟的」「之事」）。已确认的碎片在 msime-engine 的 `67fd083` 中从 `cn/BaseDictIceV1.txt` 与 `cn/BaseDictAllV1Part1.txt` 删除，本仓库的这两个文件与 msime-engine `e92a9c7c64e262f30218ca9aaad5f40d0b18cf89` 的 `dictionary/cn/` 逐字节一致。这份文件的真实来源仍然没有查清，所以不要把它描述成「原样搬运」。

`cn/Wubi98.txt` 与上游文件逐字节一致（SHA-256 `1b5a4c22eddae08d8e0e6aa8f926f92d45d6cdaa591e5cee0e8aad29271da1cc`，UTF-16LE 带 BOM、CRLF），没有改编码或换行。权利声明来自数据作者本人：上游仓库在 2024-01-20 的提交 `4dbcaa65` 加入 Unlicense，此前同一作者在 2021 年把这份表贡献给 [fcitx/fcitx5-table-extra](https://github.com/fcitx/fcitx5-table-extra)（`tables/wubi98.txt`，GPL-3.0-or-later 包内分发，Debian main 收录）。两份表 112584 条里只有 4 条不同，差异来自上游 2024-06-25 的拆分校正（`72a36bae`）。上游没有记录 GB2312/GBK 部分的单字编码与简码是怎样生成的，只能说它们依照 98 版五笔的编码规范；这里如实记下，不把它描述成独立生成。界面上称“98 五笔”，不使用“王码”“五笔字型”等商标。

## 英文词库

| 文件 | 上游 | 上游许可 |
| --- | --- | --- |
| `en/BaseDictIceEn.txt` | [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | GPL-3.0 |
| `en/google_count_1_w.txt` | [Google 1/3 million 词频表](https://www.norvig.com/ngrams/count_1w.txt) | 以来源页面说明为准 |
| `en/oaldpe_words.txt` | 自 oaldpe.mdx 提取的词形列表 | 权利归词典出版方 |

## 粤拼、注音与笔画词库

| 文件 | 上游 | 上游许可 |
| --- | --- | --- |
| `yue/jyut6ping3.chars.dict.yaml`、`yue/jyut6ping3.words.dict.yaml`、`yue/essay-cantonese.txt` | [rime/rime-cantonese](https://github.com/rime/rime-cantonese)，提交 `259f0e48bba840c3a2e0d117539e96937f3d89bc` 的同名文件 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| `tw/tsi.csv`、`tw/word.csv` | [chewing/libchewing-data](https://github.com/chewing/libchewing-data)，提交 `c44e81aef24b06f1509f19e1be54c99812d0c43f` 的 `dict/chewing/tsi.csv`、`dict/chewing/word.csv` | [LGPL-2.1-or-later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html) |
| `stroke/stroke.dict.yaml` | [rime/rime-stroke](https://github.com/rime/rime-stroke)，提交 `1e8fff9b9494ddec23b0cbc526bcfd8171a6fd48` 的 `stroke.dict.yaml` | [LGPL-3.0](https://www.gnu.org/licenses/lgpl-3.0.html) |

这六个文件与上游固定提交逐字节一致（UTF-8、LF），没有改编码、换行或内容，SHA-256 与 msime 此前直接从上游下载时锁定的值相同：

| 文件 | SHA-256 |
| --- | --- |
| `yue/jyut6ping3.chars.dict.yaml` | `9b053a594c80eae76545bcdd83239884a49b1ba48b89ca0ab9e8daac79f33013` |
| `yue/jyut6ping3.words.dict.yaml` | `54d174ad2bb997e4a678b7b076b84e4dc5914481b32467cdea3b43e88b7d5474` |
| `yue/essay-cantonese.txt` | `d08836175f598219f43c2f2f9e12e12711212dbefe08d57b2eddb7a9d9f22a5d` |
| `tw/tsi.csv` | `c889a1ac3ae1901b3f8f62748bc41b958f010bf995f7f88dbaf9e3494f341428` |
| `tw/word.csv` | `da55b8e599c1389bc486453554f3410cf9c621d0ffff0ce38855698d26b3892a` |
| `stroke/stroke.dict.yaml` | `b3e93dce89c185f45c3d6e189b86b3a8626913352cc85e1094c786579a665791` |

rime-cantonese 由粤语计算语言学基础建设组（[CanCLID](https://github.com/CanCLID)）开发和维护，按其 README，主体部分以 CC BY 4.0 发布（上游仓库的 `LICENSE-CC-BY`），拼写是香港语言学学会（LSHK）的[粤拼](https://www.lshk.org/jyutping)方案。上游另有按 ODbL 1.0 发布的 `jyut6ping3.maps.dict.yaml`，以及 `jyut6ping3.phrase.dict.yaml`、`jyut6ping3.lettered.dict.yaml`，这三个文件不收入本仓。

libchewing-data 的两个文件在文件头声明 `dc:rights,Copyright (c) 2025 libchewing Core Team` 与 `dc:license,LGPL-2.1-or-later`；上游仓库没有单独的许可证文件，许可以文件头为准。

rime-stroke 的上游仓库以 LGPL-3.0 发布（`LICENSE`）。`AUTHORS` 列出的作者是四季的風、雪齋、Kunki Chou 与宋天，并写明前三位的数据是依 CNS11643 全字库的授权声明（http://www.cns11643.gov.tw/AIDB/copyright.do）以 LGPL 再分发的。CNS11643 全字库网站以《政府資料開放授權條款－第1版》授权（见其[全字库授权](https://www.cns11643.gov.tw/pageView.jsp?ID=59)页），要求利用其资料时注明来源：數位發展部，CNS11643中文標準交換碼全字庫網站，https://www.cns11643.gov.tw 。按 `stroke.dict.yaml` 的文件头：主码表源自 CNS11643 中文标准交换码全字库网站（http://www.cns11643.gov.tw），由 Kunki Chou 整理；附码表源自北大中文论坛，由孙海峰、徐孟罗、唐捺之、谢振斌整理；至扩展 J 区的超集扩充数据来自宋天；Rime 输入方案由四季的風、雪齋、Kunki Chou 制作。

msime 用 `msime-dict-build languages` 把它们构建成 `cantonese.db`、`zhuyin.db`、`stroke.db`，以 msime 的 `langdict-v*` 发布；随产物分发的署名、改动说明与许可证全文在 msime 的 `resources/licenses/rime-cantonese-CC-BY-4.0.txt`、`resources/licenses/libchewing-data-LGPL-2.1.txt`、`resources/licenses/rime-stroke-LGPL-3.0.txt`，换上游提交时这些文件要一起改。`stroke.db` 的排序权重取自 `cn/SingleCharsAllV1.txt`。

## 下游影响

由 `cn/BaseDictAllV1Part1.txt` 与 `cn/BaseDictAllV1Part2.txt` 构建出的 `msime.db` 同时包含 rime-ice（GPL-3.0）与 CustomPinyinDictionary（未声明许可）的内容。使用该数据库的前端本身以 GPL-3.0 分发，与 rime-ice 兼容，但**必须保留对 rime-ice 的署名**。

词库由 [msime](https://github.com/metasequoiaime/msime) 的 Rust 构建器 `crates/dict-builder`（`msime-dict-build`）构建并以 `dict-v*` release 发布，随产物送到用户手上的署名在 msime 的 `resources/licenses/` 与 [MSIME-Windows](https://github.com/metasequoiaime/MSIME-Windows) 的 `THIRD_PARTY_NOTICES.txt` 里。改动本文件的来源表时，这些文件要一起改。

## 待解决

以下部分目前没有明确的再分发授权，需要与上游作者确认后才能补上：

- [wuhgit/CustomPinyinDictionary](https://github.com/wuhgit/CustomPinyinDictionary) 未声明任何许可，而它是 `cn/BaseDictAllV1Part1.txt`、`Part2.txt` 的主体。
- `cn/SingleCharWhitelist.txt` 的来源没有记录。完整构建用它过滤单字条目，所以需要补上来源；在补上之前不要假定它可以再分发。
- `en/oaldpe_words.txt` 提取自商业词典。词典本体 `en/oaldpe.mdx` 曾经也在本仓中，现已移除——构建只需要提取好的词形列表，不需要词典本体。提取脚本 `makecikudb/englishdb/extract_oaldpe_headwords.py` 已随旧的 Python 构建流程删除，需要时从 git 历史取回，自备 `.mdx` 作为参数运行。**注意移除只影响当前版本，词典本体仍留在 git 历史中。**改写历史会让所有 fork、clone 以及下游锁定的 commit 全部失效，因此暂不改写；是否改写单独决策。

### 发布构建不包含这些条目

上面这些条目**默认不进入构建产物**。判定写在 msime 的 `crates/dict-builder/src/licensing.rs` 里，`msime-dict-build` 每次运行都会打印它排除了什么、为什么排除、以及换用了什么替代输入：

| 排除的输入 | 替代 | 后果 |
| --- | --- | --- |
| `cn/BaseDictAllV1Part1.txt`、`Part2.txt` | `cn/BaseDictIceV1.txt`（rime-ice，GPL-3.0） | 中文词库召回下降；rime-ice 是合并前的子集，构建不会失败 |
| `cn/SingleCharWhitelist.txt` | 无 | 不做过滤，`SingleCharsAllV1.txt` 里的单字全部收入 |
| `en/oaldpe_words.txt` | 无 | 英文词表只来自 `BaseDictIceEn.txt` |

想构建完整词库（本地开发、评估召回率）用 `--include-unlicensed`，或设环境变量 `MSIME_DICT_INCLUDE_UNLICENSED=1`。**这样构建出来的产物不要附到 release 上。**

拿到上游的书面再分发许可之后，把对应条目从 `licensing.rs` 的 `UNLICENSED_INPUTS` 里移出，并在同一次改动里更新本文件。

## 本项目自建部分

`custom/` 下的自定义词条、候选窗翻译覆盖、英文词条与人名，`packs/` 下的专业词库，以及 `scripts/validate_packs.py` 由本项目编写，依据 GPL-3.0 提供，与组织内其他仓库一致。
