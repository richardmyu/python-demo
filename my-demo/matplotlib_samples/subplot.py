"""
https://www.runoob.com/matplotlib/matplotlib-subplots.html

subplot(nrows, ncols, index, **kwargs)
"""

import matplotlib.pyplot as plt
import numpy as np

# plot 1:
point_x = np.array([0, 6])
point_y = np.array([0, 100])

plt.subplot(1, 2, 1)
plt.plot(point_x, point_y)
plt.title("plot 1")

# plot 2:
x = np.array([1, 2, 3, 4])
y = np.array([1, 4, 9, 16])

plt.subplot(1, 2, 2)
plt.plot(x, y)
plt.title("plot 2")

plt.suptitle("subplot - Test")
plt.show()
