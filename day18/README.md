# Day 18 - RAG 检索链

> Day 18 的任务：理解并实现一条完整的 RAG 检索链。
>
> 这一节的重点不是“文档怎么加载”，也不是“向量数据库怎么存”，而是：
>
> ```text
> 用户问题 -> Retriever 检索 -> Top-K 结果 -> 上下文拼接 -> 模型/本地回答
> ```

---

## 1. 今天你要学会什么

Day 18 对应学习计划表里的任务是：`RAG 检索链`。

完成这一天后，你应该能理解：

1. 什么是 Retriever。
2. Retriever 在 RAG 中负责什么。
3. 什么是 Top-K 检索。
4. 为什么要对检索结果排序。
5. 什么是上下文拼接。
6. 为什么模型回答质量依赖检索上下文。
7. `MAX_CONTEXT_CHARS` 为什么重要。
8. 有 API Key 时如何调用在线模型生成回答。
9. 没有 API Key 时如何使用本地兜底回答。
10. 如何把“检索摘要、上下文、最终回答”分开观察。

---

## 2. 项目结构

```text
day18/
├── README.md
├── requirements.txt
├── .env.example
├── config.py
├── main.py
├── 01_build_retriever.py
├── 02_retrieval_test.py
├── 03_context_preview.py
├── 04_topk_compare.py
├── 05_full_rag_app.py
├── documents/
│   ├── 01_rag_intro.txt
│   ├── 02_retriever_notes.md
│   └── 03_context_building.txt
└── modules/
    ├── __init__.py
    ├── loader.py
    ├── splitter.py
    ├── retriever.py
    ├── rag_chain.py
    └── pipeline.py
```

Day 18 的核心链路是：

```text
documents/
  -> loader.py
  -> splitter.py
  -> retriever.py
  -> rag_chain.py
  -> pipeline.py
  -> 05_full_rag_app.py
```

---

## 3. 运行方式

### 3.1 安装依赖

在 `day18` 文件夹下运行：

```powershell
pip install -r requirements.txt
```

### 3.2 配置环境变量

复制 `.env.example` 为 `.env`：

```powershell
copy .env.example .env
```

可以配置：

```env
DOCS_DIR=documents
CHUNK_SIZE=320
CHUNK_OVERLAP=70
TOP_K=3
MAX_CONTEXT_CHARS=1600
ANSWER_STYLE=concise
OPENAI_API_KEY=你的 API Key
OPENAI_BASE_URL=https://api.deepseek.com
MODEL_NAME=deepseek-chat
TEMPERATURE=0.2
```

如果你没有 API Key，也可以直接运行。

项目会使用本地兜底回答，保证检索链可以完整跑通。

### 3.3 运行完整应用

```powershell
python main.py
```

进入程序后可以输入：

```text
load
docs
chunks
stats
ask
demo
q
```

### 3.4 分步骤运行练习脚本

```powershell
python 01_build_retriever.py
python 02_retrieval_test.py
python 03_context_preview.py
python 04_topk_compare.py
python 05_full_rag_app.py
```

---

## 4. RAG 检索链核心原理

### 4.1 什么是 Retriever

Retriever 是 RAG 里的“资料检索员”。

它不负责生成最终答案。

它只负责：

```text
根据用户问题，从文档 chunk 中找出最相关的内容。
```

在本项目中，Retriever 使用轻量级词项检索：

1. 从用户问题中提取词项。
2. 从每个 chunk 中提取词项。
3. 使用简化 TF-IDF 计算相关性。
4. 按分数排序。
5. 返回 Top-K 条结果。

### 4.2 什么是 Top-K

Top-K 表示返回最相关的前 K 条结果。

例如：

```python
top_k = 3
```

意思是每次检索返回 3 个最相关 chunk。

Top-K 太小：

1. 上下文短。
2. 可能漏掉重要资料。
3. 回答可能不完整。

Top-K 太大：

1. 上下文变长。
2. 可能混入无关内容。
3. 模型注意力被分散。

### 4.3 什么是上下文拼接

检索器返回的是多个 chunk。

模型不能直接读取 Python 对象。

所以需要把这些 chunk 拼成一段文本：

```text
【来源：01_rag_intro.txt｜chunk 1】
RAG 是检索增强生成...

【来源：02_retriever_notes.md｜chunk 2】
Retriever 的作用是...
```

这一步就叫上下文拼接。

### 4.4 为什么上下文拼接很重要

模型最终回答时看到的不是整个知识库，而是拼接后的 context。

也就是说：

```text
context 里有什么，模型就根据什么回答。
context 里没有什么，模型就不应该乱编。
```

所以观察 RAG 系统时，要按这个顺序看：

1. 检索摘要是否正确。
2. 拼接上下文是否完整。
3. 最终回答是否根据上下文。

---

## 5. 每个文件的详细解释

### 5.1 `config.py`

这个文件是 Day 18 的统一配置中心。

主要配置：

1. `DOCS_DIR`：文档目录。
2. `CHUNK_SIZE`：每个 chunk 的最大字符数。
3. `CHUNK_OVERLAP`：相邻 chunk 的重叠字符数。
4. `TOP_K`：检索返回前几条。
5. `MAX_CONTEXT_CHARS`：上下文最大字符数。
6. `ANSWER_STYLE`：回答风格。
7. `OPENAI_API_KEY`：在线模型 API Key。
8. `OPENAI_BASE_URL`：API 地址。
9. `MODEL_NAME`：模型名称。
10. `TEMPERATURE`：模型随机性。

为什么要集中配置？

因为 RAG 检索链非常依赖调参。

你经常会调整：

```text
chunk_size
chunk_overlap
top_k
max_context_chars
temperature
```

集中配置更方便实验。

---

### 5.2 `.env.example`

这个文件是配置模板。

如果你想使用真实在线模型，需要复制成 `.env` 并填写 API Key。

如果不填写 API Key，程序会自动使用本地兜底模式。

---

### 5.3 `documents/`

这个文件夹是 Day 18 的示例知识库。

当前包含：

1. `01_rag_intro.txt`
2. `02_retriever_notes.md`
3. `03_context_building.txt`

它们分别用于测试：

1. RAG 基础概念。
2. Retriever 的作用。
3. 上下文拼接的重要性。

---

### 5.4 `modules/loader.py`

这个文件负责文档加载。

核心结构：

```python
DocumentItem
```

它包含：

```text
page_content
metadata
```

核心函数：

```python
resolve_docs_dir()
load_text_file()
load_documents()
summarize_documents()
preview_documents()
```

这个模块的目标：

```text
把 documents/ 里的 .txt 和 .md 文件读成项目内部可处理的 DocumentItem。
```

---

### 5.5 `modules/splitter.py`

这个文件负责把文档切成 chunk。

核心函数：

```python
_normalize_text()
_split_by_separator()
_sliding_window()
_merge_with_overlap()
split_documents()
compare_chunk_stats()
preview_chunks()
```

切分逻辑：

1. 先清理多余空白。
2. 优先按段落和标点切。
3. 如果找不到合适分隔符，就用滑窗切分。
4. 给每个 chunk 添加 metadata。

metadata 会保存：

1. `chunk_index`
2. `chunk_count`
3. `chunk_size`
4. `splitter`

---

### 5.6 `modules/retriever.py`

这是 Day 18 的核心模块之一。

它实现一个轻量级 Retriever。

核心函数：

```python
extract_terms(text)
```

作用：

```text
从问题或 chunk 中提取检索词项。
```

中文会补充二元词组，例如：

```text
上下文拼接 -> 上下、下文、文拼、拼接
```

核心函数：

```python
build_document_profile(text)
```

作用：

```text
统计每个词项在文本中出现几次。
```

核心类：

```python
SimpleRetriever
```

它会：

1. 保存所有 chunk。
2. 为每个 chunk 建立词项画像。
3. 统计词项出现在多少个 chunk 中。
4. 对用户问题和 chunk 计算 TF-IDF 分数。
5. 返回 Top-K 检索结果。

核心函数：

```python
format_retrieval_summary(results)
```

作用：

```text
把检索结果整理成人能看懂的摘要。
```

---

### 5.7 `modules/rag_chain.py`

这是 Day 18 最重要的模块。

它把检索和回答串起来。

核心类：

```python
RAGChain
```

它负责：

1. 创建 Retriever。
2. 检索相关 chunk。
3. 拼接上下文。
4. 构建 Prompt。
5. 有 API 时调用在线模型。
6. 没有 API 时使用本地兜底回答。

核心方法：

```python
retrieve(question)
```

负责检索。

核心方法：

```python
build_context(results)
```

负责把检索结果拼成上下文。

核心方法：

```python
answer_with_context(question, context)
```

负责生成回答。

核心方法：

```python
query(question)
```

完整执行一次：

```text
检索 -> 拼接上下文 -> 生成回答 -> 返回结果字典
```

---

### 5.8 `modules/pipeline.py`

这个文件把整条 RAG 检索链封装起来。

核心类：

```python
RAGPipeline
```

它负责：

1. 加载文档。
2. 切分文档。
3. 创建 RAGChain。
4. 提供统一 `ask(question)` 入口。

为什么需要 pipeline？

因为真实项目不会让你每次手动调用所有函数。

pipeline 把常用流程整理成一个对象：

```python
pipeline.ask("什么是 RAG？")
```

---

### 5.9 `01_build_retriever.py`

这是练习 1 文件。

作用：

```text
构建检索器前的数据基础。
```

它会：

1. 创建 RAGPipeline。
2. 加载文档。
3. 切分文档。
4. 打印文档数量。
5. 打印 chunk 数量。
6. 预览 chunk。

---

### 5.10 `02_retrieval_test.py`

这是练习 2 文件。

作用：

```text
用多个问题测试检索效果。
```

它会测试：

1. 什么是 RAG？
2. Retriever 的作用是什么？
3. 上下文拼接为什么重要？

输出会显示每个问题对应的检索摘要。

---

### 5.11 `03_context_preview.py`

这是练习 3 文件。

作用：

```text
展示检索结果如何拼接成上下文。
```

它会打印：

1. 检索摘要。
2. 拼接后的 context。

这个练习非常关键，因为它告诉你：

```text
模型最终看到的资料到底是什么。
```

---

### 5.12 `04_topk_compare.py`

这是练习 4 文件。

作用：

```text
比较不同 top_k 对检索结果数量和摘要的影响。
```

它会测试：

```text
top_k = 1
top_k = 2
top_k = 3
top_k = 4
```

---

### 5.13 `05_full_rag_app.py`

这是 Day 18 的完整交互应用。

支持命令：

```text
load
docs
chunks
stats
ask
demo
q
```

其中 `ask` 会完整展示：

1. 检索结果摘要。
2. 拼接上下文。
3. 最终回答。
4. 回答模式。

---

### 5.14 `main.py`

这是 Day 18 的统一入口。

运行：

```powershell
python main.py
```

它会启动 `05_full_rag_app.py`。

---

## 6. 练习题专区

下面是 Day 18 的完整练习题。

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

### 6.1 练习 1：构建检索器数据基础

文件：

```text
01_build_retriever.py
```

练习目标：

确认文档和 chunk 已经准备好，可以用于构建 Retriever。

题目要求：

1. 创建 `RAGPipeline`。
2. 调用 `load()` 加载文档。
3. 调用 `split()` 切分文档。
4. 打印文档数量。
5. 打印 chunk 数量。
6. 预览前几个 chunk。

参考答案：

答案已经写在 `01_build_retriever.py` 中。

核心流程：

```text
RAGPipeline()
  -> load()
  -> split()
  -> document_summary()
  -> chunk_summary()
  -> chunk_previews()
```

如何运行：

```powershell
python 01_build_retriever.py
```

你应该观察到：

1. 文档数量大于 0。
2. chunk 数量大于 0。
3. chunk 预览里能看到来源文件和 chunk 编号。

---

### 6.2 练习 2：检索测试

文件：

```text
02_retrieval_test.py
```

练习目标：

测试不同问题会命中哪些不同 chunk。

题目要求：

1. 准备多个问题。
2. 对每个问题调用 `pipeline.ask()`。
3. 提取 `retrieval_summary`。
4. 用表格展示结果。

参考答案：

答案已经写在 `02_retrieval_test.py` 中。

核心代码：

```python
result = pipeline.ask(question)
result["retrieval_summary"]
```

如何运行：

```powershell
python 02_retrieval_test.py
```

你应该观察到：

1. 每个问题都有对应检索摘要。
2. 不同问题命中的文件和 chunk 可能不同。
3. 检索摘要比最终回答更适合调试。

---

### 6.3 练习 3：上下文预览

文件：

```text
03_context_preview.py
```

练习目标：

理解检索结果如何变成模型可读取的上下文。

题目要求：

1. 提问：`请解释上下文拼接的作用`。
2. 打印 `retrieval_summary`。
3. 打印 `context`。
4. 对比两者区别。

参考答案：

答案已经写在 `03_context_preview.py` 中。

核心代码：

```python
result = pipeline.ask("请解释上下文拼接的作用")
print(result["retrieval_summary"])
print(result["context"])
```

如何运行：

```powershell
python 03_context_preview.py
```

你应该观察到：

1. retrieval_summary 是简短摘要。
2. context 是完整上下文。
3. context 中会包含来源文件和 chunk 编号。

---

### 6.4 练习 4：Top-K 对比

文件：

```text
04_topk_compare.py
```

练习目标：

观察 `top_k` 改变时，检索返回数量如何变化。

题目要求：

1. 分别设置 `top_k=1/2/3/4`。
2. 对同一个问题提问。
3. 统计检索摘要行数。
4. 对比前两条摘要。

参考答案：

答案已经写在 `04_topk_compare.py` 中。

核心代码：

```python
for top_k in [1, 2, 3, 4]:
    pipeline = RAGPipeline(..., top_k=top_k)
    result = pipeline.ask("RAG 的核心流程是什么")
```

如何运行：

```powershell
python 04_topk_compare.py
```

你应该观察到：

1. top_k 越大，返回结果越多。
2. 上下文可能更完整，也可能更杂。
3. 实际项目中 top_k 需要根据文档质量调参。

---

### 6.5 练习 5：完整 RAG 检索链应用

文件：

```text
05_full_rag_app.py
```

练习目标：

体验完整的检索链：文档、chunk、检索、上下文、回答。

题目要求：

1. 启动应用。
2. 输入 `load`。
3. 输入 `docs`。
4. 输入 `chunks`。
5. 输入 `ask` 并提问。
6. 观察检索摘要、上下文和最终回答。
7. 输入 `q` 退出。

操作提示：

建议命令顺序：

```text
load
docs
chunks
stats
ask
demo
q
```

参考答案：

答案已经写在 `05_full_rag_app.py` 中。

如何运行：

```powershell
python 05_full_rag_app.py
```

或：

```powershell
python main.py
```

你应该观察到：

1. 应用显示菜单。
2. `stats` 会显示在线模型是否可用。
3. `ask` 会显示检索摘要、上下文、最终回答。
4. 没有 API Key 时显示本地兜底。
5. 有 API Key 时会尝试在线生成。

---

## 7. 练习题对应文件答案说明

Day 18 的练习答案已经写进对应代码文件中。

对应关系：

```text
练习 1 -> 01_build_retriever.py
练习 2 -> 02_retrieval_test.py
练习 3 -> 03_context_preview.py
练习 4 -> 04_topk_compare.py
练习 5 -> 05_full_rag_app.py
```

这些练习文件都是完整可运行的参考答案。

---

## 8. API Key 与本地模式说明

Day 18 支持两种回答模式。

### 8.1 没有 API Key

如果没有配置 `OPENAI_API_KEY`：

1. Retriever 仍然正常工作。
2. 上下文仍然正常拼接。
3. 最终回答使用本地兜底摘要。
4. 不会产生 API 费用。
5. 适合学习检索链结构。

### 8.2 有 API Key

如果配置了 `OPENAI_API_KEY`：

1. `RAGChain` 会尝试创建 `ChatOpenAI`。
2. 最终回答会由在线模型根据上下文生成。
3. Prompt 会要求模型只根据上下文回答。
4. 如果在线调用失败，会自动退回本地兜底。

### 8.3 如何判断当前模式

运行：

```powershell
python main.py
```

输入：

```text
stats
```

你会看到：

```text
在线模型：可用
```

或：

```text
在线模型：不可用
```

---

## 9. 常见问题

### 9.1 为什么检索结果不够准

可能原因：

1. 当前 Retriever 是轻量词项检索，不是真实向量检索。
2. 问题和文档措辞差异较大。
3. chunk 切分不合适。
4. `TOP_K` 太小。
5. 文档内容太少。

改进方式：

1. 调整 `CHUNK_SIZE`。
2. 调整 `CHUNK_OVERLAP`。
3. 调整 `TOP_K`。
4. 后续接入真实 Embedding 和向量数据库。

---

### 9.2 为什么要看 retrieval_summary

因为最终回答质量取决于检索结果。

如果 retrieval_summary 错了，最终回答大概率也会偏。

调试 RAG 时，一定要先看：

```text
模型到底拿到了哪些资料？
```

---

### 9.3 为什么上下文有长度限制

原因：

1. 模型输入长度有限。
2. 上下文太长会分散重点。
3. 太多无关资料会降低回答质量。
4. 控制长度可以减少成本。

---

### 9.4 为什么没有 API Key 也能运行

因为本项目把“检索链学习”和“在线模型调用”分开了。

即使没有模型，你仍然可以学习：

1. 文档加载。
2. 文档切分。
3. Retriever 检索。
4. Top-K。
5. 上下文拼接。

---

## 10. 推荐学习顺序

建议按这个顺序学习：

1. 先读 `README.md`。
2. 运行 `python 01_build_retriever.py`。
3. 打开 `modules/loader.py` 和 `modules/splitter.py`。
4. 运行 `python 02_retrieval_test.py`。
5. 打开 `modules/retriever.py`。
6. 运行 `python 03_context_preview.py`。
7. 打开 `modules/rag_chain.py`。
8. 运行 `python 04_topk_compare.py`。
9. 理解 Top-K 对上下文的影响。
10. 运行 `python 05_full_rag_app.py`。
11. 最后运行 `python main.py`。

---

## 11. Day 18 总结

Day 18 的关键词是：

```text
Retriever
Top-K
retrieval_summary
context
RAGChain
Prompt
在线生成
本地兜底
```

一句话总结：

```text
RAG 检索链，就是先把问题相关资料找出来，再把资料整理成上下文，最后让模型根据上下文回答。
```

如果 Day 18 学明白了，后面的 RAG 问答系统就不会只是“能跑”，而是你能真正知道它为什么这样回答、哪里可能出错、应该怎么调试。
