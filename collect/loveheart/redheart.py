# -*- coding: utf-8 -*-

"""
作者：李狗嗨
链接：https://www.zhihu.com/question/466165757/answer/1954034386
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""

import numpy as np
from skimage import measure
import matplotlib.pyplot as plt


def fun(x, y, z):
    return (x ** 2 + (9 / 4) * y ** 2 + z ** 2 - 1) ** 3 - x ** 2 * z ** 3 - (1 / 9) * y ** 2 * z ** 3


x, y, z = np.mgrid[-2:2:100j, -2:2:100j, -2:2:100j]
vol = fun(x, y, z)
iso_val = 0.0
verts, faces, _, _ = measure.marching_cubes(vol, iso_val, spacing=(0.1, 0.1, 0.1))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], color='red')
ax.view_init(25, -110)
plt.show()
