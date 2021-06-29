# -*- coding: utf-8 -*-

"""
基本思路：
  1.将 gif 图片的每一帧拆分为静态图片；
  2.将所有静态图片转换为字符图；
  3.再将所有字符图合成新 gif 图片
"""

from PIL import Image, ImageDraw, ImageFont
import argparse
import os
import imageio

# 命令行输入参数处理
parser = argparse.ArgumentParser()
parser.add_argument('file')  # 输入文件

# 获取参数
args = parser.parse_args()
IMG = args.file

if args.file.find('\\'):
    IMG_NAME_ALL = ''.join(args.file.split('\\')[-1:])
else:
    IMG_NAME_ALL = args.file

IMG_NAME = ''.join(IMG_NAME_ALL.split('.')[0])

ascii_char = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '


def gif2pic(file, is_gray=False):
    """拆分 gif 将每一帧处理成字符画
    file: gif 文件
    is_gray: 是否黑白
    font: ImageFont
    """
    print('--- do gif2pic ---')
    im = Image.open(file)

    # 返回当前工作目录
    path = os.getcwd()
    tmp_path = path + '/tmp'
    # 改变当前工作目录到指定的路径
    os.chdir(tmp_path)
    # print('gif2pic--111', path)
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)
    else:
        # 清空 tmp 目录下内容
        for f in os.listdir(tmp_path):
            os.remove(f)

    try:
        while True:
            # tell(): 返回当前帧号
            current = im.tell()
            total = im.n_frames
            if current >= (total - 1):
                break
            name = IMG_NAME + '_tmp_' + str(current) + '.png'
            # 保存每一帧图片
            im.save(name)
            # 将每一帧处理为字符画
            img2ascii(name, is_gray)
            # 继续处理下一帧
            im.seek(current + 1)
    except EOFError as e:
        # 如果调用试图在序列结束后查找
        print('EOFError', e)
    except Exception as e:
        print('Error', e)
    finally:
        os.chdir(path)


def get_char(r, g, b):
    """将 256 灰度映射到 70 个字符上"""
    length = len(ascii_char)
    gray = int(0.2116 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1) / length
    return ascii_char[int(gray / unit)]


def img2ascii(img, is_gray, scale=0.8):
    """将图片处理成字符画"""
    print('--- do img2ascii ---')
    # 将图片转换为 RGB 模式
    im = Image.open(img).convert('RGB')

    # 设定处理后的字符画大小
    raw_width = int(im.width)
    raw_height = int(im.height)

    # 获取设定的字体的尺寸
    font = ImageFont.truetype('arial.ttf', 16)
    font_x, font_y = font.getsize(' ')

    # 确定单元的大小
    block_x = int(font_x * scale)
    block_y = int(font_y * scale)

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
            line_color.append((pixel[0], pixel[1], pixel[2]))
            line += get_char(pixel[0], pixel[1], pixel[2])
        txt.append(line)
        colors.append(line_color)

    # new(mode, size, color=0): 创建具有给定模式和大小的新图像
    img_txt = Image.new('RGB', (raw_width, raw_height), (255, 255, 255))

    # ImageDraw.Draw(im, mode=None): 创建可用于绘制给定图像的对象
    draw = ImageDraw.Draw(img_txt)
    for j in range(len(txt)):
        for i in range(len(txt[0])):
            if is_gray:
                # ImageDraw.text(xy, text, fill=None): 在给定位置绘制字符串
                draw.text((i * block_x, j * block_y), txt[j][i], (119, 136, 153))
            else:
                draw.text((i * block_x, j * block_y), txt[j][i], colors[j][i])

    img_txt.save(img)


def pic2gif(out_name='chara', duration=1):
    """读取 tmp 目录下文件合成 gif"""
    print('--- do pic2gif ---')
    os.chdir('./tmp')

    # 返回 path 指定的文件夹包含的文件或文件夹的名字的列表
    # 没有参数，默认当前工作目录
    dirs = os.listdir()
    images = []
    for d in dirs:
        # imageio.imread(uri, format=None, **kwargs): 从指定的 uri 读取图像
        images.append(imageio.imread(d))

    imageio.mimsave(out_name + '_ascii.gif', images, duration=duration)
    print('--- done ---')


if __name__ == '__main__':
    gif2pic(IMG)
    pic2gif()
