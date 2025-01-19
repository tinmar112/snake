import typing

from .gameobject import GameObject
from .tile import Tile

class CheckerBoard(GameObject):

    def __init__(self, width: int, height: int, colour1: tuple[int, int, int], colour2: tuple[int, int, int]) -> None:
        super().__init__()
        self._width = width
        self._height = height
        self._colour1 = colour1  # Primary color
        self._colour2 = colour2  # Secondary color

    @property
    def tiles(self) -> typing.Iterator[Tile]:
        # Yield tiles with alternating colors
        for row in range(self._height):
            for column in range(self._width):
                yield Tile(row=row, column=column, colour=self._colour1 if ((row+column)%2 == 0) else self._colour2)