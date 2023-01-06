# -*- coding: utf-8 -*-
"""
生成指定名称的生日快乐词云。词云形状由指定背景图决定。

source:
    Python 一键生成漂亮的生日快乐词云！
    https://pythondict.com/life-intelligent/tools/python-happy-birthday/

command
    py happy.py image name
"""
import multidict
import fire
import matplotlib.pyplot as plt
import numpy.random as nr
from imageio import imread
from wordcloud import WordCloud, ImageColorGenerator

sub_title_start = '哆啦'
sub_title_end = 'A梦'


def transform_format(val):
    """
    用于去除杂色

    Args:
        val (list): RGB

    Returns:
        list: 去除杂色后的 RGB
    """
    if val[0] > 245 and val[1] > 245 and val[2] > 245:
        val[0] = val[1] = val[2] = 255
        return val
    else:
        return val


def gen_happy_birthday_cloud(file, name):
    """
    生成词云

    Args:
        file (str): 词云背景图
        name (str):
    """
    words = multidict.MultiDict()

    # 先初始化两个最大权重
    words.add(sub_title_start + sub_title_end, 10)
    words.add(name, 12)

    # 随意插入新词语
    for i in range(1000):
        words.add(sub_title_start, nr.randint(1, 5))
        words.add(sub_title_end, nr.randint(1, 5))
        words.add(name, nr.randint(1, 5))

    # 设定图片
    bimg = imread(file)
    for color in range(len(bimg)):
        bimg[color] = list(map(transform_format, bimg[color]))

    wordcloud = WordCloud(
        background_color='white', mask=bimg, font_path='simhei.ttf'
    ).generate_from_frequencies(words)

    # 生成词云
    bimgColors = ImageColorGenerator(bimg)

    # 渲染
    plt.axis('off')
    plt.imshow(wordcloud.recolor(color_func=bimgColors))
    plt.savefig(name + '.png')
    plt.show()


fire.Fire(gen_happy_birthday_cloud)
