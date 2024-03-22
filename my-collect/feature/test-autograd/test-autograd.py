# -*- config: utf-8 -*-
"""
AutoGrad 学习

https://pythondict.com/ai/machine-learning/autograd/
"""


import autograd.numpy as np
from autograd import grad
import matplotlib.pyplot as plt
from autograd import elementwise_grad as egrad


def _tanh(x):
    y = np.exp(-2.0 * x)
    return (1.0 - y) / (1.0 + y)


grad_tanh = grad(_tanh)
x = np.linspace(-7, 7, 200)
plt.plot(x, _tanh(x), x, egrad(_tanh)(x))
plt.show()
