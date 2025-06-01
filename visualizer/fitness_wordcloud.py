import os
import json
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ✅ 设置中文字体
from matplotlib import rcParams
rcParams['font.family'] = 'SimHei'
rcParams['axes.unicode_minus'] = False

DATA_PATH = "data"
DATA_FILE = os.path.join(DATA_PATH, "learning.json")

def generate_body_part_wordcloud():
    """
    从 learning.json 中收集训练部位，生成词云图
    """
    if not os.path.exists(DATA_FILE):
        print("❌ 找不到数据文件")
        return None

    parts = []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        all_records = json.load(f)
        for entry in all_records:
            fitness = entry.get("健身", {})
            parts.extend(fitness.get("训练部位", []))

    if not parts:
        print("⚠️ 没有训练部位数据")
        return None

    freq = Counter(parts)

    wc = WordCloud(
        font_path="C:/Windows/Fonts/simhei.ttf",  # 根据系统替换路径
        width=800,
        height=400,
        background_color="white"
    )
    wc.generate_from_frequencies(freq)

    output_path = "output_fitness_parts_wordcloud.png"
    wc.to_file(output_path)
    print("✅ 已生成训练部位词云图")
    return output_path