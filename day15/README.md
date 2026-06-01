# Day 15 - RAG 基础项目

> Day 15 的任务：学习并实现一个最小可运行的 RAG 系统。
>
> RAG 的完整英文是 `Retrieval-Augmented Generation`，中文常翻译成“检索增强生成”。
> 它的核心思想很简单：先从知识库里检索相关资料，再让模型根据资料回答问题。

---

## 1. 今天你要学会什么

Day 15 对应学习计划表里的任务是：`RAG 基础`。

这一天不是直接做复杂系统，而是先把 RAG 的最小链路跑通：

```text
本地文档
  -> 文档加载
  -> 文本切分
  -> 文本向量化
  -> 向量库存储
  -> 相似度检索
  -> 根据检索资料回答问题
```

完成这一天后，你应该能理解：

1. 什么是 RAG。
2. 为什么 RAG 需要先检索再回答。
3. 为什么要把长文档切成小块。
4. 什么是 Embedding。
5. 向量库是如何根据问题找资料的。
6. Retriever 和 RAGChain 分别负责什么。
7. 没有 API Key 时，如何用本地模拟方式先跑通流程。
8. 有 API Key 时，如何接入真实大模型生成回答。

---

## 2. 项目结构

```text
day15/
├── README.md
├── requirements.txt
├── .env.example
├── config.py
├── main.py
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
├── exercise5_rag_eval.py
├── documents/
│   ├── agent_guide.txt
│   ├── python_guide.txt
│   └── rag_guide.txt
└── modules/
    ├── __init__.py
    ├── loader.py
    ├── splitter.py
    ├── embeddings.py
    ├── vector_store.py
    ├── retriever.py
    └── rag_chain.py
```

---

## 3. 运行方式

### 3.1 安装依赖

在 `day15` 文件夹下运行：

```powershell
pip install -r requirements.txt
```

如果你已经安装过这些依赖，可以跳过。

### 3.2 配置 API Key

复制 `.env.example` 为 `.env`：

```powershell
copy .env.example .env
```

然后在 `.env` 里填写：

```env
OPENAI_API_KEY=你的 API Key
OPENAI_BASE_URL=https://api.deepseek.com
MODEL_NAME=deepseek-chat
EMBEDDING_MODEL=text-embedding-v3
CHUNK_SIZE=220
CHUNK_OVERLAP=50
TOP_K=3
```

如果你暂时没有 API Key，也可以直接运行。
项目会自动使用本地简化 Embedding 和离线回答方式，先帮你理解 RAG 的流程。

### 3.3 运行完整项目

```powershell
python main.py
```

### 3.4 分步骤运行

```powershell
python 01_document_loader.py
python 02_text_splitter.py
python 03_embeddings.py
python 04_vector_store.py
python 05_retriever.py
python 06_rag_chain.py
```

建议你第一次学习时按顺序运行，因为这正好对应 RAG 的数据流。

---

## 4. RAG 的核心原理

### 4.1 为什么不能只让大模型直接回答

如果直接问大模型，它可能出现这些问题：

1. 不知道你的本地文档内容。
2. 对公司内部资料、个人笔记、课程资料没有记忆。
3. 可能编造看似合理但实际错误的答案。
4. 无法告诉你答案来自哪份资料。
5. 模型知识可能过时。

RAG 的做法是：

```text
先查资料，再回答。
```

这就像你做开卷考试：

不是凭空编答案，而是先翻资料，找到相关内容，再组织回答。

### 4.2 RAG 的五个核心组件

第一个组件：文档加载器。

它负责把 `documents/` 里的资料读进程序。

第二个组件：文本切分器。

它负责把长文档切成更短的文本块。

第三个组件：Embedding 模型。

它负责把文本转换成数字向量。

第四个组件：向量库。

它负责保存文本块和向量，并计算相似度。

第五个组件：RAG 问答链。

它负责把检索结果和用户问题交给模型，生成最终答案。

---

## 5. 每个文件的详细解释

### 5.1 `config.py`

这个文件是 Day 15 的统一配置中心。

它做了这些事情：

1. 读取 `.env` 文件。
2. 获取 `OPENAI_API_KEY`。
3. 获取模型地址 `OPENAI_BASE_URL`。
4. 获取聊天模型名称 `MODEL_NAME`。
5. 获取 Embedding 模型名称 `EMBEDDING_MODEL`。
6. 设置文本切分长度 `CHUNK_SIZE`。
7. 设置文本重叠长度 `CHUNK_OVERLAP`。
8. 设置检索返回数量 `TOP_K`。

为什么要单独写配置文件？

因为这样后续所有文件都可以从 `config.py` 读取参数，不需要到处写死。

例如：

```python
from config import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K
```

如果你觉得文本块太短，就改 `CHUNK_SIZE`。
如果你觉得检索结果太少，就改 `TOP_K`。
不需要去每个 Python 文件里面找参数。

---

### 5.2 `documents/`

这个文件夹就是你的本地知识库。

当前包含三份示例资料：

1. `rag_guide.txt`：介绍 RAG 的基本概念。
2. `python_guide.txt`：介绍 Python 的特点。
3. `agent_guide.txt`：介绍 AI Agent 的作用。

你以后可以把自己的学习笔记放到这里。

当前加载器支持：

```text
.txt
.md
```

也就是说，你可以放纯文本文件，也可以放 Markdown 文件。

---

### 5.3 `modules/loader.py`

这个文件负责“加载文档”。

核心类是：

```python
DocumentItem
```

它包含两个字段：

```python
page_content: str
metadata: dict
```

`page_content` 保存正文内容。

`metadata` 保存文档来源，例如：

```python
{
    "source": "rag_guide.txt",
    "path": "D:/vscode项目/学习/day15/documents/rag_guide.txt"
}
```

核心函数是：

```python
load_documents(docs_dir: str)
```

它会：

1. 检查文档目录是否存在。
2. 遍历目录下所有文件。
3. 只读取 `.txt` 和 `.md` 文件。
4. 自动尝试 `utf-8`、`utf-8-sig`、`gbk` 编码。
5. 跳过空文件。
6. 把每份文档包装成 `DocumentItem`。

为什么要处理不同编码？

因为中文 Windows 环境里，有些文件可能是 `gbk`，有些是 `utf-8`。
如果不兼容，读取中文文档时容易出现乱码。

---

### 5.4 `01_document_loader.py`

这个文件是文档加载演示脚本。

运行：

```powershell
python 01_document_loader.py
```

它会：

1. 找到 `documents/` 文件夹。
2. 调用 `load_documents()`。
3. 打印加载到的文档数量。
4. 打印每份文档的文件名和前 80 个字符。

这个文件的作用是验证：

```text
你的知识库资料是否成功进入程序。
```

如果这里加载不到文档，后面的切分、向量化、检索都会没有数据。

---

### 5.5 `modules/splitter.py`

这个文件负责“文本切分”。

核心函数有两个：

```python
split_text(text, chunk_size, chunk_overlap)
split_documents(documents, chunk_size, chunk_overlap)
```

`split_text()` 处理一段文本。

`split_documents()` 处理多篇文档。

为什么要切分文本？

因为一整篇文档通常太长：

1. 不适合全部放进模型上下文。
2. 检索时粒度太粗。
3. 用户问题通常只和文档中的一小段有关。

切分后，系统可以只把最相关的几个小片段拿出来。

`chunk_size` 的意思：

```text
每个文本块最多保留多少字符。
```

`chunk_overlap` 的意思：

```text
相邻文本块之间重复保留多少字符。
```

为什么需要 overlap？

因为切分可能刚好把一句话切断。
保留一点重叠内容，可以减少上下文丢失。

举例：

```text
原文：RAG 是检索增强生成，它会先检索资料，再生成答案。
```

如果切得太硬，可能变成：

```text
块 1：RAG 是检索增强生成，它会先检索
块 2：资料，再生成答案。
```

有 overlap 后可能变成：

```text
块 1：RAG 是检索增强生成，它会先检索
块 2：先检索资料，再生成答案。
```

这样第二块也能保留上下文。

---

### 5.6 `02_text_splitter.py`

这个文件是文本切分演示脚本。

运行：

```powershell
python 02_text_splitter.py
```

它会：

1. 加载 `documents/` 下的文档。
2. 使用 `config.py` 中的 `CHUNK_SIZE` 和 `CHUNK_OVERLAP`。
3. 把文档切成多个 chunk。
4. 打印原始文档数量。
5. 打印切分后的文本块数量。
6. 展示前 5 个文本块。

你可以通过修改 `config.py` 来观察切分效果。

推荐实验：

```python
CHUNK_SIZE = 100
CHUNK_OVERLAP = 20
```

然后再试：

```python
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
```

你会发现：

1. `CHUNK_SIZE` 越小，文本块越多。
2. `CHUNK_SIZE` 越大，文本块越少。
3. `CHUNK_OVERLAP` 越大，相邻文本块重复内容越多。

---

### 5.7 `modules/embeddings.py`

这个文件负责“文本向量化”。

Embedding 是 RAG 的关键概念。

简单说：

```text
Embedding = 把文字变成一组数字。
```

比如：

```text
"什么是 RAG？"
```

可能会被转换成：

```text
[0.13, 0.02, 0.00, 0.31, ...]
```

向量有什么用？

因为计算机更擅长比较数字。
当问题和文档都变成向量后，就可以计算它们的相似度。

本项目提供两种 Embedding：

第一种：真实 Embedding API。

如果你配置了 `OPENAI_API_KEY`，程序会尝试使用：

```python
OpenAIEmbeddings
```

第二种：本地简化 Embedding。

如果没有 API Key，程序会使用：

```python
SimpleEmbeddingModel
```

本地模型的原理：

1. 用正则把文本拆成 token。
2. 用 md5 把 token 映射到固定向量位置。
3. 统计每个位置出现次数。
4. 对向量做归一化。

注意：

本地简化模型不是生产级语义模型。
它的目的只是帮助你理解 RAG 流程，不是为了获得最强检索效果。

---

### 5.8 `03_embeddings.py`

这个文件是 Embedding 演示脚本。

运行：

```powershell
python 03_embeddings.py
```

它会：

1. 获取 Embedding 模型。
2. 把示例文本 `Python 是一门高级编程语言` 转成向量。
3. 打印向量长度。
4. 打印前 10 维向量值。

这个文件帮助你看到：

```text
文字真的可以变成数字列表。
```

---

### 5.9 `modules/vector_store.py`

这个文件实现了一个最小版向量库。

真实项目中你可能会用：

1. FAISS
2. Chroma
3. Milvus
4. Pinecone
5. Weaviate

但是 Day 15 为了让你理解底层原理，自己写了一个简单版本。

核心函数：

```python
_cosine_similarity(a, b)
```

它计算两个向量的余弦相似度。

余弦相似度越高，说明两个向量方向越接近。
在 RAG 里通常表示两段文本语义越相似。

核心类：

```python
SimpleVectorStore
```

它有两个列表：

```python
self.documents
self.vectors
```

`self.documents` 保存文本块。

`self.vectors` 保存对应向量。

这两个列表的顺序是一一对应的。

例如：

```text
documents[0] 对应 vectors[0]
documents[1] 对应 vectors[1]
documents[2] 对应 vectors[2]
```

核心方法：

```python
add_documents(documents)
```

作用是把文本块加入向量库。

核心方法：

```python
similarity_search(query, k=3)
```

作用是：

1. 把用户问题转成向量。
2. 遍历所有文档向量。
3. 计算问题向量和文档向量的相似度。
4. 按相似度从高到低排序。
5. 返回前 k 个结果。

---

### 5.10 `04_vector_store.py`

这个文件是向量库演示脚本。

运行：

```powershell
python 04_vector_store.py
```

它会：

1. 加载文档。
2. 切分文档。
3. 获取 Embedding 模型。
4. 创建向量库。
5. 把文本块加入向量库。
6. 用问题 `什么是 RAG？` 做相似度搜索。
7. 打印 Top 3 检索结果。

你需要重点看输出里的：

```text
score
source
page_content
```

`score` 是相似度分数。

`source` 是结果来自哪个文件。

`page_content` 是被检索出来的文本块内容。

---

### 5.11 `modules/retriever.py`

这个文件实现检索器。

它很短，但很重要。

为什么需要 Retriever？

因为 RAGChain 不应该直接关心底层向量库怎么搜索。
它只需要知道：

```python
retriever.retrieve(question)
```

这样代码层次会更清楚。

当前 `Retriever` 做的事情：

1. 保存一个 `SimpleVectorStore`。
2. 保存一个 `top_k`。
3. 调用向量库的 `similarity_search()`。
4. 返回检索结果。

---

### 5.12 `05_retriever.py`

这个文件是检索器演示脚本。

运行：

```powershell
python 05_retriever.py
```

它会：

1. 加载文档。
2. 切分文本。
3. 构建向量库。
4. 创建 Retriever。
5. 用问题 `为什么要切分文本？` 检索资料。
6. 打印 Top-K 检索结果。

这个文件对应 RAG 里的：

```text
Retrieve
```

也就是“检索”。

---

### 5.13 `modules/rag_chain.py`

这个文件实现最终问答链。

它是 Day 15 最重要的文件之一。

核心类：

```python
RAGChain
```

它负责：

1. 接收用户问题。
2. 调用 Retriever 检索资料。
3. 把资料整理成上下文。
4. 如果有真实 LLM，就调用模型回答。
5. 如果没有真实 LLM，就使用离线回答。

核心方法：

```python
answer(question)
```

内部流程：

```text
用户问题
  -> retriever.retrieve(question)
  -> 得到相关文档片段
  -> 拼接 context
  -> 如果有大模型：交给大模型生成答案
  -> 如果没有大模型：直接返回检索资料整理结果
```

为什么 Prompt 里写“只根据资料回答”？

因为 RAG 的目的就是降低幻觉。
如果模型不受约束，它可能又开始凭自己的知识乱说。

当前 Prompt 要求：

1. 只根据资料回答。
2. 如果资料不足，明确说明。
3. 语言自然、简洁、准确。

---

### 5.14 `06_rag_chain.py`

这个文件是完整 RAG Chain 演示脚本。

运行：

```powershell
python 06_rag_chain.py
```

它会问三个示例问题：

1. 什么是 RAG？
2. Python 的特点是什么？
3. AI Agent 有什么作用？

每个问题都会经过：

```text
检索资料 -> 组织上下文 -> 生成回答
```

如果没有 API Key，输出会包含检索到的资料和离线说明。

如果配置了 API Key，输出会是模型根据资料生成的自然语言回答。

---

### 5.15 `main.py`

这是 Day 15 的主入口文件。

如果你不知道先运行哪个，就运行它：

```powershell
python main.py
```

它做了完整系统构建：

```python
build_rag_system()
```

内部步骤：

1. 找到 `documents/`。
2. 加载文档。
3. 切分文本。
4. 获取 Embedding 模型。
5. 创建向量库。
6. 写入文本块。
7. 创建 Retriever。
8. 创建 RAGChain。
9. 返回完整问答系统。

然后 `main()` 会打印：

1. 已加载文档数量。
2. 已切分文本块数量。
3. 示例问题回答结果。

---

### 5.16 `requirements.txt`

这个文件列出 Day 15 需要的 Python 包。

一般包括：

```text
python-dotenv
langchain
langchain-openai
```

说明：

1. `python-dotenv` 用来读取 `.env`。
2. `langchain` 用来组织 Prompt、模型和输出解析。
3. `langchain-openai` 用来调用兼容 OpenAI 格式的模型和 Embedding。

即使你没有 API Key，本项目也能先用本地模式运行。

---

### 5.17 `.env.example`

这个文件是环境变量模板。

它不会自动生效。

你需要复制成 `.env`：

```powershell
copy .env.example .env
```

然后填写真实 API Key。

为什么不直接把 Key 写进代码？

因为 API Key 属于敏感信息。
正确做法是放到 `.env`，不要写进 Python 文件，也不要提交到 GitHub。

---

## 6. 练习题专区

下面是 Day 15 的完整练习题。

以后每天的 README 都会按这个格式写：

```text
练习题编号
  -> 练习目标
  -> 题目要求
  -> 操作提示
  -> 参考答案
  -> 如何运行
  -> 你应该观察什么结果
```

这样你不是只知道“运行哪个文件”，而是能知道“为什么要做这个练习、做完应该看到什么、答案为什么这样写”。

### 6.1 练习 1：加载不同格式文档

文件：

```text
exercise1_load_docs.py
```

练习目标：

学会把本地资料放进知识库目录，并确认程序可以读取这些资料。

任务：

把 `.txt` 或 `.md` 文档放进 `documents/`，然后检查能否加载。

题目要求：

1. 在 `documents/` 文件夹中新建一个 `.txt` 或 `.md` 文件。
2. 文件中写入几句自己的学习笔记。
3. 运行文档加载脚本。
4. 观察终端是否打印出新增文件。

操作提示：

你可以新建一个文件：

```text
documents/my_notes.txt
```

内容示例：

```text
RAG 是一种先检索资料，再根据资料生成答案的方法。
它适合用来做企业知识库、学习助手和文档问答系统。
```

答案：

1. `loader.py` 已支持 `.txt` 和 `.md`。
2. 把文件放到 `day15/documents/`。
3. 运行 `python 01_document_loader.py`。
4. 如果终端显示文件名和内容预览，说明成功。

这个答案已经写在 `exercise1_load_docs.py` 后面，并且加了中文说明。

如何运行：

```powershell
python exercise1_load_docs.py
python 01_document_loader.py
```

你应该观察到：

1. `exercise1_load_docs.py` 会打印练习答案。
2. `01_document_loader.py` 会打印加载到的文档数量。
3. 如果你新增了文档，输出里应该能看到新增文件名。

---

### 6.2 练习 2：对比不同切分参数

文件：

```text
exercise2_split_compare.py
```

练习目标：

理解 `CHUNK_SIZE` 和 `CHUNK_OVERLAP` 对切分结果的影响。

任务：

对比不同 `CHUNK_SIZE` 和 `CHUNK_OVERLAP` 的效果。

题目要求：

1. 打开 `config.py`。
2. 把 `CHUNK_SIZE` 改成较小的值，例如 `100`。
3. 运行 `python 02_text_splitter.py`。
4. 再把 `CHUNK_SIZE` 改成较大的值，例如 `300`。
5. 再运行一次，比较两次结果。

操作提示：

重点观察这两项：

```text
原始文档数量
切分后文本块数量
```

答案：

1. 把 `CHUNK_SIZE` 改成 100，运行 `python 02_text_splitter.py`。
2. 把 `CHUNK_SIZE` 改成 300，再运行一次。
3. 对比输出的 chunk 数量和内容完整度。

结论：

1. `CHUNK_SIZE` 越小，文本块越多，检索更细，但上下文更碎。
2. `CHUNK_SIZE` 越大，文本块越少，上下文更完整，但可能夹杂无关信息。
3. `CHUNK_OVERLAP` 越大，上下文越连续，但重复内容越多。

这个答案已经写在 `exercise2_split_compare.py` 后面。

如何运行：

```powershell
python exercise2_split_compare.py
python 02_text_splitter.py
```

你应该观察到：

1. 小 `CHUNK_SIZE` 会产生更多 chunk。
2. 大 `CHUNK_SIZE` 会产生更少 chunk。
3. 设置 overlap 后，前后 chunk 中会出现一部分重复内容。

---

### 6.3 练习 3：自定义知识库

文件：

```text
exercise3_custom_kb.py
```

练习目标：

把自己的资料接入 RAG，让程序不只回答示例文档的问题，也能回答你的个人笔记问题。

任务：

把自己的学习笔记放入知识库。

题目要求：

1. 在 `documents/` 中新建一份自己的笔记。
2. 笔记内容可以是 Python、RAG、Agent 或任意课程内容。
3. 修改 `06_rag_chain.py` 中的示例问题，问一个和你笔记相关的问题。
4. 运行脚本，观察是否能检索到你的笔记。

操作提示：

例如你新增：

```text
documents/my_agent_notes.txt
```

内容写：

```text
Agent 的核心能力是根据任务选择工具，并把工具结果整理成最终答案。
```

然后可以把问题改成：

```python
"Agent 的核心能力是什么？"
```

答案：

1. 新建 `my_notes.txt` 或 `my_notes.md`。
2. 把自己的学习内容写进去。
3. 放到 `day15/documents/`。
4. 运行 `python 06_rag_chain.py`。
5. 提一个和笔记有关的问题。

这个答案已经写在 `exercise3_custom_kb.py` 后面。

如何运行：

```powershell
python exercise3_custom_kb.py
python 06_rag_chain.py
```

你应该观察到：

1. 如果问题和你的笔记相关，检索结果中应该出现你的文件名。
2. 如果没有出现，可能是问题措辞和笔记内容差距太大。
3. 可以尝试把问题改得更接近文档原文。

---

### 6.4 练习 4：多文档检索

文件：

```text
exercise4_multi_doc.py
```

练习目标：

理解 RAG 检索不是按“文件”查找，而是按“文本块相似度”查找。

任务：

观察一个问题如何从多份文档中检索相关内容。

题目要求：

1. 保留 `rag_guide.txt`、`python_guide.txt`、`agent_guide.txt` 三份文档。
2. 运行 `05_retriever.py`。
3. 观察 Top-K 结果分别来自哪些文件。
4. 判断检索结果是否和问题相关。

操作提示：

输出里重点看：

```text
Top 1
score
source
```

`source` 表示结果来自哪个文件。

`score` 表示相似度分数。

答案：

1. 在 `documents/` 下准备多份不同主题文档。
2. 运行 `python 05_retriever.py`。
3. 查看每条结果的 `source`。
4. 判断结果来自哪份文档。

结论：

向量库不会按文件名搜索。
它会把所有 chunk 放在一起，根据相似度排序。

这个答案已经写在 `exercise4_multi_doc.py` 后面。

如何运行：

```powershell
python exercise4_multi_doc.py
python 05_retriever.py
```

你应该观察到：

1. 检索结果可能来自不同文件。
2. 相似度最高的结果会排在最前面。
3. 本地简化 Embedding 不一定完全准确，所以重点理解流程。

---

### 6.5 练习 5：RAG 效果评估

文件：

```text
exercise5_rag_eval.py
```

练习目标：

学会用一组测试问题判断 RAG 系统是否好用。

任务：

准备多个问题测试 RAG 效果。

题目要求：

准备至少 3 个问题：

```text
1. 什么是 RAG？
2. Python 的特点是什么？
3. AI Agent 有什么作用？
```

然后运行完整问答链，观察：

1. 是否检索到了正确文件。
2. 是否找到了包含答案的文本块。
3. 回答是否只根据资料生成。
4. 资料不足时是否明确说明。

操作提示：

如果你想做得更认真，可以自己做一个表格：

```text
问题 | 期望来源 | 实际来源 | 是否正确 | 备注
```

答案：

1. 准备 3 到 5 个问题。
2. 运行 `python main.py` 或 `python 06_rag_chain.py`。
3. 观察回答是否引用了正确资料。
4. 如果回答不稳定，优先检查文档内容、切分参数和 `TOP_K`。

评估 RAG 时，不要只看回答是否通顺。
更重要的是看：

1. 检索来源是否正确。
2. 检索片段是否包含答案。
3. 模型有没有根据资料回答。
4. 资料不足时有没有明确说明。

这个答案已经写在 `exercise5_rag_eval.py` 后面。

如何运行：

```powershell
python exercise5_rag_eval.py
python main.py
```

你应该观察到：

1. RAG 不是只看最终回答，还要看检索来源。
2. 如果 Top 1 来源不对，最终回答很可能也会偏。
3. 如果资料本身没有答案，模型不应该硬编。

---

## 7. 练习题对应文件答案说明

Day 15 的练习题答案不仅写在 README 里，也写进了对应的练习文件后面。

对应关系如下：

```text
练习 1 -> exercise1_load_docs.py
练习 2 -> exercise2_split_compare.py
练习 3 -> exercise3_custom_kb.py
练习 4 -> exercise4_multi_doc.py
练习 5 -> exercise5_rag_eval.py
```

你可以直接运行每个练习文件查看答案提示：

```powershell
python exercise1_load_docs.py
python exercise2_split_compare.py
python exercise3_custom_kb.py
python exercise4_multi_doc.py
python exercise5_rag_eval.py
```

这些练习文件本身不会破坏项目，只会打印题目答案和操作步骤。

---

## 8. API Key 与本地模式说明

这个项目支持两种运行模式。

### 8.1 没有 API Key

如果没有配置 `OPENAI_API_KEY`：

1. Embedding 使用本地 `SimpleEmbeddingModel`。
2. RAGChain 使用 `_fallback_answer()`。
3. 程序不会调用真实大模型。
4. 你仍然可以看到完整 RAG 流程。

适合：

1. 学习阶段。
2. 离线演示。
3. 检查代码逻辑。
4. 避免 API 费用。

### 8.2 有 API Key

如果配置了 `OPENAI_API_KEY`：

1. Embedding 会优先尝试使用真实 Embedding API。
2. RAGChain 会优先尝试使用真实聊天模型。
3. 最终回答会更自然。

适合：

1. 做真实 RAG 问答项目。
2. 测试模型回答质量。
3. 为 Day 18、Day 20 的项目打基础。

---

## 9. 常见问题

### 9.1 为什么运行时没有调用真实模型

可能原因：

1. 没有创建 `.env`。
2. `.env` 里没有写 `OPENAI_API_KEY`。
3. API Key 写错了。
4. `langchain-openai` 没安装。
5. 网络不可用。
6. `OPENAI_BASE_URL` 和模型供应商不匹配。

项目会自动回退到本地模式，所以不会直接崩溃。

---

### 9.2 为什么检索结果看起来不够准确

可能原因：

1. 本地简化 Embedding 不是高质量语义模型。
2. 文档内容太少。
3. 问题和文档措辞差异太大。
4. `CHUNK_SIZE` 设置不合适。
5. `TOP_K` 太小。

改进方式：

1. 配置真实 Embedding API。
2. 增加更多高质量文档。
3. 调整 `CHUNK_SIZE`。
4. 调整 `CHUNK_OVERLAP`。
5. 调整 `TOP_K`。

---

### 9.3 为什么要把文档切分，而不是整篇放进去

原因：

1. 模型上下文长度有限。
2. 整篇文档可能包含很多无关内容。
3. 检索粒度太粗会影响准确性。
4. 小块文本更容易匹配具体问题。

---

### 9.4 为什么需要 metadata

metadata 可以保存来源信息。

例如：

```python
metadata={
    "source": "rag_guide.txt",
    "path": "...",
    "chunk_index": 2
}
```

有了 metadata，你就知道：

1. 答案来自哪个文件。
2. 来自第几个文本块。
3. 后续可以做引用来源。
4. 方便调试检索质量。

---

## 10. 推荐学习顺序

建议按下面顺序学习：

1. 先读 `README.md`。
2. 运行 `python 01_document_loader.py`。
3. 打开 `modules/loader.py` 看文档加载逻辑。
4. 运行 `python 02_text_splitter.py`。
5. 打开 `modules/splitter.py` 看切分逻辑。
6. 运行 `python 03_embeddings.py`。
7. 打开 `modules/embeddings.py` 看向量化逻辑。
8. 运行 `python 04_vector_store.py`。
9. 打开 `modules/vector_store.py` 看相似度搜索。
10. 运行 `python 05_retriever.py`。
11. 打开 `modules/retriever.py` 看检索封装。
12. 运行 `python 06_rag_chain.py`。
13. 打开 `modules/rag_chain.py` 看最终问答链。
14. 最后运行 `python main.py` 看完整效果。

---

## 11. Day 15 总结

Day 15 的重点不是追求复杂，而是理解 RAG 的骨架。

你现在已经有了一个最小可运行的 RAG 项目：

```text
documents/
  -> loader.py
  -> splitter.py
  -> embeddings.py
  -> vector_store.py
  -> retriever.py
  -> rag_chain.py
  -> main.py
```

这条链路跑通后，后面的内容就会更容易理解：

1. Day 16 的向量数据库。
2. Day 17 的文档加载与切分。
3. Day 18 的 RAG 检索链。
4. Day 20 的 RAG 问答系统。

一句话记住 Day 15：

```text
RAG = 先从知识库找资料，再让模型根据资料回答。
```
