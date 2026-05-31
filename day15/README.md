# Day 15 - RAG 基础项目

> 目标：搭建一个最小但完整的 RAG（Retrieval-Augmented Generation，检索增强生成）项目。
>
> 这一天的重点是把链路真正跑通：
> 文档加载 -> 文本切分 -> 向量化 -> 向量检索 -> 基于检索结果生成答案。

---

## 0. 项目结构

```text
day15/
├── README.md
├── config.py
├── main.py
├── requirements.txt
├── .env.example
├── documents/
│   ├── agent_guide.txt
│   ├── python_guide.txt
│   └── rag_guide.txt
├── modules/
│   ├── __init__.py
│   ├── embeddings.py
│   ├── loader.py
│   ├── rag_chain.py
│   ├── retriever.py
│   ├── splitter.py
│   └── vector_store.py
├── 01_document_loader.py
├── 02_text_splitter.py
├── 03_embeddings.py
├── 04_vector_store.py
├── 05_retriever.py
├── 06_rag_chain.py
├── exercise1_load_docs.py
├── exercise2_split_compare.py
├── exercise3_custom_kb.py
├── exercise4_multi_doc.py
└── exercise5_rag_eval.py
```

---

## 1. Day 15 要做什么

Day 15 的任务是理解并实现一个 RAG 最小系统。

你要完成的核心任务有：

1. 理解 RAG 的概念。
2. 准备本地知识文档。
3. 实现文档加载。
4. 实现文本切分。
5. 实现文本向量化。
6. 实现向量存储和相似度搜索。
7. 实现检索问答链。
8. 能用自己的知识库回答问题。

---

## 2. 什么是 RAG

RAG 的全称是 `Retrieval-Augmented Generation`，中文叫“检索增强生成”。

它的本质是：

> 先检索，再生成。

### 2.1 为什么需要 RAG

如果只靠大模型直接回答，可能会出现：

- 知识过时
- 胡乱编造
- 不能回答你的私有文档
- 无法引用准确资料

RAG 的作用就是让模型先从知识库里找相关内容，再根据这些内容回答。

### 2.2 RAG 的典型流程

```text
用户问题
  ↓
检索相关文档片段
  ↓
把问题 + 资料交给模型
  ↓
模型生成答案
```

---

## 3. 项目运行方式

### 3.1 安装依赖

```bash
pip install -r requirements.txt
```

### 3.2 配置环境变量

复制 `.env.example` 为 `.env`，然后填写：

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `MODEL_NAME`
- `EMBEDDING_MODEL`

如果你暂时不配置 API，也可以先运行离线版示例，项目会自动使用本地简化方案。

### 3.3 启动主程序

```bash
python main.py
```

---

## 4. 模块说明

### 4.1 `modules/loader.py`

负责从 `documents/` 目录读取文本。

### 4.2 `modules/splitter.py`

负责把长文本切成小块，避免上下文太长。

### 4.3 `modules/embeddings.py`

负责把文本转成向量。

### 4.4 `modules/vector_store.py`

负责存储向量，并根据问题找出最相关的内容。

### 4.5 `modules/retriever.py`

负责检索流程封装。

### 4.6 `modules/rag_chain.py`

负责把检索结果和问题拼接后生成答案。

---

## 5. 本项目的核心知识点

### 5.1 文档加载

先把本地文件内容读出来，再交给后续流程。

### 5.2 文本切分

长文档切成小块，便于检索。

### 5.3 Embedding

把文字转换成向量表示，便于计算相似度。

### 5.4 向量库

存储向量和原始文本块。

### 5.5 检索器

根据问题找出最相关的文档片段。

### 5.6 RAG Chain

整合“检索结果 + 用户问题 + 模型”生成答案。

---

## 6. 任务清单

### 任务 1：加载文档

要求：

- 能读取 `documents/` 下的文本
- 返回统一格式的文档对象

验收：

- 运行 `python 01_document_loader.py` 能看到加载结果

### 任务 2：切分文本

要求：

- 支持 chunk size
- 支持 overlap

验收：

- 运行 `python 02_text_splitter.py` 能看到切分后的文本块

### 任务 3：生成向量

要求：

- 文本块可以转成向量
- 向量长度一致

验收：

- 运行 `python 03_embeddings.py` 能看到向量样例

### 任务 4：构建向量库

要求：

- 保存文本块和向量
- 支持相似度搜索

验收：

- 运行 `python 04_vector_store.py` 能检索出相关文本

### 任务 5：实现检索器

要求：

- 输入问题
- 返回 Top-K 相关片段

验收：

- 运行 `python 05_retriever.py` 能看到检索结果

### 任务 6：实现 RAG 问答

要求：

- 把检索结果与问题结合
- 输出自然语言答案

验收：

- 运行 `python 06_rag_chain.py` 能得到完整问答

---

## 7. 练习说明

### 练习 1：加载不同文档格式

尝试把 `.md`、`.txt` 都纳入知识库。

### 练习 2：对比不同切分参数

对比 `chunk_size=100` 和 `chunk_size=300` 的效果。

### 练习 3：自定义知识库

把自己的学习笔记放进 `documents/`。

### 练习 4：多文档检索

同一个问题同时检索多个文档片段。

### 练习 5：RAG 效果评估

准备一组问答测试集，看看检索效果是否稳定。

---

## 8. 你应该学会的判断标准

如果你完成了 Day 15，你应该能回答：

- 为什么 RAG 比纯聊天更适合知识问答？
- 为什么要先切分文本？
- 为什么要先向量化再检索？
- 检索结果如何影响最终回答？

---

## 9. 总结

Day 15 是整个 RAG 项目的起点。

它的目标不是做一个复杂系统，而是先把最关键的链路跑通：

```text
文档 -> 切分 -> 向量 -> 检索 -> 生成
```

只要这条链路真正理解了，后面的向量数据库、文档问答、知识库 Agent 都会轻松很多。

