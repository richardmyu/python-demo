# !/usr/bin/env python
# coding= utf-8
"""
@Project         : yxtj1
@File            : boq-clt.py
@Author          : yum <richardminyu@foxmail.com>
@Date            : 2025/02/08 12:37
@Description     : 对清单进行同类项合并
"""
# TODO:Completed
import pandas as pd
import datetime
import sys


def main(f1, f2):
    df_1 = pd.read_excel(f1)
    df_2 = pd.read_excel(f2)

    # 根据具体比对内容修改
    mg = pd.merge_ordered(df_1, df_2, on=["项目名称", "项目特征描述", "单位", "单价"])
    nt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    mg.to_excel(f"{f1}-{f2}-{str(nt)}.xlsx")
    print("SUCCESS!")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Error: 请输入正确的参数：py file.py file1.xlsx file2.xlsx")
    else:
        # print(sys.argv[1], sys.argv[2])
        main(sys.argv[1], sys.argv[2])

