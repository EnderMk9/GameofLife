import numpy as np
import time
import pygame as pg

width = 1000
height = 1000
border = 1
bg = (35, 35, 35)
color = (125, 125, 125)
celX = 75
celY = 75
celw = width / celX
celh = width / celY
pause = 1
kill = 0
i=0

screen = pg.display.set_mode([width + border,height + border])
icon = pg.image.load("ICON.ico")
pg.display.set_caption("GAME OF LIFE")
pg.display.set_icon(icon)
screen.fill(bg)
gameState = np.zeros((celX,celY))
while 1:
    if not pause:
        time.sleep(2/celX)
        pg.display.set_caption("GAME OF LIFE - " + str(celX) + "x" + str(celY) + " - RUNNING - " + str(int(gameState.sum())) + " CELLS - ITERATION " + str(i))
    else:
        pg.display.set_caption("GAME OF LIFE - " + str(celX) + "x" + str(celY) + " - PAUSED - " + str(int(gameState.sum())) + " CELLS - ITERATION " + str(i))
    ev = pg.event.get()
    mouse = pg.mouse.get_pressed()
    for event in ev:
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: pause = not pause
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE: kill = 1
        if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:
            gameState = np.zeros((celX,celY)); i = 0; pause = 1
        if event.type == pg.KEYDOWN and event.key == pg.K_w:
            celX += 1; celY += 1
            celw = width / celX; celh = width / celY
            gameState = np.zeros((celX,celY)); i = 0; pause = 1
        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            celX -= 1; celY -= 1
            celw = width / celX; celh = width / celY
            gameState = np.zeros((celX,celY)); i = 0; pause = 1
        if mouse[0] == 1:
            cursor = pg.mouse.get_pos()
            gameState[int(cursor[1]/celh),int(cursor[0]/celw)] = 1
        if mouse[2] == 1:
            cursor = pg.mouse.get_pos()
            gameState[int(cursor[1]/celh),int(cursor[0]/celw)]  = 0
    if kill: break

    newgameState = np.copy(gameState)
    screen.fill(bg)
    for x in range(0,celX):
        for y in range(0, celY):
            poly = [(round(x*celw         ), round(y*celh        )),
                    (round(x*celw + celw  ), round(y*celh        )),
                    (round(x*celw + celw  ), round(y*celh + celh )),
                    (round(x*celw         ), round(y*celh + celh ))]
            if not pause:
                nvalue = gameState[(x+1) % celX , (y+1) % celY  ] + \
                         gameState[(x)   % celX , (y+1) % celY  ] + \
                         gameState[(x-1) % celX , (y+1) % celY  ] + \
                         gameState[(x-1) % celX , (y)   % celY  ] + \
                         gameState[(x-1) % celX , (y-1) % celY  ] + \
                         gameState[(x)   % celX , (y-1) % celY  ] + \
                         gameState[(x+1) % celX , (y-1) % celY  ] + \
                         gameState[(x+1) % celX , (y)   % celY  ]

                if gameState[x,y] == 0 and nvalue == 3: newgameState[x,y] = 1
                elif gameState[x,y] == 1 and (nvalue < 2 or nvalue > 3): newgameState[x,y] = 0
                if x == celX-1 and y == celY-1:
                    i += 1
            pg.draw.polygon(screen, color, poly, border)
            if not newgameState[y,x] == 0: pg.draw.polygon(screen, color, poly, 0)
    gameState = newgameState
    pg.display.flip()
