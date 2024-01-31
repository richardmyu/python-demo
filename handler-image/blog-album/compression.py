"""
@Time: 2022/09/30 16:32:55
@Author: yum
@Email: richardminyu@foxmail.com
@File: compression.py
压缩图片
生成的图片输出在当前目录下的 output（没有就自动创建）
"""

import os
import argparse
import cv2 as cv
from skimage import io


def img_resize(img, scale=0.5, interpolation=cv.INTER_LINEAR):
    img = cv.resize(
        img,
        (int(img.shape[1] * scale), int(img.shape[0] * scale)),
        interpolation=interpolation,
    )
    return img


def img_compression(image, path=''):
    path_image = os.path.join(path, image)

    # 读取图像
    img = io.imread(path_image)

    # 针对 png 图像，删除 iCCP profiles 信息
    img = cv.cvtColor(img, cv.COLOR_RGBA2BGRA)
    cv.imencode('.png', img)[1].tofile(path_image)

    # 使用 resize, 进行缩放
    new_img = img_resize(img, interpolation=cv.INTER_AREA)

    # 文件夹检测和创建
    output_img = os.getcwd() + os.path.sep + 'output'
    
    if not os.path.exists(output_img):
        os.mkdir(output_img)
        
    output_img = output_img + os.path.sep + path
    
    if not os.path.exists(output_img):
        os.mkdir(output_img)

    # 写入图片到指定文件夹
    cv.imwrite(os.path.join(output_img, image), new_img)
    print(f'--- compress {image}: success ---')
    
    if cv.waitKey(0) & 0xFF == 27:
        cv.destroyAllWindows()


def multiple_imgs(files):
    """压缩文件（内全部图片）"""
    if not os.path.exists(files):
        print(f"{files} is not exits")
        return
    
    for file in os.listdir(files):
        img_compression(file, files)


def sign_img(img):
    """压缩单张图片"""
    try:
        img_compression(img)
    except:
        print(f"{img} is not exits")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IMG compression')
    parser.add_argument('-p', '--path', type=str, help='path')
    args = parser.parse_args()
    path = args.path
    path = os.path.normpath(path)

    if path[-3:] in ['jpg', 'png']:
        sign_img(path)
    else:
        multiple_imgs(path)
