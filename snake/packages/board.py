import pygame
import random

from .subject import Subject
from .observer import Observer
from .gameobject import GameObject
from .fruit import Fruit
from .snake import Snake

class Board(Subject, Observer):

    def __init__(self, screen: pygame.Surface, tile_size: int) -> None:
        super().__init__()
        self._screen = screen
        self._tile_size = tile_size
        self._objects: list[GameObject] = []  # List of all game objects on the board

    def add_object(self, gameobject: GameObject) -> None:
        self._objects.append(gameobject)
        if isinstance(gameobject, Subject):
            gameobject.attach_obs(self)
    
    def draw(self) -> None:
        '''General draw command which draws all objects on the board.'''
        for object in self._objects:
            for tile in object.tiles:
                tile.draw(self._screen, self._tile_size)

    # Notifiers
    def notify_object_moved(self, obj: GameObject) -> None:
        for other in self._objects:
            if other is not obj:
                # Checks if the object's tiles overlap with another object
                for tile in obj.tiles:
                    if tile in other:
                        if isinstance(other, Fruit):
                            self.notify_object_eaten(other)

    def notify_object_eaten(self, obj: GameObject) -> None:
        if isinstance(obj, Fruit):
            self._objects.remove(obj)
            snake = next((o for o in self._objects if isinstance(o, Snake)), None)
            if snake is None:
                raise ValueError("No Snake object found on the board.")
            snake.grow()
            new_position = (random.randint(0, self._screen.get_height() // self._tile_size - 1),random.randint(0, self._screen.get_width() // self._tile_size - 1))
            new_fruit = Fruit(new_position, (255, 0, 0))
            self.add_object(new_fruit)