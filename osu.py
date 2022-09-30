#!/bin/python3.10
import pygame
from pygame.locals import *
from random import randint
import math
import os


FRAMERATE = 144
BACKGROUND = (10,10,10)

CURSOR_SIZE = 64
CIRCLE_SIZE = 130

WIDTH, HEIGHT = 1280, 720

pygame.init()

window = pygame.display.set_mode((WIDTH,HEIGHT), 0, 32)
surface_main = pygame.Surface((WIDTH, HEIGHT))
surface_approach = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)

pygame.display.set_caption("click the circles")

pygame.mouse.set_visible(False)

# set global variables
click = False
running = True
clock = pygame.time.Clock()

hitcircles = []

# set defaults
DEF_CURSOR              = pygame.image.load(os.path.join('assets','cursor.png')).convert_alpha()
DEF_CURSORTRAIL         = pygame.image.load(os.path.join('assets','cursortrail.png')).convert_alpha()
DEF_HITCIRCLE           = pygame.image.load(os.path.join('assets','hitcircle.png')).convert_alpha()
DEF_HITCIRCLE_OVERLAY   = pygame.image.load(os.path.join('assets','hitcircleoverlay.png')).convert_alpha()
DEF_HITCIRCLE_APPROACH  = pygame.image.load(os.path.join('assets','approachcircle.png')).convert_alpha()

# set correct size
DEF_CURSOR              = pygame.transform.scale(DEF_CURSOR, (CURSOR_SIZE, CURSOR_SIZE))
DEF_CURSORTRAIL         = pygame.transform.scale(DEF_CURSORTRAIL, (CURSOR_SIZE, CURSOR_SIZE))
DEF_HITCIRCLE           = pygame.transform.scale(DEF_HITCIRCLE, (CIRCLE_SIZE, CIRCLE_SIZE))
DEF_HITCIRCLE_OVERLAY   = pygame.transform.scale(DEF_HITCIRCLE_OVERLAY, (CIRCLE_SIZE, CIRCLE_SIZE))
DEF_HITCIRCLE_APPROACH  = pygame.transform.scale(DEF_HITCIRCLE_APPROACH, (CIRCLE_SIZE*2, CIRCLE_SIZE*2))

HITSOUND = pygame.mixer.Sound("assets/hit.wav")

class Cursor():

    def __init__(self,image=DEF_CURSOR,image_trail=DEF_CURSORTRAIL):
        self.x = 0
        self.y = 0
        self.offset = CURSOR_SIZE/2
        self.image = image
        self.image_trail = image_trail

    def draw(self):
        surface_main.blit(self.image, (self.x - self.offset,self.y - self.offset))


class Hitcircle():
    def __init__(self,x,y,time,number=0,image=DEF_HITCIRCLE,image_overlay=DEF_HITCIRCLE_OVERLAY,image_approach=DEF_HITCIRCLE_APPROACH):
        self.x = x
        self.y = y
        self.time = time

        self.number = number
        self.image = image
        self.image_overlay = image_overlay
        self.image_approach = image_approach
        self.offset = CIRCLE_SIZE / 2
        #self.rect = pygame.Rect(x - self.offset,y - self.offset,CIRCLE_SIZE,CIRCLE_SIZE)
        self.clicked = False
        self.clicktime = None
        self.missed = False
        self.shoulddraw = True
        self.growth = 0

    def draw_circle(self):
        if self.clicked == False and self.shoulddraw == True :
                surface_main.blit(self.image, (self.x - self.offset, self.y - self.offset))
                surface_main.blit(self.image_overlay, (self.x - self.offset, self.y - self.offset))

    def draw_approach(self):
        if self.clicked == False:
            if self.growth < CIRCLE_SIZE * 2:
                self.image_approach = pygame.transform.scale(DEF_HITCIRCLE_APPROACH, (CIRCLE_SIZE*3 - self.growth, CIRCLE_SIZE*3 - self.growth))
                surface_approach.blit(self.image_approach, (self.x - CIRCLE_SIZE * 1.5 + self.growth / 2, self.y - CIRCLE_SIZE* 1.5 + self.growth / 2))

            self.growth += 2

    def check_click(self,cursor):
        if self.missed == False and self.shoulddraw == True:
            if math.sqrt((self.x - cursor.x)**2 + (self.y - cursor.y)**2) < CIRCLE_SIZE / 2:
                if click == True and self.clicked == False:
                    self.clicked = True
                    self.clicktime = pygame.time.get_ticks()
                    print("x : ", self.x, ", y : ", self.y, ", spawned at : ", self.time, ", clicked at : ", self.clicktime)

    def check_hit(self):
        if self.missed == False and self.clicked == True:
            pygame.mixer.Sound.play(HITSOUND)
            self.clicked = False
            self.shoulddraw = False

    def check_miss(self):
        if self.missed != True:
            if self.clicktime != None and self.clicktime - 920 >= self.time or self.clicktime - 720 <= self.time :
                self.missed = True
                self.shoulddraw = False
                print("missed : ", (self.clicktime - 820) - self.time)
            if self.time + 1200 <= pygame.time.get_ticks():
                self.shoulddraw = False
                self.missed = True


def parse_file(path):
    f = open(path + '.osu', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')

cursor = Cursor()

frame=0
while running:
    clock.tick(FRAMERATE)
    surface_main.fill(BACKGROUND)
    surface_approach.fill((0,0,0,0))

    cursor.x, cursor.y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_v:
                click = True
            if event.key == K_b:
                click = True

    for hitcircle in hitcircles:
        if hitcircle.time <= pygame.time.get_ticks():
            hitcircle.check_click(cursor)
            hitcircle.check_miss()
            hitcircle.check_hit()
            hitcircle.draw_circle()
            hitcircle.draw_approach()

    cursor.draw()

    if frame % FRAMERATE == 0:

        for circle in hitcircles:
            if circle.clicked == True:
                hitcircles.remove(circle)

        hitcircles.append(Hitcircle(randint(64,WIDTH-64),randint(64,HEIGHT-64),pygame.time.get_ticks()))

    window.blit(surface_main, (0,0))
    window.blit(surface_approach, (0,0))
    pygame.display.update()
    click = False
    frame += 1

pygame.quit()
