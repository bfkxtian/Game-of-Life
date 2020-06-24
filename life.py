import pygame

#some variables
WHITE = ( 255, 255, 255 )
BLACK = ( 0, 0, 0 )
cell = 10 #size of each cell
tiles = 80 #number of tiles, squared

#pygame boilerplate
pygame.init( ) #start pygame
win = pygame.display.set_mode( ( tiles * cell, tiles * cell ) ) #create drawing surface
pygame.display.set_caption( "Game of Life" )
clock = pygame.time.Clock( ) #pygame clock

#initialise board
board = [ [ 0 for i in range( tiles ) ] for j in range( tiles ) ]

#check if valid cell
def check( x, y ):
    if x < 0 or x >= tiles or y < 0 or y >= tiles:
        return 0
    return 1

#kill a cell
def kill( x, y ):
    if check( x, y ):
        board[ x ][ y ] = 0
    
#create a new cell
def create( x, y ):
    if check( x, y ):
        board[ x ][ y ] = 1

#draw function
def draw( ):
    win.fill( BLACK )
    for x in range( tiles ):
        for y in range( tiles ):
            if board[ x ][ y ]:
                pygame.draw.rect( win, WHITE, pygame.Rect( x * cell, y * cell, cell, cell ) )

#get board state (if valid)
def alive( x, y ):
    if not check( x, y ):
        return 0 #since this is an invalid tile
    if board[ x ][ y ]:
        return 1
    return 0

#update cell life
def update( ):
    n = [ [ 0 for i in range( tiles ) ] for j in range( tiles ) ]
    for x in range( tiles ):
        for y in range( tiles ):
            #check this cell ^ with surrounding cells
            for i in range( -1, 2 ):
                for j in range( -1, 2 ):
                    if i == 0 and j == 0:
                        continue #don't count self
                    if alive( x + i, y + j ):
                        n[ x ][ y ] += 1
    #now update board
    for x in range( tiles ):
        for y in range( tiles ):
            if n[ x ][ y ] < 2:
                kill( x, y ) #underpopulation
            if n[ x ][ y ] > 3:
                kill( x, y ) #overpopulation
            if n[ x ][ y ] == 3:
                create( x, y ) #reproduction

#editor mode
def editor( ):
    editing = 1
    print( "Editing" )
    while editing:
        for event in pygame.event.get( ):
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #left button
                    create( event.pos[ 0 ] // cell, event.pos[ 1 ] // cell )
                if event.button == 3: #right button
                    kill( event.pos[ 0 ] // cell, event.pos[ 1 ] // cell )
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0
                if event.key == pygame.K_SPACE:
                    return 1
        draw( )
        pygame.display.flip( )
            
#main loop
def main( ):
    state = 1
    editor( )
    print( "Press SPACE to toggle editing")
    while state:
        clock.tick( 10 ) #best enjoyed at 10fps
        for event in pygame.event.get( ):
            if event.type == pygame.QUIT:
                state = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = 0
                if event.key == pygame.K_SPACE:
                    state = editor( )
                    print( "Done editing" )
        update( ) #update the game state
        draw( ) #draw next frame in memory
        pygame.display.flip( ) #push everything to display
main( )

print( "Exiting" )
pygame.quit( ) #quit pygame
