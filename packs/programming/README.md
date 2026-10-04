# 编程开发专业词库

面向中文软件开发者的可选词库，覆盖版本控制、构建与工具链、编程语言与运行时、前端、后端与基础设施、数据库、测试和安全等方向的常用术语。当前包含中文候选、带官方大小写的英文候选，以及中英双向术语释义。

## 导入

在水杉输入法设置的词库管理页面中：

1. 选择拼音词库的“编码导入”，导入 `quanpin.txt`。
2. 选择英文词库的“导入”，导入 `english.txt`。

中文文件使用 `词语<Tab>全拼<Tab>权重`，英文文件使用 `输入键<Tab>显示内容<Tab>权重`。两个文件故意不含标题或注释，避免设置程序把说明文字当作词条。

`translations.txt` 是完整的术语对照审校稿，覆盖两个文件里的每个中文词语和英文显示内容。本词库的条目都没有同步到仓库的 `custom/translations.txt`：`SSR`、`CSR`、`SSO`、`TTL`、`Go`、`Helm` 等短缩写和产品名在通用语境里有其他含义，只保留在本专业包中，不覆盖所有用户的通用释义。

## 收录原则

- 只收录开发者实际会输入的术语、模式名、工程实践名和产品名，不收句子和定义。
- 中文术语优先采用下方官方中文文档的译法；同一概念有两种通行说法时两种都收，例如“可复现构建”“可重现构建”、“特性分支”“功能分支”、“优雅停机”“优雅关闭”；主词库已有其中一种时只补另一种，例如主词库已有“命名空间”，本词库补 Kubernetes 文档用的“名字空间”。
- 发布拼音词库（`pinyin/BaseDictIceV1.txt`、`pinyin/RimeIceSupplementV1.txt`、`custom/words.txt`）里已有的词语不重复收录，即使读音不同；例如“变基”“拣选”“暂存区”“编译器”“闭包”“协程”“幂等”“灰度发布”已在主词库中。
- 中文权重统一为 10000，英文权重统一为 10，与 `unreal_houdini` 一致。
- 英文候选只收有固定官方大小写或写法的名称和缩写，例如 `GitHub`、`PostgreSQL`、`gRPC`、`WebAssembly`、`macOS`；全小写的官方名（如 `npm`、`pnpm`、`webpack`、`etcd`）不收，因为与输入键相同。
- 英文输入键只接受小写字母、连字符和撇号，含数字或符号的显示内容挂在去掉这些字符的输入键下：`http` 对应 `HTTP/2`、`HTTP/3`，`ipv` 对应 `IPv4`、`IPv6`，`utf` 对应 `UTF-8`，`sha` 对应 `SHA-256`，`cpp` 对应 `C++`，`csharp` 对应 `C#`，`golang` 对应 `Go`；`wasm` 与 `webassembly` 都对应 `WebAssembly`。
- 不单独收人名，人名只作为通行术语的一部分出现（如“帕斯卡命名”）；不含任何电话号码或地址。

## 多音字

以下多音字已逐条核对，读音以 `pinyin/SingleCharsAllV1.txt` 中列出的读音为准：

- 行：表示“行、列”时读 hang（行内评论、行级锁、行式存储、行覆盖率、缓存行）；表示“运行、施行”时读 xing（运行时多态、测试运行器、行为驱动开发、最小可行产品）。
- 调：调用、调度、回调读 diao（尾调用、回调地狱、任务调度器）；协调读 tiao（协调算法）。
- 重：表示“再次”时读 chong（热重载、重试机制、可重入锁、可重现构建、重定向符、重复代码、重命名符号）。
- 模：模板读 mu（模板特化、模板字符串）；模块、模式、模型、模拟、建模读 mo。
- 露：泄露读 lou（内存泄露、密钥泄露、凭据泄露）；披露读 lu（漏洞披露）。
- 间：间接、间隙读 jian 第四声，时间、中间、空间读 jian 第一声，拼音相同。
- 卷：持久卷、卷模式读 juan。
- 弹：弹性布局读 tan。
- 粘：粘性定位、粘性会话读 nian。
- 簇：非聚簇索引读 cu。
- 塞：队头阻塞读 se。
- 省：生命周期省略读 sheng。
- 角：基于角色的访问控制读 jue。
- 累：累积布局偏移读 lei。
- 差：差异比较、差异算法、差分数组读 cha。
- 率：缓存命中率、测试覆盖率、行覆盖率、分支覆盖率读 lv。
- 长：长期支持版读 chang。
- 传：传递依赖、错误传播、分片上传读 chuan。
- 转：转译器、核心转储、跳转到定义读 zhuan。
- 校：回调地址校验读 jiao。
- 供：供应链攻击读 gong。
- 恰：恰好一次读 qia。
- 车：边车代理、边车模式、边车容器读 che。

## 核对来源

以下官方文档访问于 2026-10-04，只用于确认术语译法，不复制定义正文：

- [Pro Git 中文版：Git 分支 - 变基](https://git-scm.com/book/zh/v2/Git-%E5%88%86%E6%94%AF-%E5%8F%98%E5%9F%BA)（变基、快进合并、三方合并、远程分支、主题分支、合并提交）
- [Pro Git 中文版：Git 工具 - 贮藏与清理](https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E8%B4%AE%E8%97%8F%E4%B8%8E%E6%B8%85%E7%90%86)（贮藏、工作目录、暂存、未跟踪文件）
- [GitHub 文档：关于协作开发模型](https://docs.github.com/zh/pull-requests/collaborating-with-pull-requests/getting-started/about-collaborative-development-models)（拉取请求、复刻、存储库、上游）
- [Rust 程序设计语言 简体中文版：RefCell 与内部可变性模式](https://kaisery.github.io/trpl-zh-cn/ch15-05-interior-mutability.html)（内部可变性、借用检查器、引用计数、智能指针、引用循环）
- [Kubernetes 文档：词汇表](https://kubernetes.io/zh-cn/docs/reference/glossary/?all=true)（存活探针、就绪探针、启动探针、污点、容忍度、控制平面、容器运行时、名字空间、边车容器、资源配额）
- [Kubernetes 文档：持久卷](https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes/)（持久卷、持久卷申领、存储类、回收策略、卷模式）
- [Kubernetes 文档：自动扩缩工作负载](https://kubernetes.io/zh-cn/docs/concepts/workloads/autoscaling/)（水平扩缩、垂直扩缩、自动扩缩）
- [MDN：跨源资源共享（CORS）](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Guides/CORS)（跨源资源共享、预检请求、简单请求、同源策略、身份凭证）
- [MDN：服务器发送事件](https://developer.mozilla.org/zh-CN/docs/Web/API/Server-sent_events)（服务器发送事件）
- [React 中文文档：hydrateRoot](https://zh-hans.react.dev/reference/react-dom/client/hydrateRoot)（服务端渲染、客户端渲染；React 中文文档把 hydration 译作“激活”，本词库按社区通行说法收“水合”系列）

以下文档同样访问于 2026-10-04，用于确认对应分组里的概念和英文原名；其中中文页面同时确认中文译法：

- [Apache Flink 中文文档：数据源和接收器的容错保证](https://nightlies.apache.org/flink/flink-docs-stable/zh/docs/connectors/datastream/guarantees/)（精确一次、至少一次、至多一次）
- [MySQL 8.0 参考手册：InnoDB Locking](https://dev.mysql.com/doc/refman/8.0/en/innodb-locking.html)（数据库分组的锁类型：间隙锁 gap lock、临键锁 next-key lock、记录锁、意向锁、插入意向锁）
- [PostgreSQL 文档：Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)（隔离级别与并发异常）
- [Google SRE Book：Embracing Risk](https://sre.google/sre-book/embracing-risk/)（服务等级目标、错误预算）
- [Alistair Cockburn：Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)（六边形架构、端口与适配器）
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)（安全分组的漏洞类别）

上面两组来源没有逐条覆盖的条目（例如湖仓一体、流批一体、同城双活、夜间构建）采用国内开发者的通行说法，没有找到官方中文出处；英文候选的大小写取自对应项目官网的名称写法。
