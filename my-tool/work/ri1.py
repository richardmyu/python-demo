# !/usr/bin/env python
# coding= utf-8
"""
@File            : ri1.py
@Author          : yum <richardminyu@foxmail.com>
@Date            : 2024/08/31 23:32
@Description     : 
"""
# TODO:On Hold
import cv2
import os
import pytesseract


def get_info(img):
    # 读取身份证图片
    img = cv2.imread(img)

    # 转换为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 对图像进行二值化处理
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 使用tesseract OCR库识别身份证号码和姓名
    config = '--psm 6'
    id_number = pytesseract.image_to_string(binary, config=config, lang='chi_sim').strip()
    config = '--psm 7'
    name = pytesseract.image_to_string(binary, config=config, lang='chi_sim').strip()

    # 输出结果
    print('身份证号码：', id_number)
    print('姓名：', name)


if __name__ == "__main__":
    for file in os.listdir('./ids'):
        get_info(file)
