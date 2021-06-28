# -*- coding: utf-8 -*-

# -*- coding=utf-8 -*-

from PIL import Image
import argparse

# 命令行输入参数处理
parser = argparse.ArgumentParser()

parser.add_argument('file')  # 输入文件
parser.add_argument('-o', '--output')  # 输出文件
parser.add_argument('--width', type=int, default=80)  # 默认输出字符宽
parser.add_argument('--height', type=int, default=40)  # 默认输出字符高

# 获取参数
args = parser.parse_args()

IMG = args.file
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output

if args.file.find("\\"):
    IMG_NAME = ''.join(args.file.split("\\")[-1:])
else:
    IMG_NAME = args.file

OUTPUT_DEFAULT = "./output_files/" + IMG_NAME + ".txt"

# 当只有一个字符串的时候：
# tuple    ("abc",)
# string   ("abc")
ascii_char = ("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


def gif2pic(file, ascii_chars, is_gray, font, scale):
    """
    file: gif 文件
    ascii_chars: 灰度值对应的字符串
    is_gray: 是否黑白
    font: ImageFont
    scale: 缩放比列
    """
    im = Image.open(file)
    try:
        while 1:
            concurrent = im.tell()
            im.save(IMG_NAME)
            img2ascii(IMG_NAME, ascii_chars, is_gray, font, scale)
    except:
        print('err')


def get_char(r, g, b, alpha=256):
    """将 256 灰度映射到 70 个字符上"""

    # alpha 值为 0 的时候表示图片中该位置为空白
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2116 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1) / length
    return ascii_char[int(gray / unit)]

def img2ascii(img,ascii_chars,is_gray,font,scale):
    """将图片处理成字符画"""
    im.Image.open(img)

if __name__ == '__main__':
    im = Image.open(IMG)
    im = im.resize((WIDTH, HEIGHT), Image.NEAREST)
    txt = ""
    colors = []

    for i in range(HEIGHT):
        for j in range(WIDTH):
            # 获取得到坐标 (j, i) 位置的 RGB 像素值
            # * 元组展开
            pixel = im.getpixel((j, i))
            colors.append(*pixel)
            txt += get_char(*pixel)
        txt += '\n'

    # im.show()
    print(txt)

    # 将字符画输出到文件
    if OUTPUT:
        with open(OUTPUT, 'w') as f:
            f.write(txt)
    else:
        with open(OUTPUT_DEFAULT, "w") as f:
            f.write(txt)
