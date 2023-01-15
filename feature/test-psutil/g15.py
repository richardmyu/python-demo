# -*- coding: utf-8 -*-

"""
查看系统信息

https://pypi.org/project/psutil/
"""

import psutil


def CPU_info():
    print("=== CPU 信息 ===")
    print("CPU 逻辑数量 ", psutil.cpu_count())
    print("CPU 物理核心 ", psutil.cpu_count(logical=False))
    print("CPU 用户／系统／空闲时间 ", psutil.cpu_times())
    print("CPU 使用率 ", psutil.cpu_percent(interval=1, percpu=True))
    print("")


def memory_info():
    print("=== 内存信息 ===")
    print("物理内存 ", psutil.virtual_memory())
    print("交换内存 ", psutil.swap_memory())
    print("")


def disk_info():
    print("=== 磁盘信息 ===")
    print("磁盘分区信息 ", psutil.disk_partitions())
    print("磁盘使用情况 ", psutil.disk_usage('/'))
    print("磁盘 IO ", psutil.disk_io_counters())
    print("")


def net_info():
    print("=== 网络信息 ===")
    print("获取网络接口状态 ", psutil.net_if_stats())
    print("获取网络接口信息 ", psutil.net_if_addrs())
    print("获取网络读写字节／包的个数 ", psutil.net_io_counters())
    print("当前网络连接信息 ", psutil.net_connections())
    print("")


def process_info():
    print("=== 进程信息 ===")
    print("所有进程 ID ", psutil.pids())
    p = psutil.Process(0)
    print("获取指定进程名称 ", p.name())
    print("")


def battery_info():
    print("=== 电池信息 ===")
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = battery.percent
    print("电量百分比 ", percent)
    print("")


if __name__ == '__main__':
    CPU_info()
    memory_info()
    disk_info()
    net_info()
    process_info()
    battery_info()
