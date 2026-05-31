from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()                          # 导入 OpenAI SDK

client = OpenAI(                                    # 创建 API 客户端实例
    api_key=os.getenv('OPENAI_API_KEY'),  # 从 .env 文件读取 API 密钥
    base_url='https://api.deepseek.com'             # DeepSeek 的 API 地址
)

stream = client.chat.completions.create(            # 调用聊天接口，返回流对象
    model="deepseek-chat",                          # 使用 DeepSeek 聊天模型
    messages=[                                      # 对话消息列表
        {"role": "user", "content": "介绍一下人工智能"}  # 用户提问
    ],
    stream=True,                                    # 开启流式输出模式
)

for chunk in stream:                                # 遍历流式输出的每个数据块
    delta = chunk.choices[0].delta                  # 获取当前数据块的增量内容
    if delta.content:                               # 如果增量内容不为空
        print(delta.content, end='', flush=True)    # 打印内容，不换行，立即刷新

# ==================== 代码详细解释 ====================
#
# 【这个脚本是做什么的？】
#   演示 AI 的"流式输出"（Streaming），即文字一个一个蹦出来，
#   类似 ChatGPT 网页版打字的效果，而不是等全部生成完再一次性显示。
#
# 【逐行解析】
#
#   from openai import OpenAI
from dotenv import load_dotenv
#     → 导入 OpenAI 官方 Python SDK，DeepSeek 兼容这个接口格式
#
#   client = OpenAI(api_key=..., base_url=...)
#     → 创建 API 客户端
#     → api_key：你的身份凭证，用于鉴权
#     → base_url：API 服务器地址，这里指向 DeepSeek（默认是 OpenAI）
#
#   stream = client.chat.completions.create(...)
#     → 调用聊天补全接口
#     → model="deepseek-chat"：指定使用 DeepSeek 的模型
#     → messages：对话上下文，role="user" 表示用户说的话
#     → stream=True：关键参数！开启流式模式后，返回的不是完整结果，
#       而是一个可迭代的"流"对象，数据会一块一块地传过来
#
#   for chunk in stream:
#     → 逐个读取流式返回的数据块（chunk）
#     → 每个 chunk 包含一小段文字（可能是一个词、一个字、甚至为空）
#
#   delta = chunk.choices[0].delta
#     → delta 是"增量"的意思，表示这一块新增的内容
#     → choices[0] 是第一个候选回复（通常只有一个）
#
#   if delta.content:
#     → 过滤掉空内容的数据块（有些 chunk 只包含元数据，没有文字）
#
#   print(delta.content, end='', flush=True)
#     → end=''：不换行，让文字连续输出
#     → flush=True：立即刷新缓冲区，让文字马上显示在屏幕上
#
# 【流式 vs 非流式的区别】
#   非流式：等 AI 全部生成完 → 一次性返回 → 用户等待时间长
#   流式：  AI 生成一点 → 立即返回一点 → 用户体验更好，感觉 AI 在"思考"
#
# 【数据流向】
#   用户提问 → 发送到 DeepSeek 服务器 → 服务器逐块返回文字
#   → 客户端逐块接收 → 逐块打印到屏幕
