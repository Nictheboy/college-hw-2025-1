#!/usr/bin/python3

import os
import re
from datetime import datetime

# 获取脚本所在目录
base_dir = os.path.dirname(os.path.abspath(__file__))

# 获取所有作业文件夹
def get_homework_folders(base_dir):
    homework_folders = []
    for root, dirs, _ in os.walk(base_dir):
        for dir_name in dirs:
            # 匹配 HW_04-06 或 HW_04-06_1 形式
            match = re.match(r'HW_(\d{2}-\d{2})(?:_\d+)?$', dir_name)
            if match:
                # 解析日期
                homework_folders.append({
                    'date': datetime.strptime(match.group(1), "%m-%d"),  # 只解析 MM-DD
                    'folder': os.path.relpath(os.path.join(root, dir_name), base_dir)  # 计算相对路径
                })
    
    return homework_folders

# 按日期排序并输出
def sort_homeworks(homework_folders):
    # 假设作业都在今年（2025年）
    current_year = datetime.now().year
    for hw in homework_folders:
        hw['date'] = hw['date'].replace(year=current_year)  # 补充年份

    sorted_homeworks = sorted(homework_folders, key=lambda x: x['date'])

    # 输出排序结果
    for hw in sorted_homeworks:
        print(f"{hw['date'].strftime('%Y-%m-%d')} | {hw['folder']}")

# 运行主程序
if __name__ == "__main__":
    homework_folders = get_homework_folders(base_dir)
    if homework_folders:
        sort_homeworks(homework_folders)
    else:
        print("未找到任何作业文件夹")
