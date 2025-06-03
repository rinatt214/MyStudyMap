import json
import os
from datetime import datetime
import plotly.graph_objects as go
import streamlit as st

DATA_PATH = "data"
DIET_FILE = os.path.join(DATA_PATH, "diet.json")

def show_diet_trend_chart():
    """
    生成每日总热量的趋势图（折线图）。

    功能：
    - 加载 diet.json 中的每日饮食记录
    - 按日期统计每天摄入的总热量（sum of 每顿 estimate_calories）
    - 使用 Plotly 绘制折线图并保存
    - 返回图片路径
    """
    if not os.path.exists(DIET_FILE):
        return None
    
    with open(DIET_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    #构建日期与总热量映射
    date_to_calories = {}
    for entry in data:
        date = entry.get("date")
        diet = entry.get("饮食", {})
        total = 0
        for meal in ["早餐", "午餐", "晚餐", "加餐"]:
            if isinstance(diet.get(meal), dict):
                total += diet[meal].get("估算热量", 0)
        date_to_calories[date] = total
    
    if not date_to_calories:
        return None
    
    #按日期排序
    sorted_items = sorted(date_to_calories.items(), key = lambda x: x[0])
    dates = [x[0] for x in sorted_items]
    calories = [x[1] for x in sorted_items]

    #生成图像
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = dates, y = calories, mode = 'lines+markers', name = '总热量'))
    fig.update_layout(
        title="每日摄入热量趋势",
        xaxis_title="日期",
        yaxis_title="热量 (kcal)",
        xaxis=dict(
            tickformat="%Y-%m-%d",  # 只显示年月日
            type="category"         # 强制按分类显示，而不是时间轴
        )
    )

    st.plotly_chart(fig, use_container_width=True)
