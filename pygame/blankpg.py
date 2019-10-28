import pygame as pg, sys
from pygame.locals import *

pg.init()
DISPLAYSURF = pg.display.set_mode((400,300))
pg.display.set_caption("Hello World!")
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    pg.display.update()
