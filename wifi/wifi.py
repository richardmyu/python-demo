# -*- coding: utf-8 -*-

import pywifi

# 获取是否来链接网络


def Check_state():
    # 抓取网卡接口
    wifi = pywifi.PyWiFi()

    # 获取第一个无线网卡
    ifaces = wifi.interfaces()[0]

    print(ifaces.status())
    print("===---===")

    if ifaces.status() == 4:
        print("电脑已连接无线")
    else:
        print("电脑未连接")


Check_state()
