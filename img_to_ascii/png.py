# -*- coding=utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import argparse

# 命令行输入参数处理
parser = argparse.ArgumentParser()

parser.add_argument('file')  # 输入文件
parser.add_argument('-o', '--output')  # 输出文件

# 获取参数
args = parser.parse_args()

IMG = args.file
OUTPUT = args.output

if args.file.find('\\'):
    IMG_NAME_ALL = ''.join(args.file.split('\\')[-1:])
else:
    IMG_NAME_ALL = args.file

IMG_NAME = ''.join(IMG_NAME_ALL.split('.')[0])

OUTPUT_DEFAULT = './output_files/' + IMG_NAME + '.txt'

# 当只有一个字符串的时候：
# tuple    ("abc",)
# string   ("abc")
ascii_char = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '


def get_char(r, g, b, alpha=256):
    """将 256 灰度映射到 70 个字符上"""
    # alpha 值为 0 的时候表示图片中该位置为空白
    if alpha == 0:
        return ' '
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

if __name__ == '__main__':

    # 将字符画输出到文件
    if OUTPUT:
        with open(OUTPUT, 'w') as f:
            f.write(txt)
    else:
        with open(OUTPUT_DEFAULT, 'w') as f:
            f.write(txt)
