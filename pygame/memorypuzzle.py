import pygame as pg, random, sys, time
from pygame.locals import *
FPS = 30
WIDTH = 640
HEIGHT = 480
REVEALSPEED = 8
BOXSIZE = 40
GAPSIZE = 10
BOARDWIDTH = 5#10
BOARDHEIGHT = 4#7
assert (BOARDWIDTH*BOARDHEIGHT)%2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WIDTH - (BOARDWIDTH*(BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int ((HEIGHT - (BOARDHEIGHT*(BOXSIZE + GAPSIZE))) / 2)
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS)*len(ALLSHAPES)*2 >= BOARDWIDTH * BOARDHEIGHT, 'Board is too big for the number of shapes/colors defined.'



def main():
    global FPSCLOCK, DISPLAYSURF, Flag_win
    Flag_win = False
    pg.init()
    FPSCLOCK = pg.time.Clock()
    DISPLAYSURF = pg.display.set_mode((WIDTH, HEIGHT))
    #Sound
    pg.mixer.music.load('bg2.mp3')
    pg.mixer.music.play(-1,0.0)
    RevealSound = pg.mixer.Sound('reveal.wav')
    WrongSound = pg.mixer.Sound('wrong.wav')
    CorrectSound = pg.mixer.Sound('correct.wav')

    #Text
    fontObj = pg.font.Font('freesansbold.ttf',32)
    textSurfaceObj = fontObj.render('...Memory Game...', True, GREEN, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (WIDTH/2, HEIGHT/8)

    textSurfaceObj2 = fontObj.render('...You Win...', True, GREEN, BLUE)
    textRectObj2 = textSurfaceObj2.get_rect()
    textRectObj2.center = (WIDTH/2, HEIGHT/8)

    #Event
    mousex = 0
    mousey = 0
    pg.display.set_caption('Memory Game')
    
    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None
    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)
    while True:
        mouseClicked = False
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes)
        if not Flag_win:
            DISPLAYSURF.blit(textSurfaceObj, textRectObj)
        else:
            DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pg.mixer.music.stop()
                pg.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        
        if boxx !=None and boxy!= None:
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True
                RevealSound.play()
                pg.time.wait(1000)
                RevealSound.stop()
                if firstSelection == None:
                    firstSelection = (boxx, boxy)
                else:
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)
                    if icon1shape != icon2shape or icon1color != icon2color:
                        WrongSound.play()
                        pg.time.wait(1000)
                        WrongSound.stop()
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):
                        Flag_win = True
                        gameWonAnimation(mainBoard)
                        
                        pg.time.wait(2000)

                        #reset Board
                        drawBoard(mainBoard, revealedBoxes)
                        
                        pg.display.update()

                        #replay the start game animation
                        startGameAnimation(mainBoard)
                        
                    elif icon1shape == icon2shape and icon1color == icon2color:
                        CorrectSound.play()
                        pg.time.wait(1000)
                        CorrectSound.stop()
                    firstSelection = None
        pg.display.update()
        FPSCLOCK.tick(FPS)
def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val]*BOARDHEIGHT)
    return revealedBoxes
def getRandomizedBoard():
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color))
    random.shuffle(icons)
    numIconsUsed = int(BOARDWIDTH*BOARDHEIGHT/2)
    icons = icons[:numIconsUsed]*2
    random.shuffle(icons)
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board
def splitIntoGroupOf(groupSize, List):
    result = []
    for i in range(0, len(List), groupSize):
        result.append(List[i:i + groupSize])
    return result
def leftTopCoordsOfBox(boxx, boxy):
    left = boxx*(BOXSIZE+GAPSIZE) + XMARGIN
    top = boxy*(BOXSIZE+GAPSIZE) + YMARGIN
    return (left, top)
def getBoxAtPixel(x,y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx,boxy)
            boxRect = pg.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x,y):
                return (boxx, boxy)
    return (None, None)
    
def drawIcon(shape, color, boxx, boxy):
    quater = int(BOXSIZE*0.25)
    half = int(BOXSIZE*0.5)
    left, top = leftTopCoordsOfBox(boxx, boxy)
    if shape == DONUT:
        pg.draw.circle(DISPLAYSURF, color, (left+half,top + half), half - 5)
        pg.draw.circle(DISPLAYSURF, BGCOLOR, (left+half, top+half),quater-5)
    elif shape == SQUARE:
        pg.draw.rect(DISPLAYSURF, color, (left + quater, top + quater, BOXSIZE-half,BOXSIZE-half))
    elif shape == DIAMOND:
        pg.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE -1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pg.draw.line(DISPLAYSURF,color, (left, top + i), (left+i, top))
            pg.draw.line(DISPLAYSURF, color, (left+i, top + BOXSIZE-1), (left + BOXSIZE -1, top +i))
    elif shape == OVAL:
        pg.draw.ellipse(DISPLAYSURF, color, (left, top + quater, BOXSIZE, half))
def getShapeAndColor(board, boxx, boxy):
    #print boxx, boxy
    #left, top = leftTopCoordsOfBox(boxx, boxy)
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board, boxes, coverage):
    #print board
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pg.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        # print box[0], box[1]
        shape, color = getShapeAndColor(board, box[0], box[1])

        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:
            pg.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pg.display.update()
    FPSCLOCK.tick(FPS)

def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(BOXSIZE, (-REVEALSPEED)-1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToCover):
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)

def drawBoard(board, revealed):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                pg.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)
def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pg.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left -5, top -5, BOXSIZE +10, BOXSIZE +10), 4)
def startGameAnimation(board):
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x,y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)

def gameWonAnimation(board):
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR
    for i in range(13):
        color1, color2 = color2, color1
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pg.display.update()
        pg.time.wait(300)

def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True

if __name__ == '__main__':
   main()
