import pygame as pg
import random as rn
import sys
import math
from time import sleep
RES = WIDTH, HEIGHT = 1800, 800
FPS = 60
SPEED = 20
clock = pg.time.Clock()

LEFT, RIGHT = 100, 1700
L = RIGHT - LEFT
MIN, MAX = 0, 100
C = 0

sc = pg.display.set_mode(RES)

def f(x):
    if x < L/2:
        return 0
    return 100

cashe = dict()
cashe['0;0'] = f(0)
cashe[str(L)+';0'] = f(L)

def u(x, t):
    if x < t//3 or x > L - (t//3):
        C = 1
    else:
        C = 1
    if t == 0:
        return f(x)
    if (x <= 0):
        return cashe['0;0']
    if (x >= L):
        return cashe[str(L)+';0']
    try:
        return (cashe[str(x - C) + ';' + str(t - 1)] + cashe[str(x + C) + ';' + str(t - 1)]) / 2
    except KeyError:
        if (str(x - C) + ';' + str(t - 1)) not in cashe:
            cashe[str(x - C) + ';' + str(t - 1)] = u(x - C, t - 1)
        if (str(x + C) + ';' + str(t - 1)) not in cashe:
            cashe[str(x + C) + ';' + str(t - 1)] = u(x + C, t - 1)
    return (cashe[str(x - C) + ';' + str(t - 1)] + cashe[str(x + C) + ';' + str(t - 1)]) / 2
    

def minimax():
    x = 0
    minimum = MIN
    maximum = MAX
    for x in range(L):
        if (f(x) < minimum):
            minimum = f(x)
        elif (f(x) > maximum):
            maximum = f(x)
    return minimum, maximum

def getcolor(x, minimum, maximum):
    color = (x - minimum) * 510 / (maximum - minimum)
    color = math.floor(color)
    if color < 0:
        color = 0
    if (color <= 255):
        return (0, color, 255 - color)
    return (color - 255, 510 - color, 0)

def getheight(x, minimum, maximum):
    height = (x - minimum) * 250 / (maximum - minimum)
    height = math.floor(height)
    if height < 0:
        height = 0
    return -height
    

def rectdraw(screen, x, t):
    color = getcolor(u(x - LEFT, t), MIN, MAX)
    pg.draw.rect(screen, color, 
                 (x, 20, 1, 75))
    pg.draw.circle(screen, (255, 255, 255),
                   (x, getheight(u(x - LEFT, t), MIN, MAX) + 500), 1)

MIN, MAX = minimax()
t = 0

while True:
    sc.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)

    for i in range(LEFT, RIGHT):
        rectdraw(sc, i, t)
    t += 10
    pg.display.update()
    clock.tick(FPS)
