import typing

from .gameobject import GameObject
from .tile import Tile

class Fruit(GameObject):

    def __init__(self, location: tuple[int, int], colour: tuple[int, int, int]) -> None:
        super().__init__()
        self._tiles = [Tile(row=location[0], column=location[1], colour=colour)]

    @property
    def tiles(self) -> typing.Iterator[Tile]:
        return iter(self._tiles)
