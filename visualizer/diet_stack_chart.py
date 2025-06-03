import json
import os
from datetime import datetime
import plotly.graph_objects as go
import streamlit as st

DATA_PATH = "data"
DIET_FILE = os.path.join(DATA_PATH, "diet.json")

def show_diet_stack_chart():
    """
    生成每日饮食热量堆叠图（按餐别显示：早餐、午餐、晚餐、加餐）。

    功能：
    - 加载 diet.json 中的每日饮食记录
    - 分别提取每种餐别的热量（estimate_calories）
    - 使用 Plotly 绘制堆叠柱状图并保存
    - 返回图片路径
    """

    if not os.path.exists(DIET_FILE):
        return None
    
    with open(DIET_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    meal_types = ["早餐", "午餐", "晚餐", "加餐"]
    date_to_meals = {}

    for entry in data:
        date = entry.get("date")
        diet = entry.get("饮食", {})

        if date not in date_to_meals:
            date_to_meals[date] = {meal: 0 for meal in meal_types}

        for meal in meal_types:
            if isinstance(diet.get(meal), dict):
                date_to_meals[date][meal] = diet[meal].get("估算热量", 0)
    
    if not  date_to_meals:
        return None
    
    # 按日期排序
    sorted_dates = sorted(date_to_meals.keys())
    meal_data = {meal: [] for meal in meal_types}

    for date in sorted_dates:
        for meal in meal_types:
            meal_data[meal].append(date_to_meals[date].get(meal, 0))  # 自动补 0

    # 生成堆叠柱状图
    fig = go.Figure()
    for meal in meal_types:
        fig.add_trace(go.Bar(x=sorted_dates, y=meal_data[meal], name=meal))

    fig.update_layout(
        barmode='stack',
        title="每日餐别热量堆叠图",
        xaxis_title="日期",
        yaxis_title="热量 (kcal)",
        xaxis=dict(
            tickformat="%Y-%m-%d",  # 只显示年月日
            type="category"         # 强制按分类显示，而不是时间轴
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    st.success("✅ 饼图已生成")
