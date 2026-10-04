# 机器学习与大模型专业词库

面向机器学习、深度学习和大语言模型工程的可选词库，覆盖训练与优化、网络结构、注意力机制、检索增强生成、对齐与强化学习、模型压缩与推理部署等方向的术语。当前包含中文候选、带官方大小写的英文候选，以及中英双向术语释义。

## 导入

在水杉输入法设置的词库管理页面中：

1. 选择拼音词库的“编码导入”，导入 `quanpin.txt`。
2. 选择英文词库的“导入”，导入 `english.txt`。

中文文件使用 `词语<Tab>全拼<Tab>权重`，英文文件使用 `输入键<Tab>显示内容<Tab>权重`。两个文件故意不含标题或注释，避免设置程序把说明文字当作词条。

`translations.txt` 是完整的术语对照审校稿，前半部分是中文候选到英文术语，后半部分是英文候选到中文释义。`MoE`、`RAG`、`CoT`、`SFT`、`MLA`、`TPOT` 等短缩写在其他领域另有含义，只保留在本专业包中，不同步到 `custom/translations.txt`。

## 收录原则

- 只收录机器学习、深度学习和大模型工程里实际会输入的术语，不收句子和定义。
- 不收已在发布拼音词库（`sources/pinyin/rime-ice.txt`、`sources/pinyin/rime-ice-supplement.txt`、`sources/pinyin/places.txt`、`custom/words.txt`）中出现的词，不论读音是否相同；例如“过拟合”“微调”“量化”“剪枝”“幻觉”“对齐”“词元”“嵌入”“推理”“反向传播”“损失函数”“梯度下降”“归一化”“强化学习”都已在发布词库中。
- “大模型”“大语言模型”“通用人工智能”“文生图”“文生视频”“图像生成”“视频生成”“文本生成”“多轮对话”“具身智能”“智能体”“提示词”“提示工程”等已进入大众用语的词留给通用词库，本包不收。“风格迁移”“文本转语音”“世界模型”保留，它们在新闻里出现得少，主要出现在论文、模型文档和工程讨论里。
- 不收组合短语和不完整的修饰语，例如“千亿参数”“批维度”“神经符号”。“每秒浮点运算次数”是 `FLOPS` 的中文全称，作为术语保留；运算总量 `FLOPs` 是另一个量，两者在英文候选里分开收录。
- “递归神经网络”严格指树结构的 Recursive Neural Network，中文资料里也常被当作循环神经网络（RNN）的别名，释义里注明了这一点。
- 同一概念有多个通行译名时并列收录，例如“暂退法 / 随机失活 / 丢弃法”“批量归一化 / 批量规范化”“指令微调 / 指令调优”“学习率 / 学习速率”“投机解码 / 推测解码”。
- 英文候选的显示内容采用项目或论文的官方写法（`PyTorch`、`cuDNN`、`vLLM`、`LoRA`、`RMSNorm`），输入键只含小写字母和连字符；`Megatron-LM` 的输入键去掉 `-LM` 后缀，写作 `megatron`；`TensorRT-LLM`、`SWE-bench` 的输入键保留连字符。发布英文词库已有同样大小写的条目（`GPT`、`CNN`、`Adam`、`GPU`、`ASR`、`OCR`、`AGI`、`AIGC`、`arXiv`）不重复收录。
- 英文大小写规则：`softmax`、`logits`、`dropout` 这类通用术语一律小写；`LayerNorm`、`BatchNorm`、`RMSNorm` 这类按 PyTorch 类名书写的保留原样；激活函数缩写 `ReLU`、`GELU`、`SiLU` 按 PyTorch 文档写。
- `translations.txt` 的英文释义用标题式大小写；连字符复合词的后半部分小写（`Self-supervised Learning`、`Full-parameter Fine-tuning`），但英文候选里收了缩写的方法按论文原名书写（`Parameter-Efficient Fine-Tuning`、`Supervised Fine-Tuning`、`Grouped-Query Attention`、`Multi-Query Attention`、`Multi-Head Attention`、`Post-Training Quantization`、`Quantization-Aware Training`、`Low-Rank Adaptation`）。
- 中文候选权重统一为 10000，英文候选权重统一为 10，与 `unreal_houdini` 一致。
- 不复制术语库或文档的定义正文，只记录术语和短释义。

## 多音字

以下字按所在术语逐条核对过读音：

- 重：`chong` 用于重参数化、重参数化技巧、重计算、激活重计算、重复惩罚、双重下降、重排序模型；`zhong` 用于权重相关术语（权重衰减、模型权重、注意力权重等）和重要性采样。
- 调：`tiao` 用于各类微调、超参数调优、指令调优；`diao` 用于工具调用、噪声调度、学习率调度。
- 模：`mu` 用于提示模板（与发布词库“模板 mu'ban”一致）；其余如模型、模态、建模、参数规模均读 `mo`。
- 长：上下文长度、长上下文、长短期记忆均读 `chang`。
- 率：学习率及其派生词（学习率衰减、学习率调度、学习率预热、自适应学习率）、学习速率、幻觉率、去噪扩散概率模型、词频逆文档频率均读 `lv`。
- 行：并行类术语读 `xing`。
- 差：残差、误差、时序差分读 `cha`。
- 似：似然、近似、相似度读 `si`。
- 藏：隐藏维度读 `cang`。
- 塞：黑塞矩阵读 `sai`。
- 场：神经辐射场读 `chang`。
- 得：得分匹配读 `de`。
- 干：骨干网络读 `gan`。
- 切：子词切分、双曲正切读 `qie`。
- 卡：蒙特卡洛、模型卡读 `ka`。
- 应：自适应、领域自适应读 `ying`。
- 期：长短期记忆、期望最大化读 `qi`。
- 弈：自对弈、自我博弈读 `yi`。

## 核对来源

按术语分组列出所依据的文档，冒号后是该文档覆盖的术语。只记录术语和译法，不复制定义正文。

### 文档（访问于 2026-10-04）

- [Google 机器学习术语表（简体中文）](https://developers.google.com/machine-learning/glossary?hl=zh-cn)：欠拟合、过拟合、上下文窗口、思维链提示、检索增强生成、梯度裁剪、损失曲线、困惑度、指令调优、批次大小、学习速率等译名。
- [《动手学深度学习》中文版](https://zh.d2l.ai/)：暂退法、词元、批量规范化、注意力汇聚、注意力评分函数、多头注意力、自注意力和位置编码、束搜索、微调等译名。
- [术语在线（全国科学技术名词审定委员会）](https://www.termonline.cn/)：规范名词的参照入口；本次自动抓取只得到站点标题，没有逐条查询，也不复制其释义。
- [PyTorch torch.nn 文档](https://docs.pytorch.org/docs/2.14/nn.html)：`LayerNorm`、`RMSNorm`、`BatchNorm`、`SiLU`、`GELU`、`ReLU`、`Transformer` 的大小写。`softmax`、`dropout` 作通用术语，按论文习惯小写，不取类名写法。
- [TensorFlow 官网（简体中文）](https://www.tensorflow.org/?hl=zh-cn)：`TensorFlow`、`Keras`、`TensorBoard` 的写法。
- [Hugging Face PEFT 文档](https://huggingface.co/docs/peft/index)：`PEFT`（Parameter-Efficient Fine-Tuning）、`Transformers`、`Diffusers` 的写法。
- [vLLM 文档](https://docs.vllm.ai/en/latest/)：`vLLM`、PagedAttention、连续批处理、前缀缓存、投机解码、张量并行与专家并行、`GPTQ`、`AWQ`、`GGUF`。
- [NVIDIA cuDNN](https://developer.nvidia.com/cudnn)：`cuDNN`、`CUDA`、`TensorRT`、`NCCL`、Tensor Core。
- [飞桨 PaddlePaddle 官网](https://www.paddlepaddle.org.cn/)：中文名“飞桨”与 `PaddlePaddle`。
- [昇思 MindSpore 官网](https://www.mindspore.cn/)：中文名“昇思”与 `MindSpore`。
- [《蘑菇书 EasyRL》强化学习中文教程](https://github.com/datawhalechina/easy-rl)：策略梯度、近端策略优化、策略网络、价值网络、价值函数、动作价值函数、状态价值函数、优势函数、时序差分、时序差分学习、蒙特卡洛方法、经验回放、探索与利用、贝尔曼方程、折扣因子、同策略、异策略、马尔可夫决策过程、逆强化学习等强化学习译名。
- [Google 机器学习术语表：强化学习（简体中文）](https://developers.google.com/machine-learning/glossary/rl?hl=zh-cn)：贝尔曼方程、经验回放、折扣因子、深度 Q 网络（`DQN`）。
- 中文维基百科（[逻辑斯谛函数](https://zh.wikipedia.org/wiki/逻辑斯谛函数)、[狄利克雷分布](https://zh.wikipedia.org/wiki/狄利克雷分布)、[边缘分布](https://zh.wikipedia.org/wiki/边缘分布)、[雅可比矩阵](https://zh.wikipedia.org/wiki/雅可比矩阵)、[高斯过程](https://zh.wikipedia.org/wiki/高斯过程)、[蒙特卡洛树搜索](https://zh.wikipedia.org/wiki/蒙特卡洛树搜索)、[近端策略优化](https://zh.wikipedia.org/wiki/近端策略优化)）：对应条目标题的写法，以及“无模型强化学习”。
- [《动手学深度学习》中文版源文件](https://github.com/d2l-ai/d2l-zh)：交并比、非极大值抑制、锚框、边界框、语义分割、实例分割、黑塞矩阵、多项分布、联合分布、马尔可夫链、对数似然、负对数似然、独立同分布。
- [scikit-learn 中文文档（ApacheCN 译本）](https://github.com/apachecn/sklearn-doc-zh)：宏平均、微平均、先验分布、后验分布、高斯过程、狄利克雷分布。
- Google 机器学习术语表（简体中文，同上）：真正例、假正例、真负例、假负例、交并比、ROC 曲线与曲线下面积（`AUC`）。
- [PaddleDetection](https://github.com/PaddlePaddle/PaddleDetection)、[PaddleSeg](https://github.com/PaddlePaddle/PaddleSeg)、[MMPose](https://github.com/open-mmlab/mmpose)、[MMDetection](https://github.com/open-mmlab/mmdetection) 中文 README：姿态估计、关键点检测、全景分割、实例分割、光流估计的写法。
- 论文题目或论文中的术语写法（[arXiv](https://arxiv.org/)）：Rotary Position Embedding（2104.09864）、Root Mean Square Layer Normalization（1910.07467）、Grouped-Query Attention（2305.13245）、Multi-Query Attention（1911.02150）、Low-Rank Adaptation（2106.09685）、Data Distillation（1712.04440）、Dataset Distillation（1811.10959）。
- 英文候选的官方写法，取自各项目官方仓库或官网：[Qwen](https://github.com/QwenLM/Qwen3)、[DeepSeek](https://github.com/deepseek-ai/DeepSeek-V3)、[Llama](https://github.com/meta-llama/llama-models)、[Mistral 与 Mixtral](https://github.com/mistralai/mistral-inference)、[Gemma](https://github.com/google-deepmind/gemma)、[ChatGLM](https://github.com/zai-org/ChatGLM-6B)、[Mamba](https://github.com/state-spaces/mamba)、[Ollama](https://github.com/ollama/ollama)、[SGLang](https://github.com/sgl-project/sglang)、[llama.cpp](https://github.com/ggml-org/llama.cpp)、[LangChain](https://github.com/langchain-ai/langchain)、[LangGraph](https://github.com/langchain-ai/langgraph)、[LlamaIndex](https://github.com/run-llama/llama_index)、[Faiss](https://github.com/facebookresearch/faiss)、[Milvus](https://github.com/milvus-io/milvus)、[Qdrant](https://github.com/qdrant/qdrant)、[Weaviate](https://github.com/weaviate/weaviate)、[pgvector](https://github.com/pgvector/pgvector)、[MLflow](https://github.com/mlflow/mlflow)、[XGBoost](https://github.com/dmlc/xgboost)、[LightGBM](https://github.com/lightgbm-org/LightGBM)、[CatBoost](https://github.com/catboost/catboost)、[MMLU](https://huggingface.co/datasets/cais/mmlu)、[HumanEval](https://github.com/openai/human-eval)、[SWE-bench](https://github.com/SWE-bench/SWE-bench)、[ROCm](https://github.com/ROCm/ROCm)、[NVLink](https://www.nvidia.com/en-us/data-center/nvlink/)、[InfiniBand](https://www.infinibandta.org/)、[MLX](https://github.com/ml-explore/mlx)、[Core ML](https://github.com/apple/coremltools)。

### 无官方中文出处的术语

上面各组文档没有点名的其余条目是领域里的通行说法，没有找到官方中文出处，按通行说法收录，没有逐条对应到单一来源。术语在线没有逐条查询，所以上面的译名也没有经过它的规范名核对。
