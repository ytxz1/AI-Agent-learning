from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from tools.calculator import calculator

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),  # 从 .env 文件读取 API 密钥
    base_url='https://api.deepseek.com'               # DeepSeek API 地址
)

tools = [
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
    }
]

messages = [
    {
        "role": "user",
        "content": "123 * 456 等于多少？"
    }
]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools
)

tool_call = response.choices[0].message.tool_calls[0]

arguments = json.loads(
    tool_call.function.arguments
)

expression = arguments["expression"]

result = calculator(expression)

print(result)