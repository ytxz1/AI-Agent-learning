# Day 17 - 文档加载与切分

> 目标：学会把本地文档加载成程序可以处理的 `Document` 对象，并掌握常见的切分方式，为后面的向量数据库和 RAG 铺路。  
> 这一节是“数据准备阶段”的核心，重点不是回答问题，而是把原始资料整理好。

---

## 1. Day 17 的定位

Day 17 位于课程中“数据处理基础”的位置。

前面的 Day 15、Day 16 已经让你了解了：

- 什么是 RAG
- 什么是向量数据库
- 为什么需要检索

而 Day 17 进一步回答一个更基础的问题：

**这些文档是怎么进入系统的？进入系统之后又是怎么被切成小块的？**

如果这一步做不好，后面的检索效果就会变差。

---

## 2. 本日学习目标

完成 Day 17 后，你应该能够：

1. 解释什么是文档加载。
2. 解释什么是文档切分。
3. 区分 `TextLoader`、`DirectoryLoader`、递归切分器、字符切分器、Markdown 标题切分器。
4. 理解 `chunk_size` 和 `chunk_overlap` 的作用。
5. 知道为什么切分策略会影响后续检索质量。
6. 独立搭建一个“加载 -> 切分 -> 统计 -> 预览”的文档处理管线。

---

## 3. 项目整体说明

这个 Day 17 项目是一个轻量级的“文档处理管线”。

它不负责生成答案，也不负责向量检索。

它只做一件事：

**把文件读进来，再把文件切成更合适的小块。**

项目里包含：

- 文档加载模块
- 文档切分模块
- 统一的配置文件
- 一个完整的命令行入口
- 5 个练习脚本

---

## 4. 目录结构总览

```text
day17/
├── README.md
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── documents/
│   ├── 01_python_intro.txt
│   ├── 02_langchain_notes.md
│   └── 03_project_brief.txt
├── modules/
│   ├── __init__.py
│   ├── loader.py
│   ├── splitter.py
│   └── pipeline.py
├── 01_loader_basics.py
├── 02_splitter_compare.py
├── 03_markdown_headers.py
├── 04_metadata_preserve.py
└── 05_full_pipeline.py
```

下面我们按文件逐个解释。

---

## 5. 核心文件详细说明

### 5.1 `main.py`

文件路径：
- [day17/main.py](/D:/vscode项目/学习/day17/main.py)

#### 作用

`main.py` 是整个项目的统一入口。

你运行：

```bash
python main.py
```

实际上就是启动 `05_full_pipeline.py` 里的交互式应用。

#### 为什么要单独有这个入口

这样做的好处是：

- 用户只要记住一个入口文件
- 后续如果想换成 Web 或 GUI，入口文件可以快速替换
- 业务逻辑可以继续保留在独立模块中

---

### 5.2 `config.py`

文件路径：
- [day17/config.py](/D:/vscode项目/学习/day17/config.py)

#### 作用

这个文件统一管理项目配置，包括：

- 文档目录
- chunk_size
- chunk_overlap
- 预览条数
- 每段预览显示的最大字符数

#### 为什么要这样做

文档切分是一个非常适合调参的任务。

比如：

- `chunk_size` 太小，信息会被切得太碎
- `chunk_size` 太大，后续处理会变慢
- `chunk_overlap` 太小，前后上下文可能断掉
- `chunk_overlap` 太大，重复内容会变多

把这些参数放在配置文件里，后面更容易实验和比较。

---

### 5.3 `requirements.txt`

文件路径：
- [day17/requirements.txt](/D:/vscode项目/学习/day17/requirements.txt)

#### 作用

记录本项目需要的依赖：

- `langchain-community`
- `langchain-text-splitters`
- `rich`
- `python-dotenv`

#### 为什么重要

这样别人可以通过：

```bash
pip install -r requirements.txt
```

快速搭建相同环境。

---

### 5.4 `.env.example`

文件路径：
- [day17/.env.example](/D:/vscode项目/学习/day17/.env.example)

#### 作用

这个文件给你提供默认配置样例。

这里并不需要 API Key，因为 Day 17 主要是本地文档处理。

#### 包含哪些配置

- `DOCS_DIR`
- `CHUNK_SIZE`
- `CHUNK_OVERLAP`
- `PREVIEW_LIMIT`
- `MAX_PREVIEW_CHARS`

---

### 5.5 `documents/`

文件路径：
- [day17/documents/](/D:/vscode项目/学习/day17/documents)

#### 作用

这个目录放示例文档，是 Day 17 最重要的输入数据区。

我们准备了三类文件：

- `01_python_intro.txt`
- `02_langchain_notes.md`
- `03_project_brief.txt`

#### 为什么要放真实文本样例

因为文档加载和切分不是空谈，它需要真实内容。

你可以通过这些样例文件观察：

- 文档是怎么被加载的
- 不同文件类型怎么处理
- 长文本怎么被切成 chunk

---

### 5.6 `modules/loader.py`

文件路径：
- [day17/modules/loader.py](/D:/vscode项目/学习/day17/modules/loader.py)

#### 作用

这个模块负责把文件读取成 `Document` 对象。

它主要做了几件事：

1. 解析文档目录路径。
2. 按文件类型加载 `.txt` 和 `.md`。
3. 给每个文档补充标准化 metadata。
4. 提供文档摘要和预览工具。

#### 为什么要单独做成模块

因为“读取文件”和“切分文本”本来就是两件事。

拆开以后你会更容易：

- 单独调试加载问题
- 单独调试切分问题
- 后面扩展 PDF、CSV、JSON 时更方便

#### 你应该重点关注什么

- `load_documents`
- `normalize_metadata`
- `summarize_documents`
- `preview_documents`

这些函数构成了加载阶段的核心。

---

### 5.7 `modules/splitter.py`

文件路径：
- [day17/modules/splitter.py](/D:/vscode项目/学习/day17/modules/splitter.py)

#### 作用

这个模块负责把长文档切成多个 chunk。

它提供了多种切分方式：

- `split_recursive`：递归切分
- `split_character`：字符切分
- `split_markdown_headers`：Markdown 标题切分
- `split_by_type`：按文件类型选择切分策略
- `compare_splitters`：对比不同切分器的结果

#### 为什么要比较多个切分器

因为不同文档结构适合不同切分方式。

比如：

- 普通文本适合递归切分
- Markdown 文档适合按标题拆分
- 简单文本也可以用字符切分做基础演示

#### 你应该重点理解的参数

`chunk_size`
- chunk 的最大长度

`chunk_overlap`
- 相邻 chunk 之间重叠的内容长度

它们直接影响后续检索和上下文连续性。

---

### 5.8 `modules/pipeline.py`

文件路径：
- [day17/modules/pipeline.py](/D:/vscode项目/学习/day17/modules/pipeline.py)

#### 作用

这个模块把加载和切分串成一个完整流程。

它负责：

- 加载文档
- 查看文档统计
- 查看文档预览
- 进行切分
- 对比切分器
- 查看 chunk 统计

#### 为什么要有这个模块

因为真实项目里通常不会只看某一个函数，而是看完整流程。

这个模块就是一个“文档处理管线”的骨架。

---

### 5.9 `modules/__init__.py`

文件路径：
- [day17/modules/__init__.py](/D:/vscode项目/学习/day17/modules/__init__.py)

#### 作用

它的作用比较简单：

- 让 `modules` 成为一个包
- 方便后续导入

---

## 6. 练习文件详细说明

### 6.1 `01_loader_basics.py`

文件路径：
- [day17/01_loader_basics.py](/D:/vscode项目/学习/day17/01_loader_basics.py)

#### 作用

这个脚本帮助你先看懂“加载”。

你会看到：

- 加载了多少文档
- 总字符数是多少
- 文件类型有哪些
- 每个文档的内容预览是什么

#### 学习重点

先别急着切分，先确认“文档有没有正确读进来”。

---

### 6.2 `02_splitter_compare.py`

文件路径：
- [day17/02_splitter_compare.py](/D:/vscode项目/学习/day17/02_splitter_compare.py)

#### 作用

这个脚本帮助你比较不同切分器的结果。

你会看到：

- recursive 切了多少块
- character 切了多少块
- by_type 切了多少块
- 平均 chunk 长度是多少

#### 学习重点

理解不同切分方式的区别，而不是只会调用一个函数。

---

### 6.3 `03_markdown_headers.py`

文件路径：
- [day17/03_markdown_headers.py](/D:/vscode项目/学习/day17/03_markdown_headers.py)

#### 作用

这个脚本专门演示 Markdown 标题切分。

它会告诉你：

- 如何按一级标题、二级标题、三级标题拆分
- 拆分后 chunk 的 metadata 是什么

#### 学习重点

Markdown 文档很适合按结构切分，因为标题本身就能表达章节边界。

---

### 6.4 `04_metadata_preserve.py`

文件路径：
- [day17/04_metadata_preserve.py](/D:/vscode项目/学习/day17/04_metadata_preserve.py)

#### 作用

这个脚本重点演示 metadata 保留。

你会看到：

- chunk 来自哪个文件
- chunk 使用了什么切分方式
- metadata 怎么跟着 chunk 一起走

#### 学习重点

后续做检索时，metadata 非常重要，因为它可以帮你追踪来源。

---

### 6.5 `05_full_pipeline.py`

文件路径：
- [day17/05_full_pipeline.py](/D:/vscode项目/学习/day17/05_full_pipeline.py)

#### 作用

这是 Day 17 的完整交互应用。

它支持：

- `load`
- `preview`
- `split`
- `compare`
- `stats`
- `chunks`

#### 为什么要有这个文件

因为 Day 17 不只是练习函数，更要让你感受到一个真正的“文档处理流程”。

---

## 7. Day 17 的核心知识点

### 7.1 什么是文档加载

文档加载就是把文件内容读成程序可以处理的对象。

在 LangChain 里，这类对象通常叫 `Document`。

一个 `Document` 往往包含两部分：

- `page_content`
- `metadata`

### 7.2 什么是文档切分

文档切分就是把长文本拆成多个小块。

这样做的目的通常是：

- 方便后续检索
- 方便做 embedding
- 方便限制上下文长度
- 方便提高回答质量

### 7.3 为什么切分很重要

如果切得太大：

- 后续处理慢
- 上下文浪费
- 检索命中不精准

如果切得太小：

- 信息被拆散
- 上下文不完整
- 答案可能丢失语义

所以切分其实是一个“平衡问题”。

### 7.4 `chunk_size` 和 `chunk_overlap`

`chunk_size`
- 控制每块最大长度

`chunk_overlap`
- 控制相邻块之间的重叠

重叠的意义是：

- 保留前后文
- 避免句子被切断
- 提升后续检索连续性

---

## 8. 推荐运行顺序

建议按照下面顺序学习：

1. 先看 `01_loader_basics.py`
2. 再看 `02_splitter_compare.py`
3. 再看 `03_markdown_headers.py`
4. 再看 `04_metadata_preserve.py`
5. 最后运行 `05_full_pipeline.py`

这样你会先从“读文件”开始，再慢慢进入“怎么切文件”。

---

## 9. 如何运行

安装依赖：

```bash
pip install -r requirements.txt
```

运行主程序：

```bash
python main.py
```

单独运行练习脚本也可以，例如：

```bash
python 01_loader_basics.py
python 02_splitter_compare.py
```

---

## 10. 常见问题

### 10.1 为什么我看不到文档内容？

先检查：

- `documents/` 目录里是否有文件
- 文件编码是不是 UTF-8
- `DOCS_DIR` 配置是否正确

### 10.2 为什么切分结果看起来很多？

这通常说明：

- `chunk_size` 太小
- 文档本身很长
- 你使用了重叠较大的设置

### 10.3 为什么 Markdown 文档更适合标题切分？

因为 Markdown 本身就已经带有清晰结构。

按照标题切分更容易保留语义边界。

---

## 11. 学习建议

1. 先把每个模块的职责看懂。
2. 自己修改 `CHUNK_SIZE` 和 `CHUNK_OVERLAP` 试试。
3. 给 `documents/` 里再加一个新文件观察效果。
4. 对比不同切分器的 chunk 结果。
5. 想一想后面的向量数据库为什么依赖这一步。

---

## 12. 小结

Day 17 是整个 RAG 体系里非常基础但又非常重要的一环。

你要记住：

- 文档先加载
- 再切分
- 再进入后续索引和检索

如果这一步做得好，后面的向量数据库和问答系统会更稳定、更容易调试。

