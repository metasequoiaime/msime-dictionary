# 水杉输入法词库

水杉输入法词库的源数据只在这个仓库维护：拼音、五笔与英文的基础词库，人工维护的自定义词条和候选窗翻译，以及用户按需导入的专业词库。这里只放文本数据，不放构建脚本；词库由 [msime](https://github.com/metasequoiaime/msime) 的构建器按固定提交取用这里的文件，构建成各平台共用的 `dict-v*` 词库发布。

## 目录

```
cn/          中文基础词库：全拼词条、单字、五笔 86、单字白名单
en/          英文基础词库：候选词表、词频、词形列表
custom/      人工维护的自定义数据
  words.txt          中文词条，并入全拼词表
  translations.txt   候选窗翻译覆盖
  english.txt        英文词条（目前没有构建读取）
  names.txt          人名（目前没有构建读取）
packs/       用户按需导入的专业词库，不进入默认词库
scripts/     维护脚本
```

## 格式

所有文件都是 UTF-8 文本。字段大多用制表符分隔，`en/BaseDictIceEn.txt` 用空格分隔；`cn/BaseDictIceV1.txt` 与 `cn/SingleCharsAllV1.txt` 开头有 `#` 注释行。`cn/` 与 `en/` 下的部分文件使用 CRLF 换行，下游按 SHA-256 锁定每个文件，所以**不要转换换行符或重新排版**，仓库的 `.gitattributes` 已关闭换行转换。

| 文件 | 每行 | 说明 |
| --- | --- | --- |
| `cn/BaseDictIceV1.txt` | `词<TAB>全拼<TAB>权重` | 雾凇拼音（rime-ice）的短语词库，经本项目修正 |
| `cn/BaseDictAllV1Part1.txt`、`cn/BaseDictAllV1Part2.txt` | `词<TAB>全拼<TAB>权重` | CustomPinyinDictionary 与雾凇合并去重后的全量词库，因 GitHub 单文件大小限制拆成两部分 |
| `cn/SingleCharsAllV1.txt` | `字<TAB>全拼<TAB>权重` | 雾凇的 8105 个常用字，补充 Unicode 中其余较常见的字，读音以 pinyin-data 校正 |
| `cn/Wubi86.txt` | `词<TAB>五笔编码<TAB>权重` | 86 版五笔，来自 rime-wubi86-jidian |
| `cn/SingleCharWhitelist.txt` | 一个字 | 完整构建时用来过滤单字条目 |
| `en/BaseDictIceEn.txt` | `编码 显示词` | 雾凇的英文词库 |
| `en/google_count_1_w.txt` | `词<TAB>次数` | Google 1/3 million 英文词频 |
| `en/oaldpe_words.txt` | 一个词形 | 从 oaldpe.mdx 提取的词形列表 |
| `custom/words.txt` | `词<TAB>全拼<TAB>权重` | 全拼音节用 `'` 分隔，如 `未来可期	wei'lai'ke'qi	5000`。已有同词同拼音时只会调高权重 |
| `custom/translations.txt` | `源词<TAB>译文` | 优先于 ECDICT；源词含汉字为中译英，否则为英译中；`#` 开头为注释，同一源词后写覆盖先写 |
| `custom/english.txt` | `编码<TAB>显示词<TAB>权重` | |
| `custom/names.txt` | 一个人名 | |

`cn/`、`en/` 下各文件的上游、许可与已知问题见 [NOTICE.md](NOTICE.md)。

## 贡献

- **官网提交**：在 [msime.app](https://msime.app) 的词条提交页填写，条目会追加到本仓库一个滚动的 Pull Request。
- **直接提 Pull Request**：往 `custom/words.txt` 末尾追加行即可，不要改动、删除或重排已有的行。

**权重只升不降**：词条已经在基础词库里而且权重更高时保留基础词库的值。`custom/words.txt` 里的历史条目大多写着占位的 `1`。需要让一个词在整句里胜出，就把权重写到同量级的真实词附近（`扛不住` 是 2430，`客气` 是 75460），不要凭感觉填一个极大值。

每个改动 `custom/words.txt` 的 Pull Request 都会由 CI 用词库构建器的同一套规则检查：只能追加、格式与拼音合法、权重在现有范围内、不与本次改动、现有词表或已发布词库重复。结果以评论写在 Pull Request 里。维护者再人工审核内容（包括敏感词）后合入。

候选窗翻译的修正写到 `custom/translations.txt`，不要去改 ECDICT。`cn/`、`en/` 下的基础词库来自第三方，不在里面加新词；只有确认的错误才修改，并在提交说明里写清依据。

## 怎样进入输入法

1. 改动合入本仓库。
2. 本仓发布 `sources-vX.Y.Z` 版本：release-please 按合入的 conventional commits 维护一个发版 Pull Request，合并它就会打标签，把 `cn/`、`en/`、`custom/` 下的每个文件和 `SHA256SUMS.txt` 作为附件上传并发布。已发布的版本不再修改，数据有误就发新版本。
3. msime 在 `resources/dictionary-sources.lock.json` 里把引用升到新版本的附件（每个文件的 URL、大小与 SHA-256 一起更新），用 `msime-dict-build` 构建并发布 `dict-v*` 词库。
4. 各平台升级各自锁定的词库版本，下一个版本随之带上新词库。

只合入本仓库而不走完后面几步，用户拿到的仍是旧词库。发版依据提交标题：合并词条 Pull Request 时用 squash，并把标题写成 `feat(words): …`（修正写成 `fix(...)`），否则 release-please 不会为它发版。

## 专业词库

| 词库 | 内容 |
| --- | --- |
| [`packs/unreal_houdini`](packs/unreal_houdini) | Unreal Engine、Houdini 和 Houdini Engine for Unreal |

专业词库不会进入所有人的候选列表，用户在设置里导入后才作为用户词条生效，所以垂直领域的短缩写（`SOP`、`TOP`、`PCG`）不会干扰普通输入。检查格式、拼音、重复项和翻译覆盖率（拼音与重复项对照 `cn/` 下的基础词库）：

```sh
python3 scripts/validate_packs.py
```

## 历史

- 本仓库最初名为 MSIME-Dict（现为 msime-dictionary，旧名称会自动重定向），保存词库源数据和 Python 构建脚本，自定义词条在独立的 MSIME-CustomDict（后改名 msime-customdict）中，以子模块引入。
- 2026-09-05，词库源数据和构建脚本并入 MSIME-Engine 的 `dictionary/`，自定义词条也并入其 `dictionary/custom/`，本仓库停止维护。
- MSIME-Engine 被 msime 的 Rust 引擎和构建器取代后，词库源数据于 2026-09-30 回到这里，同时并入 msime-customdict，本仓库成为唯一的词库源数据仓库。回迁是直接复制文件内容，没有导入历史：`cn/`、`en/` 取自 msime-engine [`e92a9c7c64e262f30218ca9aaad5f40d0b18cf89`](https://github.com/metasequoiaime/msime-engine/tree/e92a9c7c64e262f30218ca9aaad5f40d0b18cf89/dictionary) 的 `dictionary/`，`custom/`、`packs/`、`scripts/validate_packs.py` 取自 msime-customdict [`b075c8e3e71ab48b3c048c229289275b0d42b6d0`](https://github.com/metasequoiaime/msime-customdict/tree/b075c8e3e71ab48b3c048c229289275b0d42b6d0)，两边的历史仍可在源仓库中查阅（msime-engine 已归档，msime-customdict 在下游切换到本仓库后归档）。Python 构建流程、emoji、颜文字、符号与快捷短语没有迁回，后四者现在在 msime 的 `resources/dictionary-sources/`。

## 许可

本仓库**不对外提供统一的开源许可**：其中绝大部分词库并非本项目的作品，给整个仓库挂一份 LICENSE 等于替上游作者重新授权。逐项的来源与上游条款见 [NOTICE.md](NOTICE.md)，使用或再分发前请以对应上游的条款为准。本项目自建的部分（`custom/`、`packs/`、`scripts/`）以 GPL-3.0 提供。
