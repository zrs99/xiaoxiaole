import pygame
import random
import sys
from abc import ABC, abstractmethod


DRAW_TYPE_CIRCLE = 1
DRAW_TYPE_RECT = 2
DRAW_TYPE_RANDOM = 3
DRAW_TYPE_IMAGE = 4

BLOCK_NO_USE = 0
BLOCK_IS_USE = 1
BLOCK_NO_IMAGE = -1

list_animal = ['bear.png', 'chick.png', 'cow.png', 'eagle.png', 'fox.png', 'frog.png']


class Shape:
    def __init__(self, screen):
        self.leftX = 0
        self.topY = 0
        self.screen = screen
        self.isUse = BLOCK_IS_USE


    @abstractmethod
    def mouseClicked(self, x, y):
        # if x > self.leftX and x < self.leftX+55 and y > self.topY and y < self.topY+55 and self.isUse == BLOCK_IS_USE:
        #     pygame.draw.rect(self.screen, self.changeColor(), (self.leftX, self.topY, self.width, self.height))
            # print(self.imageNum)
        pass

    def changeColor(self):
        R = random.randint(0, 255)
        G = random.randint(0, 255)
        B = random.randint(0, 255)
        return R, G, B

    @abstractmethod
    def drawShape(self):
        pass

class ImageShape(Shape):
    def __init__(self, screen):
        super().__init__(screen)
        self.width = 0
        self.height = 0
        self.score = 0
        self.animalNum = BLOCK_NO_IMAGE
        self.imageType = -1

    def drawShape(self):
        if self.isUse == BLOCK_IS_USE:
            # num = random.randint(1, 11)
            self.score = self.imageNum
            img = pygame.image.load('./pic2/'+list_animal[self.imageNum])
            self.imageNum = self.imageNum
            self.screen.blit(img, (self.leftX, self.topY))

    def mouseClicked(self, x, y):
        if x > self.leftX and x < self.leftX+self.width and y > self.topY and y < self.topY+self.height and self.isUse == BLOCK_IS_USE:
            # print("--------")
            pygame.draw.rect(self.screen, self.changeColor(), (self.leftX, self.topY, self.width, self.height))
            # print(self.imageNum)

class ImageIceShape(ImageShape):
    pass

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
    def create(self, type, screen, left, top, width, height):
        if type == DRAW_TYPE_IMAGE:
            imageShape = ImageShape(screen)
            imageShape.leftX = left
            imageShape.topY = top
            imageShape.width = width
            imageShape.height = height
            imageShape.imageNum = random.randint(0, 4)
            return imageShape
        elif type == DRAW_TYPE_RECT:
            rectShape = RectShape(screen)
            rectShape.leftX = left
            rectShape.topY = top
            rectShape.width = width
            rectShape.height = height
            return rectShape
        elif type == DRAW_TYPE_CIRCLE:
            circleShape = CircleShape(screen)
            circleShape.leftX = left
            circleShape.topY = top
            circleShape.radius = width / 2
            return circleShape


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
        self.screen = screen
        self.factory = Factory()
        self.tool = Tool('./maps/1')

    def initMagicBlock(self):
        for i in range(0, self.row):
            for j in range(0, self.col):
                self.blocks[i][j] = self.factory.create(self.type, self.screen, self.screen_x+i*self.width, self.screen_y+j*self.height, self.width, self.height)
                self.blocks[i][j].isUse = self.map[i][j]
                # self.blocks[i][j].drawShape()

    def drawMagicBlock(self):
        print(self.row, self.col)
        for i in range(0, self.row):
            for j in range(0, self.col):
                self.blocks[i][j].drawShape()
                # if self.type == DRAW_TYPE_IMAGE:
                #     self.blocks[i][j] = Block(self.screen_x+i*self.width, self.screen_y+j*self.height, self.width,
                #                               self.height, DRAW_TYPE_IMAGE, self.screen)
                # elif self.type == DRAW_TYPE_RECT:
                #     self.blocks[i][j] = Block(self.screen_x+i*self.width, self.screen_y+j*self.height, self.width,
                #                               self.height, DRAW_TYPE_RECT, self.screen)
                # elif self.type == DRAW_TYPE_CIRCLE:
                #     self.blocks[i][j] = Block(self.screen_x+i*self.width, self.screen_y+j*self.height, self.width,
                #                               self.height, DRAW_TYPE_CIRCLE, self.screen)
                # self.blocks[i][j].drawBlock()

    def mouseClicked(self, mouseX, mouseY):
        # print(self.row, self.col)
        for i in range(0, self.row):
            for j in range(0, self.col):
                # print(i, j)
                self.blocks[i][j].mouseClicked(mouseX, mouseY)


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

class Tool:
    def __init__(self, filePath):
        self.row = 0
        self.col = 0
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