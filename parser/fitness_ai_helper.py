import requests

def parse_fitness_text_with_ai(text: str) -> dict:
    """
    使用 Ollama 一次性解析健身内容：
    - 抽取训练动作、每组重量与次数
    - 推断训练部位
    - 提取有氧时间
    - 估算总热量（kcal）

    返回结构如：
    {
      "训练动作": {...},
      "训练部位": [...],
      "有氧时间": 分钟（整数）,
      "估算热量": 数值（整数）
    }
    """

    prompt = f"""
你是一个专业的健身训练解析助手，请严格按照以下要求操作：

【任务】
请你对用户的一段健身训练记录进行分析，提取以下信息：
1. 所有训练动作及每组的重量和次数
2. 本次训练涉及的身体部位（如 胸、肩、背、三头、二头、腿、核心 等）
3. 有氧训练时间（单位：分钟）
4. 粗略估算总热量消耗（单位：千卡）

【输出要求】
请你只返回以下格式的 **合法 JSON 对象**，不要添加说明文字、解释、标点等。

输出格式：
{{
  "训练动作": {{
    "动作1": [{{"重量": kg, "次数": 次}}, ...],
    "动作2": [...],
    ...
  }},
  "训练部位": ["部位1", "部位2", ...],
  "有氧时间": 分钟数（整数）,
  "估算热量": 整数
}}

【训练记录】
{text}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False
        }
    )

    raw_output = response.json()["response"]

    try:
        result = eval(raw_output.strip())
    except:
        result = {
            "训练动作": {},
            "训练部位": [],
            "有氧时间": 0,
            "估算热量": 0
        }

    return result