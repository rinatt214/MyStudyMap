import streamlit as st
from datetime import datetime
import time
import os
from PIL import Image
import json

from streamlit.runtime.state.common import RegisterWidgetResult
from input_handler import get_user_input
from parser.ai_parser import extract_info
from storage.data_store import save_learning_record, save_fitness_record
from visualizer.wordcloud_gen import generate_wordcloud_image
from visualizer.trend_chart import draw_learning_trend_image
from visualizer.fitness_chart import draw_action_trend, draw_calorie_trend, draw_all_action_trends
from visualizer.fitness_wordcloud import generate_body_part_wordcloud

#设置网页标题
st.set_page_config(page_title="MyStudyMap", layout="wide")

#页面标题
st.title("📘 MyStudyMap - 智能成长记录系统")

#输入区域
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
            save_learning_record(result)
            generate_wordcloud_image()
            draw_learning_trend_image()
            st.success("✅ 内容已保存为学习记录")
        
        elif content_type == "健身":
            save_fitness_record(result)
            #draw_action_trend()
            draw_calorie_trend()
            draw_all_action_trends()
            generate_body_part_wordcloud()
            st.success("✅ 内容已保存为健身记录")
        
        else:
            st.warning("❓ 无法识别内容类型，请检查输入内容")

# --- 展示模块 ---
st.sidebar.title("📊 图表展示")
main_choice = st.sidebar.radio("选择分类：", ["学习", "健身"])

if main_choice == "学习":
    chart_choice = st.sidebar.radio("选择图表：", ["关键词词云", "趋势图"])

    if chart_choice == "关键词词云":
        generate_wordcloud_image()
        st.image("output_wordcloud.png", caption="学习关键词词云", use_container_width=True)

    elif chart_choice == "趋势图":
        draw_learning_trend_image()
        st.image("output_learning_trend.png", caption="每日学习关键词趋势图", use_container_width=True)

elif main_choice == "健身":
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