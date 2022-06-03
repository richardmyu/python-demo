# -*- coding: utf-8 -*-

'''
处理和压缩博客相册，并生成相册对应 JSON 数据

文件夹分类:
    photos 原始图片
    artwork 原始图片抹除地理等信息
    square 原始图片的剪裁版本(调整为统一 width > height)
    thumbnail 剪裁图片后再压缩
    data.json 相册的图片信息

命令:
    创建相册
    py album_tool.py -a create

    插入单张图片
    py album_tool.py -a insert

    插入全部图片
    py album_tool.py -a insert_all
'''

import os
import time
import json
import argparse
from PIL import Image
from PIL import ImageOps
import exifread
from random import randint
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

IMAGE_BED = 'https://richyu.gitee.io/img_bed/album'


class AlbumTool(object):

    def __init__(self, gallery):
        self.scale = 4
        self.gallery = gallery
        self.galleryPath = 'album/' + gallery
        self.photos = self.galleryPath + '/photos/'
        self.artwork = self.galleryPath + '/artwork/'
        self.square = self.galleryPath + '/square/'
        self.thumbnail = self.galleryPath + '/thumbnail/'
        self.data_json = self.galleryPath + '/data.json'

    def cut_by_ratio(self, infile, outfile, artwork):
        '''按照图片长宽进行分割
        取中间的部分，裁剪成正方形
        '''
        im = Image.open(infile)
        (w, h) = im.size
        if hasattr(ImageOps, 'exif_transpose'):
            handler_img = ImageOps.exif_transpose(im)
        else:
            handler_img = self.reset_orientation(im)
        handler_img.save(artwork)
        region = (0, 0, 0, 0)
        if w < h:
            w, h = h, w
        region = (int(w - h) / 2, 0, int(w + h) / 2, h)
        crop_img = handler_img.crop(region)
        crop_img.save(outfile)

    def pre_cut(self, image):
        '''裁剪图片'''
        print('Cutting the photos image to square...')
        if not os.path.exists(self.square):
            os.makedirs(self.square)
        self.cut_by_ratio(self.photos + image, self.square +
                          image, self.artwork + image)

    def compress(self, image):
        '''压缩图片'''
        print('Compressing the square image to thumbnail...')
        if not os.path.exists(self.thumbnail):
            os.makedirs(self.thumbnail)
        img = Image.open(self.square + image)
        w, h = img.size
        w, h = int(w / self.scale), int(h / self.scale)
        img.thumbnail((w, h))
        img.save(self.thumbnail + image)

    @staticmethod
    def reset_orientation(img):
        '''
        处理图片的自动(PIL处理回发生)旋转
        增加对 width / height 的调换处理
        https://cloud.tencent.com/developer/article/1523050
        '''
        # TODO: 实际结果有问题，部分旋转的图片，并非居中而是偏左显示
        exif_orientation_tag = 274
        # w, h = img.size
        if hasattr(img, '_getexif') \
                and isinstance(img._getexif(), dict) \
                and exif_orientation_tag in img._getexif():
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
                img = img.rotate(-90,
                                 expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                img = img.rotate(-90, expand=True)
            elif orientation == 7:
                img = img.rotate(90, expand=True).transpose(
                    Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
        return img

    @staticmethod
    def reverse_geocoder(geolocator, lat_lon, sleep_sec=5):
        '''
        根据经纬度，计算区域
        https://www.pythonheidong.com/blog/article/680556/d9bf76d691415de282f1/
        '''
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
        '''
        获取图片的经纬度以及拍摄时间等信息
        https://zhuanlan.zhihu.com/p/98460548
        '''
        print('Loading and Resolving: ' + img)
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

        # 照片拍摄日期-时间
        if image_map['Image DateTime']:
            img_date = image_map['Image DateTime'].printable[:10].replace(
                ':', '-')
            img_time = image_map['Image DateTime'].printable[11:]

        # 设备型号
        if image_map['Image Model']:
            img_model = image_map['Image Model'].printable

        # 曝光补偿 ExposureBiasValue
        if image_map['EXIF ExposureBiasValue']:
            img_ev = image_map['EXIF ExposureBiasValue'].printable

        # ISO感光度 ISOSpeedRatings
        if image_map['EXIF ISOSpeedRatings']:
            img_iso = image_map['EXIF ISOSpeedRatings'].printable

        # 曝光时间/快门速度 ExposureTime
        if image_map['EXIF ExposureTime']:
            img_et = image_map['EXIF ExposureTime'].printable

        # 光圈系数 FNumber
        if image_map['EXIF FNumber']:
            img_fn = image_map['EXIF FNumber'].printable

        # 焦距 FocalLength
        if image_map['EXIF FocalLength']:
            img_fl = image_map['EXIF FocalLength'].printable

        try:
            # 图片的经度
            img_longitude_ref = image_map['GPS GPSLongitudeRef'].printable
            img_longitude = image_map['GPS GPSLongitude'].printable[1:-1].replace(' ', '').replace('/', ',').split(
                ',')
            img_longitude = float(img_longitude[0]) + float(img_longitude[1]) / 60 + float(
                img_longitude[2]) / float(img_longitude[3]) / 3600
            if img_longitude_ref != 'E':
                img_longitude = img_longitude * (-1)

            # 图片的纬度
            img_latitude_ref = image_map['GPS GPSLatitudeRef'].printable
            img_latitude = image_map['GPS GPSLatitude'].printable[1:-1].replace(' ', '').replace('/', ',').split(
                ',')
            img_latitude = float(img_latitude[0]) + float(img_latitude[1]) / 60 + float(img_latitude[2]) / float(
                img_latitude[3]) / 3600
            if img_latitude_ref != 'N':
                img_latitude = img_latitude * (-1)
        except Exception as e:
            print('ERROR: 图片中不包含 Gps 信息')
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

        info = {
            'address': img_address,  # 地址
            'date': img_date,  # 日期
            'time': img_time,  # 日期
            'model': img_model,
            'ev': img_ev,
            'iso': img_iso,
            'et': img_et,
            'fn': img_fn,
            'fl': img_fl
        }
        print('--')
        print(info)
        return info

    def describe(self, image):
        '''
        根据当前传入的相册名，图片，描述更新相册的描述JSON文件
        '''
        # 生成关于 image 的新 dict
        print('Updating the data json file...')
        info = self.get_exif(self.photos + image)
        img_info = Image.open(self.photos + image)
        width, height = img_info.size

        image_dict = {
            'name': image,
            'caption': '',
            'type': 'image',
            'date': info['date'],
            'time': info['time'],
            'address': info['address'],
            'width': width,
            'height': height,
            'model': info['model'],
            'exposure_bias_value': info['ev'],
            'iso_speed_ratings': info['iso'],
            'exposure_time': info['et'],
            'f_number': info['fn'],
            'focal_length': info['fl']
        }

        item_dict = {
            'date': info['date'][:7],
            'images': [
                image_dict
            ]
        }

        items = []
        images = []
        index = 0

        current = time.strftime('%Y-%m-%d %H:%M-%S',
                                time.localtime(time.time()))
        with open(self.data_json, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            items = data['items']

        if items:
            for item in items:
                if item['date'] != info['date'][:7]:
                    continue
                images = item['images']
                index = items.index(item)
            if images:
                for img in images:
                    if img['name'] == image:
                        print('The file ' + image + ' already exists')
                        return
                images.insert(0, image_dict)
                images.sort(key=lambda image: image['date'], reverse=True)
                items[index]['images'] = images
            else:
                items.insert(0, item_dict)
        else:
            items.insert(0, item_dict)

        items.sort(key=lambda item: item['date'], reverse=True)
        data['items'] = items
        data['updated'] = current

        # 序列化数据结构到JSON文本
        with open(self.data_json, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False,
                      sort_keys=False, indent=4)

    def create(self):
        '''创建相册
        '''
        if os.path.exists(self.galleryPath):
            print('Error: gallery ' + self.gallery + ' already exists')
            return
        else:
            os.makedirs(self.galleryPath)
            os.makedirs(self.photos)
            os.makedirs(self.artwork)
            os.makedirs(self.square)
            os.makedirs(self.thumbnail)

            current = time.strftime(
                '%Y-%m-%d %H:%M-%S', time.localtime(time.time()))
            data_dict = {
                'name': self.gallery,
                'cover': '',
                'description': '',
                'created': current,
                'updated': current,
                'image_bed': IMAGE_BED,
                'items': []
            }
            with open(self.data_json, 'w', encoding='utf-8') as json_file:
                json.dump(data_dict, json_file, ensure_ascii=False,
                          sort_keys=False, indent=4)
            print('Gerry has created!')

    def insert(self):
        '''插入单张图片
        '''
        image = input('Please input the image file name: ')
        self.pre_cut(image)
        self.compress(image)
        self.describe(image)

    def insert_all(self):
        '''插入全部图片
        '''
        for image in os.listdir(self.photos):
            self.pre_cut(image)
            self.compress(image)
            self.describe(image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Album Tool')
    parser.add_argument('-a', '--action', type=str,
                        help='action to be executed')
    args = parser.parse_args()

    gallery = input('Please input the gallery name: ')

    album = AlbumTool(gallery)
    if args.action == 'create':
        album.create()
    elif args.action == 'insert':
        album.insert()
    elif args.action == 'insert_all':
        album.insert_all()
