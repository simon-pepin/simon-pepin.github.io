"""Tile, Set, and Player classes for Rummikub game."""

from typing import List, Optional, Tuple
from enum import Enum
import random


class Color(Enum):
    """Tile colors."""
    BLACK = "black"
    RED = "red"
    BLUE = "blue"
    ORANGE = "orange"
    JOKER = "joker"


class Tile:
    """Represents a single Rummikub tile."""

    def __init__(self, value: int, color: Color, is_joker: bool = False, tile_id: Optional[int] = None):
        """
        Initialize a tile.

        Args:
            value: Tile number (1-13) or 0 for joker
            color: Tile color
            is_joker: Whether this is a joker tile
            tile_id: Unique identifier for this specific tile instance
        """
        self.value = value
        self.color = color
        self.is_joker = is_joker
        self.tile_id = tile_id

    def __repr__(self):
        if self.is_joker:
            return "🃏"
        return f"{self.value}{self.color.value[0].upper()}"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        return self.tile_id == other.tile_id

    def __hash__(self):
        return hash(self.tile_id)

    def get_points(self) -> int:
        """Get point value of tile."""
        if self.is_joker:
            return 30
        return self.value

    def copy(self):
        """Create a copy of this tile."""
        return Tile(self.value, self.color, self.is_joker, self.tile_id)


class TileSet:
    """Represents a set of tiles on the table (run or group)."""

    def __init__(self, tiles: List[Tile]):
        """
        Initialize a set.

        Args:
            tiles: List of tiles in this set
        """
        self.tiles = tiles

    def __repr__(self):
        return f"Set({', '.join(str(t) for t in self.tiles)})"

    def __str__(self):
        return f"[{' '.join(str(t) for t in self.tiles)}]"

    def get_tiles(self) -> List[Tile]:
        """Get all tiles in this set."""
        return self.tiles.copy()

    def add_tile(self, tile: Tile):
        """Add a tile to this set."""
        self.tiles.append(tile)

    def remove_tile(self, tile: Tile):
        """Remove a tile from this set."""
        self.tiles.remove(tile)

    def size(self) -> int:
        """Get number of tiles in set."""
        return len(self.tiles)

    def copy(self):
        """Create a copy of this set."""
        return TileSet([t.copy() for t in self.tiles])


class Player:
    """Represents a player in the game."""

    def __init__(self, name: str, is_human: bool = False):
        """
        Initialize a player.

        Args:
            name: Player's name
            is_human: Whether this is a human player
        """
        self.name = name
        self.is_human = is_human
        self.rack: List[Tile] = []
        self.has_melded = False
        self.score = 0

    def __repr__(self):
        return f"Player({self.name}, tiles={len(self.rack)})"

    def add_tile(self, tile: Tile):
        """Add a tile to player's rack."""
        self.rack.append(tile)

    def remove_tile(self, tile: Tile):
        """Remove a tile from player's rack."""
        self.rack.remove(tile)

    def get_rack_value(self) -> int:
        """Get total point value of tiles on rack."""
        return sum(t.get_points() for t in self.rack)

    def sort_rack(self):
        """Sort tiles on rack by color and value."""
        color_order = {
            Color.BLACK: 0,
            Color.RED: 1,
            Color.BLUE: 2,
            Color.ORANGE: 3,
            Color.JOKER: 4
        }
        def sort_key(tile):
            if tile.is_joker:
                return (4, 0)  # Jokers last
            return (color_order.get(tile.color, 5), tile.value)
        self.rack.sort(key=sort_key)


def create_tile_pool() -> List[Tile]:
    """
    Create a full set of 106 Rummikub tiles.

    Returns:
        List of all tiles in the game
    """
    tiles = []
    tile_id = 0

    # Create numbered tiles (2 of each number-color combination)
    colors = [Color.BLACK, Color.RED, Color.BLUE, Color.ORANGE]
    for _ in range(2):  # Two copies
        for color in colors:
            for value in range(1, 14):  # 1-13
                tiles.append(Tile(value, color, False, tile_id))
                tile_id += 1

    # Create 2 jokers
    for _ in range(2):
        tiles.append(Tile(0, Color.JOKER, True, tile_id))
        tile_id += 1

    return tiles


def shuffle_tiles(tiles: List[Tile]) -> List[Tile]:
    """
    Shuffle tiles randomly.

    Args:
        tiles: List of tiles to shuffle

    Returns:
        Shuffled list of tiles
    """
    shuffled = tiles.copy()
    random.shuffle(shuffled)
    return shuffled
