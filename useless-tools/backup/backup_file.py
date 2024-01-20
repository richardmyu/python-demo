# -*- coding: utf-8 -*-

import os
import time
import re

# 1.将要备份的文件和目录分配到一个列表中
# Windows
source = [r'D:\Books']

# 2.必须备份到主目录中
target_dir = r'D:\Backup'

# 如果目的路径不存在，则创建
if not os.path.exists(target_dir):
    os.mkdir(target_dir)  # 创建文件夹
    print('Successfully created directory: ', target_dir)

# 3.文件备份到 ZIP
# 4.zip 命令
# 日期做文件夹名
today = target_dir + os.sep + time.strftime('%Y%m%d')
# 当前时间做文件名
now = time.strftime('%H%M%S')

# 让用户输入一个用于创建 zip 文件的名称
comment = input('Enter a comment -->')
if len(comment) == 0:
    target = today + os.sep + now + '.zip'
elif comment[0] == '_':
    target = today + os.sep + now + re.sub(r'[^a-zA-Z0-9_]', '', comment) + '.zip'
else:
    target = today + os.sep + now + '_' + re.sub(r'[^a-zA-Z0-9_]', '', comment) + '.zip'

# 若目录不存在则创建
if not os.path.exists(today):
    os.mkdir(today)
    print('Successfully created directory: ', today)

# 5.使用 zip 命令将文件放入 zip
zip_command = 'zip -r {0} {1}'.format(target, ''.join(source))

# 运行
print('Zip command is: ')
print(zip_command)
print('Running: ')
if os.system(zip_command) == 0:
    print('Successful backup to: ', target)
else:
    print('Backup FAILED!')
