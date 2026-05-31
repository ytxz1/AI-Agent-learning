from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from tools.translator import translate

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),  # 从 .env 文件读取 API 密钥
    base_url='https://api.deepseek.com'               # DeepSeek API 地址
)

tools = [
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
                        "description": "需要翻译的内容"
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
        "role": "user",
        "content": "把你好翻译成英文"
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

text = arguments["text"]

target_language = arguments["target_language"]

result = translate(
    text,
    target_language
)

print(result)