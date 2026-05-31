# Day 12 - RAG 检索增强生成：让 AI 基于你的文档回答

> **学习目标：** 掌握 RAG（Retrieval Augmented Generation）的完整流程，构建基于文档的智能问答系统。
>
> **预计阅读时间：** 30+ 分钟

---

## 目录

1. [什么是 RAG](#1-什么是-rag)
2. [RAG 的核心流程](#2-rag-的核心流程)
3. [文档加载器](#3-文档加载器)
4. [文本分割器](#4-文本分割器)
5. [向量嵌入](#5-向量嵌入)
6. [向量数据库](#6-向量数据库)
7. [检索器](#7-检索器)
8. [RAG Chain](#8-rag-chain)
9. [综合实践](#9-综合实践)
10. [最佳实践](#10-最佳实践)
11. [常见问题](#11-常见问题)
12. [知识总结](#12-知识总结)
13. [练习题](#13-练习题)

---

## 1. 什么是 RAG

### 1.1 一句话解释

**RAG = 检索 + 增强 + 生成** -- 让 AI 先从你的文档中找到相关信息，再基于这些信息回答问题。

### 1.2 为什么需要 RAG

| 问题 | 没有 RAG | 有 RAG |
|------|---------|--------|
| 知识截止 | LLM 只知道训练数据 | 可以访问最新文档 |
| 幻觉 | LLM 可能编造信息 | 基于真实文档回答 |
| 私有知识 | LLM 不知道公司内部信息 | 可以索引内部文档 |
| 准确性 | 泛泛而谈 | 精确引用文档内容 |

### 1.3 生活中的类比

```
没有 RAG 的 LLM：
  你：我们公司的请假流程是什么？
  AI：一般来说，请假流程是...（猜测，不准确）

有 RAG 的 LLM：
  你：我们公司的请假流程是什么？
  AI：[检索到公司手册] 根据员工手册第3章，请假流程如下：...（准确）
```

---

## 2. RAG 的核心流程

### 2.1 完整流程图

```
[离线索引阶段]

文档 -> 加载器 -> 文本 -> 分割器 -> 文本块 -> 嵌入模型 -> 向量 -> 向量数据库

[在线查询阶段]

用户问题 -> 嵌入模型 -> 查询向量 -> 向量数据库检索 -> 相关文档
                                                                      |
用户问题 + 相关文档 -> Prompt 模板 -> LLM -> 最终回答
```

### 2.2 六大组件

| 组件 | 作用 | 对应文件 |
|------|------|---------|
| Document Loader | 加载各种格式的文档 | 01_document_loader.py |
| Text Splitter | 将长文档切分成小块 | 02_text_splitter.py |
| Embedding | 将文本转换为向量 | 03_embeddings.py |
| Vector Store | 存储和检索向量 | 04_vector_store.py |
| Retriever | 从向量库中查找相关文档 | 05_retriever.py |
| RAG Chain | 整合检索和生成 | 06_rag_chain.py |

---

## 3. 文档加载器

> 对应文件：01_document_loader.py

### 3.1 Document 对象

```python
from langchain_core.documents import Document

doc = Document(
    page_content="Python 是一种编程语言",  # 文档内容
    metadata={"source": "wiki", "page": 1}  # 元数据
)
```

### 3.2 常用加载器

| 格式 | 加载器 | 说明 |
|------|--------|------|
| TXT | TextLoader | 纯文本 |
| PDF | PyPDFLoader | PDF 文档 |
| DOCX | Docx2txtLoader | Word 文档 |
| CSV | CSVLoader | CSV 表格 |
| HTML | BSHTMLLoader | 网页 |
| 目录 | DirectoryLoader | 批量加载 |

---

## 4. 文本分割器

> 对应文件：02_text_splitter.py

### 4.1 为什么要分割

```
LLM 有 Token 限制（如 4096、8192）
一篇长文档可能超过限制 -> 必须切分成小块

分割的好处：
  1. 适应 LLM 的上下文窗口
  2. 提高检索精度（只返回相关段落）
  3. 减少无关信息的干扰
```

### 4.2 分割参数

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| chunk_size | 每个块的最大字符数 | 200-500（中文）|
| chunk_overlap | 块之间的重叠字符数 | chunk_size 的 10%-20% |

### 4.3 推荐分割器

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "，", " ", ""]
)
chunks = splitter.split_text(text)
```

---

## 5. 向量嵌入

> 对应文件：03_embeddings.py

### 5.1 什么是 Embedding

```
Embedding 将文本映射到高维向量空间：

"猫"  -> [0.2, 0.8, -0.1, ...]  (1536 维)
"狗"  -> [0.3, 0.7, -0.2, ...]  (1536 维)
"汽车" -> [-0.5, 0.1, 0.9, ...] (1536 维)

语义相似的文本，向量距离更近
```

### 5.2 使用 Embedding 模型

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-v3")
vector = embeddings.embed_query("Python 是什么")
# 返回 1536 维的浮点数列表
```

### 5.3 余弦相似度

| 相似度 | 含义 |
|--------|------|
| 1.0 | 完全相同 |
| 0.8+ | 高度相似 |
| 0.5-0.8 | 有关联 |
| <0.5 | 关联弱 |

---

## 6. 向量数据库

> 对应文件：04_vector_store.py

### 6.1 常用向量数据库

| 数据库 | 特点 | 适用场景 |
|--------|------|---------|
| ChromaDB | 轻量级，本地开发 | 学习和原型 |
| FAISS | Facebook 开源，高性能 | 大规模数据 |
| Pinecone | 云端托管 | 生产环境 |
| Weaviate | 开源，功能丰富 | 复杂需求 |

### 6.2 使用 ChromaDB

```python
from langchain_community.vectorstores import Chroma

# 存入文档
vectorstore = Chroma.from_documents(docs, embeddings)

# 检索
results = vectorstore.similarity_search("Python 特点", k=3)

# 带分数的检索
results = vectorstore.similarity_search_with_score("Python 特点", k=3)
```

---

## 7. 检索器

> 对应文件：05_retriever.py

### 7.1 检索策略

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| similarity | 普通相似度检索 | 大多数场景 |
| MMR | 最大边际相关性 | 需要多样化结果 |

### 7.2 MMR 检索

```python
# 普通检索：可能返回高度重复的结果
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# MMR 检索：在相关性和多样性之间平衡
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 10, "lambda_mult": 0.5}
)
```

---

## 8. RAG Chain

> 对应文件：06_rag_chain.py

### 8.1 完整 RAG Chain

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# RAG 提示词
prompt = ChatPromptTemplate.from_template(
    "根据以下上下文回答问题：\n\n"
    "上下文：{context}\n\n"
    "问题：{question}\n\n回答："
)

# 构建 Chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 使用
answer = rag_chain.invoke("Python 有什么特点？")
```

### 8.2 RAG vs 直接问答

| 对比 | 直接问 LLM | RAG |
|------|-----------|-----|
| 知识来源 | 训练数据 | 你的文档 |
| 准确性 | 可能有幻觉 | 基于真实文档 |
| 可追溯 | 无法引用 | 可以引用来源 |
| 更新 | 需要重新训练 | 只需更新文档 |

---

## 9. 综合实践

> 对应文件：main.py

```bash
python main.py
```

| 命令 | 说明 |
|------|------|
| 直接输入 | 基于文档提问 |
| search | 只检索文档 |
| docs | 查看已加载文档 |
| example | 示例问题 |
| q | 退出 |

---

## 10. 最佳实践

1. **chunk_size**: 200-500（中文）或 500-1000（英文）
2. **chunk_overlap**: chunk_size 的 10%-20%
3. **检索数量 k**: 3-5 个结果通常足够
4. **使用 MMR**: 需要多样化结果时
5. **来源引用**: 让 LLM 引用文档来源
6. **定期更新**: 文档变化时重建向量库

---

## 11. 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 检索不到相关内容 | chunk_size 太大 | 减小 chunk_size |
| 回答不完整 | chunk_size 太小 | 增大 chunk_size 或 k |
| 回答有幻觉 | 检索不准确 | 优化 Embedding 模型 |
| 速度慢 | 向量库太大 | 使用 FAISS 或索引优化 |

---

## 12. 知识总结

### 12.1 学习路线

```
Day 8: LangChain 入门
Day 9: Memory 记忆
Day 10: Tools 工具
Day 11: Agents 代理
Day 12: RAG 检索增强生成 <- 你在这里
  +-- 文档加载器（Document Loader）
  +-- 文本分割器（Text Splitter）
  +-- 向量嵌入（Embedding）
  +-- 向量数据库（Vector Store）
  +-- 检索器（Retriever）
  +-- RAG Chain
```

### 12.2 文件清单

```
day12/
+-- config.py                  # 配置文件
+-- main.py                    # RAG 文档问答助手
+-- 01_document_loader.py      # 文档加载器
+-- 02_text_splitter.py        # 文本分割器
+-- 03_embeddings.py           # 向量嵌入
+-- 04_vector_store.py         # 向量数据库
+-- 05_retriever.py            # 检索器
+-- 06_rag_chain.py            # RAG Chain
+-- exercise1_doc_formats.py   # 练习1：文档格式
+-- exercise2_split_compare.py # 练习2：分割对比
+-- exercise3_custom_kb.py     # 练习3：自定义知识库
+-- exercise4_multi_doc.py     # 练习4：多文档问答
+-- exercise5_rag_eval.py      # 练习5：RAG 评估
+-- documents/                 # 示例文档
+-- .env / config.py / requirements.txt
```

---

## 13. 练习题

### 练习 1：基础（10 分钟）
加载不同格式的文档，对比 Document 对象的结构。

### 练习 2：中等（20 分钟）
对比不同 chunk_size 和 chunk_overlap 的分割效果。

### 练习 3：进阶（30 分钟）
创建自定义知识库，构建 RAG 问答系统。

### 练习 4：挑战（60 分钟）
构建多文档智能问答系统，支持来源引用。

### 练习 5：综合（90 分钟）
评估不同 RAG 配置的效果，找到最优参数。

---

> **明天预告：** Day 13 - 项目实战，综合运用所有知识构建完整的 AI 应用。
