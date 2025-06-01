"""
storage/fitness_store.py
健身记录存储模块。
功能：
- 加载和保存健身记录至 fitness.json 文件
- 按日期合并训练动作、训练部位、有氧时间和热量
"""

import json
import os
from datetime import datetime

DATA_PATH = "data"
FIT_FILE = os.path.join(DATA_PATH, "fitness.json")
os.makedirs(DATA_PATH, exist_ok=True)

def load_all_data():
    """
    加载 fitness.json 中的所有健身记录。
    如果文件不存在则返回空列表。
    """
    if os.path.exists(FIT_FILE):
        with open(FIT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_all_data(data_list):
    """
    将健身记录数据列表写入 fitness.json 文件。

    参数:
        data_list (list): 所有健身记录组成的列表，每条为 dict。
    """
    with open(FIT_FILE, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

def save_fitness_record(fitness_data: dict):
    """
    保存一条健身记录。

    功能：
    - 如果当天已有记录，则合并训练动作（append）、训练部位（去重）、
      有氧时间和估算热量（累加）；
    - 否则新增一条新记录；
    - 最终保存到 fitness.json 文件中。

    参数:
        fitness_data (dict): 包含训练动作、部位、有氧时间、热量等字段的记录。
    """
    all_data = load_all_data()
    today = datetime.now().strftime("%Y-%m-%d")
    found = False

    for entry in all_data:
        if entry.get("date") == today:
            if "健身" not in entry:
                entry["健身"] = {
                    "训练动作": {},
                    "训练部位": [],
                    "有氧时间": 0,
                    "估算热量": 0
                }

            old = entry["健身"]

            for action, sets in fitness_data.get("训练动作", {}).items():
                old["训练动作"].setdefault(action, []).extend(sets)

            old_parts = set(old.get("训练部位", []))
            new_parts = set(fitness_data.get("训练部位", []))
            old["训练部位"] = list(old_parts.union(new_parts))

            old["有氧时间"] = (old.get("有氧时间") or 0) + (fitness_data.get("有氧时间") or 0)
            old["估算热量"] = (old.get("估算热量") or 0) + (fitness_data.get("估算热量") or 0)

            found = True
            break

    if not found:
        all_data.append({
            "date": today,
            "健身": fitness_data
        })

    save_all_data(all_data)
    print("✅ 健身记录已保存")