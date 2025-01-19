import typing
import abc

from .subject import Subject
from .tile import Tile

class GameObject(Subject):

    def __init__(self) -> None:
        super().__init__()

    @property
    @abc.abstractmethod
    def tiles(self) -> typing.Iterator[Tile]:
        raise NotImplementedError

    def __contains__(self, tile: Tile) -> bool:
        if not isinstance(tile, Tile):
            return False
        return any(t.row == tile.row and t.column == tile.column for t in self.tiles)