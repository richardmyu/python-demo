# -*- coding: utf-8 -*-

"""
将动态图片(gif)转换成字符图(gif)

基本思路:
    1.将 gif 图片的每一帧拆分为静态图片；
    2.将所有静态图片转换为字符图；
    3.再将所有字符图合成新 gif 图片
"""

import PIL
from PIL import Image, ImageDraw, ImageFont
import argparse
import os
import imageio

# 命令行输入参数处理
parser = argparse.ArgumentParser()
parser.add_argument('file')  # 输入文件

# 获取参数
args = parser.parse_args()
img = args.file
s = ''.join(args.file.split('\\')[-1:]) if args.file.find('\\') else args.file
img_name = ''.join(s.split('.')[0])

ascii_char = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
tmp_path = ''


def gif2pic(gif_file, is_gray=False, scale=1, fineness=0.8):
    """拆分 gif 将每一帧处理成字符画
    :param gif_file: gif 文件
    :param is_gray: 是否灰度模式(True: 灰度模式；False: 彩色模式)
    :param scale: 输出字符图放缩比例，有效值 [0.5, 4]
    :param fineness: 输出字符图字符颗粒放缩比，有效值 [0.3, 1.2](适当地调小颗粒，使得字符图更具体，更迫近原图)
    """
    print('--- do gif2pic ---')
    im = Image.open(gif_file)

    # 返回当前工作目录
    concurrent_path = os.getcwd()
    global tmp_path
    tmp_path = concurrent_path + r'\tmp_' + img_name

    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)
        # 改变当前工作目录到指定的路径
        os.chdir(tmp_path)
    else:
        os.chdir(tmp_path)
        # 清空 tmp 目录下内容
        for f in os.listdir(tmp_path):
            os.remove(f)

    while True:
        # tell(): 返回当前帧号
        current = im.tell()
        total = im.n_frames
        name = 'tmp_' + img_name + '_' + str(current) + '.png'
        # 保存每一帧图片
        im.save(name)
        # 将每一帧处理为字符画
        img2ascii(name, is_gray, scale, fineness)
        # 继续处理下一帧
        if current >= (total - 1):
            break
        im.seek(current + 1)


def get_char(r, g, b, alpha=255):
    """将 256 灰度映射到字符上"""
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2116 * r + 0.7152 * g + 0.0722 * b)
    unit = (256 + 1) / length
    return ascii_char[int(gray / unit)]


def img2ascii(png_img, is_gray, scale, fineness):
    """将单幅 png 图片处理成字符画
    :param png_img: 要处理的图片
    :param is_gray: 是否灰度模式
    :param scale: 输出字符图放缩比例
    :param fineness: 输出字符图字符颗粒放缩比
    """
    print('--- do img2ascii ---')
    # 将图片转换为 RGB 模式
    try:
        im = Image.open(png_img).convert('RGBA')
    except FileNotFoundError as e:
        print('FileNotFoundError: {}'.format(e))
        print('File: {} line: {}'.format(
            e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))
        return
    except PIL.UnidentifiedImageError as e:
        print('PIL.UnidentifiedImageError: {}'.format(e))
        print('File: {} line: {}'.format(
            e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))
        return
    except ValueError as e:
        print('ValueError: {}'.format(e))
        print('File: {} line: {}'.format(
            e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))
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
    if 0.3 <= fineness <= 1:
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
    img_txt = Image.new('RGB', (raw_width, raw_height), (255, 255, 255, 255))

    # ImageDraw.Draw(im, mode=None): 创建可用于绘制给定图像的对象
    draw = ImageDraw.Draw(img_txt)
    for j in range(len(txt)):
        for i in range(len(txt[0])):
            if is_gray:
                # ImageDraw.text(xy, text, fill=None): 在给定位置绘制字符串
                draw.text((i * block_x, j * block_y),
                          txt[j][i], (119, 136, 153, 255))
            else:
                draw.text((i * block_x, j * block_y), txt[j][i], colors[j][i])

    img_txt.save(png_img, 'PNG')


def pic2gif(out_name='', duration=1):
    """ 读取 tmp 目录下文件合成 gif
    :param out_name: 合成图片名称
    :param duration: gif 图像间隔时间
    """
    print('--- do pic2gif ---')
    try:
        # global tmp_path
        os.chdir(tmp_path)
    except FileNotFoundError as e:
        print('FileNotFoundError: {}'.format(e))
        print('File: {} line: {}'.format(
            e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))
        return

    # 返回 path 指定的文件夹包含的文件或文件夹的名字的列表
    dirs = os.listdir()  # 没有参数，默认当前工作目录
    images = []
    for d in dirs:
        # imageio.imread(uri, format=None, **kwargs): 从指定的 uri 读取图像
        images.append(imageio.imread(d))

    # Aliases mimsave = mimwrite
    name = out_name if len(out_name) > 0 else img_name
    imageio.mimsave(name + '_ascii.gif', images, 'GIF', duration=duration)
    print('--- done ---')


if __name__ == '__main__':
    gif2pic(img)
    pic2gif()
