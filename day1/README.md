# Day 1 - Python 基础

> 目标：掌握 Python 最基础但最重要的能力，包括变量、数据类型、条件判断、循环、函数、模块和文件操作。  
> Day 1 的重点不是写复杂项目，而是把后面做 API、Agent、RAG、Coding Agent 都会用到的 Python 基本功打牢。

---

## 1. Day 1 在学习路线里的位置

Day 1 是整个 AI Agent 学习计划的第一天。

从图片里的计划来看，Day 1 属于第一周的基础铺垫阶段，主题是：

**Python 基础**

后面你会学：

- API 调用
- Prompt Engineering
- Function Calling
- LangChain
- Tools
- Agents
- RAG
- FastAPI
- Playwright
- Git 和 Docker

这些内容看起来很高级，但底层都离不开 Python 基础。

所以 Day 1 要先解决几个问题：

1. Python 里怎么保存数据？
2. Python 里怎么判断条件？
3. Python 里怎么重复执行任务？
4. Python 里怎么封装重复逻辑？
5. Python 里怎么拆分模块？
6. Python 里怎么读写文件？

---

## 2. 本日学习目标

完成 Day 1 后，你应该能够：

1. 说清楚常见数据类型的区别。
2. 会使用变量保存字符串、数字、布尔值、列表、字典。
3. 会用 `if / elif / else` 做条件判断。
4. 会用 `for` 循环遍历列表、范围和字符串。
5. 会写简单函数，并知道什么时候应该封装函数。
6. 会把函数放到 `modules/` 里，再通过 `import` 使用。
7. 会读取文本文件、写入文本文件、追加文本内容。
8. 能完成一个简单的“学习记录分析器”小项目。

---

## 3. 项目整体说明

这个 `day1` 文件夹是一个完整的 Python 基础练习项目。

它包含：

- 一个交互式入口 `main.py`
- 两个核心模块
- 五个练习脚本
- 一个示例文本文件
- 一个输出目录
- 一份详细说明文档

你可以把它理解为：

**Day 1 的所有知识点，都被拆成了可以直接运行的小例子。**

---

## 4. 目录结构

```text
day1/
├── README.md
├── requirements.txt
├── config.py
├── main.py
├── data/
│   └── sample_notes.txt
├── output/
├── modules/
│   ├── __init__.py
│   ├── basics.py
│   └── file_tools.py
├── 01_variables_types.py
├── 02_conditions_loops.py
├── 03_functions_modules.py
├── 04_file_operations.py
└── 05_mini_project.py
```

---

## 5. 每个文件详细解释

### 5.1 `requirements.txt`

文件路径：
- [day1/requirements.txt](/D:/vscode项目/学习/day1/requirements.txt)

#### 作用

这个文件记录 Day 1 项目的依赖。

当前只用了一个依赖：

- `rich`

`rich` 的作用是让命令行输出更清楚，例如表格、颜色、面板等。

安装方式：

```bash
pip install -r requirements.txt
```

---

### 5.2 `config.py`

文件路径：
- [day1/config.py](/D:/vscode项目/学习/day1/config.py)

#### 作用

`config.py` 用来集中管理路径。

里面定义了：

- `BASE_DIR`
- `DATA_DIR`
- `OUTPUT_DIR`
- `SAMPLE_NOTES_FILE`
- `OUTPUT_REPORT_FILE`

#### 为什么 Day 1 就要学配置文件

因为后面的项目会越来越复杂。

如果你在每个文件里都写死路径，后面很容易乱。

把路径集中放到 `config.py`，会让代码更容易维护。

---

### 5.3 `main.py`

文件路径：
- [day1/main.py](/D:/vscode项目/学习/day1/main.py)

#### 作用

这是 Day 1 的主入口。

运行：

```bash
python main.py
```

会进入一个交互式菜单。

菜单支持：

- `profile`
- `grade`
- `even`
- `file`
- `q`

#### 每个命令做什么

`profile`

演示变量、列表、字典和格式化输出。

`grade`

输入一个分数，然后用条件判断返回等级。

`even`

用循环和列表推导式筛选偶数。

`file`

读取 `data/sample_notes.txt`，并统计文件信息。

`q`

退出程序。

#### 学习重点

你要看懂：

- 程序怎么进入 `main()`
- 菜单怎么循环等待输入
- 不同命令怎么分发到不同函数
- 代码如何调用 `modules/` 里的函数

---

### 5.4 `modules/basics.py`

文件路径：
- [day1/modules/basics.py](/D:/vscode项目/学习/day1/modules/basics.py)

#### 作用

这个文件放 Python 基础练习中会反复使用的函数。

包含：

- `build_profile`
- `format_profile`
- `calculate_grade`
- `filter_even_numbers`
- `multiplication_table`
- `count_words`

#### 函数逐个解释

`build_profile`

把姓名、年龄、技能列表组合成一个字典。

它练习的是：

- 字符串
- 整数
- 列表
- 字典
- 布尔值

`format_profile`

把字典格式化成一段适合展示的文本。

它练习的是：

- 字典取值
- 字符串拼接
- f-string
- 条件表达

`calculate_grade`

根据分数判断等级。

它练习的是：

- `if`
- `elif`
- `else`
- 边界判断

`filter_even_numbers`

筛选偶数。

它练习的是：

- 遍历
- 条件过滤
- 列表推导式

`multiplication_table`

生成九九乘法表。

它练习的是：

- 嵌套循环
- 字符串格式化
- 列表追加

`count_words`

统计英文文本中出现最多的单词。

它练习的是：

- 字符串处理
- 列表
- 字典思想
- `Counter`

---

### 5.5 `modules/file_tools.py`

文件路径：
- [day1/modules/file_tools.py](/D:/vscode项目/学习/day1/modules/file_tools.py)

#### 作用

这个文件封装了基础文件操作。

包含：

- `read_text_file`
- `write_text_file`
- `append_line`
- `summarize_text_file`

#### 为什么要封装文件操作

因为文件读写以后会经常用到。

比如：

- 读取配置
- 读取文档
- 保存日志
- 保存结果
- 生成报告

把文件操作封装起来，后面的代码会更清楚。

#### 函数解释

`read_text_file`

读取一个文本文件，并返回字符串。

`write_text_file`

把字符串写入文件，如果父目录不存在，会自动创建。

`append_line`

向文件末尾追加一行。

`summarize_text_file`

统计文件字符数、行数和单词数。

---

### 5.6 `modules/__init__.py`

文件路径：
- [day1/modules/__init__.py](/D:/vscode项目/学习/day1/modules/__init__.py)

#### 作用

这个文件让 `modules` 成为一个 Python 包。

它还统一导出常用函数。

这样以后可以更方便地导入：

```python
from modules.basics import calculate_grade
```

---

### 5.7 `data/sample_notes.txt`

文件路径：
- [day1/data/sample_notes.txt](/D:/vscode项目/学习/day1/data/sample_notes.txt)

#### 作用

这是 Day 1 的示例文本文件。

文件操作练习会读取它，然后统计：

- 字符数
- 行数
- 单词数
- 高频词

#### 为什么需要示例文件

因为文件操作必须有真实文件可以读。

这个文件就是练习素材。

---

### 5.8 `output/`

文件路径：
- [day1/output/](/D:/vscode项目/学习/day1/output)

#### 作用

这个目录用于保存程序生成的结果。

例如：

- `day1_report.txt`
- `mini_project_report.txt`

#### 为什么要单独放输出

这样可以把“输入数据”和“程序生成结果”分开。

这也是做项目时很重要的习惯。

---

## 6. 练习脚本详细说明

### 6.1 `01_variables_types.py`

文件路径：
- [day1/01_variables_types.py](/D:/vscode项目/学习/day1/01_variables_types.py)

#### 作用

练习变量和数据类型。

它展示了：

- 字符串：`str`
- 整数：`int`
- 浮点数：`float`
- 布尔值：`bool`
- 列表：`list`
- 字典：`dict`

#### 运行方式

```bash
python 01_variables_types.py
```

#### 你应该观察什么

重点看：

- 每个变量的值
- 每个变量的类型
- 列表怎么存多个值
- 字典怎么用键值对组织信息

---

### 6.2 `02_conditions_loops.py`

文件路径：
- [day1/02_conditions_loops.py](/D:/vscode项目/学习/day1/02_conditions_loops.py)

#### 作用

练习条件判断和循环。

它包含：

- 成绩等级判断
- 偶数筛选
- 九九乘法表

#### 运行方式

```bash
python 02_conditions_loops.py
```

#### 学习重点

你要重点理解：

- 条件判断是怎么一层一层走的
- 循环怎么遍历列表
- 嵌套循环怎么生成乘法表

---

### 6.3 `03_functions_modules.py`

文件路径：
- [day1/03_functions_modules.py](/D:/vscode项目/学习/day1/03_functions_modules.py)

#### 作用

练习函数和模块。

它会从 `modules/basics.py` 中导入函数，然后调用它们。

#### 运行方式

```bash
python 03_functions_modules.py
```

#### 学习重点

你要理解：

- 为什么要写函数
- 为什么要把函数放到模块里
- `import` 是怎么把别的文件里的代码拿过来用的

---

### 6.4 `04_file_operations.py`

文件路径：
- [day1/04_file_operations.py](/D:/vscode项目/学习/day1/04_file_operations.py)

#### 作用

练习文件操作。

它会：

1. 读取 `data/sample_notes.txt`
2. 统计文件信息
3. 统计高频词
4. 生成报告到 `output/day1_report.txt`

#### 运行方式

```bash
python 04_file_operations.py
```

#### 学习重点

你要重点看：

- 文件怎么读
- 文件怎么写
- 目录不存在时怎么创建
- 程序输出结果怎么保存

---

### 6.5 `05_mini_project.py`

文件路径：
- [day1/05_mini_project.py](/D:/vscode项目/学习/day1/05_mini_project.py)

#### 作用

这是 Day 1 的综合小项目。

它的名字是：

**学习记录分析器**

它会读取学习笔记，然后生成一份报告。

#### 运行方式

```bash
python 05_mini_project.py
```

#### 它综合了哪些知识点

- 变量
- 函数
- 模块导入
- 文件读取
- 文件写入
- 字符串处理
- 列表处理
- 报告生成

---

## 7. 推荐学习顺序

建议按照下面顺序学习：

1. 先运行 `01_variables_types.py`
2. 再运行 `02_conditions_loops.py`
3. 再运行 `03_functions_modules.py`
4. 再运行 `04_file_operations.py`
5. 最后运行 `05_mini_project.py`
6. 再运行 `main.py` 做交互复习

这样顺序最自然：

- 先学数据
- 再学控制流程
- 再学函数模块
- 再学文件
- 最后做综合练习

---

## 8. 如何运行

先进入 `day1` 目录：

```bash
cd day1
```

安装依赖：

```bash
pip install -r requirements.txt
```

运行主程序：

```bash
python main.py
```

运行单个练习：

```bash
python 01_variables_types.py
python 02_conditions_loops.py
python 03_functions_modules.py
python 04_file_operations.py
python 05_mini_project.py
```

---

## 9. Day 1 必须掌握的语法

### 9.1 变量

变量就是给一个值取名字。

```python
name = "小明"
age = 20
```

### 9.2 数据类型

常见类型包括：

- `str`
- `int`
- `float`
- `bool`
- `list`
- `dict`

### 9.3 条件判断

```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
```

### 9.4 循环

```python
for number in range(1, 10):
    print(number)
```

### 9.5 函数

```python
def add(a, b):
    return a + b
```

### 9.6 模块

```python
from modules.basics import calculate_grade
```

### 9.7 文件操作

```python
text = Path("data/sample_notes.txt").read_text(encoding="utf-8")
```

---

## 10. 常见问题

### 10.1 为什么要学这么基础的东西？

因为后面所有 AI 项目都离不开这些基础。

比如：

- API 参数是字典
- 对话历史是列表
- 工具调用需要函数
- RAG 需要文件读取
- Agent 需要条件判断和流程控制

### 10.2 为什么要把函数放到 `modules/` 里？

因为后面的项目会越来越大。

如果所有代码都写在一个文件里，会非常难维护。

### 10.3 为什么要生成 output 文件？

因为真实项目常常需要保存结果。

比如：

- 日志
- 报告
- 解析结果
- 中间数据

---

## 11. 完成标准

你可以用下面标准检查自己是否完成 Day 1：

1. 能运行所有 `.py` 文件。
2. 能解释变量和数据类型。
3. 能看懂 `if / elif / else`。
4. 能看懂 `for` 循环。
5. 能写一个简单函数。
6. 能从模块中导入函数。
7. 能读取和写入文本文件。
8. 能说清楚 `05_mini_project.py` 的完整流程。

---

## 12. 小结

Day 1 是后面所有内容的地基。

今天你不需要写很复杂的程序，但要把这些基础概念真正跑通：

- 数据怎么保存
- 逻辑怎么判断
- 任务怎么重复
- 代码怎么封装
- 文件怎么读写

这些能力会一直用到 Day 30。

