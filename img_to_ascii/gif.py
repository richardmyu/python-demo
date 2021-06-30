# -*- coding: utf-8 -*-

"""
基本思路：
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
if args.file.find('\\'):
    s = ''.join(args.file.split('\\')[-1:])
else:
    s = args.file
img_name = ''.join(s.split('.')[0])

ascii_char = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
tmp_path = ''


def gif2pic(gif_file, is_gray=False):
    """拆分 gif 将每一帧处理成字符画
    gif_file: gif 文件
    is_gray: 是否灰度模式（True: 灰度模式；False: 彩色模式）
    """
    print('--- do gif2pic ---')
    im = Image.open(gif_file)

    # 返回当前工作目录
    concurrent_path = os.getcwd()
    global tmp_path
    tmp_path = concurrent_path + '/tmp_' + img_name
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)
    else:
        # 清空 tmp 目录下内容
        for f in os.listdir(tmp_path):
            os.remove(f)
    # 改变当前工作目录到指定的路径
    os.chdir(tmp_path)
    try:
        while True:
            # tell(): 返回当前帧号
            current = im.tell()
            total = im.n_frames
            if current >= (total - 1):
                break
            name = 'tmp_' + img_name + '_' + str(current) + '.png'
            # 保存每一帧图片
            im.save(name)
            # 将每一帧处理为字符画
            img2ascii(name, is_gray)
            # 继续处理下一帧
            im.seek(current + 1)
    except EOFError as e:
        # 如果调用试图在序列结束后查找
        print('EOFError', e)
        print(e.__traceback__.tb_frame.f_globals['__file__'])
        print(e.__traceback__.tb_lineno)
        return
    except Exception as e:
        print('Error', e)
        print(e.__traceback__.tb_frame.f_globals['__file__'])
        print(e.__traceback__.tb_lineno)
        return
    os.chdir(concurrent_path)


def get_char(r, g, b):
    """将 256 灰度映射到 70 个字符上"""
    length = len(ascii_char)
    gray = int(0.2116 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1) / length
    return ascii_char[int(gray / unit)]


def img2ascii(png_img, is_gray, scale=1.6, fineness=0.6):
    """将图片处理成字符画
    :param png_img: 要处理的图片
    :param is_gray: 是否灰度模式
    :param scale: 输出字符图放缩比例
    :param fineness: 输出字符图字符颗粒放缩比（适当地调小颗粒，使得字符图更具体，更迫近原图）
    """
    print('--- do img2ascii ---')
    # 将图片转换为 RGB 模式
    try:
        im = Image.open(png_img).convert('RGB')
    except FileNotFoundError as e:
        print('FileNotFoundError: {}'.format(e))
        print(e.__traceback__.tb_frame.f_globals['__file__'])
        print(e.__traceback__.tb_lineno)
        return
    except PIL.UnidentifiedImageError as e:
        print('PIL.UnidentifiedImageError: {}'.format(e))
        print(e.__traceback__.tb_frame.f_globals['__file__'])
        print(e.__traceback__.tb_lineno)
        return
    except ValueError as e:
        print('ValueError: {}'.format(e))
        print(e.__traceback__.tb_frame.f_globals['__file__'])
        print(e.__traceback__.tb_lineno)
        return

    # 设定处理后的字符画大小
    raw_width = int(im.width * scale)
    raw_height = int(im.height * scale)

    # 获取设定的字体的尺寸
    font = ImageFont.truetype('arial.ttf', 16)
    font_x, font_y = font.getsize(' ')

    # 确定单元的大小
    block_x = int(font_x * fineness)
    block_y = int(font_y * fineness)

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

    img_txt.save(img, 'PNG')


def pic2gif(out_name='chara', duration=1):
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
        print(e.__traceback__.tb_frame.f_globals['__file__'])
        print(e.__traceback__.tb_lineno)
        return

    # 返回 path 指定的文件夹包含的文件或文件夹的名字的列表
    dirs = os.listdir()  # 没有参数，默认当前工作目录
    images = []
    for d in dirs:
        # imageio.imread(uri, format=None, **kwargs): 从指定的 uri 读取图像
        images.append(imageio.imread(d))

    # Aliases mimsave = mimwrite
    imageio.mimsave(out_name + '_ascii.gif', images, 'GIF', duration=duration)
    print('--- done ---')


if __name__ == '__main__':
    gif2pic(img)
    pic2gif()
