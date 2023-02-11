# -*- coding: utf-8 -*-

"""3维红心"""

import numpy as np
from skimage import measure
import matplotlib.pyplot as plt


def heart_line(x, y, z):
    return (
        (x**2 + (9 / 4) * y**2 + z**2 - 1) ** 3
        - x**2 * z**3
        - (1 / 9) * y**2 * z**3
    )


a, b, c = np.mgrid[-2:2:100j, -2:2:100j, -2:2:100j]
vol = heart_line(a, b, c)
iso_val = 0.0
vert, face, _, _ = measure.marching_cubes(vol, iso_val, spacing=(0.1, 0.1, 0.1))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(vert[:, 0], vert[:, 1], face, vert[:, 2], color='red')
ax.view_init(25, -110)
plt.savefig('redheart.png')
plt.show()
