# -*- config: utf-8 -*-
"""
PySnooper 学习

https://pythondict.com/life-intelligent/tools/pysnooper/?hilite=pysnooper
"""

import pysnooper

# 输出到终端
# @pysnooper.snoop()


# 输出到文件
@pysnooper.snoop('./log/test-pysnooper.log')
def number_to_bits(number):
    if number:
        bits = []
        while number:
            number, remainder = divmod(number, 2)
            bits.insert(0, remainder)
        return bits
    else:
        return [0]


number_to_bits(6)
