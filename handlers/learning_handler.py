"""
handlers/learning_handler.py
学习记录处理模块。
功能：
- 接收解析后的学习记录
- 保存数据并更新当天的关键词和原始内容（合并去重）
- 调用词云图与趋势图生成函数
"""

import streamlit as st
from storage.learning_store import save_learning_record
from visualizer.wordcloud_gen import generate_wordcloud_image
from visualizer.trend_chart import draw_learning_trend_image

def handle_learning(result):
    """
    处理学习记录。
    - 保存学习数据到本地（合并关键词与内容）
    - 调用词云图和趋势图生成函数
    """
    
    save_learning_record(result)
    generate_wordcloud_image()
    draw_learning_trend_image()
    st.success("✅ 内容已保存为学习记录")