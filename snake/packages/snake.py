import typing

from .gameobject import GameObject
from .dir import Dir
from .tile import Tile

class Snake(GameObject):

    def __init__(self, locations: list[tuple[int, int]], colour: tuple[int, int, int], direction: Dir) -> None:
        super().__init__()
        self._tiles = [Tile(loc[0], loc[1], colour) for loc in locations]
        self._colour = colour
        self._direction = direction

    @property
    def dir(self) -> Dir:
        return self._direction
    
    @dir.setter
    def dir(self, new_direction: Dir) -> None:
        self._direction = new_direction
    
    @property
    def tiles(self) -> typing.Iterator[Tile]:
        return iter(self._tiles)

    def __len__(self) -> int:
        return len(self._tiles)

    def move(self) -> None:
        '''Moves snake in current direction.'''
        self._tiles.insert(0, self._tiles[0] + self._direction) # This adds a new head; the head being set to the first element in the list.
        self._tiles.pop()  # Removes tail
        self.notify_observers("notify_object_moved", self)

    def grow(self) -> None:
        '''Allows for the snake to grow whenever it ingests a fruit.'''
        self._tiles.append(self._tiles[-1])