# -*- coding: utf-8 -*-

"""
压缩图片

命令:
    py compression-img -p img_path
"""

# TODO: 当前压缩率为 3，缺少对大图片的压缩后的大小判断和再次压缩

import os
import sys
import argparse
import cv2 as cv
from skimage import io

SOURCE_IMG = ''


def img_resize(img, scale=0.5, interpolation=cv.INTER_LINEAR):
    img = cv.resize(img, (int(
        img.shape[1]*scale), int(img.shape[0]*scale)), interpolation=interpolation)
    return img


def img_compression(path):
    # 读取图像
    # img = cv.imread(path)
    global SOURCE_IMG
    img = io.imread(SOURCE_IMG + path)

    # 针对 png 图像，删除 iCCP profiles 信息
    img = cv.cvtColor(img, cv.COLOR_RGBA2BGRA)
    cv.imencode('.png', img)[1].tofile(SOURCE_IMG + path)

    # 使用 resize, 进行缩放
    new_img = img_resize(img, interpolation=cv.INTER_AREA)

    # # 显示图像
    # cv.imshow('origin', img)
    # cv.imshow('new', new_img)

    OUTPUT_IMG = os.getcwd() + '/output/'

    if not os.path.exists(OUTPUT_IMG):
        os.mkdir(OUTPUT_IMG)

    cv.imwrite(OUTPUT_IMG + path, new_img)
    print(f'--- {OUTPUT_IMG + path} ---')
    if cv.waitKey(0) & 0xFF == 27:
        cv.destroyAllWindows()


def img_lists():
    global SOURCE_IMG
    for image in os.listdir(SOURCE_IMG):
        img_compression(image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IMG compression')
    parser.add_argument('-p', '--path', type=str, help='path')
    args = parser.parse_args()
    path = str(args.path)
    if os.path.exists(path):
        # if path[0:1] == '.' & (path[0:1] == '.' or path[0:1] == '/' or path[0:1] == '\\'):
        #     print(f'the path {path} should not include "./" or "../"')
        #     sys.exit()

        SOURCE_IMG = path + '/'
        img_lists()
