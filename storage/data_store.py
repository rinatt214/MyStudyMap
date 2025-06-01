import json
import os
from datetime import datetime

DATA_PATH = "data"  # 保存目录（可在config.py中统一配置）
FILENAME = os.path.join(DATA_PATH, "learning.json")

os.makedirs(DATA_PATH, exist_ok=True)

def load_all_data():
    """加载所有记录"""
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_all_data(data_list):
    """将完整数据写入文件"""
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

def save_learning_record(learning_data: dict):
    """将学习记录保存并合并到当天"""
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

            # 合并关键词（去重）
            old_keywords = entry["学习"].get("关键词", [])
            new_keywords = learning_data.get("关键词", [])
            entry["学习"]["关键词"] = list(set(old_keywords + new_keywords))

            # 合并原始内容（去重拼接）
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

def save_fitness_record(fitness_data: dict):
    """将健身记录保存并合并到当天"""
    all_data = load_all_data()
    today = datetime.now().strftime("%Y-%m-%d")
    found = False

    for entry in all_data:
        if entry.get("date") == today:
            # 合并健身字段
            if "健身" not in entry:
                entry["健身"] = {
                    "训练动作": {},
                    "训练部位": [],
                    "有氧时间": 0,
                    "估算热量": 0
                }

            old = entry["健身"]

            # 合并训练动作
            for action, sets in fitness_data.get("训练动作", {}).items():
                old["训练动作"].setdefault(action, []).extend(sets)

            # 合并训练部位（去重）
            old_parts = set(old.get("训练部位", []))
            new_parts = set(fitness_data.get("训练部位", []))
            old["训练部位"] = list(old_parts.union(new_parts))

            # 安全累加有氧时间和热量
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