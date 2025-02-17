# !/usr/bin/env python
# coding= utf-8
"""
@Project         : python-demo
@File            : my-img-group.py
@Author          : yum <richardminyu@foxmail.com>
@Date            : 2024/03/29 21:16
@Description     : 根据图片日期信息（分类）创建文件夹并移动到对应文件夹
"""
# TODO:Completed
import os
import re
import shutil
import exifread

INPUT_FILE = ''
OUTPUT_FILE = ''
# 定义日期匹配模式
# yyyymmdd yyyy-mm-dd yyyy_mm_dd
date_re_1 = r'20\d{2}[01]\d[0-3]\d'
date_re_2 = r'20\d{2}[_-][01]\d[_-][0-3]\d'


def img_type(flag, file):
    """
    判断图片名称是否有日期信息
    Args:
        flag:
        file:

    Returns:

    """
    if re.search(date_re_1, file) is not None or re.search(date_re_2, file) is not None:
        get_date(flag, file)
    else:
        analytical_date(flag, file)


def get_date(flag, file):
    """
    通过图片名称，获取图片日期信息
    Args:
        flag: 图片类型
        file: 图片(名称)

    Returns:

    """
    file_date = ''

    # 匹配后，只获取日期字符串
    if re.search(date_re_1, file) is not None:
        file_date = re.search(date_re_1, str(file)).group()

    if re.search(date_re_2, file) is not None:
        file_date = re.search(date_re_2, str(file)).group().replace('-', '').replace('_', '')

    mk_files(flag, file, file_date)


def analytical_date(flag, file):
    """
    通过 exifread 读取图片日期信息
    Args:
        flag: 图片类型
        file: 图片(名称)

    Returns:

    """
    global INPUT_FILE
    img_date = ''
    f = open(os.path.join(INPUT_FILE, file), 'rb')
    image_map = exifread.process_file(f)

    # 照片拍摄日期-时间
    try:
        img_date = image_map['Image DateTime'].printable[:10].replace(':', '-')
    except Exception as e:
        print('Warning: No Image DateTime')
        img_date = ''

    f.close()
    if len(img_date) != 8:
        print(f'图片: {flag}/{file} 没有有效的日期信息')
        # 无日期信息，则合并在一个文件夹(others)
        mk_file('others', file)
        return
    else:
        mk_files(flag, file, img_date)


def mk_file(drc, file):
    """
    移动该文件至目标文件夹
    Args:
        drc: 图片类型
        file: 图片（名称）

    Returns:

    """
    global INPUT_FILE
    global OUTPUT_FILE
    input_path = os.path.join(INPUT_FILE, file)
    output_path = os.path.join(OUTPUT_FILE, drc)
    # 若如不存在则创建，若存在则移动
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    if not os.path.exists(os.path.join(output_path, file)):
        shutil.move(input_path, output_path)


def mk_files(drc, file, file_date):
    """
    根据图片日期信息创建对应多级文件夹，并移动该文件至目标文件夹
    Args:
        drc: 图片类型
        file: 图片（名称）
        file_date: 图片的日期

    Returns:

    """
    global INPUT_FILE
    global OUTPUT_FILE
    # 分开年，月，日，建立对应路径
    file_year = file_date[:4]
    file_month = file_date[4:6]
    file_day = file_date[6:]
    drc_path = os.path.join(OUTPUT_FILE, drc)
    year_path = os.path.join(drc_path, file_year)
    month_path = os.path.join(year_path, file_month)
    day_path = os.path.join(month_path, file_day)
    file_path = os.path.join(INPUT_FILE, file)

    # 若如不存在则创建，若存在则移动
    if not os.path.exists(drc_path):
        os.mkdir(drc_path)

    if not os.path.exists(year_path):
        os.mkdir(year_path)

    if not os.path.exists(month_path):
        os.mkdir(month_path)

    if not os.path.exists(day_path):
        os.mkdir(day_path)

    if not os.path.exists(os.path.join(day_path, file)):
        shutil.move(file_path, day_path)


def main():
    global INPUT_FILE
    global OUTPUT_FILE
    INPUT_FILE = '.' + os.sep + 'img-source'
    OUTPUT_FILE = '.' + os.sep + 'img-output'

    if not os.path.exists(INPUT_FILE):
        print(f'指定文件 {INPUT_FILE} 不存在')
        return

    if not os.path.exists(OUTPUT_FILE):
        os.mkdir(OUTPUT_FILE)

    for f in os.listdir(INPUT_FILE):
        if re.search(r'^wx_camera_', f, re.I) is not None:
            img_type('wechat', f)
        elif re.search(r'^IMG_', f, re.I) is not None:
            img_type('camera', f)
        elif re.search(r'^PANO_', f, re.I) is not None:
            img_type('camera', f)
        elif re.search(r'^Screenshot_', f, re.I) is not None:
            img_type('screenshot', f)
        elif re.search(r'^VID_', f, re.I) is not None:
            img_type('mp4', f)
        elif re.search(r'^mmexport', f, re.I) is not None:
            img_type('mmexport', f)
        else:
            img_type('others', f)


if __name__ == '__main__':
    main()
