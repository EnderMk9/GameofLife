import numpy as np      # import NumPy
import pygame as pg     # import PyGame
pg.font.init()          # Initialize font module from PyGame
def text_setup():       # Function for creating not changing fonts and texts
    global font, font2, font3, text_game,text_of,text_life,text_paused,text_running,text_it,text_cellst,text_ins1,text_ins2,text_ins3,text_ins4,text_ins5,text_ins6,text_ins7,text_ins8 # Set up these variables as global
    font = pg.font.SysFont(None, int(height/18))                    # We set up font 1 for texts, its size depends on the height of the gird. BIG
    font2 = pg.font.SysFont(None, int(height/25))                   # We set up font 2 for texts, its size depends on the height of the gird. MEDIUM
    font3 = pg.font.SysFont(None, int(height/40))                   # We set up font 3 for texts, its size depends on the height of the gird. SMALL
    text_game = font.render("Game",1,color)                         # TEXT FOR "Game"           color "color"   antialias = 1
    text_of = font.render("of",1,color)                             # TEXT FOR "of"             color "color"   antialias = 1
    text_life = font.render("Life",1,color)                         # TEXT FOR "Life"           color "color"   antialias = 1
    text_paused = font.render("Paused",1,color)                     # TEXT FOR "Paused"         color "color"   antialias = 1
    text_running = font.render("Running",1,color)                   # TEXT FOR "Running"        color "color"   antialias = 1
    text_it = font.render("Iteration:",1,color)                     # TEXT FOR "Iteration"      color "color"   antialias = 1
    text_cellst = font.render("Living Cells:",1,color)              # TEXT FOR "Living cells"   color "color"   antialias = 1
    text_ins1 = font3.render("LClick - Turn alive",1,color)         # TEXT FOR Instruc1         color "color"   antialias = 1
    text_ins2 = font3.render("RClick - Kill cell",1,color)          # TEXT FOR Instruc2         color "color"   antialias = 1
    text_ins3 = font3.render("SPACE - Pause/Unpause",1,color)       # TEXT FOR Instruc3         color "color"   antialias = 1
    text_ins4 = font3.render("Q/W - Increase X/Y of grid",1,color)  # TEXT FOR Instruc4         color "color"   antialias = 1
    text_ins5 = font3.render("A/S - Decrease X/Y of grid",1,color)  # TEXT FOR Instruc5         color "color"   antialias = 1
    text_ins6 = font3.render("BACKSPACE - Reset",1,color)           # TEXT FOR Instruc6         color "color"   antialias = 1
    text_ins7 = font3.render("F - Fill", 1, color)                  # TEXT FOR Instruc7         color "color"   antialias = 1
    text_ins8 = font3.render("ESC - End Game",1,color)              # TEXT FOR Instruc8         color "color"   antialias = 1

width = 900; height = 900                   # Establish width and height of the grid
bg = (200, 200, 200); color = (50, 50, 50)  # Establish background color of window and color for text
border = 1; margin = 10                     # Establish border size of cells and margin of teh grid
celX = 75; celY = 75                        # Establish number of cell in each dimension
celw = width / celX; celh = width / celY    # Establish the width and height of a cell depending on the size of the window and the number of cells
pause = 1; kill = 0                         # Establish the boolean variable pause, which is used to determine whether the game is paused or not. Declare the kill boolean variable, if set to TRUE, the program will end
it = 0                                      # Declare i as the number of iterations of the game
gameState = np.zeros((celX,celY))           # Establishing the matrix gameState which contains the values of all cells, its dimensions are defined with the number of cells
newgameState = np.zeros((celX,celY))        # Declaring the matrix newgameState in which we're going to write the changes before writing them into gameState again

screen = pg.display.set_mode([width + border + (margin*2) + int((width + border + (margin*2))/4),height + border + (margin*2)]) # Set up the display with size defined by width and height of the grid, plus the border so when cells are drawn it does not get cut off the edges, plus the margins times 2  and plus a fourth of the total previous width to display text.
pg.display.set_caption("GAME OF LIFE"); icon = pg.image.load("ICON.ico"); pg.display.set_icon(icon)     # Set up the window title and icon
text_setup()    # Call text_setup function to setup text

def evolve(x,y):    # Function to update the value of cells acording to the rules of the Game of Life, storing that updated state in newgameState
    global it       # set the it variable as global
    nvalue = gameState[(x + 1) % celX, (y + 1) % celY] + \
             gameState[(x) % celX, (y + 1) % celY] + \
             gameState[(x - 1) % celX, (y + 1) % celY] + \
             gameState[(x - 1) % celX, (y) % celY] + \
             gameState[(x - 1) % celX, (y - 1) % celY] + \
             gameState[(x) % celX, (y - 1) % celY] + \
             gameState[(x + 1) % celX, (y - 1) % celY] + \
             gameState[(x + 1) % celX, (y) % celY]  # To know how many living neighbours a cell has, we sum the value of the 8 cells surrounding the cell (excluding it) in the matrix, if the cell is in the edge, the modulus operation will output the cell on the other side, behaving like a torus. For example, in (5,74), if there are 75 cells and it begins counting with 0, when checking for (5,75), it will check for (5,0).

    if gameState[x, y] == 0 and nvalue == 3: newgameState[x, y] = 1  # If the cell is dead (gameState == 0) and has exactly 3 living neighbours, it becomes alive. The changes are made in newgameState
    elif gameState[x, y] == 1 and (nvalue < 2 or nvalue > 3): newgameState[x, y] = 0  # If the cell is alive (gameState == 1) and has lees than 2 or more than three living neighbours, it will die. The changes are made in newgameState

    if x == celX - 1 and y == celY - 1:  # If this is the last cell:
        it += 1  # Add 1 to i to denote that one generation or iteration has passed

def updategrid():   # Function to update the grid
    global celX,celY,celw,celh,pause,gameState,newgameState,color,border,screen     # Set these variables as global
    newgameState = np.copy(gameState)                                               # Set newgameState (the one who'll be printed) as a copy of gameState in case the game is paused, so it remains the same
    for x in range(0,celX):                                                         # Two for loops x and y for the number of cells y each dimension, x and y are the coordinates of the cells. A series of operations are going to happen for each pair of coordinates
        for y in range(0, celY):
            poly = [(round(x*celw        + margin), round(y*celh        + margin)), # This list of points contains the ordered vertices of a square, which will define the shape of the cell.
                    (round(x*celw + celw + margin), round(y*celh        + margin)), # Each vertex is calculated multiplying the cell coordinate with the cell width or height
                    (round(x*celw + celw + margin), round(y*celh + celh + margin)), # and then adding the height or the width depending on the vertex
                    (round(x*celw        + margin), round(y*celh + celh + margin))]

            if not pause: evolve(x,y)                               # If the game is paused, the operations for updating the game will not happen, and the newgameState and later consequently gameState will not change
            pg.draw.polygon(screen, color, poly, 0)                 # Draw the background of the grid, cell by cell
            pg.draw.polygon(screen, (75,75,75), poly, border)       # Draw grid lines, cell by cell, with a defined border (not 0, because that's fill) and a defined colour
            if not newgameState[x,y] == 0: pg.draw.polygon(screen, ((x/celX)*125 +50,(y/celY)*125 + 50,((((celX+1)/(x+1))+((celY+1)/(y+1)))/(celX+celY))*75 +100 ), poly, 0)  # If the cell also is alive (or not dead), the square will be filled (border = 0) with a color which depends on the grid coordinate of the cell
    gameState = newgameState                        # save the changes made in newgameState to gameState
    pg.display.flip()                               # update all the changes on the screen

def update_text(): # Function to update the text on screen
    text_i = font2.render(str(it),1,color)                           # TEXT FOR number of iterations         color "color"   antialias = 1
    text_cells = font2.render(str(int(gameState.sum())),1,color)    # TEXT FOR number of liivng cells       color "color"   antialias = 1
    text_dim = font.render(str(celX) + " x " + str(celY),1,color)   # TEXT FOR dimension of the grid        color "color"   antialias = 1
    text_x = int(width + border + margin*1.5 + int((width+border+2*margin)/8)) # Define the x coordinate for the texts
    screen.blit(text_game,  (text_x - text_game.get_width() // 2,  int(height/20)*1      + margin - text_game.get_height() // 2))
    screen.blit(text_of,    (text_x - text_of.get_width() // 2,    int(height/20)*2      + margin - text_of.get_height() // 2))
    screen.blit(text_life,  (text_x - text_life.get_width() // 2,  int(height/20)*3      + margin - text_life.get_height() // 2))
    screen.blit(text_dim,   (text_x - text_dim.get_width() // 2,   int(height/20)*5      + margin - text_dim.get_height() // 2))
    screen.blit(text_cellst,(text_x - text_cellst.get_width() // 2,int((height/20)*7.5)  + margin - text_cellst.get_height() // 2))
    screen.blit(text_cells, (text_x - text_cells.get_width() // 2, int((height/20)*8.5)  + margin - text_cells.get_height() // 2))
    screen.blit(text_it,    (text_x - text_it.get_width() // 2,    int((height/20)*9.5)  + margin - text_it.get_height() // 2))
    screen.blit(text_i,     (text_x - text_i.get_width() // 2,     int((height/20)*10.5) + margin - text_i.get_height() // 2))
    screen.blit(text_ins1,  (text_x - text_ins1.get_width() // 2,  int((height/20)*15)   + margin - text_ins1.get_height() // 2))
    screen.blit(text_ins2,  (text_x - text_ins2.get_width() // 2,  int((height/20)*15.5) + margin - text_ins2.get_height() // 2))
    screen.blit(text_ins3,  (text_x - text_ins3.get_width() // 2,  int((height/20)*16)   + margin - text_ins3.get_height() // 2))
    screen.blit(text_ins4,  (text_x - text_ins4.get_width() // 2,  int((height/20)*16.5) + margin - text_ins4.get_height() // 2))
    screen.blit(text_ins5,  (text_x - text_ins5.get_width() // 2,  int((height/20)*17)   + margin - text_ins5.get_height() // 2))
    screen.blit(text_ins6,  (text_x - text_ins6.get_width() // 2,  int((height/20)*17.5) + margin - text_ins6.get_height() // 2))
    screen.blit(text_ins7,  (text_x - text_ins7.get_width() // 2,  int((height/20)*18)   + margin - text_ins7.get_height() // 2))
    screen.blit(text_ins8,  (text_x - text_ins8.get_width() // 2,  int((height/20)*18.5)   + margin - text_ins8.get_height() // 2))
    # screen.blit render all the different texts in a relative centered position position to the right of the grid

def updatescreen():     # Function to update the whole screen
    screen.fill(bg)     # We fill the screen with the background to clean everything
    update_text()       # We call the update_text function to update the information displayed by the text
    updategrid()        # We update the grid

def events():           # Function that checks the events recorded by PyGame and acts accordingly if some of those events occur
    global gameState, celX,celY,celw,celh, pause, kill, it                  # Define these variables as global
    for event in pg.event.get():                                                    # Check for every event recorded by pygame
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: pause = not pause  # If the space bar is pressed, the value of game changes, pausing or unpausing the game
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE: kill = 1          # If the ESC key is pressed, the value if kill changes to TRUE
        if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:                # If the backspace key is pressed, the game resets:
            gameState = np.zeros((celX,celY)); it = 0; pause = 1                    # reseting the matrix with zeroes, setting iterations to 0 and pausing the game
        if event.type == pg.KEYDOWN and event.key == pg.K_f:                # If the backspace key is pressed, the game resets:
            gameState = np.ones((celX,celY)); it = 0; pause = 1                     # reseting the matrix with ones, setting iterations to 0 and pausing the game
        if event.type == pg.KEYDOWN and event.key == pg.K_q:                        # If Q key is pressed:
            celX += 1; celw = width / celX                                          # Number of cells in X increases and we recalcule the width of cells
            gameState = np.zeros((celX,celY)); it = 0; pause = 1                    # Resets the game
        if event.type == pg.KEYDOWN and event.key == pg.K_w:                        # If W key is pressed:
            celY += 1; celh = width / celY                                          # Number of cells in Y increases and we recalcule the height of cells
            gameState = np.zeros((celX,celY)); it = 0; pause = 1                    # Resets the game
        if event.type == pg.KEYDOWN and event.key == pg.K_a:                        # If A key is pressed:
            celX -= 1; celw = width / celX                                          # Number of cells in X decreases and we recalcule the width of cells
            gameState = np.zeros((celX,celY)); it = 0; pause = 1                    # Resets the game
        if event.type == pg.KEYDOWN and event.key == pg.K_s:                        # If S key is pressed:
            celY -= 1; celh = width / celY                                          # Number of cells in Y decreases and we recalcule the height of cells
            gameState = np.zeros((celX,celY)); it = 0; pause = 1                    # Resets the game
        if pg.mouse.get_pressed()[0] == 1 and border + margin < pg.mouse.get_pos()[0] < width + border + margin and border + margin < pg.mouse.get_pos()[1] < height + border + margin: # If pressing the left button of the mouse, which is stored in a tuple of 3 coordinates, position 0, and it is clicked within the grid:
            cursor = pg.mouse.get_pos()                                             # Get the coordinates of the cursor
            gameState[int((cursor[0] - border - margin)/celw),int((cursor[1] - border - margin)/celh)] = 1  # Change to 1 (alive) the state of the cell in those coordinates, for that, we divide the coordinates between the size of a cell and then take the integer part
        if pg.mouse.get_pressed()[2] == 1 and border + margin < pg.mouse.get_pos()[0] < width + border + margin and border + margin < pg.mouse.get_pos()[1] < height + border + margin: # If pressing the right button of the mouse, which is stored in a tuple of 3 coordinates, position 2, and it is clicked within the grid:
            cursor = pg.mouse.get_pos()                                             # Get the coordinates of the cursor
            gameState[int((cursor[0] - border - margin)/celw),int((cursor[1] - border - margin)/celh)] = 0  # Change to 0 (dead) the state of the cell in those coordinates, for that, we divide the coordinates between the size of a cell and then take the integer part

def update_title():     # Function to update the title and the information in it
    if not pause:                                                                   # Checks if the game is not paused
        pg.display.set_caption("GAME OF LIFE - " + str(celX) + "x" + str(celY) + " - RUNNING - " + str(int(gameState.sum())) + " CELLS - ITERATION " + str(it))  # Changes the window title to show relevant information, such as the number of cells, whether it's paused or running, the number of living cells and the iteration
        screen.blit(text_running, (width + border + int(width/8) - text_running.get_width() // 2, int((height/20)*4.5) - text_running.get_height() // 2))       # render the RUNNING text
    else:                                                                           # If the game is not unpaused, it's paused
        pg.display.set_caption("GAME OF LIFE - " + str(celX) + "x" + str(celY) + " - PAUSED - " + str(int(gameState.sum())) + " CELLS - ITERATION " + str(it))   # Changes the window title to show relevant information, such as the number of cells, whether it's paused or running, the number of living cells and the iteration
        screen.blit(text_paused, (width + border + int(width/8) - text_paused.get_width() // 2, int((height/20)*4.5) - text_paused.get_height() // 2))          # render the PAUSE text

while not kill:     # Main loop of the game, if Kill is TRUE, it does  not excute
    events()        # Execute events function, which checks if an event is happening and establish a consequence
    updatescreen()  # Update the whole screen using the updatescreen funtion
    update_title()  # Update the title, updating the information calling this function

