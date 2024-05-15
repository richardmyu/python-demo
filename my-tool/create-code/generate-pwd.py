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

HELP_INFO = """
command: python filename/filepath -h/l/...
    -h # 帮助信息
  # 单字符模式，必须指定字符类型及数量
    -n 6 # (仅数字)       152649
    -l 6 # (仅小写字母)    sdkfal
    -u 6 # (仅大写字母)    AKDDKL
    -s 6 # (仅特殊符号)    $*))%#
    -m   # (等价 -nlu，即常用字符类型)
    -a   # (等价 -nlus，即全部字符类型)
    
  # 组合字符模式，必须分别指定字符类型及其数量
  # 字符类型可以合并写，但数量参数必须空格隔开
  # 若只有一个数量参数，则视为密码的总长度，各类型字符数随机
    -nl 2 4 # (数字+小写字母)    s6gd7g
    -nu 3   # (数字+大写字母)    5F1
    -ns 6   # (数字+特殊符号)    @2#435
    -lu
    -ls
    -us
    -nlu/-m # (数字+小写字母+大写字母)
    -nls
    -nus
    -lus
    -nlus/-a # (数字+小写字母+大写字母+特殊符号)
"""


def generate_special_char(x):
    """_生成 x 位特殊字符组_

    Args:
        x (_int_): _指定特殊字符个数_

    Returns:
        _str_: _特殊字符组合_
    """
    list_s_char = ')!@#$%^&*(`~+-*'
    length = len(list_s_char)
    r = ''

    for _ in range(x):
        i = random.randint(0, length - 1)
        r += str(list_s_char[i:i + 1])

    return r


def generate_number(y):
    """_生成 l 位数字字符组_

    Args:
        y (_int_): _指定数字字符个数_

    Returns:
        _str_: _数字字符组合_
    """
    r = ''

    for _ in range(y):
        i = random.randint(0, 9)
        r += str(i)

    return r


def generate_char():
    """_生成 l 位大小写字母字符组_

    Args:
        l (_int_): _指定大小写字母字符个数_

    Returns:
        _str_: _字母字符组合_
    """
    lowercase_char = 'abcdefghijklmnopqrstuvwxyz'
    # 设置字母组合集合
    list_char = lowercase_char + lowercase_char.upper() + lowercase_char + lowercase_char.upper() + lowercase_char
    length = len(list_char)
    r = ''

    # for _ in range(l):
    #     i = random.randint(0, length - 1)
    #     r += str(list_char[i:i + 1])
    #
    # return r


def mix_all_char(l=12):
    """_数字、大小写字母和特殊字符混合组合_

    Args:
        l (int, optional): _description_. Defaults to 12.
    """
    min_s_char_count = 2
    min_num_count = 2
    r = ''

    txt_s_char = generate_special_char(min_s_char_count)
    txt_num = generate_number(min_num_count)
    txt_char = generate_char(l - min_s_char_count - min_num_count)
    txt = txt_s_char + txt_char + txt_num
    list_index = [_ for _ in range(l)]
    random.shuffle(list_index)

    for _ in list_index:
        r += txt[_:_ + 1]

    return r


def mix_num_char(l=12):
    """_数字、大小写字母混合组合_

    Args:
        l (int, optional): _description_. Defaults to 12.
    """
    min_num_count = 4
    r = ''

    txt_num = generate_number(min_num_count)
    txt_char = generate_char(l - min_num_count)
    txt = txt_char + txt_num
    list_index = [_ for _ in range(l)]
    random.shuffle(list_index)

    for _ in list_index:
        r += txt[_:_ + 1]

    return r


def analyse_sys():
    """_参数解析_

    Returns:

    """
    print(str(sys.argv))
    global HELP_INFO
    if len(sys.argv) < 3 or len(sys.argv) > 6:
        print("请输入合理的参数，如：")
        print(HELP_INFO)
        return

    # print(type(sys.argv))
    print(sys.argv[1])
    print(sys.argv[2])


if __name__ == '__main__':
    analyse_sys()
    # all_char = ''.join(mix_all_char())
    # num_char = ''.join(mix_num_char())
    # print(all_char, num_char)
