from enum import Enum

class State(Enum) :
    """Define the state that the game is currently in."""

    QUIT=0
    PLAY=1
    GAMEOVER=-1
    SCORES = 2
    INPUT_NAME=3