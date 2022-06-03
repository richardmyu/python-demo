# -*- coding: utf-8 -*-

import datetime
import logging

# case 1
# def log(func):
#     """
#     日志装饰器，简单记录函数的日志

#     Args:
#         func (function): 函数
#     """
#     def inner(*args):
#         timestamp = str(datetime.datetime.now()).split(".")[0]
#         res = func(*args)
#         print(f"[{timestamp}] ({func.__name__}) {args} -> {res}")
#         return res
#     return inner

# case 2
# def log(func):
#     """
#     日志装饰器，简单记录函数的日志

#     Args:
#         func (function): 函数
#     """
#     def inner(*args, **kwargs):
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         res = func(*args, **kwargs)
#         print(f"[{timestamp}] ({func.__name__}) {args} -> {res}")
#         return res
#     return inner

# case 3
# 获取日志记录器，配置日志等级
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

# 默认日志格式
format = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s")

# 输出到控制台的 handler
chlr = logging.StreamHandler()

# 配置默认日志格式
chlr.setFormatter(format)

# 日志记录器增加此 handler
logger.addHandler(chlr)


def log(func):
    """
    日志装饰器，简单记录函数的日志

    Args:
        func (function): 函数
    """
    def inner(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        res = func(*args, **kwargs)
        # print(f"[{timestamp}] ({func.__name__}) {args} -> {res}")
        logger.debug(f"func: {func.__name__} {args} -> {res}")
        return res
    return inner


@log
def pluser(a, b):
    return a+b


pluser(1, 2)
