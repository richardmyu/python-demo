import matplotlib.pyplot as plt
import numpy as np


# -1.2071
x1 = np.arange(-1.25, -1.15, 0.001)
y1 = x1**21 - x1**11 - 20 * x1 + 20

plt.subplot(1, 2, 1)
plt.plot(x1, y1)
plt.title('(-1.3, -1.1)')
plt.grid()

# 1.0452
x2 = np.arange(1.0, 1.1, 0.001)
y2 = x1**21 - x1**11 - 20 * x1 + 20

plt.subplot(1, 2, 2)
plt.plot(x2, y2)
plt.title('(1.00, 1.10)')
plt.grid()

plt.suptitle('x**21 - x**11 - 20 * x + 20')
plt.show()
