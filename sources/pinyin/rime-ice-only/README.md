# rime-ice 中万象没有的词条

本目录是审核用的字面差集：从 `sources/pinyin/rime-ice.txt` 和
`sources/pinyin/rime-ice-supplement.txt` 分别取出在
`sources/pinyin/wanxiang/` 全部 `.dict.yaml` 数据区中没有出现过的词。
不移动或替换原始输入；目前 msime 构建器不读取本目录，不应再次导入造成重复。

## 文件与比较规则

- `rime-ice-only-entries.txt`：主表差集，四列为 `词<TAB>全拼<TAB>原始权重<TAB>源文件行号`，文件头是 `#` 注释。
- `rime-ice-only-words.txt`：主表差集，每个词只出现一次。
- `rime-ice-supplement-only-entries.txt`、`rime-ice-supplement-only-words.txt`：补充表的对应结果。
- `manifest.json`：来源仓库与提交、完整比较输入的大小和 SHA-256、脚本 SHA-256、生成文件摘要与统计。无本机绝对路径或生成时间，同样输入和脚本可生成相同字节。

只按第一列词的原始字面精确匹配，不比较读音、声调或权重，不转换简繁，
不做 Unicode 规范化。万象同一个词有任意读音就视为已收录；包括单字、
错音表、混合词等全部词表，不仅限于提供构建权重的词表。
只跳过注释、空行和 YAML 元数据，格式错误会报错。

词条文件保留所有命中的源行，包括同词多音或重复行；按原始权重降序，
同权重按词、全拼、源行号排序。纯词语文件按该词最高权重排序并去重。
主表和补充表分开比较，跨表可能重叠；合并去重数量见 manifest。
源行号从 1 开始，包含源文件头和空行。

结果未应用 `curation/`、构建器的读音修正或其他清洗规则，也未人工逐词审核。
其中会有短语片段、错误词音和异常权重，差集不等于建议收录清单。

## 重新生成与统一更新

### 从 GitHub 拉取并生成完整候选

在仓库根目录运行：

```sh
python scripts/update_rime_ice_only.py --sync-upstream
```

也可以直接运行 `python scripts/sync_upstream_dictionaries.py`。需要 Git、
Python 3.10+、Rust/Cargo 和当前构建器要求的本机编译工具链；首次编译会下载
Cargo.lock 固定的依赖。rime-ice 默认跟随远程 `HEAD`；万象明确使用
[`amzxyz/rime-wanxiang-data`](https://github.com/amzxyz/rime-wanxiang-data)
的 [`wanxiang` 分支、`dicts/` 目录](https://github.com/amzxyz/rime-wanxiang-data/tree/wanxiang/dicts)，
Git 地址为 `https://github.com/amzxyz/rime-wanxiang-data.git`。
脚本把解析后的完整提交记录下来；不要把 `rime-wanxiang` 配置仓库当作更新数据源。

脚本在 `tmp/upstream-sync-<唯一名称>/` 中自动完成：

1. 检出两个上游，以及 `builder.lock.json` 固定的干净 msime 构建器。存在相邻
   `../msime` 时只借用 Git 对象缓存，不改变其工作区。
2. 比较新旧上游 LICENSE；许可或万象文件清单有不兼容变化时停止并保存报告。
3. 编译固定构建器，调用 `rime-ice-supplement` 生成中英文补充表及拒绝词音报告。
4. 逐字节复制已登记万象词表，在独立 `dictionary/` 候选中更新补充表、来源锁、
   NOTICE 的自动同步小节以及本目录全部差集。保留历史主表和其他来源数据。
5. 生成 msime 配套的 `msime.patch`（上游引用和许可说明）、`report.json`
   （增删、权重变化、字节摘要）及 README；许可证原文保存在 `licenses/`。

默认只准备候选，不覆盖当前仓库的源数据。可以固定上游版本或改输出位置：

```sh
python scripts/sync_upstream_dictionaries.py --rime-ice-ref <提交或标签> --wanxiang-ref <提交或标签> --output <输出父目录>
```

上游文件清单必须以数据仓库 `rime-wanxiang-data` 的目标提交为准；不能根据
配置仓库 `rime-wanxiang` 的目录推断数据仓库删了词表。若正确数据源与本仓
登记路径确有差异，脚本保留报告并停止，按路径契约处理，不混用不同提交补齐。
上游确已删除的已登记词表，审过后逐个用 `--remove-wanxiang <文件名>` 显式允许删除
（如 2026-11-16 数据仓库不再收的 `lianxiang.dict.yaml`、`renming.dict.yaml`）；
脚本只接受确实缺失的已登记文件，从候选和锁中一并删去，`--apply` 时同步删除。
删除词表要求 msime 构建器同步去掉对应路径，仍按跨仓顺序合并。
从配置仓库切换到数据仓库已于 2026-11-16 完成（`7ab73ee` → `rime-wanxiang-data`
`6b31773`），候选锁和 msime 配套补丁里的 repository 与 commit 一并更新。
只为重现旧快照时才显式指定 `--wanxiang-repository https://github.com/amzxyz/rime-wanxiang.git`
及对应旧提交；日常更新使用默认的数据仓库。

审核候选后，将 `msime.patch` 应用到基于最新 develop 的 msime 分支，按跨仓
流程提交配套 PR。该 PR 合并后，使用其完整合并提交应用候选：

```sh
python scripts/sync_upstream_dictionaries.py --apply tmp/upstream-sync-<名称> --msime-commit <40位合并提交>
```

脚本校验提交在远程 msime `develop` 上可达、全部上游引用一致、未夹带其他
构建器修改，本地输入及候选也未过期后，更新本仓源文件、锁、NOTICE、差集和
`builder.lock.json`。覆盖前在候选目录备份，写入异常时恢复。
中间若有其他 `crates/dict-builder` 改动，按 AGENTS 先单独升级构建器固定提交，
然后重新生成候选。合入前仍要试跑完整构建、审阅产物差异并通过 CI；
脚本不提交、推送、合并或发布，也不把自动生成候选标为已完成人工审核。

### 仅重算本地差集，或导入已审核候选

在仓库根目录运行（仅需 Python 3.10+ 标准库）：

```sh
python scripts/update_rime_ice_only.py
python scripts/update_rime_ice_only.py --check
```

第一条从当前已锁定输入重算全部差集和 manifest；第二条只检查是否过期，
不写文件，过期或输入摘要与 `upstream.lock.json` 不符时返回非零。
不会下载上游、猜音或改写现有源文件；README 由维护者维护。

需要统一导入新的万象、rime-ice 及重算差集时，先按根目录 README 的跨仓流程
准备一个**已审核的本仓候选检出**，其中新词表、`upstream.lock.json` 与
`NOTICE.md` 均已更新，再运行：

```sh
python scripts/update_rime_ice_only.py --from-reviewed /path/to/reviewed/msime-dictionary
python scripts/update_rime_ice_only.py --check
python scripts/check_upstream.py
```

导入会逐字节同步三个上游组 `rime-ice`、`rime-ice-supplement`、`rime-wanxiang`
的已登记文件，合并这三个组的锁记录，复制候选的整份 `NOTICE.md`，再重算差集。
`sources/english/rime-ice-en-supplement.txt` 与中文补充表共享上游提交，
因此会一起同步。导入前校验本地与候选文件摘要；不接受文件增删（同步脚本
`--apply` 按候选报告显式删除的万象词表除外）、路径变更、
任意仓库地址变化或候选同时改变其他上游引用；唯一允许的换源是逻辑名
`rime-wanxiang` 从旧 `amzxyz/rime-wanxiang.git` 切换到
`amzxyz/rime-wanxiang-data.git`。请审阅复制后的 NOTICE 差异，
候选应基于当前分支，以免覆盖本地其他来源说明。

rime-ice 主表有本项目的历史修正，不能直接拿上游 YAML 覆盖；
新补充表仍由 msime 的 `rime-ice-supplement` 生成器产生并审核。
此脚本只统一导入已审核数据和重算本目录，不替代上游候选生成、
msime 引用与许可更新、构建器升级或发布前的试跑和评测。

## 来源与许可

词条与读音来自 [iDvel/rime-ice](https://github.com/iDvel/rime-ice)，
以本仓主表和补充表实际快照为准，沿用其 GPL-3.0 及原表的来源说明。
比较集合来自作者 amzxyz 的万象词库数据仓库
[amzxyz/rime-wanxiang-data](https://github.com/amzxyz/rime-wanxiang-data)，
词库数据源自同作者的 [RIME-LMDG](https://github.com/amzxyz/RIME-LMDG)，
按 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 使用。
改动为按词字面筛选、排序、生成去重词清单并在词条文件附上源行号；
不重新计算原表权重。原表历史上的万象权重改编说明继续适用。
各上游固定提交见 manifest；完整来源、历史修正及许可边界见
[根目录 NOTICE.md](../../../NOTICE.md)。
