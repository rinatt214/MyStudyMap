import os
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import rcParams

DATA_PATH = "data"
rcParams['font.family'] = 'SimHei'  # 或 "Microsoft YaHei"
rcParams['axes.unicode_minus'] = False  # 正常显示负号

def load_fitness_data():
    """
    从 data/learning.json 中读取每日健身记录
    返回 {日期: 健身记录字典}
    """
    data = {}
    file = os.path.join(DATA_PATH, "learning.json")

    if not os.path.exists(file):
        return data

    with open(file, "r", encoding="utf-8") as f:
        all_records = json.load(f)
        for entry in all_records:
            date = entry.get("date")
            fitness = entry.get("健身")
            if date and fitness:
                data[date] = fitness

    return data

def list_all_actions():
    """
    遍历所有健身记录，列出出现过的训练动作名称（去重）
    """
    data = load_fitness_data()
    action_set = set()

    for record in data.values():
        actions = record.get("训练动作", {})
        action_set.update(actions.keys())

    return sorted(action_set)

def draw_action_trend(action_name="卧推"):
    data = load_fitness_data()
    dates, weights = [], []

    for date, record in data.items():
        actions = record.get("训练动作", {})
        sets = actions.get(action_name, [])
        # ✅ 修正：确保结构正确，避免报错
        valid_weights = [s.get("重量") for s in sets if isinstance(s, dict) and isinstance(s.get("重量"), (int, float))]
        if not valid_weights:
            continue

        max_weight = max(valid_weights)
        dates.append(date)
        weights.append(max_weight)

    if not dates:
        print(f"⚠️ 没有找到动作：{action_name} 的训练记录")
        return

    date_labels = [datetime.strptime(d, "%Y-%m-%d").strftime("%m/%d") for d in dates]

    plt.figure(figsize=(10, 5))
    plt.plot(date_labels, weights, marker='o', linewidth=2)
    plt.title(f"{action_name} - 最重组重量趋势图")
    plt.xlabel("日期")
    plt.ylabel("重量 (kg)")
    plt.grid(True)
    plt.tight_layout()
    output_path = f"output_{action_name}_trend.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path  # ✅ 加这个

def draw_all_action_trends():
    """
    自动为所有出现过的训练动作画趋势图
    """
    paths = []
    actions = list_all_actions()
    for action in actions:
        path = draw_action_trend(action)
        if path:
            paths.append(path)
    return paths

def draw_calorie_trend():
    data = load_fitness_data()
    dates, calories = [], []

    for date, record in data.items():
        kcal = record.get("估算热量", 0)
        dates.append(date)
        calories.append(kcal)

    if not dates:
        print("⚠️ 没有热量数据")
        return

    date_labels = [datetime.strptime(d, "%Y-%m-%d").strftime("%m/%d") for d in dates]

    plt.figure(figsize=(10, 5))
    plt.plot(date_labels, calories, marker='o', color='orange', linewidth=2)
    plt.title("每日训练热量趋势图")
    plt.xlabel("日期")
    plt.ylabel("热量消耗 (kcal)")
    plt.grid(True)
    plt.tight_layout()
    output_path = "output_calorie_trend.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    print("✅ 图已保存为", output_path)
    return output_path  # ✅ 加这个

