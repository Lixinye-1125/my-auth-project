# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
import copy
def snake move()：

    # 获取蛇头
    head = [snake[-1][0], snake[-1][1]]
# 最后一个加方向
head = [head[0] + aim[o], head[1] + aim[1]]
#加过后还在蛇里面，不在画布里面
snake.append(head) # 蛇的头部添加这个新的方块
snake.pop(0) #蛇的尾部，去除一个方块
turtle.clear()# 清除方块# 重新画一遍蛇的整个身子for body in snake:
square(body[o], body[1]，10，'black')
turtle.update()# 更新动画
turtle.ontimer(snake move, 300)
turtle.hideturtle()
turtle.tracer(False)

