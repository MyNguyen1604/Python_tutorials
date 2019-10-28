import pygame as pg, sys
from pygame.locals import *

#set up
pg.init()
FPS = 30
fpsClock = pg.time.Clock()

DISPLAYSURF = pg.display.set_mode((400, 300),0,32)
pg.display.set_caption("Amination")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
catImg = pg.image.load("cat.png")
catx = 10
caty = 10
direction = 'right'

flag = 0;
count = 0;
#run
pg.mixer.music.load('bg.mp3')
pg.mixer.music.play(-1, 0.0)
while True:
    if flag == 0:
        DISPLAYSURF.fill(WHITE)
    else:
        DISPLAYSURF.fill(BLACK)
    #DISPLAYSURF.fill(WHITE)
    if direction == 'right':
        catx += 5
        if catx == 280:
            direction = 'down'
    elif direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'
    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'
    elif direction == 'up':
        caty -= 5
        if caty == 10:
            direction = 'right'
            count += 1
    if (count == 2) & (flag != 1):
        flag = 1
        count = 0
    elif (count == 2) & (flag == 1):
        flag = 0
        count = 0

    DISPLAYSURF.blit(catImg,(catx,caty))
    for event in pg.event.get():
        if event.type == QUIT:
            pg.mixer.music.stop()
            pg.quit()
            sys.exit()
    pg.display.update()
    fpsClock.tick(FPS)
        
