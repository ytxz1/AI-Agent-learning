# Day 18 - RAG 检索链

> 目标：理解 Retriever、Top-K 检索、上下文拼接和在线回答生成是如何串成一条完整链路的。  
> 这一节不再只关注“文档怎么进来”，而是开始关注“文档怎么被找到、怎么被组织、怎么喂给模型”。

---

## 1. Day 18 的定位

Day 18 是 RAG 流程中的“检索链”阶段。

你可以把前面的内容理解为：

- Day 17：把文档加载进来，并切成 chunk
- Day 18：从这些 chunk 里找到最相关的内容，并组织成回答上下文

这一步是 RAG 的关键中枢，因为：

**检索找得准不准，直接决定后续回答质量。**

---

## 2. 本日学习目标

完成 Day 18 后，你应该能理解并掌握：

1. 什么是 Retriever。
2. 什么是 Top-K 检索。
3. 为什么需要检索结果排序。
4. 上下文是如何拼接出来的。
5. 为什么上下文长度会影响生成效果。
6. 如何搭建一个完整的“检索 -> 上下文 -> 回答”链路。

---

## 3. 项目整体说明

这个 Day 18 项目是一个轻量级、可本地运行且支持在线回答生成的 RAG 检索链示例。

它的核心流程是：

1. 加载文档
2. 切分文档
3. 构建检索器
4. 根据问题找相关 chunk
5. 把检索结果拼成上下文
6. 使用在线模型生成一个可读回答

这个项目特别适合用来理解 RAG 的“中间步骤”，而不是只看最终答案。

---

## 4. 目录结构总览

```text
day18/
├── README.md
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── documents/
│   ├── 01_rag_intro.txt
│   ├── 02_retriever_notes.md
│   └── 03_context_building.txt
├── modules/
│   ├── __init__.py
│   ├── loader.py
│   ├── splitter.py
│   ├── retriever.py
│   ├── rag_chain.py
│   └── pipeline.py
├── 01_build_retriever.py
├── 02_retrieval_test.py
├── 03_context_preview.py
├── 04_topk_compare.py
└── 05_full_rag_app.py
```

下面我们逐个解释。

---

## 5. 核心文件详细说明

### 5.1 `main.py`

文件路径：
- [day18/main.py](/D:/vscode项目/学习/day18/main.py)

#### 作用

`main.py` 是整个项目的统一入口。

运行：

```bash
python main.py
```

实际上就是启动 `05_full_rag_app.py`。

#### 为什么要单独保留入口

这样做的原因很简单：

- 用户只需要记住一个启动方式
- 后续如果改成 Web 或其他界面，入口可以独立替换
- 主业务代码可以继续保持清晰

---

### 5.2 `config.py`

文件路径：
- [day18/config.py](/D:/vscode项目/学习/day18/config.py)

#### 作用

这个文件统一管理所有参数：

- 文档目录
- chunk_size
- chunk_overlap
- top_k
- 上下文长度限制
- 回答风格
- 可选在线模型配置

#### 为什么这些参数重要

RAG 检索链特别适合调参。

比如：

- `chunk_size` 决定每块信息有多大
- `chunk_overlap` 决定前后文保留多少
- `top_k` 决定取多少条相关内容
- `max_context_chars` 决定最终给模型的上下文有多长

这些参数都会影响检索结果和回答质量。

---

### 5.3 `requirements.txt`

文件路径：
- [day18/requirements.txt](/D:/vscode项目/学习/day18/requirements.txt)

#### 作用

记录项目依赖，安装时可以直接运行：

```bash
pip install -r requirements.txt
```

#### 这份依赖的意义

- `rich`：用于漂亮的命令行输出
- `python-dotenv`：用于读取 `.env`
- `langchain-openai`：用于后续可选的在线模型扩展
- `langchain-core`：用于兼容 LangChain 风格的数据结构

---

### 5.4 `.env.example`

文件路径：
- [day18/.env.example](/D:/vscode项目/学习/day18/.env.example)

#### 作用

这是默认配置样例。

它提供了：

- 文档目录
- 切分参数
- 检索参数
- 可选模型配置

#### 为什么要有它

这样你就可以直接拿着样例配置开始运行，而不是每次都手写一份 `.env`。

---

### 5.5 `documents/`

文件路径：
- [day18/documents/](/D:/vscode项目/学习/day18/documents)

#### 作用

这是本项目的示例资料库。

我们准备了三份文档：

- `01_rag_intro.txt`
- `02_retriever_notes.md`
- `03_context_building.txt`

它们分别对应：

- RAG 基础概念
- Retriever 学习笔记
- 上下文拼接说明

#### 为什么要准备真实文本

因为检索链不是空跑的，必须有实际文档才能看到：

- 检索器怎么选内容
- chunk 怎么被排序
- 上下文怎么被拼出来

---

### 5.6 `modules/loader.py`

文件路径：
- [day18/modules/loader.py](/D:/vscode项目/学习/day18/modules/loader.py)

#### 作用

负责把文档从磁盘读入程序。

主要提供：

- `DocumentItem`：内部文档结构
- `load_text_file`：读取单个文本文件
- `load_documents`：批量读取目录中的文件
- `summarize_documents`：统计文档情况
- `preview_documents`：生成文档预览

#### 为什么要这样拆

因为“加载”和“切分”是两个阶段。

拆开以后更容易理解，也更容易单独调试。

---

### 5.7 `modules/splitter.py`

文件路径：
- [day18/modules/splitter.py](/D:/vscode项目/学习/day18/modules/splitter.py)

#### 作用

负责把长文档拆成更小的 chunk。

主要函数包括：

- `_split_by_separator`
- `_sliding_window`
- `split_documents`
- `compare_chunk_stats`
- `preview_chunks`

#### 这个模块的重点

你要特别关注：

- 怎么按标点拆
- 怎么保留前后文
- 怎么避免切得太碎
- metadata 是怎么跟着 chunk 一起保存的

---

### 5.8 `modules/retriever.py`

文件路径：
- [day18/modules/retriever.py](/D:/vscode项目/学习/day18/modules/retriever.py)

#### 作用

这是 Day 18 的核心模块之一。

它负责把用户问题和 chunk 做相似度匹配，选出最相关的结果。

#### 主要内容

- `extract_terms`：提取检索词项
- `build_document_profile`：为 chunk 建立词项画像
- `RetrievalResult`：检索结果结构
- `SimpleRetriever`：简单检索器
- `format_retrieval_summary`：输出检索摘要

#### 为什么要做检索器

因为在 RAG 里，模型并不是直接“背答案”，而是先去资料里找。

Retriever 就是“找资料”的这个角色。

---

### 5.9 `modules/rag_chain.py`

文件路径：
- [day18/modules/rag_chain.py](/D:/vscode项目/学习/day18/modules/rag_chain.py)

#### 作用

这个模块把检索和回答真正串起来。

它做的事情是：

1. 接收问题
2. 调用 Retriever
3. 拼接上下文
4. 基于上下文生成回答

#### 为什么叫“链”

因为它不是单独一个步骤，而是一条连续流程：

**问题 -> 检索 -> 上下文 -> 回答**

这就是 RAG 检索链的核心结构。  
如果配置了 `OPENAI_API_KEY`，最终回答会走在线模型；如果没有，就使用离线兜底。

---

### 5.10 `modules/pipeline.py`

文件路径：
- [day18/modules/pipeline.py](/D:/vscode项目/学习/day18/modules/pipeline.py)

#### 作用

它把整个文档处理和检索链组合起来：

- 加载
- 切分
- 构建检索链
- 提问

#### 为什么需要它

因为真实项目里，我们希望有一个统一入口来完成整条流程，而不是每一步都单独手动调用。

---

### 5.11 `modules/__init__.py`

文件路径：
- [day18/modules/__init__.py](/D:/vscode项目/学习/day18/modules/__init__.py)

#### 作用

把 `modules` 目录标记成 Python 包，便于导入。

---

## 6. 练习文件详细说明

### 6.1 `01_build_retriever.py`

文件路径：
- [day18/01_build_retriever.py](/D:/vscode项目/学习/day18/01_build_retriever.py)

#### 作用

这个脚本帮助你先确认：

- 文档是否成功加载
- chunk 是否成功生成
- 检索器的输入是否正确

#### 学习重点

先别急着问问题，先确认“资料库”是否建好了。

---

### 6.2 `02_retrieval_test.py`

文件路径：
- [day18/02_retrieval_test.py](/D:/vscode项目/学习/day18/02_retrieval_test.py)

#### 作用

这个脚本用多个问题测试检索效果。

你可以看到：

- 哪些 chunk 被检索到了
- 检索摘要长什么样
- 不同问题命中了哪些内容

---

### 6.3 `03_context_preview.py`

文件路径：
- [day18/03_context_preview.py](/D:/vscode项目/学习/day18/03_context_preview.py)

#### 作用

这个脚本专门展示“检索结果如何拼接成上下文”。

你会看到：

- 检索摘要
- 拼接后的 context

#### 这是非常关键的一步

因为检索只是“找出来”，而上下文拼接才是“喂给模型之前的整理”。

---

### 6.4 `04_topk_compare.py`

文件路径：
- [day18/04_topk_compare.py](/D:/vscode项目/学习/day18/04_topk_compare.py)

#### 作用

用于比较不同 `top_k` 的影响。

#### 为什么要比较

因为：

- `top_k` 太小，可能漏信息
- `top_k` 太大，上下文会变长、变杂

这个脚本能帮助你理解“检索条数”和“回答质量”之间的平衡。

---

### 6.5 `05_full_rag_app.py`

文件路径：
- [day18/05_full_rag_app.py](/D:/vscode项目/学习/day18/05_full_rag_app.py)

#### 作用

这是 Day 18 的完整交互式应用。

它支持：

- 加载文档
- 查看文档预览
- 查看 chunk 预览
- 查看统计信息
- 输入问题并获取检索链回答
- 运行示例问题
- 如果配置了 API Key，会走在线模型生成回答

#### 为什么它重要

因为它把前面的所有模块真正串起来了，能够让你看到一个完整的 RAG 检索链项目是怎么工作的。  
如果有 API，它还会演示“检索 + 在线生成”的完整闭环。

---

## 7. Day 18 的核心知识点

### 7.1 什么是 Retriever

Retriever 就是“从大量内容中找出最相关片段”的组件。

它不负责生成答案，只负责找资料。

### 7.2 什么是 Top-K

Top-K 就是返回最相关的前 K 条结果。

它是控制上下文长度和检索广度的关键参数。

### 7.3 什么是上下文拼接

上下文拼接就是把检索出来的 chunk 按一定格式组织起来，作为后续生成回答的输入。

### 7.4 为什么上下文拼接很重要

因为模型并不是直接读“数据库”。

它需要的是一段整理好的文本上下文。

所以这一步决定了：

- 模型看到什么
- 模型忽略什么
- 最终回答是否靠谱

### 7.5 为什么检索效果会受切分影响

如果 chunk 切得不好：

- 重要信息可能被切断
- 相关句子可能不在同一块里
- 检索器可能命中不完整

所以 Day 17 和 Day 18 是前后衔接的。

---

## 8. 推荐运行顺序

建议按照下面顺序学习：

1. `01_build_retriever.py`
2. `02_retrieval_test.py`
3. `03_context_preview.py`
4. `04_topk_compare.py`
5. `05_full_rag_app.py`

这样你可以从“检索器”开始，一步一步看到完整链路。

---

## 9. 如何运行

安装依赖：

```bash
pip install -r requirements.txt
```

启动主程序：

```bash
python main.py
```

单独运行练习脚本也可以：

```bash
python 01_build_retriever.py
python 05_full_rag_app.py
```

---

## 10. 常见问题

### 10.1 为什么检索结果有时看起来不够准？

因为这是一个轻量级的检索示例，主要用于学习链路结构。  
如果你想看更强的效果，可以配置 `OPENAI_API_KEY`，让最终回答走在线模型生成。

如果想更强的效果，可以后续换成真正的向量数据库和 embedding。

### 10.2 为什么上下文拼接长度有限制？

因为模型输入有长度限制，而且上下文越长不一定越好。

太长会让重点分散，太短会丢信息。

### 10.3 为什么要先看检索摘要再看最终回答？

因为你要先知道“模型看到了什么”，才能判断“为什么它会这么回答”。

---

## 11. 学习建议

1. 先理解文档加载和切分。
2. 再理解检索器的打分思路。
3. 多试几个问题，观察检索摘要变化。
4. 调整 `top_k` 和 `chunk_size` 看效果差异。
5. 想一想后续如果接入真正 embedding，会怎样升级这条链路。

---

## 12. 小结

Day 18 是 RAG 里非常关键的一步。

你要记住：

- Retriever 负责找资料
- Top-K 决定返回几条
- 上下文拼接决定模型看到什么
- 检索效果会直接影响回答质量

如果你把 Day 18 理解透了，后面做真正的 RAG 问答系统就会更顺。
