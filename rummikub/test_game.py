#!/usr/bin/env python3
"""Quick validation test for Rummikub game."""

from tiles import create_tile_pool, Tile, TileSet, Color
from validation import is_valid_run, is_valid_group, is_valid_set
from game import GameState
from ai_player import Difficulty

def test_tile_creation():
    """Test tile pool creation."""
    pool = create_tile_pool()
    assert len(pool) == 106, f"Expected 106 tiles, got {len(pool)}"
    print("✓ Tile creation test passed")

def test_valid_run():
    """Test run validation."""
    # Valid run
    tiles = [
        Tile(3, Color.RED, False, 0),
        Tile(4, Color.RED, False, 1),
        Tile(5, Color.RED, False, 2)
    ]
    assert is_valid_run(tiles), "Should be valid run"

    # Invalid run (mixed colors)
    tiles = [
        Tile(3, Color.RED, False, 0),
        Tile(4, Color.BLUE, False, 1),
        Tile(5, Color.RED, False, 2)
    ]
    assert not is_valid_run(tiles), "Should be invalid run (mixed colors)"

    print("✓ Run validation test passed")

def test_valid_group():
    """Test group validation."""
    # Valid group
    tiles = [
        Tile(7, Color.RED, False, 0),
        Tile(7, Color.BLUE, False, 1),
        Tile(7, Color.BLACK, False, 2)
    ]
    assert is_valid_group(tiles), "Should be valid group"

    # Invalid group (same color twice)
    tiles = [
        Tile(7, Color.RED, False, 0),
        Tile(7, Color.RED, False, 1),
        Tile(7, Color.BLACK, False, 2)
    ]
    assert not is_valid_group(tiles), "Should be invalid group (duplicate color)"

    print("✓ Group validation test passed")

def test_game_setup():
    """Test game initialization."""
    game = GameState(num_ai_players=3, ai_difficulty=Difficulty.MEDIUM)

    # Check players
    assert len(game.players) == 4, "Should have 4 players (1 human + 3 AI)"

    # Check initial tiles
    for player in game.players:
        assert len(player.rack) == 14, f"Player should have 14 tiles, got {len(player.rack)}"

    # Check pool
    total_tiles = sum(len(p.rack) for p in game.players) + len(game.pool)
    assert total_tiles == 106, f"Total tiles should be 106, got {total_tiles}"

    print("✓ Game setup test passed")

def test_ai_player():
    """Test AI player initialization."""
    game = GameState(num_ai_players=2, ai_difficulty=Difficulty.EASY)
    ai_players = [p for p in game.players if not p.is_human]
    assert len(ai_players) == 2, "Should have 2 AI players"

    for ai_player in ai_players:
        assert ai_player in game.ai_players, "AI player should have AI instance"

    print("✓ AI player test passed")

def main():
    """Run all tests."""
    print("Running Rummikub validation tests...\n")

    try:
        test_tile_creation()
        test_valid_run()
        test_valid_group()
        test_game_setup()
        test_ai_player()

        print("\n✓ All tests passed!")
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
