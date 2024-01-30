# -*- config: utf-8 -*-
"""
使用 Autograd 实现回归模型

https://pythondict.com/ai/machine-learning/autograd/
"""


import autograd.numpy as np
from autograd import grad

#
inputs = np.array(
    [[0.52, 1.12, 0.77], [0.88, -1.08, 0.15], [0.52, 0.06, -1.30], [0.74, -2.49, 1.39]]
)

targets = np.array([True, True, False, True])


def sigmoid(x):
    return 0.5 * (np.tanh(x / 2.0) + 1)


def logistic_predictions(weights, inputs):
    return sigmoid(np.dot(inputs, weights))


def training_loss(weights):
    preds = logistic_predictions(weights, inputs)
    label_probabilities = preds * targets + (1 - preds) * (1 - targets)
    return -np.sum(np.log(label_probabilities))


training_gradient_fun = grad(training_loss)

weights = np.array([0.0, 0.0, 0.0])
print("Initial loss: ", training_loss(weights))

for i in range(100):
    weights -= training_gradient_fun(weights) * 0.01

print("Trained loss: ", training_loss(weights))
