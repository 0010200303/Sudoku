import pygame
import math
import time
import os
import csv

#setup some stuff
pygame.init()
pygame.display.set_caption("Sudoku by BigCrafter13")
pygame.mouse.set_visible(1)
pygame.key.set_repeat(30)

clock = pygame.time.Clock()

#set some standard sizes
border = 20
cellwidth = 80                                              #width of the cell
cellheight = 80                                             #heihgt of the cell
fontname = "freesansbold.ttf"                               #choose font name
font = pygame.font.Font(fontname, 58)                       #choose font

#just colors
black = (0, 0, 0)
gray = (200, 200, 200)
lightgray = (220, 220, 220)
red = (255, 0, 0)
green = (0, 200, 0)
blue = (20, 20, 255)
white = (255, 255, 255)

#some more variable
x = -1
y = -1

index = 0
maxmaps = 1000

smap = [[0 for i in range(9)] for i in range(9)]            #create empty array for later use
cmap = [[0 for i in range(9)] for i in range(9)]            #create empty aaray for later use

smaps = ["0"]

screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)                #setup the pygame window 800 x 800 pixels
screen.fill(white)

def render():
    pygame.display.flip()

def drawgrid():                                                                                         #draw the basic grid
    #minor lines
    for i in range(9):
        pygame.draw.line(screen, gray, (border, cellheight * i + border), (cellwidth * 9 + border, cellheight * i + border), 3)             #draw horizontal lines with border as offset
        pygame.draw.line(screen, gray, (cellwidth * i + border, border), (cellwidth * i + border, cellheight * 9 + border), 3)              #draw vertical lines with border as offset

    #major lines
    for i in range(4):
        pygame.draw.line(screen, black, (border, cellheight * 3 * i + border), (cellwidth * 9 + border, cellheight * 3 * i + border), 4)    #draw horizontal lines with border as offset
        pygame.draw.line(screen, black, (cellwidth * 3 * i + border, border), (cellwidth * 3 * i + border, cellheight * 9 + border), 4)     #draw vertical lines with border as offset

    render()                                                                                                                                #put everything to the screen

def drawcell(x, y):                                                                                                                                     #draw a digit to the cell of given x and y coordinates
    pygame.draw.rect(screen, lightgray, (cellwidth * x + border + 2, cellheight * y + border + 2, cellwidth - 3, cellheight))                           #erase content of cell

    if smap[x][y] != 0:                                                                                                                                 #check if cell is not empty
        celltext = font.render("%d" % smap[x][y], True, black)                                                                                          #create text for the cell
        cellrect = celltext.get_rect(center=(round(cellwidth * x + cellwidth / 2 + border), round(cellheight * y + cellheight / 2 + border)))           #calculate center of cell to print digit
        screen.blit(celltext, cellrect)                                                                                                                 #finally print digit

    render()                                                                                                                                            #put everything to the screen

def drawallcells():                                                                                     #draw all cells at once
    for x in range(9):
        for y in range(9):
            drawcell(x, y)                                                                              #loop through x and y to draw every cell

def highlightcell(x, y, color):
    if x >= 0 and x <= 8 and y >= 0 and y <= 8:                                                                                         #check that x and y dont exceed the game    
        pygame.draw.rect(screen, color, (cellwidth * x + border, cellheight * y + border, cellwidth + 1, cellheight + 1), 2)            #draw rect around specified cell

    render()                                                                                                                            #put everything to the screen
        
def validatecell(x, y, num):                                                        #check if the digit can be set at specified cell
    setable = True

    if cmap[x][y] == -1:                                                            #check if the cell was already set by the map
        print("cell already set by map")
        highlightcell(x, y, red)
        setable = False

    if num == 0:                                                                    #clear the cell no need to check for collision
        return setable

    for i in range(9):                                                              #check if the digit collides with others in a horizontal line
        if i != x:
            if smap[i][y] == num:
                print("horizontal collision")
                highlightcell(i, y, red)
                setable = False

    for i in range(9):                                                              #check if the digit collides with others in a horizontal line
        if i != y:
            if smap[x][i] == num:
                print("vertical collision")
                highlightcell(x, i, red)
                setable = False
    
    for i in range(3):                                                              #check if the digit collides with others in a group    
        for j in range(3):
            xoff = 3 * math.floor(x / 3) + i                                        #get the x position of the cells group
            yoff = 3 * math.floor(y / 3) + j                                        #get the y position of the cells group

            if (xoff, yoff) != (x, y):
                if smap[xoff][yoff] == num:
                    print("group collision")
                    highlightcell(xoff, yoff, red)
                    setable = False

    return setable                                                                  #finally return if the cell can be set

def setcell(x, y, num):                                                             #just sets the cell without checking if its valid
    global smap                                                                     #to change values of the global smap
    global cmap                                                                     #to change values of the global cmap

    smap[x][y] = num                                                                #set digit to specified position
    cmap[x][y] += 1                                                                 #increse count at specified position

    drawcell(x, y)
    highlightcell(x, y, green)

def trysetcell(x, y, num):                                                          #set a cell but first checks if it is valid
    if validatecell(x, y, num):
        setcell(x, y, num)
        return True                                                                 #return whether the cell was setted or not
    return False

def clicked():                                                                      #handle the mouse clicks
    global x
    global y

    x, y = pygame.mouse.get_pos()                                                   #get the mouse position in pixels

    x = round((x - border - cellwidth / 2) / cellwidth)                             #calcute the actually clicked cells form pixel coordinates
    y = round((y - border - cellheight / 2) / cellheight)

    drawgrid()                                                                      #erase previous highlightet cells
    highlightcell(x, y, blue)                                                       #draw new highlight

def reset():                                                                        #just resets the game
    global smap
    global cmap

    for x in range(9):                                                              #loop through the entire map to reset each cell
        for y in range(9):
            smap[x][y] = 0
            cmap[x][y] = 0
    
    screen.fill(white)
    drawallcells()
    drawgrid()

def loadmap(_map):
    global smap
    global cmap

    for x in range(9):                                      #loop through the whole map and set every cell of smap to _map            
        for y in range(9):
            if _map[x][y] != 0:
                smap[x][y] = _map[x][y]
                cmap[x][y] = -1                                 #set cmap at given position to -1 so the game knows that value was set by the map

    drawallcells()
    drawgrid()

def loadtestmap():                                          #just loads an easy test map
    testmap = [ [ 5, 8, 6, 0, 3, 1, 0, 7, 0],  #0           #specify test map
                [ 2, 0, 7, 8, 6, 0, 5, 1, 3],  #1
                [ 0, 1, 0, 7, 0, 5, 2, 0, 6],  #2

                [ 0, 2, 8, 0, 0, 4, 3, 6, 1],  #3
                [ 6, 0, 4, 9, 1, 3, 7, 2, 0],  #4
                [ 0, 3, 1, 6, 2, 0, 0, 9, 5],  #5

                [ 4, 0, 5, 0, 8, 2, 0, 3, 7],  #6
                [ 1, 7, 0, 4, 9, 6, 8, 0, 2],  #7
                [ 0, 6, 2, 3, 5, 0, 1, 0, 9] ] #8

    loadmap(testmap)                                        #finally load the map

def findemptycell():                                        #finds the next empty cell
    for y in range(9):                                      #loop through the map until it finds a new empty map
        for x in range(9):
            if smap[x][y] == 0:
                return (x, y)
    return False                                            #if no empty cell is left it returns false

def solve(sleep):                                           #solve the map using backtrack algorithm
    time.sleep(sleep)                                       #wait x seconds until next step

    empty = findemptycell()

    if empty == False:                                      #return true (solved) if there is no empty cell left
        return True

    x, y = empty                                            #return get the x and y coordinates from empty

    #just for visualization
    drawgrid()                                              #remove past highlights
    highlightcell(x, y, blue)                               #hightlight working cell

    for i in range(1, 10):                                  #the actual algorithm
        if trysetcell(x, y, i):                             #try to set a cell with increasing value
            if solve(sleep):
                return True
            else:
                trysetcell(x, y, 0)                         #set the value of the cell to 0 if it was wrong
    return False

def resize(w, h):                                           #resize the game
    global cellwidth
    global cellheight
    global font

    cellwidth = math.floor((w - border * 2) / 9)                    #calculate the new cellwidth
    cellheight = math.floor((h - border * 2) / 9)                   #calculate the new cellheight
    
    fontwidth = round(cellwidth * 0.8)                              #calculate the new font size
    fontheight = round(cellheight * 0.8)

    if fontwidth <= fontheight:                                     #choose smaller of both sizes
        font = pygame.font.Font(fontname, fontwidth)
    else:
        font = pygame.font.Font(fontname, fontheight)

    screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)      #set the new window
    screen.fill(white)

    drawgrid()
    drawallcells()
    clicked()

def loadmapfromstring(string):                                      #loads a map from a given string
    print("loading map:")
    print(string)

    reset()

    x = 0
    y = 0

    for i in range(len(string)):                                    #loop trhough the whole string
        if x >= 9:                                                  #increase y and reset x each time it reaches the end of the line
            x = 0
            y += 1

        if not trysetcell(x, y, int(string[i])):                    #try to set the strings digits to cells
            print("map not working!!!")

        x += 1

    drawgrid()


def choosemap(i):                                                        #load chosen map from the downloaded file
    global smaps

    path = "sudoku.csv"

    if len(smaps) <= 1:
        print("loading file...")

        with open(path) as file:                                        #open the file
            reader = csv.reader(file)                                   #create a csv reader

            line = -1

            for row in reader:                                          #read all lines and save them
                line += 1

                if line == 0:
                    continue
                elif line == maxmaps:                                   #limit lines to read
                    break

                smaps.append(row[0])
                print(row[0])
            
            print("finished loading")

    loadmapfromstring(smaps[i])                                         #finally load map

def nextmap():                                                          #load the next map
    global index

    if index >= maxmaps - 1:
        index = 0

    index += 1                                                          #increase the current map index
    choosemap(index)                                                    #aaaaand finally load the map

def autoplay(sleep):                                                    #let the backtracking algorithm do all the work
    while True:
        nextmap()
        solve(0)
        time.sleep(sleep)

        if index >= maxmaps - 1:                                        #stop when the algorithm solved every map
            print("solved everything !!!")
            break

reset()
loadtestmap()

running = True
while running:
    clock.tick(69)                                                                  #tick 69 times per second

    for event in pygame.event.get():                                                #loop through the events
        if event.type == pygame.QUIT:
            running = False                                                         #exit the main loop
        elif event.type == pygame.VIDEORESIZE:                                      #resize the game
            resize(event.w, event.h)
        elif event.type == pygame.MOUSEBUTTONUP:
            clicked()
        elif event.type == pygame.KEYUP:                                            #handle the input
            if event.key == pygame.K_ESCAPE:                                        #escape key
                pygame.event.post(pygame.event.Event(pygame.QUIT))                  #post the event to quit the game
            elif event.key == pygame.K_s:                                           #start solving the map
                if solve(0.5):
                    print("Solved!!!")
                else:
                    print("Can't Solve :(")
            elif event.key == pygame.K_1:                                           #get the number keys and set the selected input
                trysetcell(x, y, 1)
            elif event.key == pygame.K_2:
                trysetcell(x, y, 2)
            elif event.key == pygame.K_3:
                trysetcell(x, y, 3)
            elif event.key == pygame.K_4:
                trysetcell(x, y, 4)
            elif event.key == pygame.K_5:
                trysetcell(x, y, 5)
            elif event.key == pygame.K_6:
                trysetcell(x, y, 6)
            elif event.key == pygame.K_7:
                trysetcell(x, y, 7)
            elif event.key == pygame.K_8:
                trysetcell(x, y, 8)
            elif event.key == pygame.K_9:
                trysetcell(x, y, 9)
            elif event.key == pygame.K_0:
                trysetcell(x, y, 0)
            elif event.key == pygame.K_n:                                           #loads the next map
                nextmap()
            elif event.key == pygame.K_a:                                           #plays all the maps itself
                autoplay(0)