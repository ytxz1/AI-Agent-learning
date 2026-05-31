"""
Day 8 - 配置文件

本文件负责加载和管理所有 API 配置信息。
其他模块通过 import 从这里获取 API Key、地址、模型名称。

为什么单独一个配置文件？
1. 集中管理：所有配置在一个地方修改，不用到处找
2. 安全性：API Key 存在 .env 文件中，不写在代码里
3. 可维护性：切换 API 提供商时只改这一个文件
"""

# ==============================
# 加载环境变量
# ==============================

# load_dotenv() 会读取当前目录下的 .env 文件
# 把里面的键值对加载到系统环境变量中
# .env 文件格式：OPENAI_API_KEY=sk-xxxxxxx
from dotenv import load_dotenv
import os

load_dotenv()  # 读取 .env 文件，加载到 os.environ

# ==============================
# API 配置
# ==============================

# 从环境变量中读取 API Key
# os.getenv("KEY名") 如果环境变量不存在，返回 None
# API Key 用于身份验证，每个请求都要带上
# ⚠️ 重要：API Key 是私密信息，不要提交到 Git！
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# DeepSeek API 的服务地址
# DeepSeek 兼容 OpenAI 的接口格式，所以 base_url 直接指向 DeepSeek
# 如果想用 OpenAI 官方 API，改成 "https://api.openai.com/v1"
# 如果想用其他兼容服务（如通义千问），改成对应的地址
OPENAI_BASE_URL = "https://api.deepseek.com"

# 模型名称
# DeepSeek 的对话模型名称
# 常见选项：
#   "deepseek-chat"     - 通用对话模型（默认）
#   "deepseek-coder"    - 代码专用模型
# 如果切换到 OpenAI，可以用 "gpt-4o"、"gpt-3.5-turbo" 等
MODEL_NAME = "deepseek-chat"