# !/usr/bin/env python
# coding= utf-8
"""
@Project         : tt2utc
@File            : tt2utc.py
@Author          : yum <richardminyu@foxmail.com>
@Date            : 2025/02/18 10:18
@Description     : 将微信图片名称中的时间戳转换UTC，并重命名
"""

import datetime
import time
import os
import re

PATH = "./imgs"


def tt_10_str(tt):
    t = datetime.datetime.utcfromtimestamp(tt)
    s = t.strftime('%Y%m%d_%H%M%S')
    return s


def tt_13_str(tt):
    # TODO:时分秒转换有问题
    tt = int(tt) / 1000.0
    t = datetime.datetime.utcfromtimestamp(tt)
    s = t.strftime('%Y%m%d_%H%M%S%f')
    return s


def set_name(pt, img, prefix, tp):
    print(pt, img, prefix, tp)
    tt = re.match(pt, img)
    txt = ""
    if len(tt.group(1)) == 10:
        print("222")
        txt = tt_10_str(tt.group(1))
    else:
        print("333")
        txt = tt_13_str(tt.group(1))

    src = os.path.join(os.path.abspath(PATH), img)
    dst = os.path.join(os.path.abspath(PATH), f"{prefix}{txt}.{tp}")
    try:
        os.rename(src, dst)
    except:
        print(f"error: {img}")


def handler_name():
    # 不同类型处理（暂只处理 .jpg）
    pt = r"^wx_camera_(\d{10}|\d{13}).jpg$"
    pt_2 = r"^mmexport(\d{10}|\d{13}).jpg$"
    imgs = os.listdir(PATH)

    for img in imgs:
        if re.search(pt, img):
            set_name(pt, img, "wx_camera_", "jpg")
        if re.search(pt_2, img):
            set_name(pt_2, img, "mmexport_", "jpg")


if __name__ == "__main__":
    handler_name()
