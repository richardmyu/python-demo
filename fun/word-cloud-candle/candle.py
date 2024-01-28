# -*- coding: utf-8 -*-
"""
绘制悼念的词云蜡烛

https://pythondict.com/python-data-analyze/python-paint-mourn-candle/
"""

import jieba
import numpy
import codecs
import pandas
from imageio import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator


def load_file_segment():
    # 加载我们自己的词典
    jieba.load_userdict("words.txt")

    # 读取文本文件并分词
    f = codecs.open(u"text.txt", 'r', encoding='utf-8')

    # 打开文件
    content = f.read()

    # 读取文件到content中
    f.close()

    # 关闭文件
    segment = []

    # 保存分词结果
    segs = jieba.cut(content)

    # 对整体进行分词
    for seg in segs:
        if len(seg) > 1 and seg != '\r\n':
            # 如果说分词得到的结果非单字，且不是换行符，则加入到数组中
            segment.append(seg)
    return segment


def get_words_count_dict():
    segment = load_file_segment()

    # 获得分词结果
    df = pandas.DataFrame({'segment': segment})

    # 将分词数组转化为pandas数据结构
    # words_count = df.groupby(by=['segment'])['segment'].agg({"计数": numpy.size})
    # https://stackoverflow.com/questions/60229375/solution-for-specificationerror-nested-renamer-is-not-supported-while-agg-alo
    words_count = df.groupby(by=['segment'])['segment'].agg(count=numpy.size)

    # 按词分组，计算每个词的个数
    words_count = words_count.reset_index().sort_values(by="count", ascending=False)

    # reset_index是为了保留segment字段，排序，数字大的在前面
    return words_count


words_count = get_words_count_dict()
# 获得词语和频数

# 获得词云对象，设定词云背景颜色及其图片和字体
bgimg = imread('candle.jpg')

# 读取我们想要生成词云的模板图片
wordcloud = WordCloud(background_color='white', mask=bgimg, font_path='simhei.ttf')

# 如果背景色是透明的，请用这条语句替换上面
# wordcloud = WordCloud(
#     background_color=None, mode='RGBA', mask=bgimg, font_path='simhei.ttf'
# )

words = words_count.set_index("segment").to_dict()

# 将词语和频率转为字典
wordcloud = wordcloud.fit_words(words["count"])

# 将词语及频率映射到词云对象上
bgimg_colors = ImageColorGenerator(bgimg)

# 设置画布大小
plt.figure(figsize=(6, 6))

# 生成颜色
plt.axis("off")

# 关闭坐标轴
plt.imshow(wordcloud.recolor(color_func=bgimg_colors))

plt.savefig('word-cloud-candle.png')

# 绘色
plt.show()
