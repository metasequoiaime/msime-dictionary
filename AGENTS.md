# AGENTS.md — msime-dictionary

组织级约定和跨仓边界以 [组织 AGENTS.md](https://github.com/metasequoiaime/.github/blob/main/AGENTS.md) 为准。本文件补充本仓的数据与验证规则。

本仓只放词库源数据：`cn/`、`en/` 下的基础词库，`yue/`、`tw/`、`stroke/`、`ja/`、`ko/` 下粤拼、注音、笔画、日文与韩文方案的上游词库，`custom/` 下的人工维护数据，`packs/` 下的专业词库。构建器仍在 msime 仓库；本仓通过 `.github/workflows/release-built-dictionaries.yml` 调用固定的 msime 提交生成并发布 `dict-vX.Y.Z`、`langdict-vX.Y.Z`，同时以 `sources-vX.Y.Z` release 发布源数据（附件是 `cn/`、`en/`、`yue/`、`tw/`、`stroke/`、`ja/`、`ko/`、`custom/` 下的文件与 `SHA256SUMS.txt`，由 `.github/workflows/release.yml` 上传），msime 的 `crates/dict-builder`（`msime-dict-build`）按 msime `resources/dictionary-sources.lock.json` 固定的版本附件下载，校验大小与 SHA-256 后构建；`yue/`、`tw/`、`stroke/`、`ja/`、`ko/` 由它构建成对应语言词库。已发布的版本不可修改。不要把构建脚本、生成的数据库或其他产物加回本仓。

## 文件是逐字节锁定的

下游按提交和 SHA-256 锁定每个文件，所以：

- 不做全量格式化，不转换编码或换行符，不排序、不去重、不补结尾换行。`cn/`、`en/` 下有 CRLF 文件；`ja/`、`ko/` 等上游原样文件也按字节锁定，`.gitattributes` 的 `* -text` 让 Git 原样保存；不要删掉它，也不要在本地用 `core.autocrlf` 之类的设置绕过。
- 路径就是契约。改名或移动文件要同时改 msime 的锁文件与构建器，并在 PR 里互相链接；下游没有跟上之前不要合入。

## 自定义词条

- `custom/words.txt`、`custom/translations.txt`、`custom/english.txt` **只追加**：新行写在文件末尾，不修改、删除或重排已有的行。check-words 会拒绝任何非追加的改动。
- 格式是 `词<TAB>全拼<TAB>权重`，全拼音节用 `'` 分隔，权重落在文件现有的范围内；不要为了让一个词靠前填一个极大值。
- 候选窗翻译的修正写到 `custom/translations.txt`，不改 ECDICT。

## 基础词库

`cn/`、`en/`、`yue/`、`tw/`、`stroke/`、`ja/`、`ko/` 下的文件来自第三方（见 `NOTICE.md`）。不直接编辑上游原表或在其中加新词；经固定上游提交生成的补充表可以作为独立文件加入，并且：

- 提交说明写清修了什么、依据是什么（上游提交、对照数据或复现方式）；
- 来源或许可有变化时同一次改动更新 `NOTICE.md`；
- 新增的第三方数据先确认再分发许可并写进 `NOTICE.md`，没有明确许可的数据会被 msime 构建器的 `licensing.rs` 挡在发布产物之外，要在那里同步登记。

## 粤拼、注音、笔画、日文与韩文词库

`yue/` 是 [rime/rime-cantonese](https://github.com/rime/rime-cantonese) 的 `jyut6ping3.chars.dict.yaml`、`jyut6ping3.words.dict.yaml`、`essay-cantonese.txt`，`tw/tsi.csv`、`tw/word.csv` 是 [chewing/libchewing-data](https://github.com/chewing/libchewing-data) 的原样文件，`tw/McBopomofoSupplement.txt` 是 [openvanilla/McBopomofo](https://github.com/openvanilla/McBopomofo) 的固定补充源转换文件，`stroke/` 是 [rime/rime-stroke](https://github.com/rime/rime-stroke) 的 `stroke.dict.yaml`，`ja/` 是 [google/mozc](https://github.com/google/mozc) 的 OSS 日文词库文件，`ko/` 是 [libhangul/libhangul](https://github.com/libhangul/libhangul) 的 `hanja.txt`，来源和许可见 `NOTICE.md`。

- 不在本仓修改这些文件，也不加词；错误报给上游。
- 更新时把整份文件换成上游新提交的版本，同一次改动更新 `NOTICE.md` 里的提交；msime 那边要同步改锁文件里的对应上游引用和 `resources/licenses/` 下对应许可证文件写明的提交，并在 PR 里互相链接。
- 发布附件是平铺的，新增文件不能和其他目录的文件同名。

## 验证

```sh
python3 scripts/validate_packs.py
```

它检查专业词库的格式、拼音（对照 `cn/SingleCharsAllV1.txt`）、与基础词库的重复项、翻译覆盖率，以及 `custom/translations.txt` 的格式。这三个文件的追加规则由 check-words workflow 用固定版本的 `msime-dict-build check-words` 检查，需要 Rust 工具链，本地一般不跑。

## 隐私

示例数据不得使用真实可拨的手机号、真实地址或真实人名，即便只是 mock。手机号用 `13800000000` 这类保留号段，地址用明显虚构串。这条来自 MSIME-Windows#74。

## 提交

只暂存本次改动的显式路径，不用 `git add -A` / `git add .`。提交信息用 `type(scope): 摘要`。不要添加 `Co-Authored-By`、`Generated with` 或其他 AI 生成标记。
