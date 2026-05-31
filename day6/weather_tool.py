"""
Weather Tool (天气工具) 示例
============================

展示如何让大语言模型调用外部工具来获取天气信息。
这是 Function Calling (函数调用) 的基础应用。
"""

from openai import OpenAI
import json


# ============================================================
# 1. 基础配置
# ============================================================
# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),  # 从 .env 文件读取 API 密钥
    base_url='https://api.deepseek.com'               # DeepSeek API 地址
)


# ============================================================
# 2. 定义工具 - 天气查询函数
# ============================================================
# 这是实际执行的函数，模拟获取天气信息
def get_weather(city: str) -> str:
    """
    获取指定城市的天气信息

    Args:
        city: 城市名称

    Returns:
        天气信息字符串
    """
    # 模拟天气数据（实际应用中会调用真实 API）
    fake_weather = {
        "北京": "25°C，晴天",
        "上海": "28°C，多云",
        "广州": "32°C，暴雨"
    }
    return fake_weather.get(city, "未知城市")


# ============================================================
# 3. 定义工具描述 - 告诉模型有哪些工具可用
# ============================================================
# 工具描述让模型知道可以调用哪些工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",  # 函数名称
            "description": "获取某个城市天气",  # 函数描述
            "parameters": {  # 参数定义
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["city"]  # 必需参数
            }
        }
    }
]


# ============================================================
# 4. 调用 API - 让模型决定是否使用工具
# ============================================================
# 发送请求，模型会分析是否需要调用工具
messages = [
    {
        "role": "user",
        "content": "北京天气怎么样？"
    }
]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools  # 传入工具描述
)


# ============================================================
# 5. 处理响应 - 检查是否需要调用工具
# ============================================================
message = response.choices[0].message

# 检查是否有工具调用请求
if message.tool_calls:
    # 有工具调用请求 - 解析并执行
    tool_call = message.tool_calls[0]  # 获取第一个工具调用
    function_name = tool_call.function.name  # 获取函数名称
    arguments = json.loads(tool_call.function.arguments)  # 解析参数

    # 执行工具调用
    if function_name == "get_weather":
        result = get_weather(arguments["city"])  # 调用实际函数

        # 将结果返回给模型，让模型生成最终回复
        messages = [
            {"role": "user", "content": "北京天气怎么样？"},
            message,  # 包含工具调用的助手消息
            {
                "role": "tool",  # 工具结果消息
                "tool_call_id": tool_call.id,
                "content": result
            }
        ]

        # 再次调用 API，让模型根据工具结果生成回复
        final_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        print(final_response.choices[0].message.content)
else:
    # 没有工具调用，直接输出文本回复
    print(message.content)


# ============================================================
# 详细解释
# ============================================================
"""
Weather Tool 天气工具详解
========================

1. 核心概念
   ----------
   Function Calling (函数调用) 是让大语言模型调用外部工具的技术。
   模型不直接回答问题，而是决定调用哪个工具，然后根据工具结果生成回复。

   在本示例中：
   - 用户问"北京天气怎么样？"
   - 模型识别出需要调用 get_weather 工具
   - 模型生成工具调用请求（包含函数名和参数）
   - 程序解析请求并执行 get_weather 函数
   - 输出天气结果

2. 工作原理
   ----------
   1) 定义工具：创建 get_weather() 函数
   2) 描述工具：通过 tools 参数告诉模型工具的功能
   3) 发送请求：将用户消息和工具描述一起发送
   4) 模型决策：模型分析用户意图，决定调用 get_weather
   5) 生成调用：模型返回 tool_calls，包含函数名和参数
   6) 解析响应：从响应中提取 tool_calls
   7) 执行工具：调用 get_weather 函数
   8) 输出结果：打印天气信息

3. 代码结构解析
   -------------
   1) get_weather() 函数：实际获取天气的函数
      - 接收城市名称参数
      - 返回天气信息字符串

   2) tools 列表：工具描述
      - 告诉模型有哪些工具可用
      - 包含函数名、描述、参数定义

   3) API 调用：传入 tools 参数
      - 模型会分析是否需要调用工具
      - 如果需要，返回 tool_calls

   4) 响应解析：
      - response.choices[0].message.tool_calls[0] 获取第一个工具调用
      - tool_call.function.name 获取函数名
      - json.loads(tool_call.function.arguments) 解析参数

   5) 工具执行：
      - 调用 get_weather(city) 获取结果
      - 输出结果

4. 工具描述 (Tool Schema) 的结构
   ------------------------------
   tools = [
       {
           "type": "function",
           "function": {
               "name": "get_weather",        # 函数名称（模型用这个名称调用）
               "description": "描述函数功能",  # 帮助模型理解何时使用
               "parameters": {                # 参数定义
                   "type": "object",
                   "properties": {
                       "city": {
                           "type": "string",
                           "description": "城市名称"
                       }
                   },
                   "required": ["city"]       # 必需参数列表
               }
           }
       }
   ]

5. 响应结构
   ---------
   当模型决定调用工具时，响应包含：
   response.choices[0].message.tool_calls = [
       {
           "id": "call_xxx",  # 调用ID（用于后续返回结果）
           "function": {
               "name": "get_weather",           # 函数名称
               "arguments": '{"city": "北京"}'  # JSON格式的参数
           }
       }
   ]

6. 适用场景
   ----------
   - 天气查询：获取实时天气（本示例）
   - 数据库查询：查询用户数据
   - API 调用：调用外部服务
   - 计算计算：执行数学运算
   - 文件操作：读写文件
   - 搜索引擎：搜索信息

7. 优点
   ------
   - 模型可以访问实时信息
   - 扩展模型的能力边界
   - 保持模型的通用性
   - 可以组合多个工具

8. 局限性
   --------
   - 需要额外的工具开发
   - 工具调用有延迟
   - 工具执行可能失败
   - 需要处理错误情况

9. 扩展示例
   ----------

   # 添加错误处理
   try:
       result = get_weather(city)
   except Exception as e:
       result = f"获取天气失败: {e}"

   # 添加更多工具
   tools = [
       {"type": "function", "function": {"name": "get_weather", ...}},
       {"type": "function", "function": {"name": "get_stock_price", ...}},
       {"type": "function", "function": {"name": "search_web", ...}}
   ]

10. 最佳实践
    ----------
    - 工具描述要清晰明确
    - 参数定义要准确
    - 处理工具调用失败的情况
    - 添加日志记录工具调用
    - 限制工具调用次数

11. 错误处理
    ----------
    if response.choices[0].message.tool_calls:
        try:
            result = get_weather(city)
        except Exception as e:
            result = f"错误: {e}"
    else:
        result = "模型未调用工具"

12. 与 system_prompt 的结合
    ------------------------
    可以在系统提示中引导模型使用工具：

    messages = [
        {"role": "system", "content": "你是一个智能助手，可以查询天气。"},
        {"role": "user", "content": "北京天气怎么样？"}
    ]

13. 与多轮对话的结合
    -----------------
    工具调用可以与多轮对话结合：

    messages = [
        {"role": "user", "content": "北京天气怎么样？"},
        # 工具调用和结果...
        {"role": "user", "content": "那上海呢？"},
        # 模型可以记住之前的对话上下文
    ]

14. 注意事项
    ----------
    - 工具描述会影响模型的决策
    - 参数验证很重要
    - 工具执行要有超时机制
    - 敏感操作需要权限控制
    - 记录工具调用日志便于调试

15. 与其他 day6 文件的关系
    ----------------------
    - calculator_tool.py: 展示计算工具
    - translate_tool.py: 展示翻译工具
    - tool_agent.py: 展示多工具智能代理
    - tools/ 目录: 工具的具体实现

    所有工具都遵循相同的模式：
    1. 定义实际函数
    2. 描述工具给模型
    3. 处理工具调用
    4. 返回结果给模型
"""
