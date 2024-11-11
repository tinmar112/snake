import argparse
import pygame

def arguments():
    '''Defines the arguments taken by the snake() function.'''

    # Note that window size is set to be a multiple of 19, to get an integer number of squares in width and height.
    # This is because each square is set to 19x19 in size, due to a reason explained in the checkerboard() function.

    MIN = (200//19)*19

    DEFAULT_WIDTH = (400//19)*19
    DEFAULT_HEIGHT = (300//19)*19

    # Declares acceptable arguments.
    parser = argparse.ArgumentParser(description='Set width and height of game window.')
    parser.add_argument('-W','--width',type=int,help="No. of columns of window",default=DEFAULT_WIDTH)
    parser.add_argument('-H','--height',type=int,help="No. of lines of window",default=DEFAULT_HEIGHT)
    args = parser.parse_args()

    if (args.width < MIN) or (args.height < MIN):
        raise ValueError("Width and height must be greater or equal to %d." % MIN)
    
    return((args.width//19)*19,(args.height//19)*19) # Again, set to the closest multiple of 19.


def checkerboard(screen,width,height):
    '''Draws a checkerboard with Pygame already running.'''
    
    screen.fill((0,0,0))
    white = (255,255,255)

    # Normally, we would like a square size of 20 by 20. However, an ODD NUMBER is needed. See why on line 34.
    # Hence the iteration step is set to the odd number closest to 20, in this case 19.

    for i in range(0,width,19):
        for j in range(0,height,19):
            if (i+j)%2 == 0:    # Iterating 20 by 20 would cause a problem here: we would always get True. The screen would turn completely white.
                rect = pygame.Rect(i,j,19,19)
                pygame.draw.rect(screen, white, rect)


def snake():
    '''Snake Game
    * Press Q or click on the close button to end the game.'''
  
    width,height = arguments()

    pygame.init()

    screen = pygame.display.set_mode((width,height))

    clock = pygame.time.Clock()

    # Setting a bool to indicate if the game should continue.
    run = True
    while run:

        clock.tick(1)

        # This loop checks whether the player asked to quit the game.
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
            if event.type == pygame.QUIT:
                run = False

        # Setting up the checkerboard.
        checkerboard(screen,width,height)

        # Assigning a global variable to indicate the snake's position, starting from (10,5).
        POS_i,POS_y = 10,5
        green = (0,255,0)
        rect = pygame.Rect(POS_y*19,POS_i*19,3*19,1*19) # Remember, we are playing on tiles that are mutliples of 19.
        pygame.draw.rect(screen,green,rect)


        pygame.display.update()

    pygame.quit()