# -*- coding: utf-8 -*-

"""
https://www.runoob.com/matplotlib/matplotlib-pie.html
"""

import matplotlib.pyplot as plt
import numpy as np

y = np.array([35, 25, 25, 15])

plt.subplot(1, 3, 1)
plt.pie(y)

plt.subplot(1, 3, 2)
plt.pie(
    y,
    labels=['A', 'B', 'C', 'D'],  # 设置饼图标签
    colors=["#d5695d", "#5d8ca8", "#65a479", "#a564c9"],  # 设置饼图颜色
)

plt.subplot(1, 3, 3)
plt.pie(
    y,
    labels=['A', 'B', 'C', 'D'],  # 设置饼图标签
    colors=["#d5695d", "#5d8ca8", "#65a479", "#a564c9"],  # 设置饼图颜色
    explode=(0.2, 0, 0, 0),  # 第二部分突出显示，值越大，距离中心越远
    autopct='%.2f%%',  # 格式化输出百分比
)

plt.show()
