# -*- coding: utf-8 -*-
"""
参考文章链接：
https://blog.csdn.net/weixin_39623050/article/details/110423917
https://gist.github.com/dengyt2018/c805f22ae8e3bda3c8d6129524c74b49
"""

import binascii


def generate_binmap_font(txt):
    KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]
    bin_list = []
    dec_list = []

    # 初始化16*16的点阵位置，每个汉字需要16*16=256个点来表示，需要32个字节才能显示一个汉字
    # 之所以32字节：256个点每个点是0或1，那么总共就是2的256次方，一个字节是2的8次方
    rect_list = [] * 16
    for i in range(16):
        rect_list.append([] * 16)

    # 获取中文的gb2312编码，一个汉字是由2个字节编码组成
    gb2312 = txt.encode('gb2312')

    # 将二进制编码数据转化为十六进制数据
    hex_str = binascii.b2a_hex(gb2312)

    # 将数据按unicode转化为字符串
    result = str(hex_str, encoding='utf-8')

    # 前两位对应汉字的第一个字节：区码，每一区记录94个字符
    area = eval('0x' + result[:2]) - 0xA0

    # 后两位对应汉字的第二个字节：位码，是汉字在其区的位置
    index = eval('0x' + result[2:]) - 0xA0

    # 汉字在HZK16中的绝对偏移位置，最后乘32是因为字库中的每个汉字字模都需要32字节
    offset = (94 * (area - 1) + (index - 1)) * 32
    font_rect = None

    # 读取HZK16汉字库文件
    with open('HZK16', 'rb') as f:
        # 找到目标汉字的偏移位置
        f.seek(offset)
        # 从该字模数据中读取32字节数据
        font_rect = f.read(32)

    # font_rect的长度是32，此处相当于for k in range(16)
    for k in range(len(font_rect) // 2):
        # 每行数据
        row_list = rect_list[k]
        for j in range(2):
            for i in range(8):
                asc = font_rect[k * 2 + j]
                # 此处&为Python中的按位与运算符
                flag = asc & KEYS[i]
                # 数据规则获取字模中数据添加到16行每行中16个位置处每个位置
                row_list.append(flag)

    # 根据获取到的16*16点阵信息，打印到控制台
    for row in range(len(rect_list)):
        # print('--', row)
        bin_str = ''
        for i in rect_list[row]:
            if i:
                # 前景字符（即用来表示汉字笔画的输出字符）
                # print('1', end=' ')
                # print('■', end=' ')●
                # print('o', end=' ')
                print('●', end=' ')
                bin_str = bin_str + '1'
            else:
                # 背景字符（即用来表示背景的输出字符）
                # print('0', end=' ')
                # print('□', end=' ')
                # print('.', end=' ')
                print('o', end=' ')
                bin_str = bin_str + '0'
        bin_list.append(bin_str)
        dec_list.append(int(bin_str[::-1], 2))
        print()

    print('----------')
    print(bin_list)
    print('----------')
    print(dec_list)


if __name__ == '__main__':
    text = input("请输入单个汉字： ")
    while text:
        if text == 'q' or text == 'quit':
            break
        generate_binmap_font(text)
        text = input("请输入单个汉字： ")
