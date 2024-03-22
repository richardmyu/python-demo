# -*- coding: utf-8 -*-

"""
斐波那契数列 (30)
"""

print(
    [
        x[0]
        for x in [
            (a[i][0], a.append([a[i][1], a[i][0] + a[i][1]]))
            for a in ([[1, 1]],)
            for i in range(30)
        ]
    ]
)
