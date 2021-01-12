import pygame,colorsys,random

"""
    John Conway's Game of Life - written in python/pygame

    GoL is intrinsicly a zero player game, just enjoy watching it evolve
    Controls are outlined in the event handling code
    The board is modulo wrapped so things will appear on other side of the window

    This is far from the fastest or most efficient implemenation of GoL
    Currently it iterates every cell on board and counts neighbours
    Then updates board state from number of neighbours - I am happy with it

    Source code by Benjamin Christian
"""

#program constants
black=(31,31,31) #background color is not entirely black

#boards above ~120 tiles will run too slow for realtime simulation
tile_size=8 #size of each cell
num_tiles=120 #number of tiles, squared

fps=30 #framerate
base_color=random.randint(1,6283)/1000 #randomly rotates base color on colorwheel
gradient=1000 #gradient means smoother color change between generations

editing=1 #flag to determine whether editing (default is true)
clicked=[0,0] #flag for whether the mouse button is being clicked

placing=0 #currently not placing any structures

#pygame boilerplate
pygame.init()
win=pygame.display.set_mode(([num_tiles*tile_size]*2)) #precompute window size
pygame.display.set_caption("Game of Life")
clock=pygame.time.Clock()

#board object
board=[[[0,0] for i in range(num_tiles)] for j in range(num_tiles)]
tiles=[i for i in range(num_tiles)]

#some structures to consider
structs=[
    [   #nothing
        [0,0]
    ],
    [   #gospers glider
        [0,0],[0,1],
        [1,0],[1,1],
        [10,0],[10,1],[10,2],
        [11,-1],[11,3],
        [12,-2],[12,4],
        [13,-2],[13,4],
        [14,1],
        [15,-1],[15,3],
        [16,0],[16,1],[16,2],
        [17,1],
        [20,-2],[20,-1],[20,0],
        [21,-2],[21,-1],[21,0],
        [22,-3],[22,1],
        [24,-4],[24,-3],[24,1],[24,2],
        [34,-2],[34,-1],
        [35,-2],[35,-1]
    ],
    [   #copperhead - symmetry if i could figure it out...
        [0,5],[0,7],[0,8],
        [1,4],[1,11],
        [2,3],[2,4],[2,8],[2,11],
        [3,0],[3,1],[3,3],[3,9],[3,10],
        [4,0],[4,1],[4,3],[4,9],[4,10],
        [5,3],[5,4],[5,8],[5,11],
        [6,4],[6,11],
        [7,5],[7,7],[7,8]
    ]
]

num_structs=3

#set tile state (dead or alive)
def set_tile(x,y,state):
	#modulo wrapping the set function
	board[x%num_tiles][y%num_tiles][0]=state #write in either true/false
	board[x%num_tiles][y%num_tiles][1]=state #generation happens to have the same value as state for 0 and 1

#check for life
def alive(x,y):
    #modulo wrapping the check function
    return board[x%num_tiles][y%num_tiles][0]

#draw board
def draw():
    win.fill(black)
    for x in range(num_tiles):
        for y in range(num_tiles):
            if board[x][y][0]:
                #create and draw rectangle if tile is alive
                pygame.draw.rect(win,
                    #get color of tile from generation
                    tuple(round(i*255) for i in colorsys.hsv_to_rgb(base_color+board[x][y][1]/gradient,1,1)),
                    #create rectangle object to draw
                    pygame.Rect(
                        x*tile_size,
                        y*tile_size,
                        tile_size,tile_size))
    pygame.display.flip()

"""
    Compute number of neighbours of each cell on board

    This currently just loops across every cell and its surrounding cells
    Eventually I would like to implement a faster algorithm (convolution or hashmap)
    But for now this will have to do -> even though it is truly slow
"""
#static kernel to index surrounding cells
kernel=(
    (-1,-1),(-1,0),(-1,1),
    (0,-1),(0,1),
    (1,-1),(1,0),(1,1)
)
def neighbours():
    #empty list of neighbours count
    n=[[0 for i in range(num_tiles)] for j in range(num_tiles)]
    for x in tiles:
        for y in tiles:
            #this is the bottleneck
            for block in kernel:
                n[x][y]+=alive(x+block[0],y+block[1])
    return n

#update board state from neighbours function and rules of life
def update():
    #first capture the number of neighbours of every cell
    n=neighbours()
    #now update board
    for x in tiles:
        for y in tiles:
            #The rules of life in code
            if n[x][y]<2:
                set_tile(x,y,False) #death by starvation
            elif n[x][y]>3:
                set_tile(x,y,False)	#death by overpopulation
            elif n[x][y]==3:
                set_tile(x,y,True)  #reproduction occurs
            if board[x][y][0]:
                if board[x][y][1]<gradient:
                    board[x][y][1]+=1   #increment if surviving another generation

#delete everything on board
def clear():
    for i in tiles:
        for j in tiles:
            board[i][j][0]=0 #set every tile to not alive

#randomise the board state -> bias affects how likely life is to spawn at cell (0-100)
bias=10 #recommened keeping this below ~25
def randomise():
    for x in tiles:
        for y in tiles:
            if random.randint(0,100)<bias:
                set_tile(x,y,True)

while 1:
    #first get the mouse position
    mouse=pygame.mouse.get_pos()
    #Start event handling
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            quit()
        """     CONTROLS
            **GoL is a zero player game by design**
            Left click/hold - create life
            Right click/hold - destroy life
            Space - toggle editing (clicking automatically puts into editing mode)
            c - clear the board
            s - save the board
            r - read from board file (if available)
            w - wild card, randomly generate board state
            b - randomise the base color for palette generator
            p - place some pre defined structures (gospers glider gun, etc.)
            Escape - quit program
        """
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                quit()
            if event.key==pygame.K_SPACE:
                editing^=1 #toggle editing
            if event.key==pygame.K_c:
                clear()
            if event.key==pygame.K_w:
                clear()
                randomise()
            if event.key==pygame.K_b:
                base_color=random.randint(1,6283)/1000 #randomly rotates base color on colorwheel
            #request to place a structure on the field
            if event.key==pygame.K_p:
                placing+=1 #iterate through structures
                placing%=num_structs #wrap structure selection
        """
            Mouse handling done by setting/unsetting a flag
            If the flag is set, every game update sets tile at position
            Clicking mouse button also switches into editing mode by default
        """
        if event.type==pygame.MOUSEBUTTONDOWN:
            editing=1
            if event.button==1: #left button
                clicked[0]=1
            if event.button==3: #right button
                clicked[1]=1
        if event.type==pygame.MOUSEBUTTONUP:
            editing=1
            if event.button==1:
                clicked[0]=0
            if event.button==3:
                clicked[1]=0
    #End event handling
    #check if buttons are clicked/held and set life accordingly
    if editing:
        if clicked[0]:
            for tile in range(len(structs[placing])):
                set_tile(
                    event.pos[0]//tile_size+structs[placing][tile][0]%num_tiles,
                    event.pos[1]//tile_size+structs[placing][tile][1]%num_tiles,
                True)
        if clicked[1]:
            set_tile(event.pos[0]//tile_size,event.pos[1]//tile_size,False)
    else:
        update()  #update game state if we are not editing
        clock.tick(fps) #only need to regulate framerate when simulating
    draw() #call board draw method
