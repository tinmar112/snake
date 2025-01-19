import pygame
import argparse
import typing

from packages.board import Board
from packages.checkerboard import CheckerBoard
from packages.dir import Dir
from packages.fruit import Fruit
from packages.snake import Snake
from packages.exceptions import GameOver

@typing.no_type_check
def arguments():

    DEFAULT_WIDTH = 20
    DEFAULT_HEIGHT = 15

    parser = argparse.ArgumentParser(description='Window size with numbers of tiles.')
    parser.add_argument('-W', '--width', type=int, default=DEFAULT_WIDTH, help="Width, expressed in no. of tiles.")
    parser.add_argument('-H', '--height', type=int, default=DEFAULT_HEIGHT, help="Height, expressed in no. of tiles.")
    args = parser.parse_args()

    # Returns TypedDict dictionary format.
    return args

def snake() -> None:

    TILE_SIZE = 20  # Size of each tile in pixels
    INITIAL_SNAKE = [(10, 7), (10, 6), (10, 5)]
    DEFAULT_DIRECTION = Dir.RIGHT  # Initial snake direction

    args = arguments()
    width, height = args.width, args.height

    pygame.init()

    try:

        screen = pygame.display.set_mode((width*TILE_SIZE,height*TILE_SIZE))

        clock = pygame.time.Clock()

        # Setting up game objects

        board = Board(screen=screen, tile_size=TILE_SIZE)
        checkerboard = CheckerBoard(width,height, (0, 0, 0), (255, 255, 255))
        snake = Snake(INITIAL_SNAKE, (0, 255, 0), DEFAULT_DIRECTION)
        fruit = Fruit((3, 3), (255, 0, 0))

        board.add_object(checkerboard)
        board.add_object(snake)
        board.add_object(fruit)

        # Main game loop
        run = True
        while run:

            clock.tick(5)  # Sets the max no. of frames per second.

            #Displays player's score
            pygame.display.set_caption("Score : %d" %len(snake))

            # This loop checks for keyboard inputs.
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    # Keyboard interrupt
                    if event.key == pygame.K_q:
                        run = False
                    # Direction inputs
                    direction = snake.dir
                    if event.key == pygame.K_RIGHT:
                        if (direction != Dir.RIGHT) and (direction != Dir.LEFT): # Can't ask for reverse course.
                            snake.dir = Dir.RIGHT
                    elif event.key == pygame.K_LEFT:
                        if (direction != Dir.LEFT) and (direction != Dir.RIGHT):
                            snake.dir = Dir.LEFT
                    elif event.key == pygame.K_UP:
                        if (direction != Dir.UP) and (direction != Dir.DOWN):
                            snake.dir = Dir.UP
                    elif event.key == pygame.K_DOWN:
                        if (direction != Dir.DOWN) and (direction != Dir.UP):
                            snake.dir = Dir.DOWN
                # Window interrupt
                if event.type == pygame.QUIT:
                    run = False

            snake.move()
            
            #Check if snake has reached the edge of the board.
            snake_head_row, snake_head_col = snake._tiles[0].row, snake._tiles[0].column
            if not ((0 <= snake_head_row <= height) and (0 <= snake_head_col <= width)):
                run = False
                raise GameOver('Snake has struck the edge of the board.')

            board.draw()

            pygame.display.update()
    
    except GameOver as e:
        print(e)
        pygame.quit()