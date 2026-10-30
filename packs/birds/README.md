# 世界鸟类名称词库

面向观鸟、鸟类摄影与自然记录的可选词库，收录 IOC 世界鸟类名录 v15.2 的简体中文鸟名和对应英文名，提供拼音输入、英文名称输入及中英双向对照。包含 9,819 条中文候选、11,041 条英文候选和 22,082 条翻译。

## 导入

在水杉输入法设置的词库管理页面中，将 `quanpin.txt` 作为拼音词库“编码导入”，将 `english.txt` 作为英文词库导入。`translations.txt` 是中英双向名称对照审校稿，与其他专业词库的用途一致。

三个词表均为 UTF-8、LF 换行，没有标题或注释行：

- `quanpin.txt`：`词语<TAB>全拼<TAB>权重`；音节用 `'` 分隔，权重统一为 1000。
- `english.txt`：`输入键<TAB>显示内容<TAB>权重`；显示内容保留原英文名的大小写、空格、重音字母及标点，权重统一为 1。
- `translations.txt`：`源词<TAB>对应名称`；先列中文到英文，再列英文到中文。

英文输入键转为小写，删除空格和句点，重音拉丁字母用 Unicode NFKD 分解后取 ASCII 字母，保留连字符与撇号。例如 `Common Ostrich` 对应 `commonostrich`，`Böhm's Spinetail` 对应 `bohm'sspinetail`，`St. Helena Plover` 对应 `sthelenaplover`。所有输入键均非空且互不重复。

## 收录与去重

- 数据来自 huashu-bird-sticker 固定提交中的 `data/species.json`，仅取 `names.zh-Hans` 和 `names.en` 两个字段，逐条与 `data/species.csv` 及此前导出的中英对照 TSV 核对；沿用原来的 IOC 分类顺序。
- 原数据共有 11,064 个鸟种，其中 11,041 个有简体中文名。这 11,041 对名称全部保留在双向翻译中；不另收中文别名、繁体名、学名或图鉴文字，不自行改写或翻译鸟名。
- 剩余 23 个鸟种原数据缺少简体中文名，因此本包的三个词表均暂不收录，避免提供没有中文对照的英文候选。缺名名单可从固定提交中 `names.zh-Hans` 为空的记录复核。
- 中文候选按 `(词语, 全拼)` 对照 `sources/pinyin/rime-ice.txt`、`sources/pinyin/rime-ice-supplement.txt`、`sources/pinyin/places.txt`、`custom/words.txt` 去重，共排除 1,222 条已有候选，留下 9,819 条。被排除的中文名仍保留双向翻译和对应英文候选。
- 不以 `sources/unlicensed/` 为排除集合；这些数据不进入发布词库，与其重复只按仓库校验规则提示。
- 英文每个鸟种保留一个完整名称，不拆成普通英文单词；不额外按基础英文词库去重。本包中文名、英文显示内容及翻译源词均无重复。
- 本包按完整鸟名清单整理，作为单包收录，属于 `packs/README.md` 中常规 100–2000 条规模限制的明确例外；三个词表各自均小于 2 MiB，不进入主词库发布构建。

## 拼音与多音字

按本次整理要求，使用 **pypinyin 0.55.0** 的 `lazy_pinyin(..., style=Style.NORMAL)` 生成无声调全拼，再进行下列语境修正。全部字音已对照 `sources/pinyin/single-chars.txt` 和 `sources/pinyin/rime-ice-supplement.txt` 的单字行，全部汉字均在对照集合内；机器校验只检查字音是否合法，**尚未逐条完成鸟名读音的人工审校**。

以下规则用于整份清单，包含已被通用词库去重的名称；括号里的数量是相对 pypinyin 默认结果实际修正的字数：

| 字或语境 | 本包处理 |
| --- | --- |
| 长尾、长嘴、长脚、长爪等形态描述 | 长读 `chang`；酋长鹂的长保留 `zhang`（修正 180 字） |
| 藏马鸡、青藏沙鸻等地理名称 | 藏读 `zang`（10 字） |
| 绿林戴胜、绿林莺等颜色描述 | 绿读 `lv`，不用绿林好汉的 `lu`（4 字） |
| 南无须小霸鹟 | 南读 `nan`、无读 `wu`，不用佛教词“南无”的读法（各 1 字） |
| 强嘴䴕雀 | 强读 `qiang`（1 字） |
| 洪都拉斯、民都洛、民都岛 | 都读 `du`（3 字） |
| 加勒比、弗洛勒斯及勒氏 | 勒读 `le`（6 字） |
| 查查波亚蚁鸫 | 两个查均读 `cha`，按地名音译处理（2 字） |
| 安卡什窜鸟 | 什读 `shi`，按地名音译处理（1 字） |
| 杓鹬 | 杓读 `shao`（9 字），参照下列涉禽调查报告中的 `Zhong Shao Yu`；不另加 `biao` 容错候选 |

其他需关注的默认读音包括：爪哇、长爪的爪 `zhao`；秘鲁的秘 `bi`；尼泊尔的泊 `po`、漂泊的泊 `bo`；佛法僧的佛 `fo`、佛得角的佛 `fu`；鳽 `jian`；靓鹦鹉、靓唐纳雀的靓 `jing`；叽喳的喳 `zha`。这些条目保留 pypinyin 的输出，列出供后续人工审校，不将字音表允许的其他读音自动扩展为候选。

## 核对来源与授权

以下资料于 **2026-10-31** 查阅；鸟名依据固定数据快照，拼音依据上述工具与语境规则，二者不混作同一来源。

- 全部鸟种中英主名：[alchaincyf/huashu-bird-sticker](https://github.com/alchaincyf/huashu-bird-sticker/tree/47bb6f366641a76a482e2fb2fd26b2ac515f1a13)，提交 `47bb6f366641a76a482e2fb2fd26b2ac515f1a13`，`data/species.json`，SHA-256 为 `f9ff7d915af2fbcef09acf6abbe90b9122fb195bd2e9c770b96501a7a9743ea9`。对照文件为同提交的 `data/species.csv`；来源说明见同提交的 `NOTICE.md` 和 `data/README.md`。
- 上述项目声明鸟名来自 **IOC World Bird List v15.2** 多语种版，编者 **Frank Gill、David Donsker、Pamela Rasmussen**，按 [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) 许可使用；原始来源为 [IOC World Bird List](https://worldbirdnames.org/)。本包沿用这些名称的许可及署名，不将其改为本仓自写数据的 GPL-3.0。
- 鳽等鸟名用字：[中国科学院辽宁沈阳城市生态系统定位观测研究站《从“鵙”到“鸬鹚”，解锁沈阳飞羽的名字密码》](https://iae.cas.cn/sycsz/xwgg/kphd/202508/t20250822_7909201.html)，用于核对鳽的 `jian` 读音，不复制文章正文。
- 杓鹬：[Yalu Jiang Estuary Shorebird Survey Report](https://shorebirds.org.nz/wp-content/uploads/2017/11/Yalu-Jiang-Report-Riegen-Vaughan-April-2014.pdf) 鸟名附录，用于核对中杓鹬的 `shao` 读音，不复制调查记录或定义。

本包的改动是筛选有简体中文名的鸟种、生成并按上述规则修正拼音、删除已收录的同词同音中文候选、生成英文输入键、设置导入权重及生成中英双向对照。鸟名本身保持原文；未使用上游贴纸、参考照片、形态数据或中文图鉴文字。鸟名清单并非中文官方命名的逐条认定，采用的是固定快照中 IOC 多语种版的对应名称。
