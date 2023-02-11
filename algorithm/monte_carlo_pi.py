"""蒙特·卡罗方法来计算圆周率

   [来源]:不明
"""

from random import random
from time import perf_counter


def calculate_pi(n=100):
    print('\n n {}'.format(n))
    hits = 0
    start = perf_counter()
    for i in range(1, n * n + 1):
        x, y = random(), random()
        dist = pow(x**2 + y**2, 0.5)
        if dist <= 1.0:
            hits += 1
    pi = (hits * 4) / (n * n)
    used_time = perf_counter() - start
    return pi, used_time


PI, used_time = calculate_pi(6000)
print('\nuse Monte Carlo method to calculate PI: {}'.format(PI))
print('use time: {} s'.format(used_time))
