# -*- coding: utf-8 -*-

"""
AutoGrad 学习

https://pythondict.com/ai/machine-learning/autograd/
"""


import autograd.numpy as np
from autograd import grad
import matplotlib.pyplot as plt
from autograd import elementwise_grad as egrad


def tanh(x):
    y = np.exp(-2.0 * x)
    return (1.0 - y) / (1.0 + y)


grad_tanh = grad(tanh)
x = np.linspace(-7, 7, 200)
plt.plot(x, tanh(x), x, egrad(tanh)(x))
plt.show()
