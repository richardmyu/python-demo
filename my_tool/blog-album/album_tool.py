"""
@Time: 2022/09/30 16:34:15
@Author: yum
@Email: richardminyu@foxmail.com
@File: album_tool.py

压缩博客相册和生成相册对应 JSON 数据
files:
    photos 原始图片
    artwork 原始图片抹除地理等信息
    thumbnail 剪裁图片后再压缩
    data.json 相册的图片信息
command:
    创建相册
        py album_tool.py -a create
    插入单张图片
        py album_tool.py -a sign
    插入多张图片
        py album_tool.py -a all

改进：为了减少 Image.open 操作，合并了 cut 和 compress 过程；
---
2022-09-25 移除多余图片，确保一年份的图片不超过 12 张，以减少图片加载
2022-09-26 移除相册按月分类规则
"""

import os
import sys
import time
import json
import argparse
from PIL import Image
from PIL import ImageOps
import exifread
from random import randint
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

IMAGE_URL = 'https://raw.githubusercontent.com/richardmyu/gallery/1.0.0/album'


class AlbumTool(object):
    def __init__(self, gallery):
        self.scale = 16
        self.gallery = gallery
        self.galleryPath = 'album/' + gallery
        self.photos = self.galleryPath + '/photos/'
        self.artwork = self.galleryPath + '/artwork/'
        self.thumbnail = self.galleryPath + '/thumbnail/'
        self.data_json = self.galleryPath + '/data.json'

    @staticmethod
    def reset_orientation(img):
        """ 
        处理图片的自动旋转
        增加对 width / height 的调换处理
        https://piexif.readthedocs.io/en/latest/sample.html#rotate-image-by-exif-orientation
        https://zhuanlan.zhihu.com/p/85923289
        https://www.codenong.com/13872331/
        """
        exif_orientation_tag = 274

        if (
            hasattr(img, '_getexif')
            and isinstance(img._getexif(), dict)
            and exif_orientation_tag in img._getexif()
        ):
            exif_data = img._getexif()
            orientation = exif_data[exif_orientation_tag]

            if orientation == 1:
                pass
            elif orientation == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                img = img.rotate(180)
            elif orientation == 4:
                img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5:
                img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                img = img.rotate(-90, expand=True)
            elif orientation == 7:
                img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                img = img.rotate(90, expand=True)

        return img

    @staticmethod
    def reverse_geocoder(geolocator, lat_lon, sleep_sec=5):
        """
        根据经纬度，计算区域
        https://www.pythonheidong.com/blog/article/680556/d9bf76d691415de282f1/
        """
        try:
            # 反向地理编码
            return geolocator.reverse(lat_lon)
        except GeocoderTimedOut:
            print('Timeout: GeocoderTimedOut Retrying...')
            time.sleep(randint(2 * 100, sleep_sec * 100) / 50)
            return AlbumTool.reverse_geocoder(geolocator, lat_lon, sleep_sec)
        except GeocoderServiceError as e:
            print('CONNECTION REFUSED: GeocoderServiceError encountered.')
            print(e)
            return None
        except Exception as e:
            print('ERROR: Terminating due to exception {}'.format(e))
            return None

    @staticmethod
    def get_exif(img):
        """
        获取图片的经纬度以及拍摄时间等信息
        https://zhuanlan.zhihu.com/p/98460548
        """
        img_address = ''
        img_date = ''
        img_time = ''
        img_model = ''
        img_ev = ''
        img_iso = ''
        img_et = ''
        img_fn = ''
        img_fl = ''
        f = open(img, 'rb')
        image_map = exifread.process_file(f)

        # DATE 照片拍摄日期-时间
        try:
            img_date = image_map['Image DateTime'].printable[:10].replace(':', '-')
            img_time = image_map['Image DateTime'].printable[11:]
        except Exception as e:
            print('Warning: No Image DateTime')
            img_date = ''
            img_time = ''

        # MODEL 设备型号
        try:
            img_model = image_map['Image Model'].printable
        except Exception as e:
            # print('Warning: No Image Model')
            img_model = ''

        # EV 曝光补偿 ExposureBiasValue
        try:
            img_ev = image_map['EXIF ExposureBiasValue'].printable
        except Exception as e:
            # print('Warning: No EXIF ExposureBiasValue')
            img_ev = ''

        # ISO 感光度 ISOSpeedRatings
        try:
            img_iso = image_map['EXIF ISOSpeedRatings'].printable
        except Exception as e:
            # print('Warning: No EXIF ISOSpeedRatings')
            img_iso = ''

        # ET 曝光时间/快门速度 ExposureTime
        try:
            img_et = image_map['EXIF ExposureTime'].printable
        except Exception as e:
            # print('Warning: No EXIF ExposureTime')
            img_et = ''

        # FN 光圈系数 FNumber
        try:
            img_fn = image_map['EXIF FNumber'].printable
        except Exception as e:
            # print('Warning: No EXIF FNumber')
            img_fn = ''

        # FL 焦距 FocalLength
        try:
            img_fl = image_map['EXIF FocalLength'].printable
        except Exception as e:
            # print('Warning: No EXIF FocalLength')
            img_fl = ''

        try:
            # 图片的经度
            img_longitude_ref = image_map['GPS GPSLongitudeRef'].printable
            img_longitude = (
                image_map['GPS GPSLongitude']
                .printable[1:-1]
                .replace(' ', '')
                .replace('/', ',')
                .split(',')
            )

            img_longitude = (
                float(img_longitude[0])
                + float(img_longitude[1]) / 60
                + float(img_longitude[2]) / float(img_longitude[3]) / 3600
            )

            if img_longitude_ref != 'E':
                img_longitude = img_longitude * (-1)

            # 图片的纬度
            img_latitude_ref = image_map['GPS GPSLatitudeRef'].printable
            img_latitude = (
                image_map['GPS GPSLatitude']
                .printable[1:-1]
                .replace(' ', '')
                .replace('/', ',')
                .split(',')
            )

            img_latitude = (
                float(img_latitude[0])
                + float(img_latitude[1]) / 60
                + float(img_latitude[2]) / float(img_latitude[3]) / 3600
            )

            if img_latitude_ref != 'N':
                img_latitude = img_latitude * (-1)
        except Exception as e:
            # print('Warning: No GPS GPSLongitudeRef and so on')
            img_latitude = ''
            img_longitude = ''

        f.close()
        location = None

        if img_latitude != '' and img_longitude != '':
            reverse_value = str(img_latitude) + ', ' + str(img_longitude)

            # 初始化 Nominatim() 时传入新的 user-agent 值，避开样例值
            user_agent = 'my_blog_agent_{}'.format(randint(10000, 99999))
            geolocator = Nominatim(user_agent=user_agent)
            location = AlbumTool.reverse_geocoder(geolocator, reverse_value)

        img_address = location and location.address or ''
        img_info = {
            'address': img_address,  # 地址
            'date': img_date,  # 日期
            'time': img_time,  # 日期
            'model': img_model,
            'ev': img_ev,
            'iso': img_iso,
            'et': img_et,
            'fn': img_fn,
            'fl': img_fl,
        }
        return img_info

    def cut_and_compress(self, image, im):
        """
        1.按照图片长宽进行分割
        取中间的部分，裁剪成正方形
        2.压缩图片
        """
        print('    Cutting and Compressing    ')

        # ImageOps.exif_transpose
        # 如果图像具有 EXIF 方向标记，则返回相应地转置的新图像。
        # 否则，返回图像的副本。
        if hasattr(ImageOps, 'exif_transpose'):
            handler_img = ImageOps.exif_transpose(im)
        else:
            handler_img = self.reset_orientation(im)

        (w, h) = handler_img.size

        # 保存抹除 exif 信息后的 “原图”
        handler_img.save(self.artwork + image)
        region = (0, 0, 0, 0)

        if w < h:
            w, h = h, w
            # 纵图处理
            region = (int(int(h - w) / 2), 0, int(int(w + h) / 2), w)
        else:
            # 横图处理
            region = (0, int(int(h - w) / 2), w, int(int(w + h) / 2))

        # Ismage.crop((left, top, right, bottom))
        # 从图像中提取出某个矩形大小的图像。
        # 坐标系统的原点（0, 0）是左上角
        crop_img = handler_img.crop(region)

        # compress
        (cw, ch) = crop_img.size
        cw, ch = int(cw / self.scale), int(ch / self.scale)
        crop_img.thumbnail((cw, ch))
        crop_img.save(self.thumbnail + image)

    def describe(self, image, img_info):
        """
        根据当前传入的相册名，图片，描述更新相册的描述 JSON 文件
        """
        print('    Updating the data.json    ')
        (w, h) = img_info.size
        img_exit_info = self.get_exif(self.photos + image)
        image_dict = {
            'name': image,
            'caption': '',
            'type': 'image',
            'date': img_exit_info['date'],
            'time': img_exit_info['time'],
            'address': img_exit_info['address'],
            'width': w,
            'height': h,
            'model': img_exit_info['model'],
            'exposure_bias_value': img_exit_info['ev'],
            'iso_speed_ratings': img_exit_info['iso'],
            'exposure_time': img_exit_info['et'],
            'f_number': img_exit_info['fn'],
            'focal_length': img_exit_info['fl'],
        }

        # img lit
        items = []
        current = time.strftime('%Y-%m-%d %H:%M-%S', time.localtime(time.time()))

        with open(self.data_json, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            items = data['items']

        if items:
            for item in items:
                if item['name'] == image:
                    # 若存在，则覆盖原信息
                    item = image_dict
                    return

            items.insert(0, image_dict)
        else:
            items.insert(0, image_dict)

        items.sort(key=lambda item: item['date'], reverse=True)
        data['items'] = items
        data['updated'] = current

        # 序列化数据结构到 JSON 文本
        with open(self.data_json, 'w', encoding='utf-8') as json_file:
            # json.dump 写入 json 文件
            json.dump(data, json_file, ensure_ascii=False, sort_keys=False, indent=4)

    def check_file(self):
        """创建所需且不存在的文件夹"""
        if not os.path.exists(self.photos):
            os.makedirs(self.photos)
        if not os.path.exists(self.artwork):
            os.makedirs(self.artwork)
        if not os.path.exists(self.thumbnail):
            os.makedirs(self.thumbnail)
        if not os.path.exists(self.data_json):
            current = time.strftime('%Y-%m-%d %H:%M-%S', time.localtime(time.time()))
            data_dict = {
                'name': self.gallery,
                'cover': '',
                'description': '',
                'created': current,
                'updated': current,
                'image_url': IMAGE_URL,
                'items': [],
            }

            with open(self.data_json, 'w', encoding='utf-8') as json_file:
                json.dump(
                    data_dict, json_file, ensure_ascii=False, sort_keys=False, indent=4
                )

    def create(self):
        """创建相册"""
        if not os.path.exists(self.galleryPath):
            os.makedirs(self.galleryPath)

        self.check_file()
        print(f'Gallery {self.gallery} has created!')

    def insert(self, image=''):
        """插入单张图片"""
        if len(str((image)).strip()) == 0:
            image = input('Please input the image file name: ')
            image = image.strip()

            # 插入单张图片的时候，需要检测照片是否存在
            if not os.path.exists(self.photos + image):
                print('Error: image ' + self.gallery + ' is not exists')
                return

        print(f'--- Handling image {image} ---')
        opened_img = Image.open(self.photos + image)
        self.cut_and_compress(image, opened_img)
        self.describe(image, opened_img)

    def insert_all(self):
        """插入全部图片"""
        self.check_file()

        for image in os.listdir(self.photos):
            self.insert(image)


if __name__ == '__main__':
    # https://docs.python.org/zh-cn/3/howto/argparse.html
    parser = argparse.ArgumentParser(description='Album Tool')
    parser.add_argument('-a', '--action', type=str, help='action to be executed')
    parser.add_argument('-f', help='cover the existing file')
    args = parser.parse_args()

    # 非法参数过滤
    COMMAND_LIST = ['create', 'sign', 'all']

    if args.action not in COMMAND_LIST:
        print(f'Error: unrecognized arguments: {args.action}')
        sys.exit()

    # 相册名
    gallery = input('Please input the gallery name: ')
    gallery = gallery.strip()

    # 生成相册实例，并进行对应处理
    album = AlbumTool(gallery)

    if args.action == 'create':
        album.create()
    elif args.action == 'sign':
        album.insert()
    elif args.action == 'all':
        album.insert_all()
