# -*- coding: utf-8 -*-
"""
https://www.runoob.com/matplotlib/matplotlib-grid.html
matplotlib.pyplot.grid(b=None, which='major', axis='both', )
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axis import Axis

x = np.array([1, 2, 3, 4])
y = np.array([1, 4, 9, 16])


plt.title("grid - Test")
plt.xlabel("x - label")
plt.ylabel("y - label")

plt.subplot(2, 2, 1)
plt.plot(x, y)
plt.grid()

plt.subplot(2, 2, 2)
plt.plot(x, y)
plt.grid(axis='x')

plt.subplot(2, 2, 3)
plt.plot(x, y)
plt.grid(color='r')

plt.subplot(2, 2, 4)
plt.plot(x, y)
plt.grid(color='r', linestyle='--', linewidth=0.5)

plt.show()
