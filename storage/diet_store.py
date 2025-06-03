import json
import os
from datetime import datetime

DATA_PATH = "data"
FILENAME = os.path.join(DATA_PATH, "diet.json")
os.makedirs(DATA_PATH, exist_ok=True)

def load_all_data():
    """
    加载 diet.json 中所有饮食记录。
    """
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_all_data(data_list):
    """
    将饮食记录数据列表写入 diet.json 文件。
    """
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

def save_diet_record(diet_data: dict):
    """
    保存一条饮食记录。
    - 按日期合并；
    - 同一餐次食物合并（去重）；
    - 原始内容合并；
    """

    all_data = load_all_data()
    today = diet_data.get("date", datetime.now().strftime("%Y-%m-%d"))
    found = False

    for entry in all_data:
        if entry.get("date") == today:
            # 如果已有“饮食”字段则合并，否则新建
            if "饮食" not in entry:
                entry["饮食"] = {}

            today_diet = entry["饮食"]

            for meal, meal_data in diet_data.get("餐次", {}).items():
                if meal not in today_diet:
                    today_diet[meal] = {"内容": [], "估算热量": 0}

                old = today_diet[meal]
                new_items = meal_data.get("内容", [])
                new_cal = meal_data.get("估算热量", 0)

                # 合并内容（去重）
                old["内容"] = list(set(old.get("内容", []) + new_items))

                # 合并热量
                old["估算热量"] += new_cal
            
            # 合并原始内容
            old_text = today_diet.get("原始内容", "")
            new_text = diet_data.get("原始内容", "")
            if new_text and new_text not in old_text:
                today_diet["原始内容"] = old_text + "。" + new_text if old_text else new_text
            
            # 合并热量（可选）
            if "总热量" in diet_data:
                old_cal = today_diet.get("总热量", 0)
                today_diet["总热量"] = old_cal + diet_data["总热量"]

            found = True
            break

    if not found:
        # 如果是新的一天，直接构造结构
        today_diet = {
            "原始内容": diet_data.get("原始内容", ""),
            "总热量": diet_data.get("总热量", 0)
        }

        for meal, meal_data in diet_data.get("餐次", {}).items():
            today_diet[meal] = {
                "内容": meal_data.get("内容", []),
                "估算热量": meal_data.get("估算热量", 0)
            }

        all_data.append({
            "date": today,
            "饮食": today_diet
        })

    save_all_data(all_data)
    print("✅ 饮食记录已保存/合并成功")