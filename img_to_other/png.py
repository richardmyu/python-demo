# -*- coding=utf-8 -*-

"""
将静态图片（png, jpg）转换成字符图（png）
"""

import os
import PIL
from PIL import Image, ImageDraw, ImageFont
import argparse
import datetime
import time

# 命令行输入参数处理
parser = argparse.ArgumentParser()
parser.add_argument('file')  # 输入文件

# 获取参数
args = parser.parse_args()
IMG = args.file
s = ''.join(args.file.split('\\')[-1:]) if args.file.find('\\') else args.file
img_name = ''.join(s.split('.')[0])
OUTPUT_DEFAULT = './output_files/' + img_name + '.txt'
ascii_char = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '


def get_char(r, g, b, alpha=255):
    """将 256 灰度映射到字符上"""
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2116 * r + 0.7152 * g + 0.0722 * b)

    unit = (256 + 1) / length
    return ascii_char[int(gray / unit)]


def img2ascii(img, is_gray=False, scale=1, fineness=0.8):
    """将图片处理成字符画
    :param img: 图像
    :param is_gray: 是否灰度模式（True: 灰度模式；False: 彩色模式）
    :param scale: 输出字符图放缩比例，有效值 [0.5, 4]
    :param fineness: 输出字符图字符颗粒放缩比，有效值 [0.3, 1.2]
    """
    print('--- do img2ascii ---')
    # 将图片转换为 RGB 模式
    try:
        im = Image.open(img).convert('RGBA')
    except FileNotFoundError as e:
        print('FileNotFoundError: {}'.format(e))
        print('File: {} line: {}'.format(e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))
        return
    except PIL.UnidentifiedImageError as e:
        print('PIL.UnidentifiedImageError: {}'.format(e))
        print('File: {} line: {}'.format(e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))
        return
    except ValueError as e:
        print('ValueError: {}'.format(e))
        print('File: {} line: {}'.format(e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))
        return

    # 设定处理后的字符画大小
    if 0.5 <= scale <= 4:
        raw_width = int(im.width * scale)
        raw_height = int(im.height * scale)
    else:
        raw_width = int(im.width * 1)
        raw_height = int(im.height * 1)

    # 获取设定的字体的尺寸
    font = ImageFont.truetype('arial.ttf', 16)
    font_x, font_y = font.getsize(' ')

    # 确定单元的大小
    if 0.3 <= fineness <= 1.2:
        block_x = int(font_x * fineness)
        block_y = int(font_y * fineness)
    else:
        block_x = int(font_x * 0.8)
        block_y = int(font_y * 0.8)

    # 确定长宽各有几个单元
    w = int(raw_width / block_x)
    h = int(raw_height / block_y)

    # 将每个单元缩小为一个像素
    im = im.resize((w, h), Image.NEAREST)

    # txt 和 colors 分别存储对应块的 ASCII 字符和 RGB 值
    txt = []
    colors = []

    for i in range(h):
        line = ''
        line_color = []
        for j in range(w):
            pixel = im.getpixel((j, i))
            line_color.append(pixel)
            line += get_char(*pixel)
        txt.append(line)
        colors.append(line_color)

    # new(mode, size, color=0): 创建具有给定模式和大小的新图像
    img_txt = Image.new('RGBA', (raw_width, raw_height), (255, 255, 255, 255))

    # ImageDraw.Draw(im, mode=None): 创建可用于绘制给定图像的对象
    draw = ImageDraw.Draw(img_txt)
    for j in range(len(txt)):
        for i in range(len(txt[0])):
            if is_gray:
                # ImageDraw.text(xy, text, fill=None): 在给定位置绘制字符串
                draw.text((i * block_x, j * block_y), txt[j][i], (119, 136, 153, 255))
            else:
                draw.text((i * block_x, j * block_y), txt[j][i], colors[j][i])
    os.chdir(r'.\img')
    img_txt.save(img_name + '_' + str(int(time.time())) + '_ascii.png')
    print('--- done ---')


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    # img2ascii(IMG, True, 2, 0.6)
    img2ascii(IMG, False, 2, 0.6)
    end_time = datetime.datetime.now()
    print('spend time: {}'.format(end_time - start_time))
