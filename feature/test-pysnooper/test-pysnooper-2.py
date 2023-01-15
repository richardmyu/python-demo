# -*- coding: utf-8 -*-

"""
PySnooper 学习

https://pythondict.com/life-intelligent/tools/pysnooper/?hilite=pysnooper
"""

import pysnooper
import random


def foo():
    lst = []
    for i in range(10):
        lst.append(random.randrange(1, 1000))

    # with 上下文中的内容，才会被调试出来
    with pysnooper.snoop():
        lower = min(lst)
        upper = max(lst)
        mid = (lower + upper) / 2
        print(lower, mid, upper)


foo()
