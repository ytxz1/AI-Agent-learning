# Day 2 - Python 进阶

> 目标：在 Day 1 的基础上，继续掌握 Python 进阶常用能力，包括列表、字典、集合、类和对象、异常处理，以及 `requests`、`json`、`os/pathlib`、`typing` 等常用库。  
> Day 2 的最终产出是一个可以运行的“学生成绩管理器”小项目。

---

## 1. Day 2 在学习路线里的位置

Day 1 学的是 Python 基础：

- 变量
- 数据类型
- 条件判断
- 循环
- 函数
- 文件操作

Day 2 往前推进一步，进入 Python 进阶：

- 更熟练地处理列表、字典、集合
- 用类和对象组织数据
- 用异常处理让程序更稳定
- 用常用库完成真实任务

这些能力会直接影响后面的 API、Tools、Agent、RAG 项目。

---

## 2. 本日学习目标

完成 Day 2 后，你应该能够：

1. 熟练使用 `list`、`dict`、`set`。
2. 会对列表排序、筛选、分组。
3. 会用字典保存结构化数据。
4. 会用集合去重。
5. 会定义一个简单类。
6. 会把字典转换成对象，也会把对象转换回字典。
7. 会使用 `try / except / finally` 处理异常。
8. 会读写 JSON 文件。
9. 会使用 `requests` 做简单网络请求。
10. 会使用 `pathlib` 处理路径。

---

## 3. 项目整体说明

这个 `day2` 项目围绕一个主题展开：

**学生成绩管理器**

项目会从 `data/students.json` 读取学生数据，然后完成：

- 加载 JSON
- 转换成 Student 对象
- 计算平均分
- 判断成绩等级
- 排序
- 分组
- 收集标签
- 输出 JSON 报告
- 输出文本报告

这个小项目虽然不复杂，但很适合练 Python 进阶基础。

---

## 4. 目录结构

```text
day2/
├── README.md
├── requirements.txt
├── config.py
├── main.py
├── data/
│   └── students.json
├── output/
├── modules/
│   ├── __init__.py
│   ├── student.py
│   ├── collections_tools.py
│   ├── json_tools.py
│   └── api_tools.py
├── 01_collections.py
├── 02_classes_objects.py
├── 03_exceptions.py
├── 04_common_libraries.py
└── 05_student_manager.py
```

---

## 5. 核心文件详细说明

### 5.1 `requirements.txt`

文件路径：
- [day2/requirements.txt](/D:/vscode项目/学习/day2/requirements.txt)

#### 作用

记录 Day 2 用到的依赖。

当前包含：

- `rich`
- `requests`

`rich` 用来美化命令行输出。  
`requests` 用来演示网络请求。

安装方式：

```bash
pip install -r requirements.txt
```

---

### 5.2 `config.py`

文件路径：
- [day2/config.py](/D:/vscode项目/学习/day2/config.py)

#### 作用

集中管理路径配置。

里面定义了：

- `BASE_DIR`
- `DATA_DIR`
- `OUTPUT_DIR`
- `STUDENTS_JSON`
- `OUTPUT_REPORT`
- `TEXT_REPORT`

#### 为什么要这样做

因为 Day 2 开始涉及多个输入输出文件。

如果路径散落在每个脚本里，后面很难维护。

---

### 5.3 `main.py`

文件路径：
- [day2/main.py](/D:/vscode项目/学习/day2/main.py)

#### 作用

这是 Day 2 的主入口。

运行：

```bash
python main.py
```

会进入交互式菜单。

支持命令：

- `list`
- `group`
- `tags`
- `api`
- `q`

#### 每个命令解释

`list`

显示学生平均分排行。

`group`

按成绩等级给学生分组。

`tags`

收集所有学生标签，并用 `set` 去重。

`api`

演示 `requests` 在线请求，如果网络不可用会自动使用本地兜底数据。

`q`

退出。

---

### 5.4 `data/students.json`

文件路径：
- [day2/data/students.json](/D:/vscode项目/学习/day2/data/students.json)

#### 作用

这是 Day 2 的示例数据文件。

里面保存了多个学生，每个学生包含：

- `id`
- `name`
- `age`
- `scores`
- `tags`

#### 为什么用 JSON

因为 JSON 是后面 API、LLM 输出解析、Agent 工具调用里非常常见的数据格式。

Day 2 先练会 JSON，后面会轻松很多。

---

## 6. 模块详细说明

### 6.1 `modules/student.py`

文件路径：
- [day2/modules/student.py](/D:/vscode项目/学习/day2/modules/student.py)

#### 作用

定义 `Student` 类。

这个类代表一个学生对象。

#### 主要字段

- `id`
- `name`
- `age`
- `scores`
- `tags`

#### 主要方法

`from_dict`

从字典创建 `Student` 对象。

`to_dict`

把 `Student` 对象转换成字典。

`average_score`

计算平均分。

`level`

根据平均分判断等级。

`has_tag`

判断学生是否有某个标签。

#### 学习重点

你要理解：

- 类是模板
- 对象是根据类创建出来的具体实例
- 方法是写在类里的函数
- 对象可以同时保存数据和行为

---

### 6.2 `modules/collections_tools.py`

文件路径：
- [day2/modules/collections_tools.py](/D:/vscode项目/学习/day2/modules/collections_tools.py)

#### 作用

封装列表、字典、集合相关操作。

包含：

- `sort_students_by_average`
- `group_students_by_level`
- `collect_all_tags`
- `find_students_by_tag`

#### 学习重点

这个文件重点练：

- `list` 排序
- `dict` 分组
- `set` 去重
- 列表推导式筛选

---

### 6.3 `modules/json_tools.py`

文件路径：
- [day2/modules/json_tools.py](/D:/vscode项目/学习/day2/modules/json_tools.py)

#### 作用

封装 JSON 读写。

包含：

- `load_json`
- `save_json`
- `safe_load_json`

#### 异常处理在哪里体现

`load_json` 会处理两类情况：

- 文件不存在
- JSON 格式错误

`safe_load_json` 会在出错时返回默认值。

这就是异常处理在真实项目里的用法。

---

### 6.4 `modules/api_tools.py`

文件路径：
- [day2/modules/api_tools.py](/D:/vscode项目/学习/day2/modules/api_tools.py)

#### 作用

演示 `requests` 的基础用法。

它会尝试请求 GitHub 的 Python 仓库信息。

如果网络不可用，就返回本地兜底数据。

#### 为什么这样设计

因为 Day 2 的重点是学习 `requests` 的流程，不应该因为网络问题导致整个脚本不能跑。

---

### 6.5 `modules/__init__.py`

文件路径：
- [day2/modules/__init__.py](/D:/vscode项目/学习/day2/modules/__init__.py)

#### 作用

让 `modules` 成为 Python 包，并统一导出常用函数和类。

---

## 7. 练习脚本详细说明

### 7.1 `01_collections.py`

文件路径：
- [day2/01_collections.py](/D:/vscode项目/学习/day2/01_collections.py)

#### 作用

练习列表、字典、集合。

它会：

1. 读取学生 JSON。
2. 转换成 Student 对象。
3. 按平均分排序。
4. 按等级分组。
5. 收集所有标签。

#### 运行方式

```bash
python 01_collections.py
```

---

### 7.2 `02_classes_objects.py`

文件路径：
- [day2/02_classes_objects.py](/D:/vscode项目/学习/day2/02_classes_objects.py)

#### 作用

练习类和对象。

它会手动创建一个 `Student` 对象，然后调用对象方法。

#### 运行方式

```bash
python 02_classes_objects.py
```

#### 学习重点

重点看：

- 对象怎么创建
- 方法怎么调用
- 对象怎么转字典

---

### 7.3 `03_exceptions.py`

文件路径：
- [day2/03_exceptions.py](/D:/vscode项目/学习/day2/03_exceptions.py)

#### 作用

练习异常处理。

它会故意读取一个不存在的文件，然后捕获错误。

#### 运行方式

```bash
python 03_exceptions.py
```

#### 学习重点

你要理解：

- `try` 里放可能出错的代码
- `except` 负责处理错误
- `finally` 不管是否出错都会执行
- 安全函数可以用默认值兜底

---

### 7.4 `04_common_libraries.py`

文件路径：
- [day2/04_common_libraries.py](/D:/vscode项目/学习/day2/04_common_libraries.py)

#### 作用

练习常用库：

- `requests`
- `os`
- `pathlib`
- `typing`

#### 运行方式

```bash
python 04_common_libraries.py
```

#### 学习重点

这个文件会让你看到：

- 当前工作目录怎么获取
- 用户目录怎么获取
- 网络请求怎么发起
- 网络失败时怎么兜底

---

### 7.5 `05_student_manager.py`

文件路径：
- [day2/05_student_manager.py](/D:/vscode项目/学习/day2/05_student_manager.py)

#### 作用

这是 Day 2 的综合小项目。

它会：

1. 加载学生 JSON。
2. 创建 Student 对象。
3. 计算平均分。
4. 判断等级。
5. 生成结构化 JSON 报告。
6. 生成文本报告。

#### 运行方式

```bash
python 05_student_manager.py
```

#### 输出文件

运行后会生成：

- [day2/output/students_report.json](/D:/vscode项目/学习/day2/output/students_report.json)
- [day2/output/students_report.txt](/D:/vscode项目/学习/day2/output/students_report.txt)

---

## 8. 推荐学习顺序

建议按下面顺序学习：

1. `01_collections.py`
2. `02_classes_objects.py`
3. `03_exceptions.py`
4. `04_common_libraries.py`
5. `05_student_manager.py`
6. `main.py`

这样顺序比较自然：

- 先学数据结构
- 再学类和对象
- 再学异常处理
- 再学常用库
- 最后做综合项目

---

## 9. 如何运行

进入 Day 2 目录：

```bash
cd D:\vscode项目\学习\day2
```

安装依赖：

```bash
pip install -r requirements.txt
```

运行主程序：

```bash
python main.py
```

运行综合项目：

```bash
python 05_student_manager.py
```

---

## 10. Day 2 必须掌握的知识点

### 10.1 列表

列表适合保存一组有顺序的数据。

```python
skills = ["Python", "AI", "FastAPI"]
```

### 10.2 字典

字典适合保存结构化数据。

```python
student = {"name": "小明", "age": 18}
```

### 10.3 集合

集合适合去重。

```python
tags = {"python", "ai", "python"}
```

### 10.4 类和对象

类是模板，对象是实例。

```python
student = Student(id=1, name="小明", age=18, scores={}, tags=[])
```

### 10.5 异常处理

异常处理让程序出错时不至于直接崩掉。

```python
try:
    data = load_json("students.json")
except FileNotFoundError:
    data = []
```

### 10.6 JSON

JSON 是非常常见的数据交换格式。

后面的 API 和 LLM 输出都会经常遇到 JSON。

### 10.7 requests

`requests` 用来发起 HTTP 请求。

后面学习 API 调用时会继续用到它。

---

## 11. 完成标准

你可以用下面标准检查自己是否完成 Day 2：

1. 能运行所有练习脚本。
2. 能解释列表、字典、集合的区别。
3. 能写一个简单类。
4. 能解释对象和字典的转换。
5. 能处理文件不存在异常。
6. 能读取和保存 JSON。
7. 能使用 `requests` 发起请求。
8. 能运行 `05_student_manager.py` 并生成报告。

---

## 12. 小结

Day 2 是从“能写简单 Python”进入“能写小工具脚本”的关键一步。

今天你要真正掌握：

- 数据怎么组织
- 逻辑怎么封装成类
- 错误怎么处理
- JSON 怎么读写
- 常用库怎么使用

这些能力后面会反复出现，尤其是在 API、Tools 和 Agent 项目里。

