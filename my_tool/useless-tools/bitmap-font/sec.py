# -*- coding: utf-8 -*-

# !/usr/bin/env python3

character = u"阵"


def get_character_offset(char):
    code = str(char.encode(encoding='gb2312', errors='strict').hex())
    area = int(code[:2], 16) - 0XA0 - 1
    index = int(code[2:], 16) - 0XA0 - 1

    return ((0X5E * area) + index) * 32


def get_character_matrix_mode(font_set, char):
    fontSet.seek(get_character_offset(char))
    char_source = font_set.read(32)
    char_matrix = []
    for k in range(0, len(char_source), 2):
        n = []
        for i in char_source[k:k + 2]:
            n.append(format(i, '08b'))
        char_matrix.append(''.join(n))
    return char_matrix


def show_bit_map_font(font_set, char):
    for i in get_character_matrix_mode(font_set, char):
        for k in i:
            if int(k):
                print("0", end=" ")
            else:
                print(".", end=" ")
        print()


if __name__ == "__main__":
    fontSet = open("./HZK16", "rb")  # Keep font memery-resident
    show_bit_map_font(fontSet, character)

    fontSet.close()
