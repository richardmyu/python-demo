# -*- coding: utf-8 -*-

import time


def bar(scale):
    print('===========执行开始============')
    for i in range(scale + 1):
        a = '*' * i
        b = '.' * (scale - i)
        c = (i / scale) * 100
        print('\r{:^3.0f}%[{}->{}]'.format(c, a, b), end='')
        time.sleep(0.05)
    print('\n===========执行结束============')


bar(50)


def pro_bar(scale):
    print('执行开始'.center(scale // 2, '='))
    start = time.perf_counter()
    for i in range(scale + 1):
        a = '*' * i
        b = '.' * (scale - i)
        c = (i / scale) * 100
        dur = time.perf_counter() - start
        print('\r{:^3.0f}%[{}->{}] {:.2f}s'.format(c, a, b, dur), end='')
        time.sleep(0.05)
    print('\n' + '执行结束'.center(scale // 2, '='))


pro_bar(50)
