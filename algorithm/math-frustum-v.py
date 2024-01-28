"""
计算圆台体积去除中间圆柱后的体积
"""

import math

def frustum_v(a, d, h):
    r1 = d / 2  # 上底
    r2 = a + d / 2  # 下底
    ss = math.pow(r1, 2) + r1 * r2 + math.pow(r2, 2)
    v1 = math.pi * ss * h / 3

    # 以上底为底的圆柱体积
    v2 = math.pi * math.pow(r1, 2) * h

    # 单位换到 m^3，保留三位小数
    rm = round((v1 - v2) / 1000000, 3)

    return rm


# 特例
def frustum_vII(a):
    d = 100
    h = 2 * a
    return frustum_v(a, d, h)


print(f'WZ1 V is (a=20, d=100, hc=40) m*3 {frustum_vII(20)}')
print(f'WZ2 V is (a=30, d=100, hc=60) m*3 {frustum_vII(30)}')
print(f'WZ3 V is (a=40, d=100, hc=80) m*3 {frustum_vII(40)}')
print(f'WZ4 V is (a=50, d=100, hc=100) m*3 {frustum_vII(50)}')
print(f'WZ5 V is (a=60, d=100, hc=120) m*3 {frustum_vII(60)}')
