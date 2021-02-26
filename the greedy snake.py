# 导入模块
import pygame
import time
import random
import sys

pygame.init()  # 初始化
Display = pygame.display.set_mode((640, 480))  # 窗口大小
pygame.display.set_caption('贪吃蛇')  # 窗口名称

speed = pygame.time.Clock()  # 游戏速度

# 定义颜色
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREY = pygame.Color(150, 150, 150)
defaultfont = pygame.font.get_default_font()  # 获得默认字体的文件名
basicfont = pygame.font.Font(defaultfont, 46)  # 默认字体

# 贪吃蛇头的的初始位置
snake_Head = [100, 100]
# 初始化贪吃蛇的长度 (注：这里以20*20为一个标准小格子)
snake_Body = [[80, 100], [60, 100]]
# 指定蛇初始前进的方向，向右
direction = 'right'

# 将蛇的头部当前的位置加入到蛇身的列表中
snake_Body.insert(0, list(snake_Head))


# 绘制贪吃蛇
def drawSnake(snake_Body):
    for i in snake_Body:
        pygame.draw.rect(Display, WHITE, ((i[0], i[1]), (20, 20)))


# 给定第一枚食物的位置
food_Position = [300, 300]
# 食物标记：0代表食物已被吃掉；1代表未被吃掉。
food_flag = 1


# 绘制食物的位置
def drawFood(food_Position):
    pygame.draw.rect(Display, RED, ((food_Position[0], food_Position[1]), (20, 20)))


# 打印出当前得分
def drawScore(score):
    # 设置分数的显示颜色
    score_Surf = basicfont.render('%s' % score, True, GREY)
    # 设置分数的位置
    score_Rect = score_Surf.get_rect()
    score_Rect.midtop = (320, 240)
    # 绑定以上设置到句柄
    Display.blit(score_Surf, score_Rect)


# 游戏结束并退出
def GameOver():
    # 设置GameOver的显示颜色
    GameOver_Surf = basicfont.render('Game Over!', True, GREY)
    # 设置GameOver的位置
    GameOver_Rect = GameOver_Surf.get_rect()
    GameOver_Rect.midtop = (320, 10)
    # 绑定以上设置到句柄
    Display.blit(GameOver_Surf, GameOver_Rect)

    pygame.display.flip()
    # 等待3秒
    time.sleep(3)
    # 退出游戏
    pygame.quit()
    # 退出程序
    sys.exit()


while True:
    # pygame检测按键
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 接收到退出事件后，退出程序
            pygame.quit()
            sys.exit()
        # 判断键盘事件，用 方向键 或 wsad 来表示上下左右，且无法向相反方向转
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != 'down':
                direction = 'up'
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != 'up':
                direction = 'down'
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != 'right':
                direction = 'left'
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != 'left':
                direction = 'right'

    # 根据键盘的输入，改变蛇的头部，进行转弯操作
    if direction == 'left':
        snake_Head[0] -= 20
    if direction == 'right':
        snake_Head[0] += 20
    if direction == 'up':
        snake_Head[1] -= 20
    if direction == 'down':
        snake_Head[1] += 20

    # 移动（加蛇头，去蛇尾（去蛇尾在144行判断是否吃到食物处）
    snake_Body.insert(0, list(snake_Head))

    # 画面填黑
    Display.fill(BLACK)

    # 画食物
    drawFood(food_Position)

    # 画蛇
    drawSnake(snake_Body)

    # 画分数
    drawScore(len(snake_Body) - 4)

    # 控制游戏速度
    speed.tick(7)

    # 刷新Pygame的显示层，贪吃蛇与食物的每一次移动，都会进行刷新显示层的操作来显示。
    pygame.display.flip()

    # 游戏结束的判断
    # 贪吃蛇触碰到边界
    if snake_Head[0] < 0 or snake_Head[0] > 620:
        GameOver()
    if snake_Head[1] < 0 or snake_Head[1] > 460:
        GameOver()
    # 贪吃蛇触碰到自己
    for i in snake_Body[1:]:
        if snake_Head[0] == i[0] and snake_Head[1] == i[1]:
            GameOver()

    # 判断是否吃掉食物
    if snake_Head[0] == food_Position[0] and snake_Head[1] == food_Position[1]:
        food_flag = 0
    else:
        snake_Body.pop()

    # 生成新的食物
    if food_flag == 0:
        # 随机生成x, y
        x = random.randrange(1, 32)
        y = random.randrange(1, 24)
        food_Position = [int(x * 20), int(y * 20)]
        food_flag = 1
