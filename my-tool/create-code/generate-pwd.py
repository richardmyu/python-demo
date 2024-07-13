# !/usr/bin/env python
# coding= utf-8
"""
Author         : yum <richardminyu@foxmail.com>
Date           : 2024-01-20 21:57:04
LastEditors    : yum <richardminyu@foxmail.com>
LastEditTime   : 2024-01-20 22:00:20
Description    : 在命令行中直接生成指定个数密码（包含数字、大小写字母和特殊字符）
"""

import random
import sys
import math

HELP_INFO = """
command: python filename/filepath -h/n/m/a num
    -h # 帮助信息
    -n # (数字+小写字母，即常用字符类型)
    -m # (数字+大、小写字母，即常用字符类型)
    -a # (数字+大、小写字母+特殊字符，即全部字符类型)
    
    num 总长度

"""


def generate_num(x):
    """_生成 x 位数字字符组_

    Args:
        x (_int_): _指定字符个数_

    Returns:
        _r_: _特殊字符组合_

    """
    r = ''
    for _ in range(x):
        i = random.randint(0, 10)
        r += str(i)

    return r


def generate_spe_char(x):
    """_生成 x 位特殊字符组_

    Args:
        x (_int_): _指定字符个数_

    Returns:
        _r_: _特殊字符组合_
    """
    list_s_char = ')!@#$%^&*(`~+-*/'
    length = len(list_s_char)
    r = ''

    for _ in range(x):
        i = random.randint(0, length - 1)
        r += str(list_s_char[i:i + 1])

    return r


def generate_char(x):
    """_生成 x 位大/小写字母字符组_

    Args:
        x (_int_): _指定大小写字母字符个数_

    Returns:
        _r_: _字母字符组合_
    """
    lowercase_char = 'abcdefghijklmnopqrstuvwxyz'

    # 设置字母组合集合
    length = len(lowercase_char)
    r = ''

    for _ in range(x):
        i = random.randint(0, length - 1)
        r += str(lowercase_char[i:i + 1])

    return r


def mix_num_lower(l=8):
    """_数字+小写字母 混合组合_

    Args:
        l (int, optional): _description_. Defaults to 8.

    Returns:

    """
    r = ''
    list_r = []
    step = 0

    if l >= 12:
        step = 3
    else:
        step = 2

    leng_nem = random.randint(math.floor(l / step), math.floor((l - 1) / 2))
    txt_num = generate_num(leng_nem)
    txt_char = generate_char(l - leng_nem)
    list_r = list(txt_num + txt_char)
    random.shuffle(list_r)
    r = ''.join(list_r)
    print(r)


def mix_num_char(l=8):
    """_数字+大小写字母 混合组合_

    Args:
        l (int, optional): _description_. Defaults to 8.
    """
    r = ''
    list_r = []
    step = 0

    if l > 8:
        step = 3
    else:
        step = 2

    leng_low = random.randint(math.floor(l / step), math.floor((l - 1) / 2))
    leng_num = l - leng_low * 2
    txt_num = generate_num(leng_num)
    txt_low = generate_char(leng_low)
    txt_upp = generate_char(leng_low).upper()
    list_r = list(txt_num + txt_low + txt_upp)
    random.shuffle(list_r)
    r = ''.join(list_r)
    print(r)


def mix_all_char(l=12):
    """_数字+大小写字母+特殊字符 混合组合_

    Args:
        l (int, optional): _description_. Defaults to 12.
    """
    r = ''
    list_r = []
    # TODO: 个数组成待调整优化
    leng_low = math.ceil(l / 4)
    leng_spe = math.floor(l / 4)
    leng_num = l - leng_low * 2 - leng_spe
    txt_num = generate_num(leng_num)
    txt_low = generate_char(leng_low)
    txt_upp = generate_char(leng_low).upper()
    txt_spe = generate_spe_char(leng_spe)
    list_r = list(txt_num + txt_low + txt_upp + txt_spe)
    random.shuffle(list_r)
    r = ''.join(list_r)
    print(r)


def analyse_sys():
    """_参数解析_

    Returns:

    """
    print(str(sys.argv[1]))
    global HELP_INFO
    if 3 >= len(sys.argv) >= 2:
        if sys.argv[1] == '-h':
            print(HELP_INFO)
            return
        elif sys.argv[1] == '-n':
            print(sys.argv[2])
            if sys.argv[2].isdigit():
                mix_num_lower(int(sys.argv[2]))
            else:
                mix_num_lower()
        elif sys.argv[1] == '-m':
            if sys.argv[2].isdigit():
                mix_num_char(int(sys.argv[2]))
            else:
                mix_num_char()
        elif sys.argv[1] == '-a':
            if sys.argv[2].isdigit():
                mix_all_char(int(sys.argv[2]))
            else:
                mix_all_char()
    else:
        print("请输入合理的参数，使用 -h 提供帮助信息")
        return


if __name__ == '__main__':
    analyse_sys()
    # all_char = ''.join(mix_all_char())
    # num_char = ''.join(mix_num_char())
    # print(all_char, num_char)
