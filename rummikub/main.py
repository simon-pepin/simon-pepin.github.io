#!/usr/bin/env python3
"""Main entry point for Rummikub game."""

import sys
import time
from game import GameState, Move
from ui import RummikubUI
from ai_player import Difficulty
from validation import validate_all_sets


def play_human_turn(game: GameState, ui: RummikubUI) -> bool:
    """
    Handle human player's turn.

    Args:
        game: Current game state
        ui: UI instance

    Returns:
        True if player wants to continue, False to quit
    """
    player = game.get_current_player()

    while True:
        ui.display_game_state(game)
        action = ui.get_player_action(player)

        if action == "quit":
            return False

        elif action == "view":
            ui.prompt_continue()
            continue

        elif action == "draw":
            tile = game.player_draws(player)
            if tile:
                ui.show_success(f"Drew tile: {ui.format_tile(tile)}")
            else:
                ui.show_error("No tiles left in pool!")
            ui.prompt_continue()
            return True

        elif action == "play":
            # Get tiles to play
            tile_indices = ui.get_tiles_to_play(player)
            if not tile_indices:
                continue

            # Get selected tiles
            tiles_to_play = [player.rack[i] for i in tile_indices]

            # Build new table configuration
            # Simple approach: create one new set with all selected tiles
            new_table = [s.copy() for s in game.table_sets]

            # Ask how to arrange tiles
            print("\nHow would you like to arrange these tiles?")
            print("1. Create a new set")
            print("2. Add to existing set")

            choice = input("Choice (1-2): ").strip()

            if choice == "1":
                from tiles import TileSet
                new_set = TileSet(tiles_to_play)
                new_table.append(new_set)
            elif choice == "2":
                if not new_table:
                    ui.show_error("No existing sets to add to!")
                    continue

                print("\nExisting sets:")
                for i, s in enumerate(new_table):
                    tiles_str = " ".join(ui.format_tile(t) for t in s.get_tiles())
                    print(f"  {i+1}. {tiles_str}")

                try:
                    set_idx = int(input("Which set? ")) - 1
                    if 0 <= set_idx < len(new_table):
                        for tile in tiles_to_play:
                            new_table[set_idx].add_tile(tile)
                    else:
                        ui.show_error("Invalid set number!")
                        continue
                except ValueError:
                    ui.show_error("Invalid input!")
                    continue
            else:
                ui.show_error("Invalid choice!")
                continue

            # Validate and apply move
            is_valid, error = game.validate_move(player, tiles_to_play, new_table)

            if is_valid:
                game.apply_move(player, tiles_to_play, new_table)
                ui.show_success(f"Played {len(tiles_to_play)} tiles!")

                if game.game_over:
                    return True

                ui.prompt_continue()
                return True
            else:
                ui.show_error(error)
                ui.prompt_continue()


def play_ai_turn(game: GameState, ui: RummikubUI):
    """
    Handle AI player's turn.

    Args:
        game: Current game state
        ui: UI instance
    """
    player = game.get_current_player()

    print(f"\n{player.name} is thinking...")
    time.sleep(0.5)  # Brief pause for realism

    played, move = game.execute_ai_turn(player)

    ui.display_ai_move(player.name, move if played else None, not played)
    time.sleep(1.5)  # Let player see AI's move


def main():
    """Main game loop."""
    ui = RummikubUI()
    ui.show_welcome()

    # Setup game
    print("Game Setup")
    print("-" * 40)

    # Get number of AI opponents
    while True:
        try:
            num_ai = int(input("Number of AI opponents (1-3): "))
            if 1 <= num_ai <= 3:
                break
            print("Please enter a number between 1 and 3.")
        except ValueError:
            print("Please enter a valid number.")

    # Get AI difficulty
    print("\nAI Difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    while True:
        try:
            diff_choice = int(input("Choose difficulty (1-3): "))
            if diff_choice == 1:
                difficulty = Difficulty.EASY
                break
            elif diff_choice == 2:
                difficulty = Difficulty.MEDIUM
                break
            elif diff_choice == 3:
                difficulty = Difficulty.HARD
                break
            print("Please enter 1, 2, or 3.")
        except ValueError:
            print("Please enter a valid number.")

    # Create game
    game = GameState(num_ai_players=num_ai, ai_difficulty=difficulty)

    # Main game loop
    while not game.game_over:
        current_player = game.get_current_player()

        if current_player.is_human:
            should_continue = play_human_turn(game, ui)
            if not should_continue:
                print("\nThanks for playing!")
                sys.exit(0)
        else:
            ui.display_game_state(game)
            play_ai_turn(game, ui)

        if not game.game_over:
            game.next_turn()

    # Game over
    ui.show_game_over(game)
    print("\nThanks for playing Rummikub!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)
