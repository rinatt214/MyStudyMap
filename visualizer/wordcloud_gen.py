import os
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter


DATA_PATH = "data"  # 存放 JSON 的目录

def collect_keywords():
    """
    从 data/learning.json 中读取所有记录，提取 '学习' 下的关键词
    """
    json_path = os.path.join(DATA_PATH, "learning.json")
    if not os.path.exists(json_path):
        return []

    with open(json_path, "r", encoding="utf-8") as f:
        all_data = json.load(f)

    keywords = []
    for entry in all_data:
        learning = entry.get("学习", {})
        keywords.extend(learning.get("关键词", []))

    return keywords

def generate_wordcloud_image():
    """
    生成词云图并保存为 output_wordcloud.png
    """
    keywords = collect_keywords()
    if not keywords:
        return None

    freq = Counter(keywords)

    wc = WordCloud(
        font_path=r"C:\Windows\Fonts\simhei.ttf",
        width=800,
        height=400,
        background_color="white"
    )
    wc.generate_from_frequencies(freq)
    wc.to_file("output_wordcloud.png")
    return "output_wordcloud.png"