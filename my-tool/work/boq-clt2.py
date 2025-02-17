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


def main():
    # # 逐个合并，效果较差
    df_1 = pd.read_excel("./YXTJ-1-01.xlsx")
    df_2 = pd.read_excel("./YXTJ-1-02.xlsx")
    df_3 = pd.read_excel("./YXTJ-1-03.xlsx")
    df_4 = pd.read_excel("./YXTJ-1-04.xlsx")
    df_5 = pd.read_excel("./YXTJ-1-05.xlsx")
    df_6 = pd.read_excel("./YXTJ-1-06.xlsx")
    df_7 = pd.read_excel("./YXTJ-1-07.xlsx")
    df_8 = pd.read_excel("./YXTJ-1-08.xlsx")
    # print(df_1)

    mg_1 = pd.merge_ordered(df_1, df_2, on=["项目名称", "项目特征描述", "计量单位"])
    mg_2 = pd.merge_ordered(mg_1, df_3, on=["项目名称", "项目特征描述", "计量单位"])
    mg_3 = pd.merge_ordered(mg_2, df_4, on=["项目名称", "项目特征描述", "计量单位"])
    mg_4 = pd.merge_ordered(mg_3, df_5, on=["项目名称", "项目特征描述", "计量单位"])
    mg_5 = pd.merge_ordered(mg_4, df_6, on=["项目名称", "项目特征描述", "计量单位"])
    mg_6 = pd.merge_ordered(mg_5, df_7, on=["项目名称", "项目特征描述", "计量单位"])
    mg = pd.merge_ordered(mg_6, df_8, on=["项目名称", "项目特征描述", "计量单位"])

    nt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    mg.to_excel(f"合并_{str(nt)}.xlsx")
    print("SUCCESS!")


# def main():
#     # 分裂合并，重合合并，效果极差
#     df_1 = pd.read_excel("./YXTJ-1-01.xlsx")
#     df_2 = pd.read_excel("./YXTJ-1-02.xlsx")
#     df_3 = pd.read_excel("./YXTJ-1-03.xlsx")
#     df_4 = pd.read_excel("./YXTJ-1-04.xlsx")
#     df_5 = pd.read_excel("./YXTJ-1-05.xlsx")
#     df_6 = pd.read_excel("./YXTJ-1-06.xlsx")
#     df_7 = pd.read_excel("./YXTJ-1-07.xlsx")
#     df_8 = pd.read_excel("./YXTJ-1-08.xlsx")
#     # print(df_1)
#
#     mg_1 = pd.merge_ordered(df_1, df_2, on=["项目名称", "项目特征描述", "计量单位"])
#     mg_2 = pd.merge_ordered(df_1, df_3, on=["项目名称", "项目特征描述", "计量单位"])
#     mg_3 = pd.merge_ordered(df_1, df_4, on=["项目名称", "项目特征描述", "计量单位"])
#     mg_4 = pd.merge_ordered(df_1, df_5, on=["项目名称", "项目特征描述", "计量单位"])
#     mg_5 = pd.merge_ordered(df_1, df_6, on=["项目名称", "项目特征描述", "计量单位"])
#     mg_6 = pd.merge_ordered(df_1, df_7, on=["项目名称", "项目特征描述", "计量单位"])
#     mg_7 = pd.merge_ordered(df_1, df_8, on=["项目名称", "项目特征描述", "计量单位"])
#
#     mg_1_2 = pd.merge_ordered(mg_1, mg_2, on=["项目名称", "项目特征描述", "计量单位"])
#     mg_3_4 = pd.merge_ordered(mg_3, mg_4, on=["项目名称", "项目特征描述", "计量单位"])
#     mg_5_6 = pd.merge_ordered(mg_5, mg_6, on=["项目名称", "项目特征描述", "计量单位"])
#
#     mg_12_34 = pd.merge_ordered(mg_1_2, mg_3_4, on=["项目名称", "项目特征描述", "计量单位"])
#     mg_56_7 = pd.merge_ordered(mg_5_6, mg_7, on=["项目名称", "项目特征描述", "计量单位"])
#
#     mg = pd.merge_ordered(mg_12_34, mg_56_7, on=["项目名称", "项目特征描述", "计量单位"])
#
#     nt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
#     mg.to_excel(f"合并_{str(nt)}.xlsx")
#     print("SUCCESS!")


if __name__ == '__main__':
    main()
