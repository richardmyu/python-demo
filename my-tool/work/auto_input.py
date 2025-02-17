import easyocr
import pandas as pd
import os
import re
import time

def date_to_timestamp(date,format_string="%Y-%m-%d %H:%M:%S"):
    time_array=time.strptime(date,format_string)
    time_stamp=int(time.mktime(time_array))
    return time_stamp

images = './id_card/'
ocr = easyocr.Reader(['ch_sim', 'en'], gpu=False)
data = []

for image in os.listdir(images):
    content = ''
    name = ''
    gender = ''
    number = ''

    content = ocr.readtext(f'{images}/{image}', detail=0)
    print(f'正在识别：{image}')
    print(content)

    # # 姓名处理
    # str_1 = content[0] + content[1]
    # # print('111',str_1)
    # str_1 = str_1.replace('姓', '')
    # str_1 = str_1.replace('名', '')
    # str_1 = str_1.replace(':', '')
    # index_1 = str_1.find('性')
    # index_2 = str_1.find('别')

    # if index_1 :
    #     str_1 = str_1[0:index_1]
    # if index_2 :
    #     str_1 = str_1[0:index_2]

    # str_1 = str_1.replace(r'[\u4e00-\u9fa5]', '')
    # name = str_1.replace(' ', '')
    # # print('222',name)

    # for x in content:
    #     if len(x) == 18 and not re.search(r'[^0-9x*]+',x):
    #         number = x
    # # print('333',number)

    if len(content) == 2:
        name = content[0]
        number = content[1]
    elif len(content) == 3:
        if re.search(r'[0-9*]+', content[1]):
            number = content[1] + content[2]
        else:
            name = content[0] + content[1]
            number = content[2]
    elif len(content) == 4:
        if (re.search(r'[0-9*]+',content[1])) and (re.search(r'[0-9*]+', content[2])):
            name = content[0].replace(' ', '')
            number = content[1] + content[2] + content[3]
        elif (not re.search(r'[0-9*]+',content[1])) and (not re.search(r'[0-9*]+', content[2])):
            name = content[0] + content[1] + content[2]
            number = content[3]
        elif (not re.search(r'[0-9*]+',content[1])) and (re.search(r'[0-9*]+', content[2])):
            name = content[0] + content[1]
            number = content[2] +content[3]
    else:
        name = content[0]
        number = 'null'

    name = name.replace(' ', '')


    if number[-1] == '*':
        number = number[:-1] + 'x'

    if len(number)==18:
        if int(number[-2:-1]) % 2 == 0:
            gender = '女'
        else:
            gender = '男'

    print(f'识别完成：{image}')

    print('-' * 24)
    print(f'{name} {gender} {number}')
    print('-' * 24)

    idcard_type='身份证'

    data.append([name, gender, idcard_type,number])

df = pd.DataFrame(data, columns=["姓名", "性别","证件类型", "身份证号"])
df.to_excel(f"{time.time()}-result.xlsx", index=False)
