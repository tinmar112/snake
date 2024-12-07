import argparse
import pygame
from collections import deque

############### Setting up classes needed for this code. ###############

class Tile:
    
    def __init__(self,size,loc : tuple):
        self._size = size
        self._loc = loc
    
    def draw(self,screen,colour):
        size = self._size
        rect = pygame.Rect(self._loc[0]*size,self._loc[1]*size,size,size)
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
    
    def __init__(self, tiles : deque, tile_size,colour=(0,255,0),direction=(1,0)):
        self._tiles = tiles
        self._tile_size = tile_size
        self._colour = colour
        self._direction = direction

    def __contains__(self,tile):
        return(tile in self._tiles)

    def draw(self,screen):
        for tile in self._tiles:
            S_Tile = Tile(self._tile_size,tile)
            S_Tile.draw(screen,self._colour)

    def move(self,direction : tuple):
        '''Specify a 2-tuple :
        * (1,0) moves right;
        * (-1,0) moves left;
        * (0,1) moves down;
        * (0,-1) moves right.'''
        (head_x,head_y) = self._tiles[-1]
        self._tiles.append((head_x + direction[0],head_y + direction[1]))
    
    def remove_tail(self):
        self._tiles.popleft()

class Fruit:

    def __init__(self,loc: tuple,size,colour=(255,0,0)):
        self._loc = loc
        self._size = size
        self._colour = colour

    def draw(self,screen):
        fruit = Tile(self._size,self._loc)
        fruit.draw(screen,self._colour)

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

    # Setting a bool to indicate if the game should continue.
    run = True

    score = 0

    # Initialising snake and fruit.
    snake = Snake(deque([(10,5),(11,5),(12,5),(13,5),(14,5)]),tile_size)
    the_fruit = Fruit((3,3),tile_size)

    ##### Main game loop
    while run:

        clock.tick(5) # Here you can adjust the maximum number of FPS. Right now, it is set to 5. This somewhat controls game speed.

        pygame.display.set_caption('Score : %d' % score) # Displaying player's score.
        
        # This loop checks for keyboard inputs.
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                # Keyboard interrupt
                if event.key == pygame.K_q:
                    run = False
                # Direction inputs
                direction = snake._direction
                if event.key == pygame.K_RIGHT:
                    if (direction != (1,0)) and (direction != (-1,0)): # Can't ask for reverse course.
                        snake._direction = (1,0)
                elif event.key == pygame.K_LEFT:
                    if (direction != (-1,0)) and (direction != (1,0)):
                        snake._direction = (-1,0)
                elif event.key == pygame.K_UP:
                    if (direction != (0,-1)) and (direction != (0,1)):
                        snake._direction = (0,-1)
                elif event.key == pygame.K_DOWN:
                    if (direction != (0,1)) and (direction != (0,-1)):
                        snake._direction = (0,1)
            # Window interrupt
            if event.type == pygame.QUIT:
                run = False

        snake.move(snake._direction)

        # Checking for self-collision.
        if len(set(snake._tiles)) < len(snake._tiles):
            run = False
        # Checking whether the snake has reached the edge of the board.
        (head_x,head_y) = snake._tiles[-1]
        if (head_x == 0) or (head_y == 0) or (head_y == lines-1) or (head_x == cols-1):
            run = False

        checkerboard = Checkerboard(cols,lines,tile_size)

        # This handles fruit-eating.
        if the_fruit._loc == snake._tiles[-1]:
            score = score + 1
            if the_fruit._loc == (3,3):
                the_fruit._loc = (15,10)
            elif the_fruit._loc == (15,10):
                the_fruit._loc = (3,3)
        else:
            snake.remove_tail()
        
        # Position updates
        checkerboard.draw(screen)
        the_fruit.draw(screen)
        snake.draw(screen)

        pygame.display.update()

    pygame.quit()