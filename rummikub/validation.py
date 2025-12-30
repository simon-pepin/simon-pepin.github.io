"""Validation logic for Rummikub sets."""

from typing import List, Optional, Tuple
from tiles import Tile, TileSet, Color


def is_valid_run(tiles: List[Tile]) -> bool:
    """
    Check if tiles form a valid run.

    A run is 3+ consecutive numbers in the same color.

    Args:
        tiles: List of tiles to check

    Returns:
        True if tiles form a valid run
    """
    if len(tiles) < 3:
        return False

    # Sort tiles by value
    sorted_tiles = sorted(tiles, key=lambda t: t.value if not t.is_joker else 0)

    # Determine the color (from non-joker tiles)
    colors = set(t.color for t in sorted_tiles if not t.is_joker)
    if len(colors) > 1:
        return False  # Mixed colors
    if len(colors) == 0:
        return False  # All jokers

    color = colors.pop()

    # Track expected values
    expected_values = []
    joker_count = 0

    for tile in sorted_tiles:
        if tile.is_joker:
            joker_count += 1
        else:
            expected_values.append(tile.value)

    # Check if values can form a consecutive sequence with jokers filling gaps
    if not expected_values:
        return False

    expected_values.sort()

    # Check for duplicates
    if len(expected_values) != len(set(expected_values)):
        return False

    # Calculate the range and check if jokers can fill gaps
    min_val = expected_values[0]
    max_val = expected_values[-1]
    total_needed = max_val - min_val + 1

    return len(tiles) == total_needed


def is_valid_group(tiles: List[Tile]) -> bool:
    """
    Check if tiles form a valid group.

    A group is 3-4 tiles of the same number in different colors.

    Args:
        tiles: List of tiles to check

    Returns:
        True if tiles form a valid group
    """
    if len(tiles) < 3 or len(tiles) > 4:
        return False

    # Get values and colors
    values = set()
    colors = set()
    joker_count = 0

    for tile in tiles:
        if tile.is_joker:
            joker_count += 1
        else:
            values.add(tile.value)
            colors.add(tile.color)

    # All non-joker tiles must have the same value
    if len(values) > 1:
        return False

    # All non-joker tiles must have different colors
    if len(colors) != len([t for t in tiles if not t.is_joker]):
        return False

    return True


def is_valid_set(tile_set: TileSet) -> bool:
    """
    Check if a set is valid (either a run or a group).

    Args:
        tile_set: Set to validate

    Returns:
        True if set is valid
    """
    tiles = tile_set.get_tiles()
    if len(tiles) < 3:
        return False

    return is_valid_run(tiles) or is_valid_group(tiles)


def validate_all_sets(sets: List[TileSet]) -> bool:
    """
    Validate that all sets on the table are legal.

    Args:
        sets: List of sets to validate

    Returns:
        True if all sets are valid
    """
    return all(is_valid_set(s) for s in sets)


def can_initial_meld(tiles: List[Tile], sets: List[TileSet]) -> bool:
    """
    Check if tiles from rack can satisfy initial meld requirement (30+ points).

    Args:
        tiles: Tiles from player's rack being played
        sets: New sets being created using these tiles

    Returns:
        True if the tiles sum to at least 30 points
    """
    # Calculate total value of tiles used from rack
    total = sum(t.get_points() for t in tiles)
    return total >= 30


def validate_initial_meld(rack_tiles_used: List[Tile]) -> Tuple[bool, int]:
    """
    Validate initial meld and return total points.

    Args:
        rack_tiles_used: Tiles from rack being used in initial meld

    Returns:
        Tuple of (is_valid, total_points)
    """
    total = sum(t.get_points() for t in rack_tiles_used)
    return (total >= 30, total)
