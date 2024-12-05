import argparse
import pygame
from collections import deque
import random as rd

############### Setting up classes needed for this code. ###############

class Tile:
    
    def __init__(self,size,loc : tuple):
        self._size = size
        self._loc = loc
    
    def draw(self,screen,colour):
        size = self._size
        rect = pygame.Rect(self._loc[1]*size,self._loc[0]*size,size,size)
        pygame.draw.rect(screen,colour,rect)


class Checkerboard:
    
    def __init__(self,lines,columns,tile_size):
        self._lines = lines
        self._columns = columns
        self._tile_size = tile_size
    
    def draw(self,screen,colour_1=(0,0,0),colour_2=(255,255,255)):
        '''Draws a checkerboard with colours 1 and 2.'''
        
        tile_size = self._tile_size
        screen.fill(colour_1)

        for i in range(self._lines):
            for j in range(self._columns):
                if (i+j)%2 == 0:
                    tile = Tile(tile_size,(i,j))
                    tile.draw(screen,colour_2)

class Snake:
    
    def __init__(self, tiles : deque, tile_size,colour=(0,255,0)):
        '''A snake of shape (i,j): i lines and j columns, at location (x,y).'''
        self._tiles = tiles
        self._length = len(tiles)
        self._tile_size = tile_size
        self._colour = colour
        self._popped = None # This will store the last known position of the snake's tail.

    def __contains__(self,tile):
        return(tile == self._tiles[-1])

    def draw(self,screen):
        for tile in self._tiles:
            S_Tile = Tile(self._tile_size,(tile[1],tile[0]))
            S_Tile.draw(screen,self._colour)
    
    def moveRight(self):
        (head_x,head_y) = self._tiles[-1]
        self._tiles.append((head_x + 1,head_y))
        self._popped = self._tiles[0]
        self._tiles.popleft()
    def moveLeft(self):
        (head_x,head_y) = self._tiles[-1]
        self._tiles.append((head_x - 1,head_y))
        self._popped = self._tiles[0]
        self._tiles.popleft()
    def moveUp(self):
        (head_x,head_y) = self._tiles[-1]
        self._tiles.append((head_x,head_y - 1))
        self._popped = self._tiles[0]
        self._tiles.popleft()
    def moveDown(self):
        (head_x,head_y) = self._tiles[-1]
        self._tiles.append((head_x,head_y + 1))
        self._popped = self._tiles[0]
        self._tiles.popleft()

    def move(self,direction):
        if direction == 'Right':
            self.moveRight()
        if direction == 'Left':
            self.moveLeft()
        if direction == 'Up':
            self.moveUp()
        if direction == 'Down':
            self.moveDown()
    
    def lengthen(self):
        self._tiles.appendleft(self._popped)

############### Main functions. ###############

def arguments():
    '''Defines the arguments taken by the snake() function.'''

    MIN = 5

    DEFAULT_LINES = 20
    DEFAULT_COLUMNS = 40

    # Declares acceptable arguments.
    parser = argparse.ArgumentParser(description='Set width and height of game window.')
    parser.add_argument('-l','--lines',type=int,help="No. of lines of window",default=DEFAULT_LINES)
    parser.add_argument('-c','--columns',type=int,help="No. of columns of window",default=DEFAULT_COLUMNS)
    args = parser.parse_args()

    if (args.lines < MIN) or (args.columns < MIN):
        raise ValueError("Width and height must be greater or equal to %d." % MIN)
    
    return(args)

def snake():
    '''Snake Game
    * Press Q or click on the close button to end the game.'''
  
    args = arguments()
    cols,lines = args.columns,args.lines
    tile_size = 20

    pygame.init()

    screen = pygame.display.set_mode((cols*tile_size,lines*tile_size))

    clock = pygame.time.Clock()

    snake = Snake(deque([(10,5),(11,5),(12,5),(13,5),(14,5)]),tile_size)

    # Setting a bool to indicate if the game should continue.
    run = True

    # Bools that indicate the latest direction and whether a fruit is present.

    direction = 'Right'
    fruit1 = False
    fruit_tile = None
    
    ##### Main game loop
    while run:

        clock.tick(5) # Here you can adjust the number of FPS.
        changed_direction = False

        # This loop checks for keyboard inputs.
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                # Keyboard interrupt
                if event.key == pygame.K_q:
                    run = False
                # Direction inputs
                if event.key == pygame.K_RIGHT:
                    if (direction != 'Right') and (direction != 'Left'): # Can't ask for reverse course.
                        snake.moveRight()
                        direction = 'Right'
                        changed_direction = True
                if event.key == pygame.K_LEFT:
                    if (direction != 'Left') and (direction != 'Right'):
                        snake.moveLeft()
                        direction = 'Left'
                        changed_direction = True
                if event.key == pygame.K_UP:
                    if (direction != 'Up') and (direction != 'Down'):
                        snake.moveUp()
                        direction = 'Up'
                        changed_direction = True
                if event.key == pygame.K_DOWN:
                    if (direction != 'Down') and (direction != 'Up'):
                        snake.moveDown()
                        direction = 'Down'
                        changed_direction = True
            # Window interrupt
            if event.type == pygame.QUIT:
                run = False
        
        # When the player asks for no specific direction change, the snake should continue in the same direction as before.
        if not changed_direction:
            snake.move(direction)
        
        # Checking whether the snake has reached the edge of the board.
        if (snake._tiles[-1][0] == cols - 1) or (snake._tiles[-1][0] == 0) or (snake._tiles[-1][1] == lines - 1) or (snake._tiles[-1][1] == 0):
            run = False
        
        checkerboard = Checkerboard(lines,cols,tile_size)
        checkerboard.draw(screen)

        # Setting up fruits.
        fruits = [(3,3),(10,15)]
        
        if not fruit1:
            fruit = rd.choice(fruits)
            fruit_tile = Tile(tile_size,fruit)
            fruit1 = True
        
        if fruit_tile._loc in snake:
            snake.lengthen()
            fruit1 = False

        fruit_tile.draw(screen,(255,0,0))
        
        # Updating the snake's position on the checkerboard.
        snake.draw(screen)

        pygame.display.update()

    pygame.quit()