# -*- coding: utf-8 -*-

"""心形字符串"""

import string

l = string.ascii_letters
s = []
s.append(l[34])
s.append(l[11])
s.append(l[14])
s.append(l[21])
s.append(l[4])
s.append(l[24])
s.append(l[14])
s.append(l[20])
s.insert(1, " ")
s.insert(6, " ")

string = "".join(s)

# 心形的构成字符
sourceStr = 'o-0'

# print(string)

# print('\n'.join([''.join([('Love'[(x - y) % len('Love')] if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (
#     x * 0.05) ** 2 * (y * 0.1) ** 3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(30, -30, -1)]))

# print('\n'.join([''.join([('SB'[(x - y) % len('SB')] if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (
#     x * 0.05) ** 2 * (y * 0.1) ** 3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(30, -30, -1)]))

txt = '\n'.join(
    [
        ''.join(
            [
                (
                    sourceStr[(x - y) % len(sourceStr)]
                    if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3
                       - (x * 0.05) ** 2 * (y * 0.1) ** 3
                       <= 0
                    else ' '
                )
                for x in range(-30, 30)
            ]
        )
        for y in range(30, -30, -1)
    ]
)

with open("output.txt", "w") as f:
    f.write(txt)
