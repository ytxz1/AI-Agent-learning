# Day 17 - 文档加载与切分

> Day 17 的任务：掌握 RAG 项目里的数据准备阶段。
>
> 这一节不做问答，也不做向量检索，而是专门解决一个非常基础但非常关键的问题：
>
> ```text
> 原始文件如何进入程序？
> 长文档如何切成适合后续 Embedding 和检索的小块？
> ```

---

## 1. 今天你要学会什么

Day 17 对应学习计划表里的任务是：`文档加载与切分`。

完成这一天后，你应该能理解：

1. 什么是文档加载。
2. 什么是 LangChain 的 `Document` 对象。
3. `page_content` 和 `metadata` 分别保存什么。
4. 为什么长文档不能直接进入后续 RAG 流程。
5. 什么是 `chunk_size`。
6. 什么是 `chunk_overlap`。
7. 递归切分器和字符切分器有什么区别。
8. Markdown 标题切分适合什么场景。
9. metadata 为什么要跟着 chunk 保留下来。
10. 如何搭建一个完整的“加载 -> 预览 -> 切分 -> 统计”管线。

---

## 2. 项目结构

```text
day17/
├── README.md
├── requirements.txt
├── .env.example
├── config.py
├── main.py
├── 01_loader_basics.py
├── 02_splitter_compare.py
├── 03_markdown_headers.py
├── 04_metadata_preserve.py
├── 05_full_pipeline.py
├── documents/
│   ├── 01_python_intro.txt
│   ├── 02_langchain_notes.md
│   └── 03_project_brief.txt
└── modules/
    ├── __init__.py
    ├── loader.py
    ├── splitter.py
    └── pipeline.py
```

Day 17 的核心是：

```text
documents/
  -> loader.py
  -> splitter.py
  -> pipeline.py
  -> 练习脚本
```

---

## 3. 运行方式

### 3.1 安装依赖

在 `day17` 文件夹下运行：

```powershell
pip install -r requirements.txt
```

### 3.2 配置环境变量

复制 `.env.example` 为 `.env`：

```powershell
copy .env.example .env
```

Day 17 不需要 API Key。

因为这一节只做本地文档加载和文本切分，不调用大模型。

你可以在 `.env` 中调整：

```env
DOCS_DIR=documents
CHUNK_SIZE=300
CHUNK_OVERLAP=60
PREVIEW_LIMIT=3
MAX_PREVIEW_CHARS=160
```

### 3.3 运行完整交互程序

```powershell
python main.py
```

进入程序后可以输入：

```text
load
preview
split
compare
stats
chunks
q
```

### 3.4 分步骤运行练习脚本

```powershell
python 01_loader_basics.py
python 02_splitter_compare.py
python 03_markdown_headers.py
python 04_metadata_preserve.py
python 05_full_pipeline.py
```

建议第一次学习时按顺序运行。

---

## 4. 文档加载与切分的核心原理

### 4.1 什么是文档加载

文档加载就是把本地文件读进程序。

在 LangChain 中，加载后的文档通常是 `Document` 对象。

一个 `Document` 主要包含两部分：

```python
Document(
    page_content="文档正文内容",
    metadata={"source": "文件路径"}
)
```

`page_content` 保存正文。

`metadata` 保存来源、文件名、文件类型、长度等附加信息。

### 4.2 为什么需要 metadata

metadata 是“描述数据的数据”。

在 RAG 项目中，它非常重要。

原因：

1. 可以知道 chunk 来自哪个文件。
2. 可以知道 chunk 属于什么文件类型。
3. 可以在检索结果中展示引用来源。
4. 可以按文件、标签、用户、项目做过滤。
5. 方便调试切分和检索效果。

如果没有 metadata，后面检索出来的内容就很难追踪来源。

### 4.3 什么是文本切分

文本切分就是把长文档拆成多个小块。

这些小块通常叫：

```text
chunk
```

为什么要切分？

1. 长文档不适合直接做 Embedding。
2. 长文档不适合全部塞进模型上下文。
3. 用户问题通常只和文档中的一小段相关。
4. 切成小块后，向量检索会更精准。
5. 后续 RAG 可以只拿最相关的几个 chunk 回答。

### 4.4 什么是 chunk_size

`chunk_size` 表示每个 chunk 的最大长度。

例如：

```python
CHUNK_SIZE = 300
```

意思是每个文本块大约控制在 300 个字符以内。

如果 `chunk_size` 太小：

1. 文本会被切得很碎。
2. 上下文容易不完整。
3. 一个答案可能被拆到多个 chunk 里。

如果 `chunk_size` 太大：

1. 每个 chunk 内容太杂。
2. 检索可能不够精准。
3. 后续模型上下文会被浪费。

### 4.5 什么是 chunk_overlap

`chunk_overlap` 表示相邻 chunk 之间重复保留多少字符。

例如：

```python
CHUNK_OVERLAP = 60
```

意思是前后两个 chunk 会有大约 60 个字符重叠。

为什么需要 overlap？

因为句子可能刚好被切断。

overlap 可以保留前后文，让语义更连续。

---

## 5. 每个文件的详细解释

### 5.1 `config.py`

这个文件是 Day 17 的统一配置中心。

它负责读取 `.env` 和 `.env.example`。

主要配置：

1. `DOCS_DIR`：文档目录，默认是 `documents`。
2. `CHUNK_SIZE`：每个 chunk 的最大字符数。
3. `CHUNK_OVERLAP`：相邻 chunk 的重叠字符数。
4. `PREVIEW_LIMIT`：预览文档时展示几份文档。
5. `MAX_PREVIEW_CHARS`：每份预览最多展示多少字符。
6. `MARKDOWN_HEADERS`：Markdown 标题切分规则。

为什么要有配置文件？

因为文档切分经常需要调参。

你可以只改 `config.py` 或 `.env`，不用到处改代码。

---

### 5.2 `.env.example`

这个文件是配置模板。

Day 17 不需要 API Key。

它主要提供这些默认值：

```text
DOCS_DIR
CHUNK_SIZE
CHUNK_OVERLAP
PREVIEW_LIMIT
MAX_PREVIEW_CHARS
```

你可以复制成 `.env` 后修改。

---

### 5.3 `documents/`

这个文件夹保存示例文档。

当前有三份：

1. `01_python_intro.txt`
2. `02_langchain_notes.md`
3. `03_project_brief.txt`

它们分别用于演示：

1. 普通文本加载。
2. Markdown 文档加载。
3. 项目说明类文档切分。

你可以继续往里面添加 `.txt` 或 `.md` 文件。

---

### 5.4 `modules/loader.py`

这个文件负责文档加载。

核心函数：

```python
resolve_docs_dir(base_dir, docs_dir)
```

作用：

```text
把相对路径 documents 转成绝对路径。
```

核心函数：

```python
_load_by_glob(docs_path, glob_pattern)
```

作用：

```text
按文件类型加载文档，例如 *.txt 或 *.md。
```

它内部使用：

```python
DirectoryLoader
TextLoader
```

核心函数：

```python
normalize_metadata(doc)
```

作用：

```text
给每份文档补充统一 metadata。
```

补充字段包括：

1. `source`
2. `file_name`
3. `file_type`
4. `doc_length`

核心函数：

```python
load_documents(docs_path)
```

作用：

```text
加载 documents/ 中所有 .txt 和 .md 文档。
```

核心函数：

```python
summarize_documents(documents)
```

作用：

```text
统计文档数量、文件类型和总字符数。
```

核心函数：

```python
preview_documents(documents)
```

作用：

```text
生成文档预览文本。
```

---

### 5.5 `modules/splitter.py`

这个文件负责文档切分。

核心函数：

```python
split_recursive(documents, chunk_size, chunk_overlap)
```

作用：

```text
使用 RecursiveCharacterTextSplitter 递归切分文档。
```

递归切分器会按优先级尝试更自然的分隔符。

本项目设置的分隔符包括：

```python
["\n\n", "\n", "。", "！", "？", "；", ";", " "]
```

核心函数：

```python
split_character(documents, chunk_size, chunk_overlap)
```

作用：

```text
使用 CharacterTextSplitter 做基础字符切分。
```

它比较简单，适合和递归切分器做对比。

核心函数：

```python
split_markdown_headers(document)
```

作用：

```text
按 Markdown 标题结构切分文档。
```

它会识别：

1. `#`
2. `##`
3. `###`

这种方式适合结构清晰的 Markdown 文档。

核心函数：

```python
split_by_type(documents, chunk_size, chunk_overlap)
```

作用：

```text
根据文件类型自动选择切分方式。
```

当前逻辑：

```text
.md -> Markdown 标题切分
其他 -> 递归切分
```

核心函数：

```python
compare_splitters(documents, chunk_size, chunk_overlap)
```

作用：

```text
对比 recursive、character、by_type 三种切分策略。
```

---

### 5.6 `modules/pipeline.py`

这个文件把加载和切分串成完整管线。

核心类：

```python
DocumentPipeline
```

它保存这些状态：

1. `base_dir`
2. `docs_dir`
3. `chunk_size`
4. `chunk_overlap`
5. `documents`
6. `chunks`
7. `comparisons`

常用方法：

```python
load()
document_summary()
document_previews()
split()
split_by_type()
compare()
chunk_report()
chunk_previews()
```

为什么要有 pipeline？

因为真实项目不是只调用一个函数，而是一整条流程：

```text
加载文档
  -> 查看统计
  -> 预览内容
  -> 切分文档
  -> 查看 chunk 统计
  -> 预览 chunk
```

---

### 5.7 `modules/__init__.py`

这个文件让 `modules/` 成为 Python 包。

Day 17 的核心逻辑在：

1. `loader.py`
2. `splitter.py`
3. `pipeline.py`

---

### 5.8 `01_loader_basics.py`

这是练习 1 的代码文件。

作用：

```text
演示文档加载基础。
```

它会打印：

1. 文档数量。
2. 总字符数。
3. 文件类型分布。
4. 文档内容预览。

重点理解：

```python
pipeline.load()
pipeline.document_summary()
pipeline.document_previews()
```

---

### 5.9 `02_splitter_compare.py`

这是练习 2 的代码文件。

作用：

```text
对比不同切分器的结果。
```

它会展示：

1. 切分策略名称。
2. chunk 数量。
3. 平均 chunk 长度。

重点理解：

```python
pipeline.compare()
```

---

### 5.10 `03_markdown_headers.py`

这是练习 3 的代码文件。

作用：

```text
专门演示 Markdown 标题切分。
```

它会：

1. 加载全部文档。
2. 筛选 `.md` 文档。
3. 使用 `split_markdown_headers()` 切分。
4. 打印 chunk 内容和 metadata。

---

### 5.11 `04_metadata_preserve.py`

这是练习 4 的代码文件。

作用：

```text
观察文档切分后 metadata 是否被保留。
```

你应该重点看输出里的：

```text
source
file_name
file_type
doc_length
splitter
```

这些信息后面做 RAG 引用来源时很重要。

---

### 5.12 `05_full_pipeline.py`

这是 Day 17 的完整交互应用。

它提供一个命令行小程序。

支持命令：

```text
load
preview
split
compare
stats
chunks
q
```

核心类：

```python
DocumentApp
```

它负责：

1. 创建 `DocumentPipeline`。
2. 显示菜单。
3. 加载文档。
4. 预览文档。
5. 切分文档。
6. 对比切分器。
7. 预览 chunk。

---

### 5.13 `main.py`

这是 Day 17 的统一入口。

运行：

```powershell
python main.py
```

它会启动 `05_full_pipeline.py` 中的完整交互应用。

---

## 6. 练习题专区

下面是 Day 17 的完整练习题。

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

### 6.1 练习 1：文档加载基础

文件：

```text
01_loader_basics.py
```

练习目标：

确认本地文档可以被正确读取成 LangChain `Document` 对象。

题目要求：

1. 加载 `documents/` 下的 `.txt` 和 `.md` 文件。
2. 打印文档数量。
3. 打印总字符数。
4. 打印文件类型分布。
5. 打印文档内容预览。

操作提示：

重点观察：

```text
文档数量
总字符数
文件类型
文档预览
```

参考答案：

答案已经写在 `01_loader_basics.py` 中。

核心流程：

```text
DocumentPipeline()
  -> load()
  -> document_summary()
  -> document_previews()
```

如何运行：

```powershell
python 01_loader_basics.py
```

你应该观察到：

1. 文档数量应该是 3。
2. 文件类型里应该包含 `.txt` 和 `.md`。
3. 文档预览中能看到每个文件的部分内容。

---

### 6.2 练习 2：对比不同切分器

文件：

```text
02_splitter_compare.py
```

练习目标：

理解不同切分策略会产生不同数量和长度的 chunk。

题目要求：

1. 加载示例文档。
2. 使用 recursive 切分器切分。
3. 使用 character 切分器切分。
4. 使用 by_type 策略切分。
5. 用表格对比 chunk 数量和平均长度。

操作提示：

重点看：

```text
recursive
character
by_type
```

参考答案：

答案已经写在 `02_splitter_compare.py` 中。

核心代码：

```python
comparisons = pipeline.compare()
```

如何运行：

```powershell
python 02_splitter_compare.py
```

你应该观察到：

1. 不同切分器的 chunk 数量可能不同。
2. 平均长度也可能不同。
3. Markdown 文档在 `by_type` 中会优先使用标题切分。

---

### 6.3 练习 3：Markdown 标题切分

文件：

```text
03_markdown_headers.py
```

练习目标：

理解 Markdown 文档可以按标题层级切分。

题目要求：

1. 加载全部文档。
2. 找到 `.md` 文件。
3. 使用 `split_markdown_headers()` 切分。
4. 打印每个 chunk 的内容和 metadata。

操作提示：

Markdown 标题切分会识别：

```text
#
##
###
```

参考答案：

答案已经写在 `03_markdown_headers.py` 中。

核心代码：

```python
md_docs = [doc for doc in pipeline.documents if doc.metadata.get("file_type") == ".md"]
chunks = split_markdown_headers(md_docs[0])
```

如何运行：

```powershell
python 03_markdown_headers.py
```

你应该观察到：

1. 输出中会出现多个 Markdown chunk。
2. metadata 中会保留原始文件信息。
3. metadata 中可能包含标题层级信息。

---

### 6.4 练习 4：保留 metadata

文件：

```text
04_metadata_preserve.py
```

练习目标：

确认文档切分后，来源信息仍然保留在 chunk 里。

题目要求：

1. 加载文档。
2. 使用 `split_by_type()` 切分。
3. 打印前 5 个 chunk。
4. 查看每个 chunk 的 metadata。

操作提示：

重点看：

```text
source
file_name
file_type
doc_length
splitter
```

参考答案：

答案已经写在 `04_metadata_preserve.py` 中。

核心代码：

```python
pipeline.split_by_type()
for chunk in pipeline.chunks[:5]:
    print(chunk.metadata)
```

如何运行：

```powershell
python 04_metadata_preserve.py
```

你应该观察到：

1. 每个 chunk 都能追踪到来源文件。
2. Markdown chunk 会带有 `splitter=markdown_headers`。
3. metadata 没有因为切分而丢失。

---

### 6.5 练习 5：完整文档处理管线

文件：

```text
05_full_pipeline.py
```

练习目标：

把加载、预览、切分、对比和 chunk 预览串成一个完整交互流程。

题目要求：

1. 启动交互程序。
2. 输入 `load` 加载文档。
3. 输入 `preview` 查看文档预览。
4. 输入 `split` 执行切分。
5. 输入 `chunks` 查看 chunk 预览。
6. 输入 `compare` 对比切分策略。
7. 输入 `q` 退出。

操作提示：

建议按这个命令顺序输入：

```text
load
preview
split
chunks
compare
stats
q
```

参考答案：

答案已经写在 `05_full_pipeline.py` 中。

核心类：

```python
DocumentApp
```

如何运行：

```powershell
python 05_full_pipeline.py
```

或：

```powershell
python main.py
```

你应该观察到：

1. 程序会显示命令菜单。
2. `load` 后显示加载文档数量。
3. `preview` 后显示文档统计和预览。
4. `split` 后显示 chunk 数量和平均长度。
5. `chunks` 后显示切分结果预览。
6. `compare` 后显示不同切分策略对比。

---

## 7. 练习题对应文件答案说明

Day 17 的练习答案已经写进对应代码文件中。

对应关系：

```text
练习 1 -> 01_loader_basics.py
练习 2 -> 02_splitter_compare.py
练习 3 -> 03_markdown_headers.py
练习 4 -> 04_metadata_preserve.py
练习 5 -> 05_full_pipeline.py
```

这些练习文件都是完整可运行的参考答案。

你可以直接运行它们查看效果。

---

## 8. Day 17 是否需要 API Key

Day 17 不需要 API Key。

原因：

1. 这一节只处理本地文件。
2. 不调用大模型。
3. 不生成 Embedding。
4. 不访问向量数据库 API。

Day 17 的输出完全来自本地文档加载和文本切分。

真正需要 API 的地方通常是：

1. Embedding。
2. Chat 模型回答。
3. 在线检索服务。

这些会在后续 RAG 问答系统里使用。

---

## 9. 常见问题

### 9.1 为什么加载不到文档

可能原因：

1. `documents/` 文件夹不存在。
2. 文件不是 `.txt` 或 `.md`。
3. `DOCS_DIR` 配置写错。
4. 文件编码不是 UTF-8。

解决方式：

1. 检查 `day17/documents/` 是否有文件。
2. 检查 `.env` 中的 `DOCS_DIR`。
3. 先运行 `python 01_loader_basics.py`。

---

### 9.2 为什么切分结果很多

可能原因：

1. `CHUNK_SIZE` 太小。
2. `CHUNK_OVERLAP` 太大。
3. 文档本身比较长。
4. Markdown 标题比较多。

解决方式：

1. 把 `CHUNK_SIZE` 调大。
2. 把 `CHUNK_OVERLAP` 调小。
3. 运行 `python 02_splitter_compare.py` 对比结果。

---

### 9.3 为什么 Markdown 适合按标题切分

因为 Markdown 本身有结构。

例如：

```markdown
# 一级标题
## 二级标题
### 三级标题
```

标题通常代表章节边界。

按标题切分更容易保留语义完整性。

---

### 9.4 为什么 metadata 必须保留

因为后续 RAG 检索时，需要知道答案来源。

metadata 可以帮助你：

1. 展示引用来源。
2. 过滤某个文件。
3. 调试检索结果。
4. 定位原始资料。

---

## 10. 推荐学习顺序

建议按这个顺序学习：

1. 先读 `README.md`。
2. 运行 `python 01_loader_basics.py`。
3. 打开 `modules/loader.py` 看加载逻辑。
4. 运行 `python 02_splitter_compare.py`。
5. 打开 `modules/splitter.py` 看切分逻辑。
6. 运行 `python 03_markdown_headers.py`。
7. 理解 Markdown 标题切分。
8. 运行 `python 04_metadata_preserve.py`。
9. 理解 metadata 为什么要保留。
10. 运行 `python 05_full_pipeline.py`。
11. 最后运行 `python main.py`。

---

## 11. Day 17 总结

Day 17 的关键词是：

```text
Document
page_content
metadata
loader
splitter
chunk_size
chunk_overlap
Markdown header
pipeline
```

你可以这样理解：

```text
Day 15 是理解 RAG 整体。
Day 16 是理解向量库存储和检索。
Day 17 是把原始资料整理成后续可以检索的数据块。
```

一句话总结：

```text
文档加载与切分，就是把杂乱的原始文件变成结构清楚、来源可追踪、适合检索的 chunk。
```

这一步做好了，后面的向量数据库、RAG 检索链、文档问答系统都会更稳定。
