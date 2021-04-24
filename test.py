# -*- coding: utf-8 -*-

class A(object):
    def __init__(self, x):
        self.x = x

    def hello(self):
        return 'hello func'

    def __getattr__(self, item):
        print('in __getattr__')
        return 100

    def __getattribute__(self, item):
        print('in __getattribute__', item)
        return super(A, self).__getattribute__(item)


a = A(10)
print(a.x)
print(a.y)
print(a.z)
