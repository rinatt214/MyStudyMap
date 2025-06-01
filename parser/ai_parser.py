from numpy import test
import requests
import json

def extract_info(text: str) -> dict:
    """
    使用 Ollama 本地模型提取学习关键词和领域。
    输入：原始学习内容（如“今天复习了监督学习和逻辑回归”）
    输出：结构化信息，如 {"关键词": ["监督学习", "逻辑回归"], "领域": "AI"}
    """

    #构造prompt（提示词）
    prompt = f"""
    你是一个智能记录分析助手，我会给你一段日常记录内容，你需要判断它属于哪一类（学习/健身/刷题），并进行结构化信息提取，输出一个 JSON 对象。格式如下：

学习类：
{{
  "类型": "学习",
  "关键词": ["人工智能", "卷积神经网络"]
}}

健身类：
{{
  "类型": "健身",
  "训练动作": {{
    "卧推": [{{"重量": 40, "次数": 10}}, {{"重量": 50, "次数": 8}}],
    "推肩": [{{"重量": 20, "次数": 12}}]
  }},
  "训练部位": ["胸部", "肩部"],
  "有氧时间": 30,
  "估算热量": 230
}}

刷题类（LeetCode）：
{{
  "类型": "刷题",
  "题目数量": 4,
  "题号": [12, 31, 94, 206],
  "知识点": ["二叉树", "动态规划"]
}}

现在的输入是：{text}
请输出对应的 JSON 字典，不要多余解释。
    """

    #请求Ollama本地服务
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1",  # 根据你安装的模型名字修改
            "prompt": prompt,
            "stream": False
        }
    )

    #获取回复文本
    raw_output = response.json()["response"]

    #解析为字典（如果格式不标准也不会报错）
    try:
    # 尝试用 eval 解析
        parsed_data = eval(raw_output.strip())
    except:
        try:
            # 如果失败，用 json.loads 再试一次（可能是纯 JSON）
            parsed_data = json.loads(raw_output.strip())
        except:
            parsed_data = {"关键词": [], "领域": "未知", "raw_output": raw_output}

    return parsed_data