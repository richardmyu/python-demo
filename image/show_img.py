# -*- coding: utf-8 -*-

import sys
import os
from PIL import Image
import exifread

def reset_orientation(img):
    """
    处理图片的自动（PIL处理回发生）旋转
    https://cloud.tencent.com/developer/article/1523050
    """
    exif_orientation_tag = 274
    w, h = img.size
    print('--', w, h)
    if hasattr(img, "_getexif") and isinstance(img._getexif(), dict) and exif_orientation_tag in img._getexif():
        exif_data = img._getexif()
        orientation = exif_data[exif_orientation_tag]

        print(img.size)
        print('orientation ', orientation)

        # Handle EXIF Orientation
        if orientation == 1:
            # Normal image - nothing to do!
            pass
        elif orientation == 2:
            # Mirrored left to right
            # img = img.transpose(Image.FLIP_LEFT_RIGHT)
            pass
        elif orientation == 3:
            # Rotated 180 degrees
            # img = img.rotate(180)
            pass
        elif orientation == 4:
            # Mirrored top to bottom
            # img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            pass
        elif orientation == 5:
            # Mirrored along top-left diagonal
            # img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            w, h = h, w
        elif orientation == 6:
            # Rotated 90 degrees
            # img = img.rotate(-90, expand=True)
            w, h = h, w
        elif orientation == 7:
            # Mirrored along top-right diagonal
            # img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            w, h = h, w
        elif orientation == 8:
            # Rotated 270 degrees
            # img = img.rotate(90, expand=True)
            w, h = h, w
    # img.size = (w, h)
    return {
        "image": img,
        "size": (w, h)
    }


def get_area(img):
    im = Image.open('./img/' + img)
    print('-- im{} --'.format(img))
    # print(dir(im))
    print(im.size)
    w_h = reset_orientation(im)
    print(w_h["size"])

    # f = open('./img/' + img, 'rb')
    # image_map = exifread.process_file(f)
    # print("{}".format('-' * 20))
    # try:
    #     print("--- " + img + " ---")
    #     for item in image_map:
    #         print(item, image_map[item])
    #     print("Image ImageWidth ", image_map["Image ImageWidth"])
    #     print("Image ImageLength ", image_map["Image ImageLength"])
    #     print("Image Orientation ", image_map["Image Orientation"])
    #     print("Image DateTime ", image_map["Image DateTime"])
    #     print("EXIF ExifImageWidth ", image_map["EXIF ExifImageWidth"])
    #     print("EXIF ExifImageLength ", image_map["EXIF ExifImageLength"])
    # except Exception as e:
    #     print('ERROR: 图片中不包含 Gps 信息')


if __name__ == "__main__":
    images = os.listdir('./img')
    for image in images:
        get_area(image)
