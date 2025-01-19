import pygame

from .dir import Dir

class Tile:

    def __init__(self, row: int, column: int, colour: tuple[int, int, int]) -> None:
        self._row = row
        self._column = column
        self._colour = colour

    @property
    def row(self) -> int:
        return self._row
    @property
    def column(self) -> int:
        return self._column

    # Draw the tile on the screen
    def draw(self, screen: pygame.Surface, tile_size: int) -> None:
        rect = pygame.Rect(self._column * tile_size, self._row * tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, self._colour, rect)

    # Add a direction to a tile to create a new tile
    def __add__(self, other: Dir) -> 'Tile':
        if isinstance(other, Dir):
            return Tile(self._row + other.value[1], self._column + other.value[0], self._colour)
        else:
            raise ValueError('Wrong types used in attempted addition of 2 tiles')