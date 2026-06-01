# Day 3 - API 调用入门

> 目标：理解什么是 API，学会配置 API Key，掌握 Chat Completions 的基本请求方式，并能够解析模型返回的响应。  
> Day 3 是从“只写本地 Python”走向“调用在线 AI 能力”的第一步。

---

## 1. Day 3 在学习路线里的位置

Day 1 和 Day 2 主要是 Python 基础和进阶。

Day 3 开始进入 AI 应用开发中非常重要的一块：

**API 调用**

后面你要做的很多事情都离不开 API：

- 调用大模型
- 调用工具服务
- 调用搜索接口
- 调用天气接口
- 调用向量数据库服务
- 调用自己写的 FastAPI 服务

所以 Day 3 的重点是：

1. 认识 API。
2. 知道 API 请求由哪些部分组成。
3. 会把 API Key 放到 `.env` 里。
4. 会发送 Chat Completions 请求。
5. 会解析模型返回的 JSON。

---

## 2. 本日学习目标

完成 Day 3 后，你应该能够：

1. 解释什么是 API。
2. 解释什么是 URL、Header、Payload、Response。
3. 知道为什么 API Key 不能写死在代码里。
4. 会使用 `requests.post` 发送 JSON 请求。
5. 会构造 Chat Completions 的 `messages` 参数。
6. 会从响应里提取 `choices[0].message.content`。
7. 会保存请求和响应日志，方便调试。
8. 能运行一个简单的 API 对话助手。

---

## 3. 项目整体说明

这个 `day3` 项目是一个 API 调用入门项目。

它包含：

- API 基础概念演示
- 环境变量配置演示
- Chat Completions 请求封装
- 响应解析
- 本地模拟 API
- 交互式对话 Demo

这个项目的设计是：

**有 API Key 就调用在线 API，没有 API Key 或请求失败就使用本地模拟响应。**

这样你既能学习真实 API 调用，也不会因为网络或 key 问题卡住。

---

## 4. 目录结构

```text
day3/
├── README.md
├── requirements.txt
├── .env.example
├── config.py
├── main.py
├── data/
├── output/
├── modules/
│   ├── __init__.py
│   ├── http_client.py
│   ├── mock_api.py
│   ├── response_parser.py
│   └── chat_client.py
├── 01_what_is_api.py
├── 02_environment_config.py
├── 03_chat_completions.py
├── 04_parse_response.py
└── 05_full_chat_demo.py
```

---

## 5. API 基础概念

### 5.1 什么是 API

API 可以理解为：

**程序和程序之间约定好的调用接口。**

你按照对方规定的格式发送请求，对方按照规定的格式返回结果。

### 5.2 一个 API 请求通常包含什么

一个常见 API 请求通常包含：

- URL
- Method
- Headers
- Payload
- Response

### 5.3 URL

URL 是请求地址。

例如：

```text
https://api.openai.com/v1/chat/completions
```

### 5.4 Method

Method 是请求方法。

常见有：

- `GET`
- `POST`
- `PUT`
- `DELETE`

Chat Completions 通常使用 `POST`。

### 5.5 Headers

Headers 是请求头。

常见内容：

```json
{
  "Authorization": "Bearer YOUR_API_KEY",
  "Content-Type": "application/json"
}
```

### 5.6 Payload

Payload 是请求体。

Chat Completions 常见请求体：

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {"role": "user", "content": "什么是 API？"}
  ],
  "temperature": 0.2
}
```

### 5.7 Response

Response 是 API 返回结果。

Chat Completions 的回答通常在：

```python
response["choices"][0]["message"]["content"]
```

---

## 6. 核心文件详细说明

### 6.1 `requirements.txt`

文件路径：
- [day3/requirements.txt](/D:/vscode项目/学习/day3/requirements.txt)

#### 作用

记录项目依赖。

包含：

- `python-dotenv`
- `requests`
- `rich`

安装方式：

```bash
pip install -r requirements.txt
```

---

### 6.2 `.env.example`

文件路径：
- [day3/.env.example](/D:/vscode项目/学习/day3/.env.example)

#### 作用

这是环境变量示例文件。

里面包含：

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `OPENAI_MODEL`
- `TEMPERATURE`
- `TIMEOUT_SECONDS`
- `USE_MOCK_WHEN_FAILED`

#### 如何使用

你可以新建一个 `.env` 文件，然后参考 `.env.example` 填入真实配置。

示例：

```env
OPENAI_API_KEY=你的真实key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

#### 为什么不能把 key 写到代码里

因为 API Key 是敏感信息。

如果写进代码，可能会被上传到 GitHub 或发给别人。

---

### 6.3 `config.py`

文件路径：
- [day3/config.py](/D:/vscode项目/学习/day3/config.py)

#### 作用

统一读取 `.env` 和 `.env.example`。

并生成：

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `OPENAI_MODEL`
- `CHAT_COMPLETIONS_URL`
- `REQUEST_LOG_FILE`
- `RESPONSE_LOG_FILE`

#### 为什么重要

它让其他文件不用关心环境变量怎么读，只需要导入配置即可。

---

### 6.4 `modules/http_client.py`

文件路径：
- [day3/modules/http_client.py](/D:/vscode项目/学习/day3/modules/http_client.py)

#### 作用

封装底层 HTTP 请求。

主要内容：

- `APIRequestError`
- `post_json`

#### 为什么单独封装

因为真实项目里 API 请求经常需要：

- 超时控制
- 错误处理
- 重试
- 日志记录

先封装起来，后面扩展更方便。

---

### 6.5 `modules/mock_api.py`

文件路径：
- [day3/modules/mock_api.py](/D:/vscode项目/学习/day3/modules/mock_api.py)

#### 作用

提供本地模拟 API 响应。

当没有 API Key 或在线请求失败时，项目会使用它。

#### 为什么需要 mock

因为 Day 3 的目标是学会 API 调用流程。

如果网络或 key 有问题，学习不应该中断。

mock 响应的结构和真实 Chat Completions 类似，因此也能练习响应解析。

---

### 6.6 `modules/response_parser.py`

文件路径：
- [day3/modules/response_parser.py](/D:/vscode项目/学习/day3/modules/response_parser.py)

#### 作用

解析 API 响应。

包含：

- `extract_message_text`
- `summarize_response`

#### 学习重点

你要知道模型真正回复的文字通常在：

```python
response["choices"][0]["message"]["content"]
```

---

### 6.7 `modules/chat_client.py`

文件路径：
- [day3/modules/chat_client.py](/D:/vscode项目/学习/day3/modules/chat_client.py)

#### 作用

这是 Day 3 的核心模块。

它负责：

1. 构造 `messages`
2. 构造请求体
3. 构造请求头
4. 发送请求
5. 失败时使用 mock
6. 保存请求和响应日志

#### 你应该重点看什么

- `build_messages`
- `build_payload`
- `_headers`
- `chat`

这些方法就是一次 Chat Completions 调用的完整流程。

---

### 6.8 `main.py`

文件路径：
- [day3/main.py](/D:/vscode项目/学习/day3/main.py)

#### 作用

Day 3 的主入口。

支持：

- `chat`
- `summary`
- `q`

#### 运行方式

```bash
python main.py
```

---

## 7. 练习脚本详细说明

### 7.1 `01_what_is_api.py`

文件路径：
- [day3/01_what_is_api.py](/D:/vscode项目/学习/day3/01_what_is_api.py)

#### 作用

讲清楚 API 的基本概念。

运行：

```bash
python 01_what_is_api.py
```

---

### 7.2 `02_environment_config.py`

文件路径：
- [day3/02_environment_config.py](/D:/vscode项目/学习/day3/02_environment_config.py)

#### 作用

演示环境变量和配置读取。

运行后会显示：

- Base URL
- Chat Completions URL
- 模型名
- 超时时间
- 是否检测到 API Key

---

### 7.3 `03_chat_completions.py`

文件路径：
- [day3/03_chat_completions.py](/D:/vscode项目/学习/day3/03_chat_completions.py)

#### 作用

发送一次 Chat Completions 请求。

如果配置了 API Key，会优先请求在线 API。

如果没有配置，会使用本地 mock。

---

### 7.4 `04_parse_response.py`

文件路径：
- [day3/04_parse_response.py](/D:/vscode项目/学习/day3/04_parse_response.py)

#### 作用

专门练习响应解析。

这个脚本使用 mock 响应，因此不需要 API Key。

---

### 7.5 `05_full_chat_demo.py`

文件路径：
- [day3/05_full_chat_demo.py](/D:/vscode项目/学习/day3/05_full_chat_demo.py)

#### 作用

Day 3 综合小项目：

**API 对话助手**

它支持持续输入问题，并返回模型回复。

---

## 8. 输出文件说明

运行 `chat` 请求后，程序会在 `output/` 下保存：

- `last_request.json`
- `last_response.json`

它们用于学习和调试。

你可以打开它们观察：

- 请求体长什么样
- 响应体长什么样
- 模型回答在哪个字段里

---

## 9. 推荐学习顺序

建议按这个顺序学习：

1. `01_what_is_api.py`
2. `02_environment_config.py`
3. `04_parse_response.py`
4. `03_chat_completions.py`
5. `05_full_chat_demo.py`
6. `main.py`

这样你会先理解概念，再看配置，再看响应结构，最后跑真实对话。

---

## 10. 如何运行

进入目录：

```bash
cd D:\vscode项目\学习\day3
```

安装依赖：

```bash
pip install -r requirements.txt
```

运行主程序：

```bash
python main.py
```

运行综合 Demo：

```bash
python 05_full_chat_demo.py
```

---

## 11. 完成标准

你可以用下面标准检查自己是否完成 Day 3：

1. 能解释 API 是什么。
2. 能解释 Header、Payload、Response。
3. 能看懂 `.env.example`。
4. 能运行 `02_environment_config.py`。
5. 能运行 `04_parse_response.py` 并提取回复文本。
6. 能运行 `03_chat_completions.py`。
7. 能在 `output/` 中看到请求和响应日志。
8. 能运行 `05_full_chat_demo.py` 进行简单对话。

---

## 12. 常见问题

### 12.1 没有 API Key 能不能运行？

可以。

这个项目会自动使用本地 mock 响应。

### 12.2 为什么我配置了 API Key 还是走 mock？

可能原因：

- 网络不可用
- Base URL 写错
- Key 无效
- 请求超时
- `USE_MOCK_WHEN_FAILED=true`

### 12.3 为什么要保存请求和响应？

因为学习 API 最重要的是看清楚数据结构。

保存日志后，你可以慢慢研究：

- 你发了什么
- 对方返回了什么
- 你应该解析哪个字段

---

## 13. 小结

Day 3 是 AI 应用开发的入口。

你要记住这条主线：

```text
准备 API Key -> 构造请求 -> 发送请求 -> 接收响应 -> 解析结果
```

后面所有大模型应用，基本都离不开这条链路。

