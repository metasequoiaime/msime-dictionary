# AGENTS.md — msime-dictionary

组织级约定和跨仓边界以 [组织 AGENTS.md](https://github.com/metasequoiaime/.github/blob/main/AGENTS.md) 为准。本文件补充本仓的数据与验证规则。

本仓只放词库源数据：`cn/`、`en/` 下的基础词库，`custom/` 下的人工维护数据，`packs/` 下的专业词库。这里没有构建脚本，也不产出词库；msime 的 `crates/dict-builder`（`msime-dict-build`）按 msime `resources/dictionary-sources.lock.json` 固定的提交下载这里的文件，校验大小与 SHA-256 后构建并发布 `dict-v*`。不要把构建脚本、生成的数据库或其他产物加回本仓。

## 文件是逐字节锁定的

下游按提交和 SHA-256 锁定每个文件，所以：

- 不做全量格式化，不转换编码或换行符，不排序、不去重、不补结尾换行。`cn/`、`en/` 下有 CRLF 文件，`.gitattributes` 的 `* -text` 让 Git 原样保存；不要删掉它，也不要在本地用 `core.autocrlf` 之类的设置绕过。
- 路径就是契约。改名或移动文件要同时改 msime 的锁文件与构建器，并在 PR 里互相链接；下游没有跟上之前不要合入。

## 自定义词条

- `custom/words.txt` **只追加**：新词条写在文件末尾，不修改、删除或重排已有的行。check-words 会拒绝任何非追加的改动。
- 格式是 `词<TAB>全拼<TAB>权重`，全拼音节用 `'` 分隔，权重落在文件现有的范围内；不要为了让一个词靠前填一个极大值。
- 候选窗翻译的修正写到 `custom/translations.txt`，不改 ECDICT。

## 基础词库

`cn/`、`en/` 下的文件来自第三方（见 `NOTICE.md`）。不在里面加新词；只有经过确认的错误才修改，并且：

- 提交说明写清修了什么、依据是什么（上游提交、对照数据或复现方式）；
- 来源或许可有变化时同一次改动更新 `NOTICE.md`；
- 新增的第三方数据先确认再分发许可并写进 `NOTICE.md`，没有明确许可的数据会被 msime 构建器的 `licensing.rs` 挡在发布产物之外，要在那里同步登记。

## 验证

```sh
python3 scripts/validate_packs.py
```

它检查专业词库的格式、拼音（对照 `cn/SingleCharsAllV1.txt`）、与基础词库的重复项、翻译覆盖率，以及 `custom/translations.txt` 的格式。`custom/words.txt` 的追加规则由 check-words workflow 用固定版本的 `msime-dict-build check-words` 检查，需要 Rust 工具链，本地一般不跑。

## 隐私

示例数据不得使用真实可拨的手机号、真实地址或真实人名，即便只是 mock。手机号用 `13800000000` 这类保留号段，地址用明显虚构串。这条来自 MSIME-Windows#74。

## 提交

只暂存本次改动的显式路径，不用 `git add -A` / `git add .`。提交信息用 `type(scope): 摘要`。不要添加 `Co-Authored-By`、`Generated with` 或其他 AI 生成标记。
