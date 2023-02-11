"""
https://www.runoob.com/matplotlib/matplotlib-marker.html
"""

import matplotlib.pyplot as plt
import numpy as np

y = np.array([1, 3, 4, 5, 8, 9, 6, 1, 3, 4, 5, 2, 4])

plt.plot(y, marker='o')
# plt.plot(y, 'o-')
plt.show()
