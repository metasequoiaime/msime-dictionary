# 来源与授权说明

本仓库**不对外提供统一的开源许可**，因为其中绝大部分词库并非本项目的作品，而是从其他项目收集、合并、去重而来（见 [README](README.md)）。给整个仓库挂一份 LICENSE 等于替上游作者重新授权，因此这里改为逐项说明来源与上游条款。使用或再分发本仓库的数据时，请以对应上游的条款为准。

## 中文词库

| 文件 | 上游 | 上游许可 |
| --- | --- | --- |
| `cn/BaseDictIceV1.txt` | [iDvel/rime-ice](https://github.com/iDvel/rime-ice)，对照提交 `9e66b0729083b37d217312294f6d516c8d7234be`（见下） | GPL-3.0 |
| `cn/BaseDictAllV1Part1.txt`、`cn/BaseDictAllV1Part2.txt` | [wuhgit/CustomPinyinDictionary](https://github.com/wuhgit/CustomPinyinDictionary)（`2023-09-28(No.82)` 版）与 rime-ice 合并去重 | GPL-3.0 与**未声明**的混合 |
| `cn/SingleCharsAllV1.txt` | [iDvel/rime-ice](https://github.com/iDvel/rime-ice)，读音以 [mozillazg/pinyin-data](https://github.com/mozillazg/pinyin-data) 校正 | GPL-3.0 + MIT |
| `cn/Wubi86.txt` | [KyleBing/rime-wubi86-jidian](https://github.com/KyleBing/rime-wubi86-jidian) | Apache-2.0 |
| `cn/SingleCharWhitelist.txt` | **待确认**，见下方「待解决」 | **待确认** |

`cn/BaseDictIceV1.txt` 的上游提交是后来补记的：此前它是唯一没有被记录提交的中文词库来源，没有办法判断树里那份是从哪个版本导出的。按 rime-ice `9e66b0729083b37d217312294f6d516c8d7234be` 比对，它的前身 `BaseDictIce.txt` 有 28185 条上游不存在的词条，另有 8328 条权重与上游不同。多出来的条目里既有上游没收的真词（地名、品牌），也有语料切分留下的碎片（例如「米高」「钟的」「之事」）。已确认的碎片在 msime-engine 的 `67fd083` 中从 `cn/BaseDictIceV1.txt` 与 `cn/BaseDictAllV1Part1.txt` 删除，本仓库的这两个文件与 msime-engine `e92a9c7c64e262f30218ca9aaad5f40d0b18cf89` 的 `dictionary/cn/` 逐字节一致。这份文件的真实来源仍然没有查清，所以不要把它描述成「原样搬运」。

## 英文词库

| 文件 | 上游 | 上游许可 |
| --- | --- | --- |
| `en/BaseDictIceEn.txt` | [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | GPL-3.0 |
| `en/google_count_1_w.txt` | [Google 1/3 million 词频表](https://www.norvig.com/ngrams/count_1w.txt) | 以来源页面说明为准 |
| `en/oaldpe_words.txt` | 自 oaldpe.mdx 提取的词形列表 | 权利归词典出版方 |

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
