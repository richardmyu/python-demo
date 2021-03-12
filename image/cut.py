# -*- coding: utf-8 -*-

import os
from PIL import Image

width = int(1920 / 2)
height = int(1080 / 2)


def cut(img):
    im = Image.open('img/' + img)

    crop_im = im.resize((width, height), Image.ANTIALIAS)
    crop_im.save('handled/' + img)


if __name__ == "__main__":
    images = os.listdir('./img')
    for image in images:
        # print(image)
        cut(image)
