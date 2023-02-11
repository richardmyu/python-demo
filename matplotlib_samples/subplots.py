"""
https://www.runoob.com/matplotlib/matplotlib-subplots.html
"""

import matplotlib.pyplot as plt
import numpy as np

# 创建一些测试数据
x = np.linspace(0, 2 * np.pi, 400)
y = np.sin(x**2)

# 创建一个画像和子图 -- 图1
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title('Simple plot')

# 创建两个子图 -- 图2
f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
ax1.plot(x, y)
ax1.set_title('Sharing Y axis')
ax2.scatter(x, y)

# 创建四个子图 -- 图3
fig, axs = plt.subplots(2, 2, subplot_kw=dict(projection="polar"))
axs[0, 0].plot(x, y)
axs[1, 1].scatter(x, y)
axs[0, 1].set_title('polar')

# 共享 x 轴 -- 图4
plt.subplots(2, 2, num=4, sharex='col')

# 共享 y 轴 -- 图5
plt.subplots(2, 2, num=5, sharey='row')

# 共享 x 轴和 y 轴 -- 图6
plt.subplots(2, 2, num=6, sharex='all', sharey='all')

# 这个也是共享 x 轴和 y 轴 -- 图7
plt.subplots(2, 2, num=7, sharex=True, sharey=True)

# 创建标识为 10 的图，已经存在的则删除 -- 图10
fig, ax = plt.subplots(num=10, clear=True)

plt.show()
