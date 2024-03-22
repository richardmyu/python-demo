import turtle

top_level = 8  # 一共递归6层
angle = 30
range = 15


def draw_tree(length, level):
    turtle.left(angle)  # 绘制左枝
    turtle.color("black")
    turtle.forward(length)

    if level == top_level:  # 叶子
        turtle.color("pink")
        turtle.circle(2, 360)

    if level < top_level:  # 在左枝退回去之前递归
        draw_tree(length - 10, level + 1)
    turtle.back(length)

    turtle.right(angle + range)  # 绘制右枝
    turtle.color("black")
    turtle.forward(length)

    if level == top_level:  # 叶子
        turtle.color("pink")
        turtle.circle(2, 360)

    if level < top_level:  # 在右枝退回去之前递归
        draw_tree(length - 10, level + 1)
        turtle.color("black")
    turtle.back(length)
    turtle.left(range)


turtle.left(90)
turtle.penup()
turtle.back(300)
turtle.pendown()
turtle.forward(100)
turtle.speed('fastest')
draw_tree(80, 1)

turtle.done()
