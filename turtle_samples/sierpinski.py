import turtle as t
from turtle import *

length = 5
angle = -60
t.setup(1280, 720)
up()

goto(-640, -350)
down()


def draw_path(path):
    for symbol in path:
        if symbol == 'A' or symbol == 'B':
            import random
            colormode(255)
            color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            forward(length)
        elif symbol == '-':
            right(angle)
        elif symbol == '+':
            left(angle)
    ht()


def apply_rules(path, rules):
    lit = [_ for _ in path]
    for i in range(len(lit)):
        symbol = lit[i]
        if symbol in rules:
            lit[i] = rules[symbol]
    path = ''.join(lit)
    return path


rules = {
    'A': 'B-A-B',
    'B': 'A+B+A'
}
path = 'A'
speed(0)
for i in range(7):
    path = apply_rules(path, rules)
draw_path(path)
up()
goto(0, -340)
angle = 60
down()
draw_path(path)
up()
goto(0, -340)
angle = -60
down()
draw_path(path)
