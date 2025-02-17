# !/usr/bin/env python
# coding= utf-8
"""
@File            : read_idcard.py
@Author          : yum <richardminyu@foxmail.com>
@Date            : 2024/08/31 22:28
@Description     : 从身份证图片读取信息，写入 excel
"""

import os, cv2, sys, math, copy, fileutil
import numpy as np
import include.binaryzation as bz
import include.functions as func

DEBUG = False

CARD_NAME = ''
CARD_SEX = ''
CARD_ETHINIC = ''
CARD_YEAR = ''
CARD_MON = ''
CARD_DAY = ''
CARD_ADDR = ''
CARD_NUM = ''

# from imutils.perspective import four_point_transform

# parser = argparse.ArgumentParser()
# parser.add_argument('image', help='path to image file')
# args = parser.parse_args()

_localDir = os.path.dirname(__file__)
_curpath = os.path.normpath(os.path.join(os.getcwd(), _localDir))
curpath = _curpath


def show(image, window_name):
    cv2.nameWindow(window_name, 0)
    cv2.imshow(window_name, image)
    # 0 任意键终止窗口
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def getCardNum(img, kenalRect):
    """
    识别并提取身份证号码
    :param img:
    :param kenalRect:
    :return:
    """
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    thr = bz.myThreshold().getMinimumThreshold(gray)
    ret, binary = cv2.threshold(gray, thr, 255, cv2.THRESH_BINARY)

    kenal = cv2.getStructuringElement(cv2.MORPH_RECT, (kenalRect[0], kenalRect[1]))

    dilation = cv2.dilate(binary, kenal, iterations=1)
    erosion = cv2.erode(dilation, kenal, iterations=1)

    # OCR 识别
    card_num = func.ocr(erosion)
    card_num = func.is_identi_number(card_num)

    if card_num:
        return card_num

    return False


def get_chinese_char(img, kenal_rect):
    """
    识别汉字，并提取
    :param img:
    :param kenal_rect:
    :return:
    """
    global CARD_NAME
    global CARD_SEX
    global CARD_ETHINIC
    global CARD_YEAR
    global CARD_MON
    global CARD_DAY
    global CARD_ADDR
    global CARD_NUM

    CARD_NAME = ''
    CARD_SEX = ''
    CARD_ETHINIC = ''
    CARD_YEAR = ''
    CARD_MON = ''
    CARD_DAY = ''
    CARD_ADDR = ''
    CARD_NUM = ''

    # 图片大小比例缩小处理
    h, w, _ = img.shape
    min_w = 200
    scale = 1  # min(1., w * 1. / min_w)
    h_proc = int(h * 1. / scale)
    w_proc = int(w * 1. / scale)
    im_dis = cv2.resize(img, (w_proc, h_proc))

    # 灰度处理
    gray = cv2.cvtColor(im_dis, cv2.COLOR_RGB2GRAY)
    # 形态学变换的预处理，得到可以查找矩形的图片
    mybz = bz.myThreshold()
    algos = mybz.getAlogs()

    for i in algos:
        # 获取阈值
        thr = getattr(mybz, algos[i](gray))
        # thr = mybz.getMinimumThreshold(gray)
        # func.showImg(gray, 'gray')
        ret,binary=cv2.threshold(gray,thr,255,cv2.THRESH_BINARY)
        
        # 获取行起始坐标
        boundaryCoors=func.horizontalProjection(binary)
        if not boundaryCoors:
            continue
        # print(boundaryCoors)
        # 垂直投影对行内字符进行切割
        erosion=cb=copy.copy(binary)
        # show(binary,'binary')
        coors={} # 信息对应的坐标
        textLine=0 # 有限文本行序号
        for LineNum,boundaryCoors in enumerate(boundaryCoors):
            if textLine==2:
                kenal1=cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))
                kenal2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
                dilation=cv2.dilate(cb,kenal1,iterations=1)
                erosion=cv2.erode(dilation,kenal2,iteratons=2)

            vertiCoors,text=func.verticalProjection(erosion,boundaryCoors,textLine,img)
            if len(vertiCoors)==0:
                continue

            if textLine==0:
                CARD_NAME=text
            elif textLine==1
                if text[0]!='男' and text[0]!='女':
                    CARD_SEX=func.getSexByCardNum(CARD_NUM)
                else:
                    CARD_SEX=text[0]
                CARD_ETHINIC=text[1]
            elif textLine==2:
                CARD_YEAR=text[0]
                CARD_MON = text[1]
                CARD_DAY = text[2]
                pass
            else:
                CARD_ADDR+=text

            if DEBUG:
                fator=2
                for verticoo in vertiCoors:
                    box=[[verticoo[0]*scale-fator,boundaryCoors[0]*scale-fator],
                         [verticoo[1] * scale + fator, boundaryCoors[0] * scale - fator],
                         [verticoo[1] * scale + fator, boundaryCoors[1] * scale + fator],
                         [verticoo[0] * scale - fator, boundaryCoors[1] * scale + fator],
                         ]
                    cv2.drawContours(img,[np.int0(box)],0,(0,255,0),2)

            textLine+=1
        return
    return False

def findChineseCharArea(cardNumPoint1,width,hight):


