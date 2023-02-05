# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 4 * np.pi, 0.1)
y = np.sin(x)
z = np.cos(x)

plt.plot(x, y, x, z, 'r')
plt.show()
