#MyStudyMap

**一个本地运行的 AI 个人成长记录工具，支持自然语言输入、关键词提取与可视化分析。**  
**A local LLM-powered personal growth tracking app that supports natural language input, keyword extraction, and visual analysis.**

##项目简介 / Overview

MyStudyMap 利用本地大语言模型（如 Ollama）结合 Streamlit 前端，实现对日常学习与健身记录的自动化处理，包括：

- ✍️ 自然语言输入每日记录（如学习计划、训练内容）
- 🤖 自动识别记录类型（学习 / 健身）
- 🧠 提取关键词、动作、部位、时长等信息
- 📊 自动生成词云图、关键词趋势图、训练部位热力图等
- 💾 所有数据以 JSON 格式保存在本地，适合长期追踪

---

MyStudyMap combines a local LLM (e.g., Ollama) with a Streamlit front-end to automate the analysis of daily learning and fitness logs:

- ✍️ Input natural language entries (e.g., study plans, workout logs)
- 🤖 Automatically detect the type (study or fitness)
- 🧠 Extract key terms, actions, body parts, duration, etc.
- 📊 Generate word clouds, keyword trends, and training heatmaps
- 💾 All data is saved locally in JSON format for long-term tracking

## 🚀 快速启动 / Quick Start

### 1. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```
### 2. 运行应用 / Run the App

streamlit run app.py

确保本地 Ollama 模型已启动（例如使用 llama3）  
Make sure the Ollama model is running locally (e.g., llama3):

ollama run llama3

## 📁 项目结构 / Project Structure

```bash
MyStudyMap/
├── app.py                   # Streamlit 主程序 / Main Streamlit app
├── .gitignore               # Git 忽略文件配置 / Git ignore settings
├── requirements.txt         # 依赖包列表 / Python dependency list
│
├── data/                    # JSON 数据存储 / Data storage (JSON)
│   └── learning.json
│
├── display/                 # 图表显示模块 / Display charts
│   ├── show_fitness_charts.py
│   └── show_learning_charts.py
│
├── handlers/                # 处理用户输入与数据的逻辑 / Input and data handlers
│   ├── fitness_handler.py
│   └── learning_handler.py
│
├── parser/                  # AI 模型解析相关模块 / AI parsing modules
│   ├── ai_parser.py
│   └── fitness_ai_helper.py
│
├── storage/                 # 数据存储逻辑 / JSON storage logic
│   ├── fitness_store.py
│   └── learning_store.py
│
├── visualizer/              # 可视化生成模块 / Visualization components
│   ├── fitness_chart.py
│   ├── fitness_wordcloud.py
│   ├── trend_chart.py
│   └── wordcloud_gen.py
```

## ✅ 功能进展 / Features & Progress

- [x] 接入本地大语言模型（Ollama） / Integrated local LLM (Ollama)
- [x] 自动解析学习与健身内容 / Automatically parse study & fitness records
- [x] 提取关键词、部位、时间、重量等详细信息 / Extract keywords, body parts, time, weights, etc.
- [x] 数据本地保存为 JSON 文件 / Save data locally in JSON format
- [x] 可视化展示（词云图、趋势图、训练部位图等） / Visualization (word cloud, trend chart, body part chart)
- [x] 使用模块化架构，方便维护和扩展 / Modular architecture for easy extension
- [ ] 新增“饮食记录”模块（开发中） / Add "diet tracking" module (in progress)
- [ ] 用户多账户支持（规划中） / Multi-user support (planned)
- [ ] 数据导入导出功能 / Data import/export feature (planned)

## 📄 许可协议 / License

本项目基于 MIT License 开源发布，详细内容请查看 LICENSE 文件。  
This project is released under the MIT License. See the LICENSE file for details.
