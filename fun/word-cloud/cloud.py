# -*- coding: utf-8 -*-
"""
生成指定名称词云。
词云形状由指定背景图决定。

https://pythondict.com/life-intelligent/tools/python-happy-birthday/

command
    ./ll_env/Scripts/activate

    py happy.py image new_image_name
"""

import multidict
import fire
import matplotlib.pyplot as plt
import numpy.random as nr
from imageio import imread
from wordcloud import WordCloud, ImageColorGenerator

# Doraemon
# Nobita

# sub_title_start = '哆啦'
# sub_title_end = 'A梦'

sub_title_start = '3.14'
sub_title_end = '3.14159'


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
    word_cloud = ImageColorGenerator(bimg)

    # 渲染
    plt.figure(figsize=(6, 6))
    plt.axis('off')
    plt.imshow(wordcloud.recolor(color_func=word_cloud))
    plt.savefig(name + '.png')
    plt.show()


fire.Fire(gen_happy_birthday_cloud)
