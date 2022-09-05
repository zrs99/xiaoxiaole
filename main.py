import pygame
import time
import sys
import random
from Block import *
import queue

DRAW_TYPE_CIRCLE = 1
DRAW_TYPE_RECT = 2
DRAW_TYPE_RANDOM = 3
DRAW_TYPE_IMAGE = 4

BLOCK_NO_USE = 0
BLOCK_IS_USE = 1

WIDTH = 47
HEIGHT = 47
SCREEN_X = 100
SCREEN_Y = 100


def ChangeColor():
    R = random.randint(0, 255)
    B = random.randint(0, 255)
    G = random.randint(0, 255)
    return R,B,G

def Draw(screen, x, y, row, col, width, height, type, **kwargs):
    typy_random_flag = False
    is_Fixed_Point = len(kwargs['fixed_point']) != 0

    if is_Fixed_Point:
        pygame.draw.circle(screen, (123, 42, 22), (x + kwargs['fixed_point'][0] * width + width / 2, y + kwargs['fixed_point'][1] * height + height / 2), width / 2)
        pygame.draw.circle(screen, (23, 212, 122), (x + kwargs['fixed_point'][0] * width + width / 2, y + kwargs['fixed_point'][1] * height + height / 2),
                       width / 2-5)

    for i in range(0, row):
        for j in range(0, col):

            if is_Fixed_Point:
                if i == kwargs['fixed_point'][0] and j == kwargs['fixed_point'][1]:
                    continue

            if type == DRAW_TYPE_RANDOM or typy_random_flag:
                type = random.randint(1, 4)
                typy_random_flag = True

            if type == DRAW_TYPE_RECT:
                pygame.draw.rect(screen, ChangeColor(), (x+i*width, y+j*height, width, height))
            elif type == DRAW_TYPE_CIRCLE:
                pygame.draw.rect(screen, (0, 0, 0), (x + i * width, y + j * height, width, height))
                pygame.draw.circle(screen, ChangeColor(), (x+i*width+width/2, y+j*height+height/2), width/2)
            elif type == DRAW_TYPE_IMAGE:
                order = random.randint(1, 8)
                str = './images2/%s.png' % order
                img = pygame.image.load(str)
                pygame.draw.rect(screen, (0, 0, 0), (x + i * width, y + j * height, width, height))
                screen.blit(img, (x+i*width, y+j*height, width, height))


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("桃桃消消乐")


    mixer = pygame.mixer
    mixer.init()
    music = mixer.music
    music.load(r"./sound/WorldSceneBGM.ogg")
    # music.set_volume()
    music.play()

    font = pygame.font.Font(r'C:\Windows\Fonts\simsun.ttc', 40)
    process_font = pygame.font.Font(r'C:\Windows\Fonts\simsun.ttc', 20)

    # 开始界面
    step = 0
    begin_flag = False
    last_x = last_y = -1
    blingNum = 0

    while True:
        pygame.display.update()
        # time.sleep(0.05)

        if blingNum == 0:
            background = pygame.image.load('pic2/开始界面.jpeg')
            background = pygame.transform.scale(background, (900, 670))
            screen.blit(background, (0, 0, 768, 768))

        # print(blingNum)
        imgBling = pygame.image.load('./pic2/bling%s.png'%(blingNum+1))
        screen.blit(imgBling, (100, 100))
        blingNum = (blingNum+1)%9



        # screen.blit(pygame.image.load('./pic2/task.png').convert_alpha(), (600, 0))
        beginBotton = font.render('开始游戏', True, (0, 0, 0))
        screen.blit(beginBotton, (360, 530))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                begin_flag = True

        if begin_flag == True:
            screen.blit(background, (0, 0, 768, 768))
            pygame.draw.rect(screen, (255, 255, 255), (200, 540, 445, 16))
            pygame.draw.rect(screen, (174, 213, 76), (200, 540, step % 448, 16))
            process_text = process_font.render('%s %%' % str(int((step % 445) / 445 * 100)), True, (0, 0, 0))
            screen.blit(process_text, (200 + step, 538))
            step += 3

            if step > 445:
                break

    # -------------------------------------------------------
    # 游戏界面
    step = 448
    level = 1
    score = 0

    # 背景音乐
    gameTool = Tool('./maps/1', SCREEN_X, SCREEN_Y, WIDTH, HEIGHT)
    music.stop()

    game_music = mixer.music
    game_music.load(r"./sound/GameSceneBGM.ogg")
    # music.set_volume()
    music.play()
    levelCtrl = ImageLevelShape(screen, 750, 0)
    while True:
        # time.sleep(0.01)
        pygame.display.update()
        #关卡地图刷新
        if step % 448 == 0:

            #关卡刷新
            mapPath = 'maps/%s' % level
            gameTool.filePath = mapPath
            # magicBlock.row, magicBlock.col = gameTool.getRowCol()
            gameRow, gameCol = gameTool.getRowCol()
            magicBlock = MagicBlock(SCREEN_X, SCREEN_Y, gameRow, gameCol, WIDTH, HEIGHT, DRAW_TYPE_IMAGE, screen)
            magicBlock.readMap(mapPath)
            magicBlock.initMagicBlock()

            #背景图
            mainBackground = pygame.image.load('pic2/bg.png')
            mainBackground = pygame.transform.scale(mainBackground, (900, 670))
            screen.blit(mainBackground, (0, 0, 768, 768))

            #text 第几关
            # question_font = pygame.font.Font(r'C:\Windows\Fonts\simsun.ttc', 16)
            #    question_text = question_font.render('第%s关' % question, True, (174, 213, 76))
            levelCtrl.drawShape(level)
            magicBlock.drawMagicSquare()
            magicBlock.drawMagicBlock()

            #刷新得分
            # pygame.display.update()
            # score += magicBlock.refreshScore()
            # stepImg = pygame.image.load('./pic2/step.png')
            # screen.blit(stepImg, (0, 0))

            level += 1
            if level == 4:
                break

        # 得分
        score_font = pygame.font.Font(r'C:\Windows\Fonts\simsun.ttc', 16)
        screen.blit(pygame.image.load('./pic2/task.png').convert_alpha(), (-15, -20))
        textScore = score_font.render('%s分' % score, True, (0, 0, 0))
        screen.blit(textScore, (20, 40))

        # pygame.display.update()
        #网格绘制
        # magicBlock.drawGrids()

        # 进度条
        # magicBlock.drawProcess(step)
        img = pygame.image.load(('./images/process3.png')).convert_alpha()
        screen.blit(img,(52,17,500,10))
        pygame.draw.rect(screen, (255, 255, 255), (80, 25, 445, 16))
        pygame.draw.rect(screen, (174,213,76), (80, 25, step % 448, 16))

        step -= 0.01

        #刷新
        clock = pygame.time.Clock()
        clock.tick(60)
        pygame.display.flip()

        #鼠标点击事件
        flag_tow = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                Tool.gameQueue.put((x, y))
                x, y = gameTool.get_IJ(x, y)
                imgFrame = pygame.image.load('./pic2/frame.png')
                screen.blit(imgFrame, (magicBlock.blocks[x][y].leftX,magicBlock.blocks[x][y].topY))
                score += magicBlock.mouseClicked()
