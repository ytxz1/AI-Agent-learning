"""
Day 8 - LangChain 入门：LLM 基础调用

本示例演示如何使用 LangChain 调用 DeepSeek（OpenAI 兼容）大模型。
LangChain 对底层 API 进行了封装，使调用更简洁。

知识点：
1. ChatOpenAI 类的创建和配置
2. invoke() 同步调用
3. stream() 流式输出
4. batch() 批量调用
5. AIMessage 返回值结构
"""

# ==============================
# 导入所需模块
# ==============================

# ChatOpenAI: LangChain 对 OpenAI 兼容 Chat 模型的封装类
# 它内部调用的是 OpenAI 的 /v1/chat/completions 接口
from langchain_openai import ChatOpenAI

# HumanMessage: 用户发送的消息，对应 role="user"
# SystemMessage: 系统消息，对应 role="system"，用于设定 AI 的行为
# 这两个类是 LangChain 对 OpenAI messages 格式的类型化封装
from langchain_core.messages import HumanMessage, SystemMessage

# 从配置文件导入 API 相关变量
# config.py 中定义了 OPENAI_API_KEY、OPENAI_BASE_URL、MODEL_NAME
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME

# ==============================
# 1. 创建 LLM 实例
# ==============================

# ChatOpenAI 是 LangChain 对 Chat 模型的核心封装
# 通过指定 base_url 可以对接 DeepSeek、通义千问等 OpenAI 兼容的 API
# 参数说明：
#   api_key     - API 密钥，用于身份验证
#   base_url    - API 服务地址，DeepSeek 的地址是 https://api.deepseek.com
#   model       - 模型名称，deepseek-chat 是 DeepSeek 的对话模型
#   temperature - 温度参数，控制输出的随机性，范围 0~2
#                 0 = 确定性输出（每次结果差不多）
#                 1 = 正常随机
#                 2 = 非常随机/有创意
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,       # 从 .env 文件读取的 API Key
    base_url=OPENAI_BASE_URL,     # DeepSeek API 地址
    model=MODEL_NAME,             # 模型名称：deepseek-chat
    temperature=0.7,              # 温度 0.7，适中的随机性
)

# 打印分隔线，方便终端阅读
print("=" * 50)
print("Day 8 - LangChain LLM 基础调用")
print("=" * 50)

# ==============================
# 2. 最简单的调用方式：直接传入字符串
# ==============================

# 这是最简单的用法，直接把字符串传给 llm.invoke()
# LangChain 内部会自动把字符串包装成 HumanMessage 格式
# 返回值是一个 AIMessage 对象，.content 属性存储文本内容
print("\n--- 方式一：直接传入字符串 ---")
response = llm.invoke("用一句话介绍你自己")  # invoke() 是同步调用方法
print(f"AI: {response.content}")  # response.content 是字符串类型

# ==============================
# 3. 使用消息列表调用
# ==============================

# 方式二：使用 LangChain 的消息对象列表
# 这和 OpenAI API 的 messages 参数格式完全一致：
#   [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
# 区别是用类型化的消息类代替字典，更安全、更易读
print("\n--- 方式二：使用消息列表 ---")
messages = [
    SystemMessage(content="你是一个专业的Python老师，回答简洁明了。"),  # 系统提示词
    HumanMessage(content="什么是列表推导式？给我一个例子。"),           # 用户问题
]
response = llm.invoke(messages)  # 传入消息列表
print(f"AI: {response.content}")

# ==============================
# 4. 流式输出（stream）
# ==============================

# stream() 方法返回一个迭代器，每次产出一小段文本（chunk）
# 优点：用户不需要等待完整回复，体验更好
# 每个 chunk 是一个 AIMessageChunk 对象
# chunk.content 是当前这一小段的文本
print("\n--- 流式输出 ---")
print("AI: ", end="")  # end="" 表示不换行
for chunk in llm.stream("简述Python的三大特性"):  # stream 返回迭代器
    print(chunk.content, end="", flush=True)  # flush=True 确保立即输出到终端
print()  # 最后换行

# ==============================
# 5. 批量调用（batch）
# ==============================

# batch() 方法一次传入多个请求，LangChain 会尽量并行处理
# 比逐个调用 invoke() 更高效，尤其是请求量大的时候
# 输入是一个列表，每个元素是一组消息（也是列表）
# 输出也是一个列表，顺序和输入对应
print("\n--- 批量调用 ---")
batch_messages = [
    [HumanMessage(content="Python是什么？用一句话回答。")],     # 第1个请求
    [HumanMessage(content="Java是什么？用一句话回答。")],       # 第2个请求
    [HumanMessage(content="JavaScript是什么？用一句话回答。")], # 第3个请求
]
responses = llm.batch(batch_messages)  # 批量调用，返回 AIMessage 列表
for i, resp in enumerate(responses):  # enumerate 同时获取索引和值
    print(f"问题{i + 1}: {resp.content}")

# 演示完成提示
print("\n✅ LLM 基础调用演示完成！")