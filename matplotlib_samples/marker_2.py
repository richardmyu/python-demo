"""
fmt = '[marker][line][color]'
"""

import matplotlib.pyplot as plt
import numpy as np

y = np.array([6, 2, 13, 10])

plt.plot(y, 'o:r')
plt.show()
