"""
display/show_learning_charts.py
学习图表展示模块。
功能：
- 在侧边栏中让用户选择图表类型
- 显示关键词词云图或学习趋势图
"""

import streamlit as st
from visualizer.wordcloud_gen import generate_wordcloud_image
from visualizer.trend_chart import draw_learning_trend_image

def show_learning_charts():
    """
    显示学习图表。

    功能：
    - 用户在侧边栏选择「关键词词云」或「趋势图」
    - 调用可视化函数生成图像并展示
    """
    chart_choice = st.sidebar.radio("选择图表：", ["关键词词云", "趋势图"])

    if chart_choice == "关键词词云":
        generate_wordcloud_image()
        st.image("output_wordcloud.png", caption="学习关键词词云", use_container_width=True)

    elif chart_choice == "趋势图":
        draw_learning_trend_image()
        st.image("output_learning_trend.png", caption="每日学习关键词趋势图", use_container_width=True)