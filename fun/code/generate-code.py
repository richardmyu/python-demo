# !/usr/bin/env python
# coding= utf-8
"""
Author         : yum <richardminyu@foxmail.com>
Date           : 2024-01-20 14:57:36
LastEditors    : yum <richardminyu@foxmail.com>
LastEditTime   : 2024-01-20 22:00:31
Description    : 生成指定位数密码，写人 TXT
"""

# TODO: 有空继续完善
import random
import os

CODE_PATH = "./code.txt"
CODED_PATH = "./coded.txt"


def generate_special_char(l):
    """_生成 l 位特殊字符组_

    Args:
        l (_int_): _指定特殊字符个数_

    Returns:
        _str_: _特殊字符组合_
    """
    list_s_char = ')!@#$%^&*(`~+-*'
    length = len(list_s_char)
    r = ''

    for _ in range(l):
        i = random.randint(0, length - 1)
        r += str(list_s_char[i:i + 1])

    return r


def generate_number(l):
    """_生成 l 位数字字符组_

    Args:
        l (_int_): _指定数字字符个数_

    Returns:
        _str_: _数字字符组合_
    """
    r = ''

    for _ in range(l):
        i = random.randint(0, 9)
        r += str(i)

    return r


def generate_char(l):
    """_生成 l 位大小写字母字符组_

    Args:
        l (_int_): _指定大小写字母字符个数_

    Returns:
        _str_: _字母字符组合_
    """
    lowercase_char = 'abcdefghijklmnopqrstuvwxyz'
    uppercase_char = 'ABCDEFJHIJKLMNOPQRSTUVWXYZ'
    list_char = lowercase_char + uppercase_char + lowercase_char + uppercase_char + lowercase_char
    length = len(list_char)
    r = ''

    for _ in range(l):
        i = random.randint(0, length - 1)
        r += str(list_char[i:i + 1])

    return r


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


def input_txt(filepath):
    list_name = []

    if not os.path.exists(filepath):
        print(f'当前环境：{os.getcwd()}')
        print(f'文件路径：{filepath}')
        print("文件不存在，请检查文件是否存在或文件路径是否正确。")
    else:
        try:
            with open(filepath, 'r', encoding="utf-8") as file:
                list_name = file.readlines()
        except FileNotFoundError:
            print(f'当前环境：{os.getcwd()}')
            print(f'文件路径：{filepath}')
            print("文件未找到，请检查文件路径是否正确。")

    return list_name


def output_txt(filepath):
    input_list = input_txt(CODE_PATH)
    input_diff = []

    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding="utf-8") as file:
            for line in input_list:
                if line.strip("\n"):
                    all_char = ''.join(mix_all_char())
                    num_char = ''.join(mix_num_char())
                    txt = line.strip("\n") + " " + all_char + " " + num_char + "\n"
                    file.write(txt)
    else:
        with open(filepath, 'r', encoding="utf-8") as file:
            inputed_list = file.readlines()

        for _ in input_list:
            if _.strip("\n") not in ''.join(inputed_list):
                input_diff.append(_)

        with open(filepath, 'a', encoding="utf-8") as file:
            for line in input_diff:
                if line.strip("\n"):
                    all_char = ''.join(mix_all_char())
                    num_char = ''.join(mix_num_char())
                    txt = line.strip("\n") + " " + all_char + " " + num_char + "\n"
                    file.write(txt)


if __name__ == "__main__":
    output_txt(CODED_PATH)
