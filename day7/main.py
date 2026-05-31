from openai import OpenAI
from rich.console import Console
from rich.panel import Panel

import json
import time

from config import OPENAI_API_KEY
from config import OPENAI_BASE_URL
from config import MODEL_NAME

from prompts import SYSTEM_PROMPT

from memory import Memory

from tools import (
    get_weather,
    calculator,
    translate
)

# 初始化客户端
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

console = Console()

memory = Memory()

# system prompt
memory.add_message(
    "system",
    SYSTEM_PROMPT
)

# tools schema
tools = [

    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["city"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "数学计算器",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式"
                    }
                },
                "required": ["expression"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "translate",
            "description": "文本翻译工具",
            "parameters": {
                "type": "object",
                "properties": {

                    "text": {
                        "type": "string",
                        "description": "待翻译文本"
                    },

                    "target_language": {
                        "type": "string",
                        "description": "目标语言"
                    }

                },

                "required": [
                    "text",
                    "target_language"
                ]
            }
        }
    }
]

# 启动界面
console.print(
    Panel.fit(
        "AI ChatBot 启动成功！\n输入 quit 退出",
        style="bold green"
    )
)

# 主循环
while True:

    user_input = input("\n你: ")

    if user_input.lower() == "quit":

        console.print(
            "\nAI助手已退出",
            style="bold red"
        )

        break

    # 保存用户消息
    memory.add_message(
        "user",
        user_input
    )

    # 限制记忆长度
    memory.limit_memory()

    # 第一次请求
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=memory.get_messages(),
        tools=tools
    )

    response_message = response.choices[0].message

    tool_calls = response_message.tool_calls

    # ==========================
    # 如果AI决定调用工具
    # ==========================

    if tool_calls:

        tool_call = tool_calls[0]

        function_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        console.print(
            f"\n[调用工具] {function_name}",
            style="bold yellow"
        )

        # 天气工具
        if function_name == "get_weather":

            result = get_weather(
                arguments["city"]
            )

        # 计算器工具
        elif function_name == "calculator":

            result = calculator(
                arguments["expression"]
            )

        # 翻译工具
        elif function_name == "translate":

            result = translate(
                arguments["text"],
                arguments["target_language"]
            )

        else:

            result = "未知工具"

        console.print(
            f"[工具结果] {result}",
            style="cyan"
        )

        # 添加tool call
        memory.messages.append(response_message)

        # 添加tool结果
        memory.messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })

        # 第二次请求
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=memory.get_messages(),
            stream=True
        )

        console.print(
            "\nAI: ",
            style="bold green",
            end=""
        )

        full_response = ""

        for chunk in stream:

            delta = chunk.choices[0].delta

            if delta.content:

                text = delta.content

                print(
                    text,
                    end="",
                    flush=True
                )

                full_response += text

        # 保存AI回复
        memory.add_message(
            "assistant",
            full_response
        )

    # ==========================
    # 普通聊天
    # ==========================

    else:

        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=memory.get_messages(),
            stream=True
        )

        console.print(
            "\nAI: ",
            style="bold green",
            end=""
        )

        full_response = ""

        for chunk in stream:

            delta = chunk.choices[0].delta

            if delta.content:

                text = delta.content

                print(
                    text,
                    end="",
                    flush=True
                )

                full_response += text

                time.sleep(0.01)

        # 保存AI回复
        memory.add_message(
            "assistant",
            full_response
        )