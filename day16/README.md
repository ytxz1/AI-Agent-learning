# Day 16 - 向量数据库

> Day 16 的任务：理解并实现一个轻量级向量数据库。
>
> Day 15 已经跑通了 RAG 的完整流程，Day 16 专门把其中最重要的一段拆开讲清楚：
>
> ```text
> 文本块 -> Embedding 向量 -> 向量库保存 -> 相似度检索 -> Top-K 返回
> ```

---

## 1. 今天你要学会什么

Day 16 对应学习计划表里的任务是：`向量数据库`。

完成这一天后，你应该能理解：

1. 什么是向量数据库。
2. 为什么 RAG 需要向量数据库。
3. 文本为什么要先变成 Embedding。
4. 向量库里到底保存了什么。
5. 什么是相似度搜索。
6. 什么是 Top-K。
7. 什么是 metadata。
8. 如何按来源文件过滤检索结果。
9. 如何把向量库保存到磁盘。
10. 没有 API Key 时如何使用本地 Embedding 兜底。
11. 有 API Key 时如何优先使用在线 Embedding。

---

## 2. 项目结构

```text
day16/
├── README.md
├── requirements.txt
├── .env.example
├── config.py
├── main.py
├── 01_store_chunks.py
├── 02_similarity_search.py
├── 03_metadata_filter.py
├── 04_topk_compare.py
├── 05_persistent_db.py
├── documents/
│   ├── ai_agents_notes.txt
│   ├── rag_notes.txt
│   └── vector_db_notes.txt
└── modules/
    ├── __init__.py
    ├── embeddings.py
    ├── loader.py
    ├── splitter.py
    ├── vector_store.py
    └── search_demo.py
```

这个结构和 Day 15 很像，但 Day 16 的重点更集中：

```text
不是完整 RAG 问答，而是重点研究“向量存储和检索”。
```

---

## 3. 运行方式

### 3.1 安装依赖

在 `day16` 文件夹下运行：

```powershell
pip install -r requirements.txt
```

### 3.2 配置 API Key

复制 `.env.example` 为 `.env`：

```powershell
copy .env.example .env
```

然后填写：

```env
OPENAI_API_KEY=你的 API Key
OPENAI_BASE_URL=https://api.deepseek.com
EMBEDDING_MODEL=text-embedding-v3
CHUNK_SIZE=240
CHUNK_OVERLAP=60
TOP_K=3
EMBEDDING_DIM=128
VECTOR_DB_FILE=D:/vscode项目/学习/day16/vector_db.json
```

如果你没有 API Key，也可以直接运行。

项目会自动使用本地 `SimpleEmbeddingModel`，保证学习过程不断掉。

### 3.3 运行完整命令行程序

```powershell
python main.py
```

进入程序后可以输入：

```text
build
search 什么是 RAG？
search 向量数据库有什么作用？
search:source=rag_notes.txt 什么是检索增强生成？
stats
save
load
demo
q
```

### 3.4 分步骤运行练习脚本

```powershell
python 01_store_chunks.py
python 02_similarity_search.py
python 03_metadata_filter.py
python 04_topk_compare.py
python 05_persistent_db.py
```

建议第一次学习时按顺序运行。

---

## 4. 向量数据库的核心原理

### 4.1 普通数据库和向量数据库有什么不同

普通数据库擅长：

1. 精确查询。
2. 条件过滤。
3. 表格数据。
4. 事务处理。

例如：

```sql
SELECT * FROM users WHERE age > 18;
```

向量数据库擅长：

1. 语义相似度搜索。
2. 模糊匹配。
3. 高维向量检索。
4. 找“意思接近”的内容。

例如用户问：

```text
什么是检索增强生成？
```

向量数据库可能找到包含下面内容的文本：

```text
RAG 是 Retrieval-Augmented Generation 的缩写。
```

即使问题里没有直接写 `RAG`，也可能通过语义找到相关内容。

### 4.2 向量数据库里保存什么

本项目里的向量库保存三类信息：

```text
文本块原文
metadata 来源信息
vector 文本向量
```

对应代码里的数据结构是：

```python
VectorRecord(
    page_content="文本块内容",
    metadata={"source": "rag_notes.txt", "chunk_index": 0},
    vector=[0.1, 0.0, 0.2, ...],
)
```

为什么不能只保存向量？

因为检索出来以后，你还需要知道：

1. 原文是什么。
2. 来自哪个文件。
3. 是第几个文本块。
4. 后续要把哪些资料交给大模型。

### 4.3 什么是相似度搜索

相似度搜索的流程：

```text
用户问题
  -> 转成问题向量
  -> 和向量库里的每个文档向量计算相似度
  -> 按分数从高到低排序
  -> 返回前 K 条
```

本项目使用的是余弦相似度：

```text
cosine similarity
```

你可以把它简单理解成：

```text
两个向量方向越接近，文本语义越相似。
```

### 4.4 什么是 Top-K

`Top-K` 表示返回最相关的前 K 条结果。

例如：

```python
similarity_search(question, k=3)
```

意思是：

```text
返回相似度最高的 3 个文本块。
```

Top-K 很重要，因为一个问题往往需要多个片段一起支撑回答。

---

## 5. 每个文件的详细解释

### 5.1 `config.py`

这个文件是 Day 16 的统一配置中心。

它负责读取 `.env` 和 `.env.example`。

主要配置包括：

1. `CHUNK_SIZE`：每个文本块的最大长度。
2. `CHUNK_OVERLAP`：相邻文本块之间的重叠长度。
3. `TOP_K`：检索返回前几条。
4. `VECTOR_DB_FILE`：向量库 JSON 文件保存路径。
5. `EMBEDDING_DIM`：本地 Embedding 向量维度。
6. `OPENAI_API_KEY`：在线 Embedding 所需 API Key。
7. `OPENAI_BASE_URL`：API 地址。
8. `EMBEDDING_MODEL`：Embedding 模型名称。

为什么要集中配置？

因为后面做实验时，经常要调整：

```text
chunk 大小
overlap 大小
top_k 数量
embedding 模式
保存路径
```

集中放在 `config.py` 会更方便。

---

### 5.2 `.env.example`

这个文件是环境变量模板。

它不会自动保存你的真实 Key。

你应该复制成 `.env` 后再填写真实配置。

如果没有 `.env`，代码会读取 `.env.example` 里的默认值作为兜底。

注意：

```text
不要把真实 API Key 写进 README 或提交到 GitHub。
```

---

### 5.3 `documents/`

这个文件夹保存示例知识库文档。

当前有三份：

1. `rag_notes.txt`
2. `vector_db_notes.txt`
3. `ai_agents_notes.txt`

它们分别用于测试不同主题的语义检索。

你可以继续往里面添加 `.txt` 或 `.md` 文件。

---

### 5.4 `modules/loader.py`

这个文件负责加载文档。

核心数据结构：

```python
DocumentItem
```

它包含：

```python
page_content
metadata
```

`page_content` 是正文。

`metadata` 是来源信息。

核心函数：

```python
load_documents(docs_dir)
```

它会：

1. 遍历 `documents/` 文件夹。
2. 只读取 `.txt` 和 `.md`。
3. 尝试 `utf-8`、`utf-8-sig`、`gbk` 编码。
4. 跳过空文件。
5. 返回 `DocumentItem` 列表。

这个文件解决的问题是：

```text
如何把本地知识库资料读进程序。
```

---

### 5.5 `modules/splitter.py`

这个文件负责文本切分。

核心函数：

```python
split_text(text, chunk_size, chunk_overlap)
split_documents(documents, chunk_size, chunk_overlap)
```

为什么要切分？

因为文档太长时：

1. 不适合直接做检索。
2. 不适合整篇交给模型。
3. 一个问题通常只需要文档中的一小段。

为什么要 overlap？

因为切分可能刚好把一句话切断。

overlap 可以让相邻文本块保留一部分重复内容，让上下文更连续。

---

### 5.6 `modules/embeddings.py`

这个文件负责把文本变成向量。

它有两个核心类：

```python
SimpleEmbeddingModel
HybridEmbeddingModel
```

`SimpleEmbeddingModel` 是本地兜底模型。

特点：

1. 不需要 API Key。
2. 不需要联网。
3. 使用 md5 哈希把 token 映射到向量维度。
4. 适合教学演示。
5. 不适合生产环境。

`HybridEmbeddingModel` 是混合模型。

逻辑：

```text
如果有 API Key，并且 langchain-openai 可用：
    优先使用在线 Embedding
否则：
    使用本地 SimpleEmbeddingModel
```

为什么要这样设计？

因为学习时不能因为没有 API Key 就卡住。
但真实项目里，有 API 的地方应该尽量使用真实 Embedding，检索效果会更好。

---

### 5.7 `modules/vector_store.py`

这是 Day 16 最核心的文件。

它实现了一个轻量可持久化向量库。

核心函数：

```python
_cosine_similarity(a, b)
```

作用：

```text
计算两个向量的相似度。
```

核心数据结构：

```python
SearchResult
VectorRecord
```

`SearchResult` 表示检索结果。

包含：

```text
document
score
```

`VectorRecord` 表示向量库里的单条记录。

包含：

```text
page_content
metadata
vector
```

核心类：

```python
PersistentVectorStore
```

它提供这些能力：

1. `add_documents()`：把文本块写入向量库。
2. `similarity_search()`：执行相似度搜索。
3. `stats()`：查看向量库统计信息。
4. `save()`：保存到 JSON 文件。
5. `load()`：从 JSON 文件加载。

为什么叫 `PersistentVectorStore`？

因为它不仅能在内存中检索，还能保存到磁盘。

---

### 5.8 `modules/search_demo.py`

这个文件负责把搜索过程包装成演示友好的格式。

核心类：

```python
SearchDemo
```

它有两个方法：

```python
search(question, metadata_filter=None)
format_results(results)
```

`search()` 负责调用向量库搜索。

`format_results()` 负责把结果格式化成可读文本。

如果你看到输出里有：

```text
分数
来源
块编号
文本内容
```

就是这个模块格式化出来的。

---

### 5.9 `modules/__init__.py`

这个文件让 `modules/` 成为 Python 包。

它统一导出常用类和函数。

以后可以写：

```python
from modules import PersistentVectorStore, load_documents
```

而不是每次都从具体文件导入。

---

### 5.10 `01_store_chunks.py`

这是练习 1 的代码文件。

作用：

```text
把文档加载、切分，并存入向量库。
```

它会打印：

1. 文档数量。
2. 文本块数量。
3. 向量库统计信息。

重点理解：

```python
store.add_documents(chunks)
```

这行代码内部会做：

```text
文本块 -> Embedding 向量 -> VectorRecord -> 保存到 records
```

---

### 5.11 `02_similarity_search.py`

这是练习 2 的代码文件。

作用：

```text
根据一个问题执行相似度搜索。
```

问题示例：

```text
什么是向量数据库？
```

它会返回最相关的 Top-K 文本块。

重点看输出中的：

```text
分数
来源
块编号
```

---

### 5.12 `03_metadata_filter.py`

这是练习 3 的代码文件。

作用：

```text
演示如何用 metadata_filter 限定搜索范围。
```

核心代码：

```python
metadata_filter={"source": "rag_notes.txt"}
```

意思是：

```text
只在 rag_notes.txt 这个来源文件里搜索。
```

metadata 过滤常用于：

1. 只搜索某个文件。
2. 只搜索某个用户的资料。
3. 只搜索某个项目的文档。
4. 只搜索某个时间范围的数据。

---

### 5.13 `04_topk_compare.py`

这是练习 4 的代码文件。

作用：

```text
对比 Top-1 和 Top-3 的检索效果。
```

Top-1 的特点：

1. 信息最集中。
2. 输出最短。
3. 可能遗漏上下文。

Top-3 的特点：

1. 信息更充分。
2. 更适合交给大模型综合回答。
3. 可能混入一些不太相关内容。

---

### 5.14 `05_persistent_db.py`

这是练习 5 的代码文件。

作用：

```text
演示向量库保存到磁盘，再重新加载。
```

核心代码：

```python
store.save()
reload_store.load()
```

运行后会生成或更新：

```text
vector_db.json
```

这个文件就是当前项目的简化版持久化向量库。

---

### 5.15 `main.py`

这是 Day 16 的主入口。

它提供一个命令行交互程序。

支持命令：

```text
build
search
stats
save
load
demo
q
```

它内部封装了一个类：

```python
VectorDBApp
```

这个类负责：

1. 加载文档目录。
2. 获取 Embedding 模型。
3. 创建向量库。
4. 创建搜索演示器。
5. 解析命令。
6. 执行搜索。
7. 保存和加载向量库。

---

## 6. 练习题专区

下面是 Day 16 的完整练习题。

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

---

### 6.1 练习 1：把文本块存入向量库

文件：

```text
01_store_chunks.py
```

练习目标：

理解文档如何经过加载、切分、向量化后写入向量库。

题目要求：

1. 加载 `documents/` 下的所有文档。
2. 使用 `split_documents()` 切成文本块。
3. 创建 `PersistentVectorStore`。
4. 调用 `add_documents()` 写入向量库。
5. 打印向量库统计信息。

操作提示：

重点看这行：

```python
store.add_documents(chunks)
```

它会把文本块转成向量，并保存成 `VectorRecord`。

参考答案：

答案已经写在 `01_store_chunks.py` 中。

核心流程是：

```text
load_documents()
  -> split_documents()
  -> PersistentVectorStore()
  -> add_documents()
  -> stats()
```

如何运行：

```powershell
python 01_store_chunks.py
```

你应该观察到：

1. 文档数量大于 0。
2. 文本块数量大于文档数量或等于文档数量。
3. `record_count` 等于文本块数量。
4. `source_counts` 中能看到每个文件贡献了多少块。

---

### 6.2 练习 2：执行相似度搜索

文件：

```text
02_similarity_search.py
```

练习目标：

理解用户问题如何在向量库中找到语义相近的文本块。

题目要求：

1. 构建向量库。
2. 准备一个问题：`什么是向量数据库？`
3. 调用搜索方法。
4. 打印 Top-K 检索结果。

操作提示：

重点看输出中的：

```text
分数
来源
块编号
```

参考答案：

答案已经写在 `02_similarity_search.py` 中。

核心代码：

```python
results = demo.search(question)
print(demo.format_results(results))
```

如何运行：

```powershell
python 02_similarity_search.py
```

你应该观察到：

1. 返回结果中通常会出现 `vector_db_notes.txt`。
2. 相似度分数越高，排名越靠前。
3. 如果使用本地 Embedding，结果可能不如真实 API 精准，但流程是正确的。

---

### 6.3 练习 3：使用 metadata 过滤

文件：

```text
03_metadata_filter.py
```

练习目标：

理解向量搜索不仅可以按语义查，还可以加条件过滤。

题目要求：

1. 构建完整向量库。
2. 搜索问题：`RAG 是什么？`
3. 加上过滤条件：只搜索 `rag_notes.txt`。
4. 打印结果。

操作提示：

过滤条件写法：

```python
metadata_filter={"source": "rag_notes.txt"}
```

参考答案：

答案已经写在 `03_metadata_filter.py` 中。

核心代码：

```python
results = demo.search(
    "RAG 是什么？",
    metadata_filter={"source": "rag_notes.txt"},
)
```

如何运行：

```powershell
python 03_metadata_filter.py
```

你应该观察到：

1. 输出结果的来源都应该是 `rag_notes.txt`。
2. 不会出现 `ai_agents_notes.txt` 或 `vector_db_notes.txt`。
3. 如果没有符合条件的数据，会返回空结果。

---

### 6.4 练习 4：对比 Top-1 和 Top-3

文件：

```text
04_topk_compare.py
```

练习目标：

理解返回不同数量的检索结果，会影响后续 RAG 可用上下文。

题目要求：

1. 用同一个问题检索。
2. 先设置 `k=1`。
3. 再设置 `k=3`。
4. 对比返回内容。

问题示例：

```text
AI Agent 为什么要结合向量检索？
```

参考答案：

答案已经写在 `04_topk_compare.py` 中。

核心代码：

```python
store.similarity_search(question, k=1)
store.similarity_search(question, k=3)
```

如何运行：

```powershell
python 04_topk_compare.py
```

你应该观察到：

1. Top-1 只返回一条。
2. Top-3 返回三条。
3. Top-3 信息更丰富，但也可能包含相关性较弱的内容。
4. 真正做 RAG 时，Top-K 需要根据文档质量和模型上下文调整。

---

### 6.5 练习 5：持久化向量库

文件：

```text
05_persistent_db.py
```

练习目标：

理解为什么要把向量库保存到磁盘。

题目要求：

1. 构建向量库。
2. 调用 `save()` 保存到 JSON。
3. 新建一个空向量库对象。
4. 调用 `load()` 从磁盘恢复。
5. 打印恢复后的统计信息。

参考答案：

答案已经写在 `05_persistent_db.py` 中。

核心代码：

```python
store.save()
reload_store = PersistentVectorStore(get_embedding_model(), VECTOR_DB_FILE)
reload_store.load()
```

如何运行：

```powershell
python 05_persistent_db.py
```

你应该观察到：

1. 项目目录下生成或更新 `vector_db.json`。
2. 重新加载后的 `record_count` 不为 0。
3. 保存前后的来源统计一致。

---

## 7. 练习题对应文件答案说明

Day 16 的练习答案已经写进对应代码文件中。

对应关系如下：

```text
练习 1 -> 01_store_chunks.py
练习 2 -> 02_similarity_search.py
练习 3 -> 03_metadata_filter.py
练习 4 -> 04_topk_compare.py
练习 5 -> 05_persistent_db.py
```

你可以直接运行这些文件查看答案效果。

这些文件不是单纯提示，而是完整可运行的参考答案。

---

## 8. API Key 与本地模式说明

Day 16 的 Embedding 是混合模式。

### 8.1 没有 API Key

如果没有配置 `OPENAI_API_KEY`：

1. 自动使用 `SimpleEmbeddingModel`。
2. 不需要联网。
3. 不会产生 API 费用。
4. 检索效果只是教学级别。
5. 适合先理解流程。

### 8.2 有 API Key

如果配置了 `OPENAI_API_KEY`：

1. 优先使用 `OpenAIEmbeddings`。
2. 检索语义效果通常更好。
3. 更接近真实 RAG 项目。
4. 如果在线调用失败，会自动回退本地模式。

### 8.3 如何判断当前模式

运行：

```powershell
python main.py
```

程序顶部会显示：

```text
Embedding 模式：在线 API
```

或：

```text
Embedding 模式：本地兜底
```

---

## 9. 常见问题

### 9.1 为什么检索结果不够准

可能原因：

1. 当前使用的是本地简化 Embedding。
2. 文档内容太少。
3. 问题和文档措辞差异太大。
4. `CHUNK_SIZE` 设置不合适。
5. `TOP_K` 太小或太大。

解决方式：

1. 配置真实 Embedding API。
2. 增加更多高质量文档。
3. 调整 `CHUNK_SIZE`。
4. 调整 `CHUNK_OVERLAP`。
5. 调整 `TOP_K`。

---

### 9.2 为什么要保存 metadata

因为检索结果必须可追踪。

metadata 可以告诉你：

1. 结果来自哪个文件。
2. 是第几个 chunk。
3. 后续是否要展示引用来源。
4. 是否可以按来源过滤。

没有 metadata，检索出来的结果就很难解释。

---

### 9.3 为什么要持久化

如果不持久化，每次程序启动都要：

1. 重新加载文档。
2. 重新切分文本。
3. 重新计算 Embedding。
4. 重新构建向量库。

真实项目中文档很多，Embedding 又可能要花钱。

所以需要保存索引，下次直接加载。

---

### 9.4 `vector_db.json` 可以删除吗

可以。

删除后，重新运行：

```powershell
python main.py
```

或：

```powershell
python 05_persistent_db.py
```

程序会重新构建向量库。

---

## 10. 推荐学习顺序

建议按这个顺序学习：

1. 读 `README.md`。
2. 运行 `python 01_store_chunks.py`。
3. 打开 `modules/loader.py` 和 `modules/splitter.py`。
4. 运行 `python 02_similarity_search.py`。
5. 打开 `modules/embeddings.py` 和 `modules/vector_store.py`。
6. 运行 `python 03_metadata_filter.py`。
7. 理解 metadata 过滤。
8. 运行 `python 04_topk_compare.py`。
9. 理解 Top-K。
10. 运行 `python 05_persistent_db.py`。
11. 查看生成的 `vector_db.json`。
12. 最后运行 `python main.py` 体验完整命令行工具。

---

## 11. Day 16 总结

Day 16 的关键词是：

```text
向量
Embedding
向量库
相似度
Top-K
metadata
持久化
```

你可以这样理解：

```text
Day 15 是理解 RAG 整条路。
Day 16 是把 RAG 里面“怎么存资料、怎么找资料”这一步练扎实。
```

一句话总结：

```text
向量数据库的作用，就是让文档可以按照语义被找出来。
```

学完 Day 16 后，你再看 Day 17、Day 18、Day 20 的 RAG 项目，会明显更容易，因为你已经知道底层检索到底在做什么。
