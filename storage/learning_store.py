"""
storage/learning_store.py
学习记录存储模块。
功能：
- 加载和保存学习记录至 learning.json 文件
- 按日期合并关键词与原始内容（避免重复）
"""

import json
import os
from datetime import datetime

DATA_PATH = "data"
LEARN_FILE = os.path.join(DATA_PATH, "learning.json")
os.makedirs(DATA_PATH, exist_ok=True)

def load_all_data():
    """
    加载 learning.json 中的所有学习记录。
    如果文件不存在则返回空列表。
    """
    if os.path.exists(LEARN_FILE):
        with open(LEARN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_all_data(data_list):
    """
    将学习记录数据列表写入 learning.json 文件。

    参数:
        data_list (list): 所有学习记录组成的列表，每条为 dict。
    """
    with open(LEARN_FILE, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

def save_learning_record(learning_data: dict):
    """
    保存一条学习记录。

    功能：
    - 如果当天已有记录，则合并关键词（去重）与原始内容（拼接去重）；
    - 否则新增一条新的记录；
    - 最终保存到 learning.json 文件中。

    参数:
        learning_data (dict): 格式如 {"关键词": [...], "原始内容": "..."}
    """
    all_data = load_all_data()
    today = datetime.now().strftime("%Y-%m-%d")
    found = False

    for entry in all_data:
        if entry.get("date") == today:
            if "学习" not in entry:
                entry["学习"] = {
                    "关键词": [],
                    "原始内容": ""
                }

            old_keywords = entry["学习"].get("关键词", [])
            new_keywords = learning_data.get("关键词", [])
            entry["学习"]["关键词"] = list(set(old_keywords + new_keywords))

            old_raw = entry["学习"].get("原始内容", "")
            new_raw = learning_data.get("原始内容", "")
            if new_raw and new_raw not in old_raw:
                entry["学习"]["原始内容"] = old_raw + "。" + new_raw if old_raw else new_raw

            found = True
            break

    if not found:
        all_data.append({
            "date": today,
            "学习": {
                "关键词": learning_data.get("关键词", []),
                "原始内容": learning_data.get("原始内容", "")
            }
        })

    save_all_data(all_data)
    print("✅ 学习记录已保存并合并")