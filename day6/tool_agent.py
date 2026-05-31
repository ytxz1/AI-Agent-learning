from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console

import os
import json

from tools.weather import get_weather
from tools.calculator import calculator
from tools.translator import translate

load_dotenv()

console = Console()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),  # 从 .env 文件读取 API 密钥
    base_url='https://api.deepseek.com'               # DeepSeek API 地址
)

tools = [

    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取天气",
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
            "description": "翻译工具",
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

messages = [
    {
        "role": "system",
        "content": """
你是一个智能AI助手。

你可以：
1. 查询天气
2. 数学计算
3. 文本翻译

请根据用户问题自动调用工具。
"""
    }
]

console.print(
    "\nAI Agent 启动成功！",
    style="bold green"
)

while True:

    user_input = input("\n你: ")

    if user_input == "quit":
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )

    response_message = response.choices[0].message

    tool_calls = response_message.tool_calls

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

        # 把工具调用记录加入messages
        messages.append(response_message)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })

        # 第二次请求
        final_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )

        final_text = final_response.choices[0].message.content

        console.print(
            f"\nAI: {final_text}",
            style="bold green"
        )

        messages.append({
            "role": "assistant",
            "content": final_text
        })

    else:

        text = response_message.content

        console.print(
            f"\nAI: {text}",
            style="bold green"
        )

        messages.append({
            "role": "assistant",
            "content": text
        })