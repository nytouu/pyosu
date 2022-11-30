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
surface_cursor = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
surface_approach = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)

pygame.display.set_caption("click the circles")

pygame.mouse.set_visible(False)

# set global variables
click = False
running = True
clock = pygame.time.Clock()

hitcircles = []

# set defaults
DEF_CURSOR = pygame.image.load(os.path.join('assets','cursor.png')).convert_alpha()
DEF_CURSORTRAIL = pygame.image.load(os.path.join('assets','cursortrail.png')).convert_alpha()
DEF_HITCIRCLE = pygame.image.load(os.path.join('assets','hitcircle.png')).convert_alpha()
DEF_HITCIRCLE_OVERLAY = pygame.image.load(os.path.join('assets','hitcircleoverlay.png')).convert_alpha()
DEF_HITCIRCLE_APPROACH = pygame.image.load(os.path.join('assets','approachcircle.png')).convert_alpha()

DEF_NUMBER0 = pygame.image.load(os.path.join('assets','default-0.png')).convert_alpha()
DEF_NUMBER1 = pygame.image.load(os.path.join('assets','default-1.png')).convert_alpha()
DEF_NUMBER2 = pygame.image.load(os.path.join('assets','default-2.png')).convert_alpha()
DEF_NUMBER3 = pygame.image.load(os.path.join('assets','default-3.png')).convert_alpha()
DEF_NUMBER4 = pygame.image.load(os.path.join('assets','default-4.png')).convert_alpha()
DEF_NUMBER5 = pygame.image.load(os.path.join('assets','default-5.png')).convert_alpha()
DEF_NUMBER6 = pygame.image.load(os.path.join('assets','default-6.png')).convert_alpha()
DEF_NUMBER7 = pygame.image.load(os.path.join('assets','default-7.png')).convert_alpha()
DEF_NUMBER8 = pygame.image.load(os.path.join('assets','default-8.png')).convert_alpha()
DEF_NUMBER9 = pygame.image.load(os.path.join('assets','default-9.png')).convert_alpha()


# set correct size
DEF_CURSOR = pygame.transform.scale(DEF_CURSOR, (CURSOR_SIZE, CURSOR_SIZE))
DEF_CURSORTRAIL = pygame.transform.scale(DEF_CURSORTRAIL, (CURSOR_SIZE, CURSOR_SIZE))
DEF_HITCIRCLE = pygame.transform.scale(DEF_HITCIRCLE, (CIRCLE_SIZE, CIRCLE_SIZE))
DEF_HITCIRCLE_OVERLAY = pygame.transform.scale(DEF_HITCIRCLE_OVERLAY, (CIRCLE_SIZE, CIRCLE_SIZE))
DEF_HITCIRCLE_APPROACH = pygame.transform.scale(DEF_HITCIRCLE_APPROACH, (CIRCLE_SIZE * 2, CIRCLE_SIZE * 2))

HITSOUND = pygame.mixer.Sound("assets/hit.wav")
MISSSOUND = pygame.mixer.Sound("assets/miss.wav")

HITSOUND.set_volume(0.1)
MISSSOUND.set_volume(0.1)

class Cursor():

    def __init__(self,image=DEF_CURSOR,image_trail=DEF_CURSORTRAIL):
        self.x = 0
        self.y = 0
        self.offset = CURSOR_SIZE / 2
        self.image = image
        self.image_trail = image_trail

    def draw(self):
        """
        draw cursor onto its surface
        """
        surface_cursor.blit(self.image, (self.x - self.offset,self.y - self.offset))


class Hitcircle():
    def __init__(self,x,y,time,number=0,image=DEF_HITCIRCLE,
                 image_overlay=DEF_HITCIRCLE_OVERLAY,image_approach=DEF_HITCIRCLE_APPROACH):
        # mandatory argments
        self.x = x
        self.y = y
        self.time = time

        self.number = number
        self.numbers = list(str(self.number))
        self.image = image
        self.image_overlay = image_overlay
        self.image_approach = image_approach
        self.offset = CIRCLE_SIZE / 2
        self.clicked = False
        self.clicktime = None
        self.missed = False
        self.shoulddraw = True
        self.growth = 0
        self.soundplayed = False

    def draw_circle(self):
        """
        draw hitcircle onto the main surface
        """
        if self.clicked is False and self.shoulddraw is True:
            surface_main.blit(self.image, (self.x - self.offset, self.y - self.offset))
            surface_main.blit(self.image_overlay, (self.x - self.offset, self.y - self.offset))
            # self.draw_numbers()

    def draw_numbers(self):
        for digit in self.numbers:
            self.draw_number()

    def draw_number(self,digit):
        offset = -2
        digit = 1

        match len(self.numbers):
            case 1:
                offset = -2
            case 2:
                if digit == 1:
                    offset = -16
                else:
                    offset = 14

        for current in str(self.number):
            match current:
                case '0':
                    surface_main.blit(DEF_NUMBER0, (self.x - self.offset / 2 + offset, self.y - self.offset / 2))
                case '1':
                    surface_main.blit(DEF_NUMBER1, (self.x - self.offset / 2 + offset, self.y - self.offset / 2))
                case '2':
                    surface_main.blit(DEF_NUMBER2, (self.x - self.offset / 2 + offset, self.y - self.offset / 2))
                case '3':
                    surface_main.blit(DEF_NUMBER3, (self.x - self.offset / 2 + offset, self.y - self.offset / 2))
                case '4':
                    surface_main.blit(DEF_NUMBER4, (self.x - self.offset / 2 + offset, self.y - self.offset / 2))
                case '5':
                    surface_main.blit(DEF_NUMBER5, (self.x - self.offset / 2 + offset, self.y - self.offset / 2))
                case '6':
                    surface_main.blit(DEF_NUMBER6, (self.x - self.offset / 2 + offset, self.y - self.offset / 2))
                case '7':
                    surface_main.blit(DEF_NUMBER7, (self.x - self.offset / 2 + offset, self.y - self.offset / 2))
                case '8':
                    surface_main.blit(DEF_NUMBER8, (self.x - self.offset / 2 + offset, self.y - self.offset / 2))
                case '9':
                    surface_main.blit(DEF_NUMBER9, (self.x - self.offset / 2 + offset, self.y - self.offset / 2))

    def draw_approach(self):
        """
        draw the approach circle, this method keeps track of the approach circle's size
        and shrinks it accordingly

        coordinates are hardcoded but it works, might stop working with a different circle size
        """
        if self.clicked is False and self.shoulddraw:
            if self.growth < CIRCLE_SIZE * 2:
                self.image_approach = pygame.transform.scale(DEF_HITCIRCLE_APPROACH,
                                                             (CIRCLE_SIZE * 3 - self.growth,
                                                              CIRCLE_SIZE * 3 - self.growth))
                surface_approach.blit(self.image_approach, (self.x - CIRCLE_SIZE * 1.5 + self.growth / 2,
                                                            self.y - CIRCLE_SIZE * 1.5 + self.growth / 2))

            self.growth += 2

    def check_click(self,cursor):
        """
        check if click is inside the hitcircle and change the clicked,
        shoulddraw, clicked and clickedtime values when clicked
        """
        if self.missed is False and self.shoulddraw is True:
            if math.sqrt((self.x - cursor.x)**2 + (self.y - cursor.y)**2) < CIRCLE_SIZE / 2:
                if click is True and self.clicked is False:
                    self.clicked = True
                    self.clicktime = pygame.time.get_ticks()
                    print("x : ", self.x, ", y : ", self.y, ", spawned at : ", self.time, ", clicked at : ",
                          self.clicktime, ", timing : ", (self.clicktime - 820) - self.time)

    def check_hit(self):
        """
        check if hitcircle should be considered hit or missed
        play hitsound when hit successfully
        """
        if self.missed is False and self.clicked is True:
            self.clicked = False
            self.shoulddraw = False
            self.hitsound("hit")

    def check_miss(self):
        """
        check if hitcircle is missed and change missed and shoulddraw values

        valid timing is hardcoded and not properly calculated rn
        """
        if self.missed is False:
            if self.clicktime is not None and self.clicktime - 920 >= self.time \
                    or self.clicktime is not None and self.clicktime - 720 <= self.time:
                self.missed = True
                self.shoulddraw = False
                print("missed : ", (self.clicktime - 820) - self.time)
                self.hitsound("miss")
            if self.time + 1200 <= pygame.time.get_ticks():
                if self.clicktime is None:
                    self.hitsound("miss")
                    self.missed = True
                    print("missed, out of time")
                self.shoulddraw = False

    def hitsound(self,soundtype):
        if not self.soundplayed:
            if soundtype == "miss":
                pygame.mixer.Sound.play(MISSSOUND)
                self.soundplayed = True
            if soundtype == "hit":
                pygame.mixer.Sound.play(HITSOUND)
                self.soundplayed = True


def parse_file(path):
    """
    should parse an osu map and create hitcircles with correct coord values etc etc

    does nothing rn
    """
    f = open(path + '.osu', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')

cursor = Cursor()

circle_number = 10
frame = 0

while running:
    clock.tick(FRAMERATE)
    surface_main.fill(BACKGROUND)
    surface_approach.fill((0,0,0,0))
    surface_cursor.fill((0,0,0,0))

    cursor.x, cursor.y = pygame.mouse.get_pos()

    # input check loop
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_w:
                click = True
            if event.key == K_x:
                click = True

    # handle hitcircles
    for hitcircle in hitcircles:

        # handle hitcircle if clock passed its time value
        if hitcircle.time <= pygame.time.get_ticks():
            hitcircle.check_click(cursor)
            hitcircle.check_miss()
            hitcircle.check_hit()
            hitcircle.draw_circle()
            hitcircle.draw_approach()

    cursor.draw()

    if frame % FRAMERATE == 0:

        # cleanup hitcircle list every second (doesnt need to be done every frame)
        for circle in hitcircles:
            if circle.clicked is True:
                hitcircles.remove(circle)

        # spawns a random hitcircle in the playfield
        hitcircles.append(Hitcircle(randint(64,WIDTH - 64),randint(64,HEIGHT - 64),
                                    pygame.time.get_ticks(),circle_number))

        circle_number += 1
        if circle_number == 15:
            circle_number = 10

    window.blit(surface_main, (0,0))
    window.blit(surface_approach, (0,0))
    window.blit(surface_cursor, (0,0))

    pygame.display.update()
    click = False
    frame += 1

pygame.quit()
