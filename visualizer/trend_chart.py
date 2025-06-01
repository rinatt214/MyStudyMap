import os
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import rcParams

DATA_PATH = "data"      #学习记录的文件

rcParams['font.family'] = 'SimHei'  # 中文黑体（需系统支持）
rcParams['axes.unicode_minus'] = False  # 正确显示负号

def collect_learning_stats():
    """
    从 learning.json 中统计每一天的关键词数量
    返回：两个列表，日期（str）和关键词数量（int）
    """
    json_path = os.path.join(DATA_PATH, "learning.json")
    if not os.path.exists(json_path):
        return [], []

    with open(json_path, "r", encoding="utf-8") as f:
        all_data = json.load(f)

    from collections import Counter
    counter = Counter()
    for entry in all_data:
        date = entry.get("date")
        keywords = entry.get("学习", {}).get("关键词", [])
        if date and isinstance(keywords, list):
            counter[date] += len(keywords)

    sorted_dates = sorted(counter)
    counts = [counter[d] for d in sorted_dates]

    return sorted_dates, counts

def draw_learning_trend_image():
    dates, counts = collect_learning_stats()
    if not dates:
        return None

    date_labels = [datetime.strptime(d, "%Y-%m-%d").strftime("%m/%d") for d in dates]
    path = "output_learning_trend.png"

    plt.figure(figsize=(10, 5))
    plt.plot(date_labels, counts, marker='o', linewidth=2)
    plt.title("每日学习关键词数量趋势图", fontsize=14)
    plt.xlabel("日期")
    plt.ylabel("关键词数量")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()

    return path
