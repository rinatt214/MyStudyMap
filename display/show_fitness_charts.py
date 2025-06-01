"""
display/show_fitness_charts.py
健身图表展示模块。
功能：
- 在侧边栏中让用户选择图表类型
- 显示热量趋势图、训练部位词云、各动作重量趋势图
"""

import streamlit as st
from visualizer.fitness_chart import draw_calorie_trend, draw_all_action_trends
from visualizer.fitness_wordcloud import generate_body_part_wordcloud
import os

def show_fitness_charts():
    """
    显示健身图表。

    功能：
    - 用户在侧边栏选择「热量趋势图」、「训练部位词云」或「各动作趋势图」
    - 调用相应的可视化函数生成图像并展示
    """
    chart_choice = st.sidebar.radio("选择图表：", ["热量趋势图", "训练部位词云", "各动作重量趋势"])

    if chart_choice == "热量趋势图":
        path = draw_calorie_trend()
        if path:
            st.image(path, caption="训练热量趋势图", use_container_width=True)

    elif chart_choice == "训练部位词云":
        path = generate_body_part_wordcloud()
        if path:
            st.image(path, caption="训练部位词云", use_container_width=True)

    elif chart_choice == "各动作重量趋势":
        paths = draw_all_action_trends()
        if paths:
            for path in paths:
                name = os.path.basename(path).replace("output_", "").replace("_trend.png", "")
                st.image(path, caption=f"{name} 重量趋势图", use_container_width=True)