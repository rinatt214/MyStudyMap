import streamlit as st
from datetime import datetime
from storage.diet_store import save_diet_record
from display.show_diet_charts import show_diet_charts

def handle_diet(record):
    """
    处理饮食记录。
    - 保存到本地 JSON（自动合并）
    - 调用饮食趋势图可视化
    """
    save_diet_record(record)
    show_diet_charts()
    st.success("✅ 饮食记录已保存")