import streamlit as st
from visualizer.diet_stack_chart import show_diet_stack_chart
from visualizer.diet_trend import show_diet_trend_chart


def show_diet_charts():
    """
    显示饮食图表。

    功能：
    - 用户在侧边栏选择图表类型：「热量趋势图」、「各餐热量堆叠图」
    - 调用相应的函数生成图像并展示
    """
    chart_choice = st.sidebar.radio("选择饮食图表：", ["热量趋势图", "各餐热量堆叠图"])

    if chart_choice == "热量趋势图":
        path = show_diet_trend_chart()
        if path:
            st.image(path, caption="每日总热量趋势图", use_container_width=True)

    elif chart_choice == "各餐热量堆叠图":
        path = show_diet_stack_chart()
        if path:
            st.image(path, caption="每日各餐热量堆叠图", use_container_width=True)