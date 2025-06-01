"""
handlers/fitness_handler.py
健身记录处理模块。
功能：
- 接收解析后的健身记录
- 保存数据并合并训练动作、部位、有氧时间与热量
- 调用趋势图和词云图生成函数
"""

import streamlit as st
from storage.fitness_store import save_fitness_record
from visualizer.fitness_chart import draw_calorie_trend, draw_all_action_trends
from visualizer.fitness_wordcloud import generate_body_part_wordcloud

def handle_fitness(result):
    """
    处理健身记录。
    - 保存健身数据到本地（合并训练动作等）
    - 调用热量趋势图、训练部位词云和动作趋势图生成函数
    """

    save_fitness_record(result)
    draw_calorie_trend()
    draw_all_action_trends()
    generate_body_part_wordcloud()
    st.success("✅ 内容已保存为健身记录")