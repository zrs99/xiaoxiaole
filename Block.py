import pygame
import random
import sys
from abc import ABC, abstractmethod

import time

DRAW_TYPE_CIRCLE = 1
DRAW_TYPE_RECT = 2
DRAW_TYPE_RANDOM = 3
DRAW_TYPE_IMAGE = 4
DRAW_TYPE_ICE = 5

BLOCK_NO_USE = 0
BLOCK_IS_USE = 1
BLOCK_NO_IMAGE = -1

list_animal = ['bear.png', 'chick.png', 'cow.png', 'eagle.png', 'fox.png', 'frog.png']

class Block:
    def __init__(self, leftX, topY, width, height, type, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.leftX = leftX
        self.topY = topY
        self.blockType = type
        self.isUse = 1
        self.randomIndex = random.randint(1, 4)
        self.imageNum = BLOCK_NO_IMAGE

    def changeColor(self):
        R = random.randint(0, 255)
        G = random.randint(0, 255)
        B = random.randint(0, 255)
        return R,G,B

    def drawBlock(self):
        if self.blockType == DRAW_TYPE_RECT and self.isUse == BLOCK_IS_USE:
            pygame.draw.rect(self.screen, self.changeColor(), (self.leftX, self.topY, self.width, self.height))
        elif self.blockType == DRAW_TYPE_CIRCLE and self.isUse == BLOCK_IS_USE:
            pygame.draw.rect(self.screen, (0, 0, 0), (self.leftX, self.topY, self.width, self.height))
            pygame.draw.circle(self.screen, self.changeColor(), (self.leftX + self.width / 2, self.topY + self.height / 2),
                               self.width / 2)
        elif self.blockType == DRAW_TYPE_IMAGE and self.isUse == BLOCK_IS_USE:
            num = random.randint(1, 12)
            self.imageNum = num
            str = './images/%s.png' % num
            img = pygame.image.load(str)
            self.screen.blit(img, (self.leftX, self.topY, self.width, self.height))

    def mouseClicked(self, x, y):
        if x > self.leftX and x < self.leftX+self.width and y > self.topY and y < self.topY+self.height and self.isUse == BLOCK_IS_USE:
            pygame.draw.rect(self.screen, self.changeColor(), (self.leftX, self.topY, self.width, self.height))
            print(self.imageNum)

class Shape:
    def __init__(self, screen):
        self.leftX = 0
        self.topY = 0
        self.screen = screen
        self.isUse = BLOCK_IS_USE

    @abstractmethod
    def mouseClicked(self, x, y):
        pass

    def changeColor(self):
        R = random.randint(0, 255)
        G = random.randint(0, 255)
        B = random.randint(0, 255)
        return R, G, B

    @abstractmethod
    def drawShape(self):
        pass

class ImageLevelShape(Shape):
    def __init__(self, screen, left, top):
        super().__init__(screen)
        self.leftX = left
        self.topY = top

    def drawShape(self, level):
        levelImg = pygame.image.load('./pic2/level%s.png'%level)
        self.screen.blit(levelImg, (self.leftX, self.topY))

class ImageShape(Shape):
    def __init__(self, screen):
        super().__init__(screen)
        self.width = 0
        self.height = 0
        self.score = 0
        self.pos_x = 0
        self.pos_y = 0
        self.animalNum = BLOCK_NO_IMAGE
        self.imageType = -1

    def drawShape(self):
        if self.isUse == BLOCK_IS_USE:
            img = pygame.image.load('./pic2/'+list_animal[self.animalNum])
            self.screen.blit(img, (self.leftX, self.topY))
        elif self.isUse == BLOCK_NO_USE:
            self.screen.blit(pygame.image.load('./pic2/fruit.png'), (self.leftX, self.topY))

    def drawSquare(self):
         self.screen.blit(pygame.image.load('./pic2/brick.png'), (self.leftX, self.topY))

    def mouseClicked(self, x, y):
        if x > self.leftX and x < self.leftX+self.width and y > self.topY and y < self.topY+self.height and self.isUse == BLOCK_IS_USE:
            # print("--------")
            pygame.draw.rect(self.screen, self.changeColor(), (self.leftX, self.topY, self.width, self.height))
            # print(self.imageNum)



class ImageIceShape(ImageShape):
    def __init__(self, screen):
        super().__init__(screen)
        self.freezeLevel = -1

    def drawShape(self):
        if self.isUse == BLOCK_IS_USE:
            iceImg = pygame.image.load('./pic2/ice%s.png'%self.freezeLevel)
            self.screen.blit(iceImg, (self.leftX, self.topY))


class RectShape(Shape):
    def __init__(self, screen):
        super().__init__(screen)
        self.width = 0
        self.height = 0

    def drawShape(self): #高度宽度
        if self.isUse == BLOCK_IS_USE:
            rect_pos = self.leftX, self.topY, self.width, self.height
            pygame.draw.rect(self.screen, (0, 0, 0), rect_pos)

class CircleShape(Shape):
    def __init__(self, screen):
        super().__init__(screen)
        self.radius = 0

    def drawShape(self): #高度宽度
        if self.isUse == BLOCK_IS_USE:
            pygame.draw.circle(self.screen, self.changeColor, (self.leftX+self.radius, self.topY+self.radius, self.radius))


#工厂类 专门生产Shape的子类
class Factory:
    def create(self, type, screen, screen_x, screen_y, width, height, pos_i, pos_j, map):
        if type == DRAW_TYPE_IMAGE:
            imageShape = ImageShape(screen)
            imageShape.leftX = screen_x+pos_i*width
            imageShape.topY = screen_y+pos_j*height
            imageShape.width = width
            imageShape.height = height
            imageShape.imageNum = random.randint(0, 4)
            imageShape.animalNum = random.randint(0, 4)
            imageShape.isUse = map[pos_i][pos_j]
            imageShape.pos_i = pos_i
            imageShape.pos_j = pos_j
            return imageShape
        elif type == DRAW_TYPE_RECT:
            rectShape = RectShape(screen)
            rectShape.leftX = screen_x+pos_i*width
            rectShape.topY = screen_y+pos_j*height
            rectShape.width = width
            rectShape.height = height
            return rectShape
        elif type == DRAW_TYPE_CIRCLE:
            circleShape = CircleShape(screen)
            circleShape.leftX = screen_x+pos_i*width
            circleShape.topY = screen_y+pos_j*height
            circleShape.radius = width / 2
            return circleShape
        elif type == DRAW_TYPE_ICE:
            iceImageShape = ImageIceShape(screen)
            iceImageShape.leftX = screen_x+pos_i*width
            iceImageShape.topY = screen_y+pos_j*height
            iceImageShape.width = width
            iceImageShape.height = height
            iceImageShape.isUse = map[pos_i][pos_j]
            iceImageShape.pos_i = pos_i
            iceImageShape.pos_j = pos_j
            iceImageShape.freezeLevel = random.randint(0, 8)
            iceImageShape.imageNum = random.randint(0, 8)
            return iceImageShape



class MagicBlock:
    def __init__(self, screen_x, screen_y, row, col, width, height, type, screen):
        self.type = type
        self.width = width
        self.height = height
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.row = row
        self.col = col
        self.blocks = [[0]*self.col for i in range(self.row)]
        self.map = [[0]*self.col for i in range(self.row)]
        self.iceBlocks = [[0]*self.col for i in range(self.row)]
        self.screen = screen
        self.factory = Factory()
        self.tool = Tool('./maps/1', screen_x, screen_y, width, height)

    def initMagicBlock(self):
        print(self.row, self.col)
        for i in range(0, self.row):
            for j in range(0, self.col):
                self.blocks[i][j] = self.factory.create(self.type, self.screen, self.screen_x, self.screen_y,
                                                        self.width, self.height, i, j, self.map)
                self.iceBlocks[i][j] = self.factory.create(DRAW_TYPE_ICE, self.screen, self.screen_x, self.screen_y,
                                                           self.width, self.height, i, j, self.map)

    def drawMagicBlock(self):
        for i in range(0, self.row):
            for j in range(0, self.col):
                # self.iceBlocks[i][j].drawShape()
                self.blocks[i][j].drawShape()

    def drawMagicSquare(self):
        for i in range(0, self.row):
            for j in range(0, self.col):
                self.blocks[i][j].drawSquare()


    def mouseClicked(self, lastMouseX, lastMouseY, nextMouseX, nextMouseY):
        score = 0
        lastMouseX, lastMouseY = self.tool.get_IJ(lastMouseX, lastMouseY)
        nextMouseX, nextMouseY = self.tool.get_IJ(nextMouseX, nextMouseY)
        temp = self.blocks[lastMouseX][lastMouseY].animalNum
        self.blocks[lastMouseX][lastMouseY].animalNum = self.blocks[nextMouseX][nextMouseY].animalNum
        self.blocks[nextMouseX][nextMouseY].animalNum = temp

        score += self.eliminateAnimal(lastMouseX, lastMouseY)
        score += self.eliminateAnimal(nextMouseX, nextMouseY)
        return score

    def readMap(self, path):
        with open(path, 'r') as file:
            mapFile = file.readlines()
            for i in range(0, self.row):
                for j in range(0, self.col):
                    self.map[j][i] = int(mapFile[i][j])

    def drawGrids(self):
        for x in range(0, self.row):
            for y in range(0, self.col):
                rect = pygame.Rect((self.screen_x+x*self.width, self.screen_y+y*self.height, self.width, self.height))
                pygame.draw.rect(self.screen, (255, 165, 0), rect, 1)

    def eliminateAnimal(self, pos_x, pos_y):
        up = 0
        down = 0
        left = 0
        right = 0
        score = 0
        # print(pos_x, pos_y)
        while pos_y+up-1 >= 0 and self.blocks[pos_x][pos_y+up-1].animalNum == self.blocks[pos_x][pos_y].animalNum : up-=1
        while pos_y+down+1 < self.row and self.blocks[pos_x][pos_y+down+1].animalNum == self.blocks[pos_x][pos_y].animalNum : down+=1
        while pos_x+left-1 >= 0 and self.blocks[pos_x+left-1][pos_y].animalNum == self.blocks[pos_x][pos_y].animalNum : left-=1
        while pos_x+right+1 < self.col and self.blocks[pos_x+right+1][pos_y].animalNum == self.blocks[pos_x][pos_y].animalNum : right+=1

        if down-up >= 2:
            for y in range(pos_y+up, pos_y+down+1):
                print(pos_x, y)
                score += 1
                self.blocks[pos_x][y] = self.factory.create(self.type, self.screen, self.screen_x, self.screen_y,
                                                            self.width, self.height, pos_x, y, self.map)
        if right-left >= 2:
            for x in range(pos_x+left, pos_x+right+1):
                print((x, pos_y))
                score += 1
                self.blocks[x][pos_y] = self.factory.create(self.type, self.screen, self.screen_x, self.screen_y,
                                                            self.width, self.height, x, pos_y, self.map)
        if down-up >= 2 and right-left >= 2:
            score -= 1
        # time.sleep(1)
        self.drawMagicSquare()
        self.drawMagicBlock()
        return score

    def drawProcess(self, step):
        img = pygame.image.load(('./images/process3.png')).convert_alpha()
        self.screen.blit(img,(52,17,500,10))
        pygame.draw.rect(self.screen, (255, 255, 255), (80, 25, 445, 16))
        pygame.draw.rect(self.screen, (174,213,76), (80, 25, step % 448, 16))

    def refreshScore(self):
        score = 0
        for i in range(self.row):
            for j in range(self.col):
                score += self.eliminateAnimal(i, j)
        return score

class Tool:
    def __init__(self, filePath, screen_x, screen_y, width, height):
        self.row = 0
        self.col = 0
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.width = width
        self.height = height
        self.filePath = filePath

    # def readMap(self):
    #     with open(self.filePath, 'r') as file:
    #         for i in range(0, self.row):
    #             mapFile = file.readline()
    #             for j in range(0, self.col):
    #                 self.map[i][j] = int(mapFile[j])

    def getRowCol(self):
        file = open(self.filePath, 'r')
        map = file.readlines()
        self.row = len(map)
        self.col = len(map[0])-1
        file.close()
        return self.row, self.col

    def get_IJ(self, x, y):
        return int((x-self.screen_x)/self.width), int((y-self.screen_y)/self.height)