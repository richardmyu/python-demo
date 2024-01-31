"""
https://www.runoob.com/matplotlib/matplotlib-line.html
"""

import matplotlib.pyplot as plt
import numpy as np

y = np.array([6, 2, 13, 10])
plt.plot(y, linestyle='dotted')
# plt.plot(y, ls='-.')
plt.show()
