import matplotlib.pyplot as plt
import numpy as np

y1 = np.array([3, 7, 5, 9])
y2 = np.array([6, 2, 13, 10])
plt.plot(y1, linestyle='dotted', linewidth='3')
plt.plot(y2, ls='-.', c='r')
plt.show()
