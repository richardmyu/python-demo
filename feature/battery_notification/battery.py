# -*- coding: utf-8 -*-

# pip install psutil
import psutil

battery = psutil.sensors_battery()
plugged = battery.power_plugged
percent = battery.percent
print('---', percent)
