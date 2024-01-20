# -*- coding: utf-8 -*-

# !/usr/bin/env python3

character = u"阵"


def getCharacterOffset(character):
    code = str(character.encode(encoding='gb2312', errors='strict').hex())
    area = int(code[:2], 16) - 0XA0 - 1
    index = int(code[2:], 16) - 0XA0 - 1

    return ((0X5E * area) + index) * 32


def getCharacterMatrixMode(fontSet, character):
    fontSet.seek(getCharacterOffset(character))
    characterSource = fontSet.read(32)
    characterMatrix = []
    for k in range(0, len(characterSource), 2):
        n = []
        for i in characterSource[k:k + 2]:
            n.append(format(i, '08b'))
        characterMatrix.append(''.join(n))
    return characterMatrix


def showBitMapFont(fontSet, character):
    for i in getCharacterMatrixMode(fontSet, character):
        for k in i:
            if (int(k)):
                print("0", end=" ")
            else:
                print(".", end=" ")
        print()


if __name__ == "__main__":
    fontSet = open("./HZK16", "rb")  # Keep font memery-resident
    showBitMapFont(fontSet, character)

    fontSet.close()
