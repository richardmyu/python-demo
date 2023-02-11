import numpy as np
from matplotlib import pyplot as plt
import matplotlib

font = matplotlib.font_manager.FontProperties(fname="SourceHanSansSC-Bold.otf")

x = np.arange(1, 11)
y = 2 * x + 5
plt.title("测试 - banana", fontproperties=font)

plt.xlabel("x 轴", fontproperties=font)
plt.ylabel("y 轴", fontproperties=font)
plt.plot(x, y)
plt.show()
