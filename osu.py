#!/bin/python3.10
import pygame
from pygame.locals import *
import os


FRAMERATE = 144
BACKGROUND = (20,20,20)

CURSOR_SIZE = 64
CIRCLE_SIZE = 130

WIDTH, HEIGHT = 1280, 720

pygame.init()

window = pygame.display.set_mode((WIDTH,HEIGHT), 0, 32)
pygame.display.set_caption("click the circles")

pygame.mouse.set_visible(False)


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
DEF_HITCIRCLE_APPROACH  = pygame.transform.scale(DEF_HITCIRCLE_APPROACH, (CIRCLE_SIZE, CIRCLE_SIZE))

HITSOUND = pygame.mixer.Sound("assets/hit.wav")

class Cursor():

    def __init__(self,image=DEF_CURSOR,image_trail=DEF_CURSORTRAIL):
        self.x = 0
        self.y = 0
        self.offset = CURSOR_SIZE/2
        self.image = image
        self.image_trail = image_trail

    def draw(self):
        window.blit(self.image, (self.x - self.offset,self.y - self.offset))


class Hitcircle():
    def __init__(self,x,y,image=DEF_HITCIRCLE,image_overlay=DEF_HITCIRCLE_OVERLAY,image_approach=DEF_HITCIRCLE_APPROACH):
        self.x = x
        self.y = y
        self.image = image
        self.image_overlay = image_overlay
        self.image_approach = image_approach
        self.offset = CIRCLE_SIZE/2
        self.rect = pygame.Rect(x - self.offset,y - self.offset,CIRCLE_SIZE,CIRCLE_SIZE)

    def draw_circle(self):
        window.blit(self.image, (self.x - self.offset, self.y - self.offset))
        window.blit(self.image_overlay, (self.x - self.offset, self.y - self.offset))

    def check_hit(self,cursor):
        if self.rect.collidepoint((cursor.x,cursor.y)):
            if click == True:
                print("clicked")
                pygame.mixer.Sound.play(HITSOUND)


def draw():
    window.fill(BACKGROUND)

    hitcircle.draw_circle()
    cursor.draw()

    pygame.display.update()

cursor = Cursor()
hitcircle = Hitcircle(200,200)

click = False
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(FRAMERATE)

    cursor.x, cursor.y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_v:
                click = True
            if event.key == K_b:
                click = True

    draw()
    hitcircle.check_hit(cursor)

    click = False

pygame.quit()
