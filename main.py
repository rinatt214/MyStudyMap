from input_handler import get_user_input
from parser.ai_parser import extract_learning_info
from parser.fitness_ai_helper import parse_fitness_text_with_ai
from storage.data_store import save_learning_record, save_fitness_record

def main():
    print("📌 请选择记录类型：")
    print("1 - 学习记录")
    print("2 - 健身记录")
    choice = input("输入编号：").strip()

    text = get_user_input()

    if choice == "1":
        parsed = extract_learning_info(text)
        parsed["原始内容"] = text
        save_learning_record(parsed)

        print("✅ 学习记录已保存，提取结果如下：")
        print(parsed)

    elif choice == "2":
        parsed = parse_fitness_text_with_ai(text)
        parsed["原始内容"] = text
        save_fitness_record(parsed)

        print("✅ 健身记录已保存，AI解析结果如下：")
        print(parsed)

    else:
        print("❌ 输入无效，请输入 1 或 2")

if __name__ == "__main__":
    main()