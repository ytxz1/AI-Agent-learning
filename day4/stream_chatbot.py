from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()                          # 导入 OpenAI SDK

client = OpenAI(                                    # 创建 API 客户端实例
    api_key=os.getenv('OPENAI_API_KEY'),  # 从 .env 文件读取 API 密钥
    base_url='https://api.deepseek.com'             # DeepSeek 的 API 地址
)

messages = [                                        # 对话历史列表
    {
        "role": "system",                           # system 角色：设定 AI 的行为和人设
        "content": "你是一个专业AI助手"              # 系统提示词
    }
]

print("AI聊天机器人启动！输入 quit 退出。")          # 启动提示

while True:                                         # 主循环，持续对话

    user_input = input("\n你: ")                    # 获取用户输入

    if user_input == "quit":                        # 如果输入 quit
        break                                       # 退出循环，结束程序

    messages.append({                               # 将用户消息加入对话历史
        "role": "user",
        "content": user_input
    })

    print("\nAI: ", end="")                         # 打印 AI 回复的前缀

    full_response = ""                              # 初始化完整回复字符串

    stream = client.chat.completions.create(        # 调用 API，开启流式模式
        model="deepseek-chat",                      # 使用 DeepSeek 模型
        messages=messages,                          # 传入完整对话历史
        stream=True,                                # 流式输出
        temperature=0.7                             # 温度 0.7，平衡创意和准确性
    )

    for chunk in stream:                            # 遍历流式数据块

        delta = chunk.choices[0].delta              # 获取增量内容

        if delta.content:                           # 如果有实际文字

            text = delta.content                    # 取出文字

            print(text, end="", flush=True)         # 逐字打印，不换行

            full_response += text                   # 拼接到完整回复中

    messages.append({                               # 将 AI 回复加入对话历史
        "role": "assistant",                        # assistant 角色代表 AI
        "content": full_response                    # 保存完整的 AI 回复
    })

# ==================== 代码详细解释 ====================
#
# 【这个脚本是做什么的？】
#   一个支持多轮对话的 AI 聊天机器人，具有流式输出效果。
#   你可以不断和 AI 对话，它会记住之前的聊天内容。
#
# 【核心概念】
#
#   1. 多轮对话的原理：messages 列表
#     → 每次调用 API 时，把"完整对话历史"一起发给服务器
#     → AI 就能"记住"之前说过什么，实现上下文连贯的对话
#     → messages 列表不断增长，包含所有历史消息
#
#   2. 三种角色（role）：
#     → "system"：系统提示词，设定 AI 的人设和行为规则（用户看不到）
#     → "user"：用户说的话
#     → "assistant"：AI 的回复
#
#   3. 流式输出：
#     → stream=True 让 AI 的回复逐字显示，体验更流畅
#     → full_response 用于收集完整的回复内容
#
# 【逐段解析】
#
#   messages = [{"role": "system", "content": "你是一个专业AI助手"}]
#     → 初始化对话历史，第一条是系统提示词
#     → 告诉 AI 要扮演"专业AI助手"的角色
#
#   while True:
#     → 无限循环，让程序持续运行，直到用户输入 quit
#
#   user_input = input("\n你: ")
#     → 等待用户输入，input() 会阻塞程序直到用户按回车
#
#   if user_input == "quit": break
#     → 输入 quit 时退出循环，结束程序
#
#   messages.append({"role": "user", "content": user_input})
#     → 把用户输入添加到对话历史中
#     → 这样下次调用 API 时，AI 就能看到这句话
#
#   print("\nAI: ", end="")
#     → 打印 "AI: " 前缀，不换行，后面 AI 的回复会紧跟其后
#
#   full_response = ""
#     → 初始化空字符串，用于收集流式返回的所有文字
#
#   client.chat.completions.create(messages=messages, stream=True, temperature=0.7)
#     → messages=messages：传入完整对话历史（包含 system、所有 user 和 assistant 消息）
#     → stream=True：开启流式输出
#     → temperature=0.7：中等创意度
#
#   for chunk in stream:
#     → 遍历每个数据块
#
#   delta = chunk.choices[0].delta
#     → 取出当前块的增量文字
#
#   if delta.content:
#     → 过滤空内容块
#
#   text = delta.content
#     → 取出文字
#
#   print(text, end="", flush=True)
#     → 逐字打印，end="" 不换行，flush=True 立即显示
#
#   full_response += text
#     → 把这段文字拼接到完整回复中
#
#   messages.append({"role": "assistant", "content": full_response})
#     → AI 回复完成后，把完整回复加入对话历史
#     → 这样下次对话时，AI 就知道自己之前说了什么
#
# 【程序运行流程】
#   启动 → 打印欢迎语 → 进入循环
#   → 等待用户输入 → 用户说话 → 加入历史
#   → 调用 AI（带完整历史）→ 流式显示回复 → 回复加入历史
#   → 回到循环开头 → 等待用户输入 → ...
#   → 用户输入 quit → 退出循环 → 程序结束
#
# 【消息列表增长示例】
#   初始: [system]
#   第1轮: [system, user("你好"), assistant("你好！有什么...")]
#   第2轮: [system, user("你好"), assistant("你好！有什么..."), user("天气如何"), assistant("今天天气...")]
#   → 列表越来越长，AI 的"记忆"也越来越长