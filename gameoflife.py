import numpy as np      # import NumPy
import time             # import Time
import pygame as pg     # import PyGame
import math             # import Math

width = 1000; height = 1000                 # Establish width and height of the window
bg = (35, 35, 35)                           # Establish background color of window
border = 1; color = (125, 125, 125)         # Establish color and border size of cells
celX = 75; celY = 75                        # Establish number of cell in each dimension
celw = width / celX; celh = width / celY    # Establish the width and height of a cell depending on the size of the window and the number of cells
pause = 1                                   # Establish the boolean variable pause, which is used to determine whether the game is paused or not
kill = 0                                    # Declare the kill boolean variable, if set to TRUE, the program will end
i=0                                         # Declare i as the number of iterations of the game

screen = pg.display.set_mode([width + border,height + border])                                          # Set up the display with size defined by width and height, plus the border so when cells are drawn it does not get cut off the edges
pg.display.set_caption("GAME OF LIFE"); icon = pg.image.load("ICON.ico"); pg.display.set_icon(icon)     # Set up the window title and icon
screen.fill(bg)                                                                                         # Coloring the background with the colour established in bg
gameState = np.zeros((celX,celY))                                                                       # Establishing the matrix gameState which contains the values of all cells, its dimensions are defined with the number of cells
while 1:                                                                            # Main loop of the game, if it ends (and the only way is through a break statement), the game ends
    if not pause:                                                                   # Checks if the game is not paused
        time.sleep(4/math.sqrt(celX*celY))                                          # Creates a delay proportional to the number of cells
        pg.display.set_caption("GAME OF LIFE - " + str(celX) + "x" + str(celY) + " - RUNNING - " + str(int(gameState.sum())) + " CELLS - ITERATION " + str(i))  # Changes the window title to show relevant information, such as the number of cells, whether it's paused or running, the number of living cells and the iteration
    else:                                                                           # If the game is not unpaused, it's paused
        pg.display.set_caption("GAME OF LIFE - " + str(celX) + "x" + str(celY) + " - PAUSED - " + str(int(gameState.sum())) + " CELLS - ITERATION " + str(i))   # Changes the window title to show relevant information, such as the number of cells, whether it's paused or running, the number of living cells and the iteration
    ev = pg.event.get()                                                             # Get events from PyGame, inputs. Storing it into a variable
    mouse = pg.mouse.get_pressed()                                                  # Get which buttons of the mouse are pressed, storing it into a tuple
    for event in ev:                                                                # Check for every event
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: pause = not pause  # If the space bar is pressed, the value of game changes, pausing or unpausing the game
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE: kill = 1          # If the ESC key is pressed, the value if kill changes to TRUE
        if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:                # If the backspace key is pressed, the game resets:
            gameState = np.zeros((celX,celY)); i = 0; pause = 1                     # reseting the matrix with zeroes, setting iterations to 0 and pausing the game
        if event.type == pg.KEYDOWN and event.key == pg.K_q:                        # If Q key is pressed:
            celX += 1; celw = width / celX                                          # Number of cells in X increases and we recalcule the width of cells
            gameState = np.zeros((celX,celY)); i = 0; pause = 1                     # Resets the game
        if event.type == pg.KEYDOWN and event.key == pg.K_w:                        # If W key is pressed:
            celY += 1; celh = width / celY                                          # Number of cells in Y increases and we recalcule the height of cells
            gameState = np.zeros((celX,celY)); i = 0; pause = 1                     # Resets the game
        if event.type == pg.KEYDOWN and event.key == pg.K_a:                        # If A key is pressed:
            celX -= 1; celw = width / celX                                          # Number of cells in X decreases and we recalcule the width of cells
            gameState = np.zeros((celX,celY)); i = 0; pause = 1                     # Resets the game
        if event.type == pg.KEYDOWN and event.key == pg.K_s:                        # If S key is pressed:
            celY -= 1; celh = width / celY                                          # Number of cells in Y decreases and we recalcule the height of cells
            gameState = np.zeros((celX,celY)); i = 0; pause = 1                     # Resets the game
        if mouse[0] == 1:                                                           # If pressing the left button of the mouse:
            cursor = pg.mouse.get_pos()                                             # Get the coordinates of the cursor
            gameState[int(cursor[0]/celw),int(cursor[1]/celh)] = 1                  # Change to 1 (alive) the state of the cell in those coordinates, for that, we divide the coordinates between the size of a cell and then take the integer part
        if mouse[2] == 1:                                                           # If pressing the right button of the mouse:
            cursor = pg.mouse.get_pos()                                             # Get the coordinates of the cursor
            gameState[int(cursor[0]/celw),int(cursor[1]/celh)]  = 0                 # Change to 0 (dead) the state of the cell in those coordinates, for that, we divide the coordinates between the size of a cell and then take the integer part
    if kill: break                                                                  # If kill is TRUE, the while loop breaks and the program ends
    newgameState = np.copy(gameState)                                               # We make a copy of the game matrix in which we are going to make the changes each generation so we do not overwrite gameState while we are reading it
    screen.fill(bg)                                                                 # We fill the screen with the background to clean everything
    for x in range(0,celX):                                                         # Two for loops x and y for the number of cells y each dimension, x and y are the coordinates of the cells. A series of operations are going to happen for each pair of coordinates
        for y in range(0, celY):
            poly = [(round(x*celw         ), round(y*celh        )),                # This list of points contains the ordered vertices of a square, which will define the shape of the cell.
                    (round(x*celw + celw  ), round(y*celh        )),                # Each vertex is calculated multiplying the cell coordinate with the cell width or height
                    (round(x*celw + celw  ), round(y*celh + celh )),                # and then adding the height or the width depending on the vertex
                    (round(x*celw         ), round(y*celh + celh ))]
            if not pause:                                                           # If the game is paused, the operations for updating the game will not happen, and the gameState will not change
                nvalue = gameState[(x+1) % celX , (y+1) % celY  ] + \
                         gameState[(x)   % celX , (y+1) % celY  ] + \
                         gameState[(x-1) % celX , (y+1) % celY  ] + \
                         gameState[(x-1) % celX , (y)   % celY  ] + \
                         gameState[(x-1) % celX , (y-1) % celY  ] + \
                         gameState[(x)   % celX , (y-1) % celY  ] + \
                         gameState[(x+1) % celX , (y-1) % celY  ] + \
                         gameState[(x+1) % celX , (y)   % celY  ]  # To know how many living neighbours a cell has, we sum the value of the 8 cells surrounding the cell (excluding it) in the matrix, if the cell is in the edge, the modulus operation will output the cell on the other side, behaving like a torus. For example, in (5,74), if there are 75 cells and it begins counting with 0, when checking for (5,75), it will check for (5,0).
                if gameState[x,y] == 0 and nvalue == 3: newgameState[x,y] = 1                   # If the cell is dead (gameState == 0) and has exactly 3 living neighbours, it becomes alive. The changes are made in newgameState
                elif gameState[x,y] == 1 and (nvalue < 2 or nvalue > 3): newgameState[x,y] = 0  # If the cell is alive (gameState == 1) and has lees than 2 or more than three living neighbours, it will die. The changes are made in newgameState
                if x == celX-1 and y == celY-1:                                     # If this is the last cell:
                    i += 1                                                          # Add 1 to i to denote that one generation or iteration has passed
            pg.draw.polygon(screen, color, poly, border)                                    # Draw the cell grid for each cell, with a defined border (not 0, because that's fill) and a defined colour     These two always happen even if the game is paused
            if not newgameState[x,y] == 0: pg.draw.polygon(screen, color, poly, 0)          # If the cell also is alive (or not dead), the square will be filled (border = 0)                               These two always happen even if the game is paused
    gameState = newgameState                        # save the changes made in newgameState to gameState
    pg.display.flip()                               # update all the changes on the screen
