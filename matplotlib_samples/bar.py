# -*- coding: utf-8 -*-

"""
https://www.runoob.com/matplotlib/matplotlib-bar.html
"""

import matplotlib.pyplot as plt
import numpy as np

x = np.array(["class-1", "class-2", "class-3", "class-4"])
y = np.array([12, 22, 6, 18])

plt.subplot(2, 2, 1)
plt.bar(x, y)

# 垂直方向
plt.subplot(2, 2, 2)
plt.barh(x, y)

# 设置柱形图颜色
plt.subplot(2, 2, 3)
plt.bar(x, y, color=["#4CAF50", "red", "hotpink", "#556B2F"])

# 设置柱形图宽度
plt.subplot(2, 2, 4)
plt.bar(x, y, color="#4CAF50", width=0.1)

plt.show()
