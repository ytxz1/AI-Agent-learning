# Day 19 - 项目 2：RAG 问答系统

> Day 19 的任务：把前几天学过的文档加载、文本切分、Embedding、向量数据库、Retriever 和 RAG Chain 组合成一个完整的本地文档问答系统。
>
> 这一节开始进入项目实战，不再只是单点知识演示，而是要把链路真正跑起来：
>
> ```text
> 上传/准备文档 -> 加载文档 -> 切分文本 -> 生成向量 -> 存入 Chroma -> 检索相关资料 -> 调用模型回答
> ```

---

## 1. 今天你要学会什么

Day 19 对应学习计划表里的任务是：`项目 2：RAG 问答系统`。

完成这一天后，你应该能理解：

1. 一个完整 RAG 问答系统由哪些模块组成。
2. 文档加载器如何读取本地知识库。
3. 文本切分参数如何影响检索效果。
4. Embedding 为什么是语义检索的基础。
5. Chroma 向量数据库如何保存和检索文档。
6. Retriever 如何从向量库里找相关资料。
7. RAG Chain 如何把检索结果和问题交给模型。
8. 主程序如何做成交互式问答助手。
9. 练习题如何一步步扩展成完整项目。
10. 如何评估 RAG 系统的效果。

---

## 2. 项目结构

```text
day19/
├── README.md
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── config.py
├── main.py
├── 01_document_loader.py
├── 02_text_splitter.py
├── 03_embeddings.py
├── 04_vector_store.py
├── 05_retriever.py
├── 06_rag_chain.py
├── exercise1_doc_formats.py
├── exercise2_split_compare.py
├── exercise3_custom_kb.py
├── exercise4_multi_doc.py
├── exercise5_rag_eval.py
├── documents/
│   ├── ai_intro.txt
│   ├── langchain_doc.txt
│   └── sample.txt
└── tools/
    └── __init__.py
```

Day 19 的主线是：

```text
01_document_loader.py
  -> 02_text_splitter.py
  -> 03_embeddings.py
  -> 04_vector_store.py
  -> 05_retriever.py
  -> 06_rag_chain.py
  -> main.py
```

---

## 3. 运行方式

### 3.1 安装依赖

在 `day19` 文件夹下运行：

```powershell
pip install -r requirements.txt
```

### 3.2 配置 API Key

Day 19 是完整 RAG 问答系统。

这里需要在线 Embedding 和在线聊天模型，所以建议配置 API Key。

复制 `.env.example` 为 `.env`：

```powershell
copy .env.example .env
```

然后填写：

```env
OPENAI_API_KEY=你的 API Key
OPENAI_BASE_URL=https://api.deepseek.com
MODEL_NAME=deepseek-chat
EMBEDDING_MODEL=text-embedding-v3
CHUNK_SIZE=200
CHUNK_OVERLAP=50
TOP_K=3
TEMPERATURE=0.7
```

注意：

```text
.env 里是真实密钥，不要提交到 GitHub。
```

当前 `.gitignore` 已经包含 `.env`。

### 3.3 运行完整项目

```powershell
python main.py
```

进入交互式问答助手后，可以输入：

```text
example
docs
search
你的问题
q
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

建议第一次学习时按顺序运行。

---

## 4. RAG 问答系统核心流程

### 4.1 离线索引阶段

离线索引阶段负责把文档变成可以检索的数据。

流程：

```text
documents/
  -> TextLoader / DirectoryLoader
  -> Document
  -> RecursiveCharacterTextSplitter
  -> chunk
  -> OpenAIEmbeddings
  -> vector
  -> Chroma
```

这一阶段的目标：

```text
把本地文档变成向量数据库里的可检索文本块。
```

### 4.2 在线问答阶段

在线问答阶段负责根据用户问题查资料并生成回答。

流程：

```text
用户问题
  -> Embedding
  -> Retriever
  -> 相关文档 chunk
  -> Prompt
  -> ChatOpenAI
  -> 最终回答
```

这一阶段的目标：

```text
让模型根据检索到的真实资料回答，而不是凭空编。
```

### 4.3 为什么 Day 19 是项目实战

前几天你分别学了：

1. Day 15：RAG 基础流程。
2. Day 16：向量数据库。
3. Day 17：文档加载与切分。
4. Day 18：RAG 检索链。

Day 19 要做的是：

```text
把这些能力合成一个能交互提问的 RAG 问答系统。
```

---

## 5. 每个文件的详细解释

### 5.1 `config.py`

这个文件是 Day 19 的统一配置中心。

它读取：

1. `.env`
2. `.env.example`

主要配置：

1. `OPENAI_API_KEY`：API Key。
2. `OPENAI_BASE_URL`：OpenAI 兼容接口地址。
3. `MODEL_NAME`：聊天模型名称。
4. `EMBEDDING_MODEL`：Embedding 模型名称。
5. `CHUNK_SIZE`：文本块大小。
6. `CHUNK_OVERLAP`：文本块重叠长度。
7. `TOP_K`：检索返回数量。
8. `TEMPERATURE`：模型随机性。

为什么要集中配置？

因为 RAG 项目经常要调：

```text
chunk_size
chunk_overlap
top_k
temperature
model
embedding_model
```

集中配置可以减少到处改代码。

---

### 5.2 `documents/`

这个文件夹是本项目的知识库。

当前有三份示例文档：

1. `sample.txt`
2. `langchain_doc.txt`
3. `ai_intro.txt`

你可以把自己的 `.txt` 文档放进去，然后重新运行项目。

注意：

如果你修改了 documents 内容，最好删除旧的 `chroma_db/`，让系统重新创建向量库。

---

### 5.3 `01_document_loader.py`

这个文件演示文档加载。

它包括：

1. 手动创建 `Document`。
2. 用 `TextLoader` 加载单个文本文件。
3. 用 `DirectoryLoader` 批量加载目录。
4. 给 Document 补充 metadata。
5. 展示常见文档加载器。

重点理解：

```python
Document = page_content + metadata
```

`page_content` 是正文。

`metadata` 是来源、文件名、字符数等附加信息。

---

### 5.4 `02_text_splitter.py`

这个文件演示文本切分。

它包括：

1. 为什么要切分。
2. `RecursiveCharacterTextSplitter` 的使用。
3. 不同 `chunk_size` 和 `chunk_overlap` 对比。
4. 对 Document 对象进行切分。
5. 文本切分最佳实践。

重点理解：

```python
chunk_size=200
chunk_overlap=50
```

`chunk_size` 太小会丢上下文。

`chunk_size` 太大会降低检索精度。

---

### 5.5 `03_embeddings.py`

这个文件演示 Embedding。

它包括：

1. 什么是向量嵌入。
2. 如何调用在线 Embedding 模型。
3. 单条文本向量化。
4. 批量文本向量化。
5. 余弦相似度计算。

重点理解：

```text
文本 -> 向量 -> 相似度
```

RAG 能做语义检索，就是因为问题和文档都能被转换成向量。

---

### 5.6 `04_vector_store.py`

这个文件演示 Chroma 向量数据库。

它包括：

1. 什么是向量数据库。
2. 加载并切分文档。
3. 使用 Embedding 生成向量。
4. 把文档存入 Chroma。
5. 相似度搜索。
6. 带分数的搜索。

重点理解：

```python
Chroma.from_documents(...)
vectorstore.similarity_search(...)
```

---

### 5.7 `05_retriever.py`

这个文件演示 Retriever。

它包括：

1. 创建向量库。
2. 创建普通相似度检索器。
3. 创建 MMR 检索器。
4. 对比普通检索和 MMR 检索。

普通检索：

```text
只看相似度，可能返回重复内容。
```

MMR 检索：

```text
兼顾相关性和多样性。
```

---

### 5.8 `06_rag_chain.py`

这个文件演示完整 RAG Chain。

它包括：

1. 加载文档。
2. 切分文档。
3. 创建 Embedding。
4. 创建 Chroma 向量库。
5. 创建 Retriever。
6. 创建 ChatOpenAI。
7. 创建 Prompt。
8. 创建 RAG Chain。
9. 测试多个问题。
10. 对比有 RAG 和无 RAG。

重点理解：

```python
{"context": retriever | format_docs, "question": RunnablePassthrough()}
| prompt
| llm
| StrOutputParser()
```

这就是 LangChain 表达式语言串起来的 RAG 流程。

---

### 5.9 `main.py`

这是 Day 19 的完整交互式 RAG 问答助手。

它会：

1. 加载 documents 文档。
2. 切分文档。
3. 创建或加载 `chroma_db/`。
4. 创建 Retriever。
5. 创建聊天模型。
6. 创建 RAG Chain。
7. 提供交互式命令。

支持命令：

```text
example
docs
search
q
直接输入问题
```

其中：

`search` 只检索文档，不调用模型。

直接输入问题会执行完整 RAG 问答。

---

## 6. 练习题专区

下面是 Day 19 的完整练习题。

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

### 6.1 练习 1：加载不同格式的文档

文件：

```text
exercise1_doc_formats.py
```

练习目标：

理解 Document 对象结构，并学会从不同来源加载文档。

题目要求：

1. 手动创建多个 Document。
2. 使用 TextLoader 加载本地文件。
3. 给文档补充 metadata。
4. 用表格展示文档结构。

参考答案：

答案已经写在 `exercise1_doc_formats.py` 中。

核心知识：

```text
Document = page_content + metadata
```

如何运行：

```powershell
python exercise1_doc_formats.py
```

你应该观察到：

1. 手动创建的 Document 内容。
2. 从文件加载的 Document。
3. metadata 表格。

---

### 6.2 练习 2：对比文本切分参数

文件：

```text
exercise2_split_compare.py
```

练习目标：

理解不同 chunk 参数会改变文本块数量和上下文完整度。

题目要求：

1. 加载 documents 文档。
2. 用不同 `chunk_size` 和 `chunk_overlap` 切分。
3. 对比文本块数量。
4. 预览切分结果。

参考答案：

答案已经写在 `exercise2_split_compare.py` 中。

如何运行：

```powershell
python exercise2_split_compare.py
```

你应该观察到：

1. chunk_size 越小，文本块越多。
2. chunk_size 越大，文本块越少。
3. overlap 可以减少上下文断裂。

---

### 6.3 练习 3：构建自定义知识库

文件：

```text
exercise3_custom_kb.py
```

练习目标：

用代码创建一组自定义 Document，并构建一个小型 RAG 问答链。

题目要求：

1. 创建多条自定义知识文档。
2. 切分文档。
3. 创建 Embedding。
4. 存入 Chroma。
5. 创建 Retriever。
6. 创建 RAG Chain。
7. 对比有 RAG 和无 RAG。

参考答案：

答案已经写在 `exercise3_custom_kb.py` 中。

如何运行：

```powershell
python exercise3_custom_kb.py
```

你应该观察到：

1. 自定义知识库被创建。
2. RAG Chain 被构建。
3. 有 RAG 的回答更依赖自定义资料。

---

### 6.4 练习 4：多文档智能问答

文件：

```text
exercise4_multi_doc.py
```

练习目标：

构建支持多个文档来源的 RAG 问答，并在回答中引用来源。

题目要求：

1. 加载多份文档。
2. 统计每个来源的 chunk 数量。
3. 构建向量库和 Retriever。
4. 在 context 中保留来源信息。
5. 让模型回答时引用来源。

参考答案：

答案已经写在 `exercise4_multi_doc.py` 中。

如何运行：

```powershell
python exercise4_multi_doc.py
```

你应该观察到：

1. 文档来源统计表。
2. 每个问题检索到的来源。
3. 回答中包含来源引用。

---

### 6.5 练习 5：RAG 效果评估

文件：

```text
exercise5_rag_eval.py
```

练习目标：

学会评估不同 RAG 配置对回答效果的影响。

题目要求：

1. 对比不同 chunk_size。
2. 对比不同检索数量 k。
3. 观察回答预览。
4. 总结 RAG 质量评估指标。

参考答案：

答案已经写在 `exercise5_rag_eval.py` 中。

如何运行：

```powershell
python exercise5_rag_eval.py
```

你应该观察到：

1. chunk_size 影响文本块数量。
2. k 影响检索上下文数量。
3. RAG 评估不只看回答通顺，还要看检索相关性和是否幻觉。

---

## 7. 练习题对应文件答案说明

Day 19 的练习答案已经写进对应代码文件中。

对应关系：

```text
练习 1 -> exercise1_doc_formats.py
练习 2 -> exercise2_split_compare.py
练习 3 -> exercise3_custom_kb.py
练习 4 -> exercise4_multi_doc.py
练习 5 -> exercise5_rag_eval.py
```

这些文件不是空题目，而是完整可运行的参考答案。

---

## 8. API Key 与运行模式说明

Day 19 是完整 RAG 问答系统。

它和 Day 17 不同，Day 19 需要：

1. Embedding 模型。
2. Chat 模型。

因此推荐配置 API Key。

如果 API Key 或网络不可用：

1. `03_embeddings.py` 会打印失败原因。
2. `04_vector_store.py` 可能无法创建向量库。
3. `main.py` 初始化可能失败。

这是正常的，因为 Day 19 是完整在线 RAG 项目，不是纯本地模拟项目。

---

## 9. 常见问题

### 9.1 为什么初始化失败

可能原因：

1. `.env` 没有 API Key。
2. API Key 无效。
3. 网络不可用。
4. `OPENAI_BASE_URL` 和模型不匹配。
5. 依赖没有安装完整。

解决：

```powershell
pip install -r requirements.txt
```

并检查 `.env`。

---

### 9.2 为什么修改文档后答案没变

可能是因为已有旧的 `chroma_db/`。

解决方式：

1. 删除 `day19/chroma_db/`。
2. 重新运行 `python main.py`。
3. 系统会重新创建向量库。

---

### 9.3 为什么 search 结果对，但回答不理想

可能原因：

1. Prompt 不够明确。
2. 检索到的 chunk 太短。
3. top_k 太少。
4. 模型生成时有随机性。

可以尝试：

1. 调大 `TOP_K`。
2. 调整 `CHUNK_SIZE`。
3. 降低 `TEMPERATURE`。
4. 在 Prompt 中要求“只根据上下文回答”。

---

## 10. 推荐学习顺序

建议按这个顺序学习：

1. 读 `README.md`。
2. 运行 `python 01_document_loader.py`。
3. 运行 `python 02_text_splitter.py`。
4. 运行 `python 03_embeddings.py`。
5. 运行 `python 04_vector_store.py`。
6. 运行 `python 05_retriever.py`。
7. 运行 `python 06_rag_chain.py`。
8. 运行 `python main.py`。
9. 再做 5 个练习题。
10. 最后修改 documents，做自己的知识库问答。

---

## 11. Day 19 总结

Day 19 的关键词是：

```text
项目实战
RAG 问答系统
Document
Text Splitter
Embedding
Chroma
Retriever
RAG Chain
交互式问答
RAG 评估
```

一句话总结：

```text
Day 19 是把 RAG 从“知识点”变成“完整项目”的一天。
```

如果你能把 Day 19 跑通并解释每个模块的作用，说明你已经具备构建基础文档问答系统的能力了。
