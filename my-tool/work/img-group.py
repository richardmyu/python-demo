# !/usr/bin/env python
# coding= utf-8
"""
@Project         : python-demo
@File            : img-group.py
@Author          : yum <richardminyu@foxmail.com>
@Date            : 2024/03/21 18:19
@Description     : 根据图片名称中的 日期 信息分类创建文件夹并移动到对应年月日文件夹
"""

import os
import re
import shutil

INPUT_FILE = '.' + os.sep + 'img-source'
OUTPUT_FILE = '.' + os.sep + 'output-output'


def main():
    """
    对名称带有日期信息的文件进行分类
    :return:
    """
    global INPUT_FILE
    global OUTPUT_FILE
    for file in os.listdir(INPUT_FILE):
        # 定义日期匹配模式
        # yyyymmdd yyyy-mm-dd yyyy_mm_dd
        date_re_1 = r'20\d{2}[01]\d[0-3]\d'
        date_re_2 = r'20\d{2}[_-][01]\d[_-][0-3]\d'
        file_date = ''

        # 匹配后，只获取日期字符串
        if re.search(date_re_1, str(file)) is not None:
            file_date = re.search(date_re_1, str(file)).group()

        if re.search(date_re_2, str(file)) is not None:
            file_date = re.search(date_re_2, str(file)).group().replace('-', '').replace('_', '')

        # 分开年，月，日，建立对应路径
        file_year = file_date[:4]
        file_month = file_date[4:6]
        file_day = file_date[6:]
        year_path = os.path.join(OUTPUT_FILE, file_year)
        month_path = os.path.join(year_path, file_month)
        day_path = os.path.join(month_path, file_day)
        file_path = os.path.join(INPUT_FILE, file)

        # 若如不存在则创建，若存在则移动
        if not os.path.exists(year_path):
            os.mkdir(year_path)

        if not os.path.exists(month_path):
            os.mkdir(month_path)

        if not os.path.exists(day_path):
            os.mkdir(day_path)

        shutil.move(file_path, day_path)


if __name__ == '__main__':
    main()
