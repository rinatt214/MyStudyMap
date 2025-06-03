"""
app.py
应用主入口文件。
功能：
- 接收用户输入（自然语言）
- 使用本地 AI 模型自动解析内容类型（学习 or 健身）
- 调用对应处理模块保存记录与生成可视化
- 显示图表展示区域（在侧边栏中切换展示）
"""

import streamlit as st
from datetime import datetime
import time
import os
from PIL import Image
import json

from streamlit.runtime.state.common import RegisterWidgetResult
from input_handler import get_user_input
from parser.ai_parser import extract_info

from handlers.learning_handler import handle_learning
from handlers.fitness_handler import handle_fitness
from handlers.diet_handler import handle_diet
from display.show_learning_charts import show_learning_charts
from display.show_fitness_charts import show_fitness_charts
from display.show_diet_charts import show_diet_charts

#设置网页标题
st.set_page_config(page_title="MyStudyMap", layout="wide")

#页面标题
st.title("📘 MyStudyMap - 智能成长记录系统")

#=== 输入区域 ===
st.subheader("📝 请输入你的学习或健身内容（系统将自动识别）")
user_input = st.text_area("例如：今天复习了神经网络，练了卧推40×10，跑步30分钟", height=150)

if st.button("提交并解析"):
    if not user_input.strip():
        st.warning("请输入内容再提交")
    else:
        #使用本地AI模型分析
        result = extract_info(user_input)
        st.json(result)
        result["原始内容"] = user_input
        result["date"] = datetime.today().strftime("%Y-%m-%d")

        content_type = result.get("类型", "未知")

        if content_type == "学习":
            handle_learning(result)
        
        elif content_type == "健身":
            handle_fitness(result)
        
        elif content_type == "饮食":
            handle_diet(result)
        
        else:
            st.warning("❓ 无法识别内容类型，请检查输入内容")

# --- 展示模块 ---
st.sidebar.title("📊 图表展示")
main_choice = st.sidebar.radio("选择分类：", ["学习", "健身", "饮食"])

if main_choice == "学习":
    show_learning_charts()

elif main_choice == "健身":
    show_fitness_charts()

elif main_choice == "饮食":
    show_diet_charts()