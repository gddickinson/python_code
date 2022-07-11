# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 16:01:38 2018

@author: George
"""

import pygame
import sys
import time
import random
import numpy as np
from gridData import Grid

from pygame.locals import *

FPS = 5
pygame.init()
fpsClock=pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 320, 320
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill((255,255,255))
clock = pygame.time.Clock()

pygame.display.set_caption("Cell World Display Test")

pygame.key.set_repeat(1, 40)

GRIDSIZE = 50
ROWS = GRIDSIZE
COLUMNS = GRIDSIZE
GRID_WIDTH = SCREEN_WIDTH / ROWS
GRID_HEIGHT = SCREEN_HEIGHT / COLUMNS

screen.blit(surface, (0,0))

BLACK  = (0, 0,0)
WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE   = (0,0,255)
GREEN = (0,255,0)


def draw_box(surf, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (GRID_WIDTH, GRID_HEIGHT))
    pygame.draw.rect(surf, color, r)



class World(object):
    def __init__(self):
        self.colourList = [BLACK, WHITE, GREEN, BLUE, RED, YELLOW]
        self.randomWorld = np.random.randint(len(self.colourList), size=(ROWS, COLUMNS))
        print(self.randomWorld)
    
    def draw(self, surf):
        x = 0
        y = 0
        for x in range(ROWS):
            for y in range(COLUMNS):
                draw_box(surf, self.getColour(x,y), (x*GRID_WIDTH,y*GRID_HEIGHT))
                y = y + 1
            x = x+1
            y = 0
                       
    def getColour(self, x,y):
        return self.colourList[self.randomWorld[x,y]]
    
    def updateStauts(self):
        self.randomWorld = np.random.randint(len(self.colourList), size=(ROWS, COLUMNS))
        
    

if __name__ == '__main__':
    testWorld = World()
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()

            if event.type == pygame.VIDEORESIZE:
                surface = pygame.display.set_mode((event.w, event.h),
                            pygame.RESIZABLE)
                GRID_WIDTH = event.w / GRIDSIZE
                GRID_HEIGHT = event.h / GRIDSIZE

        surface.fill((255,255,255))
        testWorld.draw(surface)
        testWorld.updateStauts()

        #font = pygame.font.Font(None, 36)
        #text = font.render(str('Hello'), 1, (10, 10, 10))
        #textpos = text.get_rect()
        #textpos.centerx = 20
        #surface.blit(text, textpos)
        screen.blit(surface, (0,0))

        pygame.display.flip()
        pygame.display.update()
        fpsClock.tick(FPS)