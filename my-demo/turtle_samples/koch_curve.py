from turtle import *
import random

length = 2
angle = 90
setup(1280, 720)
up()
goto(-600, -350)
down()


def draw_path(path):
    for symbol in path:
        if symbol == 'F':
            colormode(255)
            color(
                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            )
            forward(length)
        elif symbol == '-':
            right(angle)
        elif symbol == '+':
            left(angle)
    ht()


def apply_rule(path):
    rule = 'F+F-F-F+F'
    return path.replace('F', rule)


path = 'F'
speed(0)
for i in range(5):
    path = apply_rule(path)
for i in range(5):
    draw_path(path)
up()
goto(-478, -228)
down()
for i in range(4):
    draw_path(path)
up()
goto(-356, -106)
down()
for i in range(3):
    draw_path(path)
up()
goto(-235, 16)
down()
for i in range(2):
    draw_path(path)
up()
goto(-115, 137)
down()
draw_path(path)
