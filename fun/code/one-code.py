# !/usr/bin/env python
# coding= utf-8
'''
Author         : yum <richardminyu@foxmail.com>
Date           : 2024-01-20 21:57:04
LastEditors    : yum <richardminyu@foxmail.com>
LastEditTime   : 2024-01-20 22:00:20
Description    : 在命令行中直接生成密码
'''

import random


# TODO: 有空继续完善

def generate_special_char(l):
    """_生成 l 位特殊字符组_

    Args:
        l (_int_): _指定特殊字符个数_

    Returns:
        _str_: _特殊字符组合_
    """
    LIST_S_CHAR = ')!@#$%^&*(`~+-*'
    length = len(LIST_S_CHAR)
    r = ''

    for _ in range(l):
        i = random.randint(0, length - 1)
        r += str(LIST_S_CHAR[i:i + 1])

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
    LOWERCASE_CHAR = 'abcdefghijklmnopqrstuvwxyz'
    UPPERCASE_CHAR = 'ABCDEFJHIJKLMNOPQRSTUVWXYZ'
    LIST_CHAR = LOWERCASE_CHAR + UPPERCASE_CHAR + LOWERCASE_CHAR + UPPERCASE_CHAR + LOWERCASE_CHAR
    length = len(LIST_CHAR)
    r = ''

    for _ in range(l):
        i = random.randint(0, length - 1)
        r += str(LIST_CHAR[i:i + 1])

    return r


def mix_all_char(l=12):
    """_数字、大小写字母和特殊字符混合组合_

    Args:
        l (int, optional): _description_. Defaults to 12.
    """
    MIN_S_CHAR_COUNT = 2
    MIN_NUM_COUNT = 2
    r = ''

    txt_s_char = generate_special_char(MIN_S_CHAR_COUNT)
    txt_num = generate_number(MIN_NUM_COUNT)
    txt_char = generate_char(l - MIN_S_CHAR_COUNT - MIN_NUM_COUNT)
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
    MIN_NUM_COUNT = 4
    r = ''

    txt_num = generate_number(MIN_NUM_COUNT)
    txt_char = generate_char(l - MIN_NUM_COUNT)
    txt = txt_char + txt_num
    list_index = [_ for _ in range(l)]
    random.shuffle(list_index)

    for _ in list_index:
        r += txt[_:_ + 1]

    return r


if __name__ == "__main__":
    all_char = ''.join(mix_all_char())
    num_char = ''.join(mix_num_char())
    print(all_char, num_char)
