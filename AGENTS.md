# AGENTS.md — msime-dictionary

组织级约定和跨仓边界以 [组织 AGENTS.md](https://github.com/metasequoiaime/.github/blob/main/AGENTS.md) 为准。本文件补充本仓的数据与验证规则。

本仓只放词库源数据，分三个顶层目录：`sources/` 是构建器经 msime 锁文件读取的全部输入，按输入方案分子目录（`sources/pinyin/`、`sources/wubi/`、`sources/english/` 是拼音、五笔与英文的基础词库，`sources/cantonese/`、`sources/zhuyin/`、`sources/stroke/`、`sources/japanese/`、`sources/korean/` 是粤拼、注音、笔画、日文与韩文方案的词库，`sources/unlicensed/` 是没有再分发授权、发布构建不使用的文件）；`custom/` 是人工维护数据，也是唯一接受投稿的目录；`packs/` 是用户按需导入的专业词库，不进入构建。构建器在 msime 仓库的 `crates/dict-builder`（`msime-dict-build`），它按 msime `resources/dictionary-sources.lock.json` 锁定的本仓提交，从 `raw.githubusercontent.com/metasequoiaime/msime-dictionary/<提交>/<路径>` 读取每个文件，并校验锁文件记下的大小与 SHA-256。`sources/cantonese/`、`sources/zhuyin/`、`sources/stroke/` 由 `languages` 子命令构建成 `msime-cantonese.db`、`msime-zhuyin.db`、`msime-stroke.db`；`sources/japanese/` 由主构建生成 `msime-japanese.dat`；`sources/korean/hanja.txt` 由 `hanja` 子命令生成 msime 源码里引擎内嵌的 `crates/engine/src/korean/hanja.tsv`，不是 Release 附件。构建产物由本仓 `.github/workflows/release-built-dictionaries.yml` 手动触发，发布为 `dict-vX.Y.Z` Release；已发布的版本不可修改。发版的完整步骤（包括去 msime 更新锁文件）写在 `README.md`，本文件只列约束。不要把构建脚本、生成器、生成的数据库或其他产物加回本仓。

上面的按提交读取目前只在尚未合入的 msime PR #3513 上实现，合入前的发版参数见 `README.md` 发布一节的过渡说明。

## 文件是逐字节锁定的

下游按提交和 SHA-256 锁定每个文件，所以：

- 不做全量格式化，不转换编码或换行符，不排序、不去重、不补结尾换行。`sources/pinyin/`、`sources/wubi/`、`sources/english/`、`sources/unlicensed/` 下有 CRLF 文件，`sources/wubi/wubi98.txt` 是 UTF-16LE；`sources/japanese/`、`sources/korean/` 等上游原样文件也按字节锁定，`.gitattributes` 的 `* -text` 让 Git 原样保存；不要删掉它，也不要在本地用 `core.autocrlf` 之类的设置绕过。
- 路径就是契约。msime 按提交锁定本仓文件，锁定旧提交的构建不受本仓改名或移动影响；但 msime 下次把锁文件升级到新提交时，必须同时改锁文件里的路径和构建器里的常量。所以改名或移动文件时，先备好 msime 那边的 PR（构建器与测试改动，锁文件先指向本仓 PR 分支上的提交验证），本仓合入后再把锁文件改指 `main` 上的合入提交，两边 PR 互相链接。`custom/` 与 `packs/` 不要移动：msime-web 和 msime-cloud 不经锁文件，直接按 `main` 读写这两个目录。

## 自定义词条

- `custom/words.txt`、`custom/translations.txt`、`custom/english.txt` **只追加**：新行写在文件末尾，不修改、删除或重排已有的行。check-words 会拒绝任何非追加的改动。
- `custom/words.txt` 的格式是 `词<TAB>全拼<TAB>权重`，全拼音节用 `'` 分隔；另外两个文件的格式见 `README.md`。词语和英文的权重落在所在文件现有的范围内；不要为了让一个词靠前填一个极大值。
- 候选窗翻译的修正写到 `custom/translations.txt`，不改 ECDICT。

## 基础词库

`sources/pinyin/`、`sources/wubi/`、`sources/english/`、`sources/cantonese/`、`sources/zhuyin/`、`sources/stroke/`、`sources/japanese/`、`sources/korean/`、`sources/unlicensed/` 下的数据来自第三方（见 `NOTICE.md`）。其中一部分是本项目从固定上游提交生成的补充表（`sources/pinyin/rime-ice-supplement.txt`、`sources/pinyin/places.txt`、`sources/english/rime-ice-en-supplement.txt`、`sources/zhuyin/mcbopomofo-supplement.txt`），不是上游原样文件。不直接编辑上游原表或在其中加新词；经固定上游提交生成的补充表可以作为独立文件加入（规则见下一节），并且：

- 提交说明写清修了什么、依据是什么（上游提交、对照数据或复现方式）；
- 来源或许可有变化时同一次改动更新 `NOTICE.md`；
- 新增的第三方数据先确认再分发许可并写进 `NOTICE.md`，没有明确许可的数据会被 msime 构建器的 `licensing.rs` 挡在发布产物之外，要在那里同步登记。

## 补充表

- 新文件命名为 `sources/<方案>/<来源>-<内容>.txt`，全部小写、用连字符分隔，名字说明数据从哪来、是什么，例如 `sources/english/rime-ice-en-supplement.txt`、`sources/zhuyin/mcbopomofo-supplement.txt`；来源就是内容时可以只写一段，如 `sources/pinyin/places.txt`。不带 `V<N>` 之类的版本后缀：内容由 msime 锁文件里的 SHA-256 固定，文件名不需要表达版本。`sources/cantonese/`、`sources/zhuyin/tsi.csv` 与 `sources/zhuyin/word.csv`、`sources/stroke/`、`sources/japanese/`、`sources/korean/` 下的上游原样文件保留上游文件名，不套用这条规则；上游原样文件的名字不是 ASCII 或会和别的文件同名时（如 `sources/wubi/wubi98.txt`、`sources/wubi/wubi98-fcitx.txt`），改用 `<来源>-<内容>` 形式的名字，并在 `NOTICE.md` 里写明上游的原文件名。
- 文件头用 `#` 注释写明：上游仓库与提交；生成命令及其所在的 msime 提交；去重规则，并写全对照集合（排除了哪些文件里已有的哪种组合）。msime 构建器把拼音词表逐行直接插入，不去重，没写进对照集合的文件里的重复行会原样进入产物。
- 换到新的上游提交或改了生成规则时，用同一个生成器在原路径整份重新生成，不另起新文件名；行格式变了也在原路径重新生成，同时改 msime 读取它的构建阶段。
- 生成器放在 msime 的 `crates/dict-builder`，不放本仓；补充表不手工编辑。`sources/pinyin/places.txt` 的生成器是 msime `crates/dict-builder/src/places_supplement.rs`（`msime-dict-build places-supplement`）；现有的 `sources/pinyin/rime-ice-supplement.txt`、`sources/english/rime-ice-en-supplement.txt`、`sources/zhuyin/mcbopomofo-supplement.txt` 在 msime 里只有读取它们的代码，没有生成器，要重新生成时先把生成器补进 dict-builder。
- 同一次改动更新本仓 `NOTICE.md`；msime 那边同步改锁文件、读取它的构建阶段和 `resources/licenses/` 下的许可证说明。两边 PR 互相链接，下游没有跟上之前不要合入。

## 粤拼、注音、笔画、日文与韩文词库

`sources/cantonese/` 是 [rime/rime-cantonese](https://github.com/rime/rime-cantonese) 的 `jyut6ping3.chars.dict.yaml`、`jyut6ping3.words.dict.yaml`、`essay-cantonese.txt`，`sources/zhuyin/tsi.csv`、`sources/zhuyin/word.csv` 是 [chewing/libchewing-data](https://github.com/chewing/libchewing-data) 的原样文件，`sources/zhuyin/mcbopomofo-supplement.txt` 是 [openvanilla/McBopomofo](https://github.com/openvanilla/McBopomofo) 的固定补充源转换文件，`sources/stroke/` 是 [rime/rime-stroke](https://github.com/rime/rime-stroke) 的 `stroke.dict.yaml`，`sources/japanese/` 是 [google/mozc](https://github.com/google/mozc) 的 OSS 日文词库文件，`sources/korean/` 是 [libhangul/libhangul](https://github.com/libhangul/libhangul) 的 `hanja.txt`，来源和许可见 `NOTICE.md`。

- 不在本仓修改这些文件，也不加词；错误报给上游。`sources/zhuyin/mcbopomofo-supplement.txt` 是本项目转换出的补充表，按上一节的规则重新生成，同样不手工改。
- 更新时把整份文件换成上游新提交的版本，同一次改动更新 `NOTICE.md` 里的提交；msime 那边要同步改锁文件里的对应上游引用和 `resources/licenses/` 下对应许可证文件写明的提交，并在 PR 里互相链接。

## 验证

```sh
python3 scripts/validate_packs.py
```

它检查专业词库的格式与读音（对照 `sources/pinyin/single-chars.txt` 和 `sources/pinyin/rime-ice-supplement.txt` 的单字行）、与发布用拼音输入的重复项、翻译覆盖率，以及 `custom/translations.txt` 的格式；完整检查项见 `README.md` 专业词库一节和 `packs/README.md` 的验收清单。这三个文件的追加规则由 check-words workflow 用固定版本的 `msime-dict-build check-words` 检查，需要 Rust 工具链，本地一般不跑。

## 隐私

示例数据不得使用真实可拨的手机号、真实地址或真实人名，即便只是 mock。手机号用 `13800000000` 这类保留号段，地址用明显虚构串。这条来自 MSIME-Windows#74。

## 提交

只暂存本次改动的显式路径，不用 `git add -A` / `git add .`。提交信息用 `type(scope): 摘要`。合并 Pull Request 用 squash，标题同样写成 `type(scope): 摘要`（词条用 `feat(custom): …`，修正用 `fix(...)`），便于追踪源数据变更。不要添加 `Co-Authored-By`、`Generated with` 或其他 AI 生成标记。
