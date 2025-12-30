"""Terminal-based user interface for Rummikub."""

from typing import List, Optional
from tiles import Tile, TileSet, Player, Color
from game import GameState, Move
from ai_player import AIMove
import os
import sys

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_ENABLED = True
except ImportError:
    COLORS_ENABLED = False
    # Fallback if colorama not available
    class Fore:
        BLACK = RED = BLUE = YELLOW = WHITE = GREEN = CYAN = MAGENTA = RESET = ""
    class Back:
        BLACK = RED = BLUE = YELLOW = WHITE = GREEN = CYAN = MAGENTA = RESET = ""
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""


class RummikubUI:
    """Terminal UI for Rummikub game."""

    def __init__(self):
        """Initialize UI."""
        self.color_map = {
            Color.BLACK: Fore.WHITE + Back.BLACK,
            Color.RED: Fore.RED + Style.BRIGHT,
            Color.BLUE: Fore.BLUE + Style.BRIGHT,
            Color.ORANGE: Fore.YELLOW + Style.BRIGHT,
            Color.JOKER: Fore.MAGENTA + Style.BRIGHT,
        }

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name != 'nt' else 'cls')

    def format_tile(self, tile: Tile) -> str:
        """
        Format a tile with color.

        Args:
            tile: Tile to format

        Returns:
            Formatted string
        """
        if not COLORS_ENABLED:
            return str(tile)

        if tile.is_joker:
            return f"{self.color_map[Color.JOKER]}🃏{Style.RESET_ALL}"

        color_code = self.color_map.get(tile.color, "")
        return f"{color_code}{tile.value:2}{Style.RESET_ALL}"

    def display_game_state(self, game: GameState):
        """
        Display the current game state.

        Args:
            game: Game state to display
        """
        self.clear_screen()
        print("=" * 80)
        print(f"{Fore.CYAN}{Style.BRIGHT}RUMMIKUB{Style.RESET_ALL}".center(80))
        print("=" * 80)
        print()

        # Show current player
        current = game.get_current_player()
        print(f"{Fore.GREEN}Current Turn: {current.name}{Style.RESET_ALL}")
        print(f"Pool: {len(game.pool)} tiles remaining")
        print()

        # Show scores
        print(f"{Fore.YELLOW}Scores:{Style.RESET_ALL}")
        for player in game.players:
            meld_status = "✓" if player.has_melded else "✗"
            print(f"  {player.name}: {player.score} points [{meld_status} melded] ({len(player.rack)} tiles)")
        print()

        # Show table sets
        print(f"{Fore.YELLOW}Table Sets:{Style.RESET_ALL}")
        if game.table_sets:
            for i, tile_set in enumerate(game.table_sets):
                tiles_str = " ".join(self.format_tile(t) for t in tile_set.get_tiles())
                print(f"  Set {i+1}: {tiles_str}")
        else:
            print("  (No sets on table)")
        print()

        # Show player's rack if human
        if current.is_human:
            print(f"{Fore.YELLOW}Your Rack:{Style.RESET_ALL}")
            for i, tile in enumerate(current.rack):
                print(f"  {i+1}. {self.format_tile(tile)}")
            print()

    def display_ai_move(self, ai_name: str, move: Optional[AIMove], drew_tile: bool):
        """
        Display AI's move.

        Args:
            ai_name: Name of AI player
            move: The move made (or None if drew)
            drew_tile: Whether AI drew a tile
        """
        print(f"\n{Fore.CYAN}{ai_name}'s turn:{Style.RESET_ALL}")
        if drew_tile:
            print(f"  → Drew a tile")
        elif move:
            print(f"  → Played {len(move.tiles_played)} tiles")
            tiles_str = ", ".join(self.format_tile(t) for t in move.tiles_played)
            print(f"  → Tiles: {tiles_str}")
        print()

    def get_player_action(self, player: Player) -> str:
        """
        Get player's action choice.

        Args:
            player: The player

        Returns:
            Action choice ('play', 'draw', 'quit')
        """
        print(f"{Fore.GREEN}What would you like to do?{Style.RESET_ALL}")
        print("  1. Play tiles")
        print("  2. Draw a tile")
        print("  3. View table")
        print("  4. Quit game")
        print()

        while True:
            choice = input("Enter choice (1-4): ").strip()
            if choice == "1":
                return "play"
            elif choice == "2":
                return "draw"
            elif choice == "3":
                return "view"
            elif choice == "4":
                return "quit"
            else:
                print(f"{Fore.RED}Invalid choice. Please enter 1-4.{Style.RESET_ALL}")

    def get_tiles_to_play(self, player: Player) -> List[int]:
        """
        Get tiles player wants to play.

        Args:
            player: The player

        Returns:
            List of tile indices (0-based)
        """
        print(f"\n{Fore.GREEN}Enter tile numbers to play (comma-separated), or 'back' to cancel:{Style.RESET_ALL}")

        while True:
            choice = input("Tiles: ").strip().lower()
            if choice == 'back':
                return []

            try:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                # Validate indices
                if all(0 <= i < len(player.rack) for i in indices):
                    return indices
                else:
                    print(f"{Fore.RED}Invalid tile numbers. Please try again.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter numbers separated by commas.{Style.RESET_ALL}")

    def build_sets_from_tiles(self, tiles: List[Tile], table_sets: List[TileSet]) -> List[TileSet]:
        """
        Interactive builder to create sets from tiles.

        Args:
            tiles: Tiles to place
            table_sets: Current table sets

        Returns:
            New table configuration
        """
        new_table = [s.copy() for s in table_sets]
        remaining_tiles = tiles.copy()

        print(f"\n{Fore.GREEN}Building sets...{Style.RESET_ALL}")
        print("You can:")
        print("  - Create new sets by grouping tiles")
        print("  - Add tiles to existing sets")
        print()

        # For simplicity, just create a new set with all tiles
        # In a full implementation, this would be more interactive
        if remaining_tiles:
            new_set = TileSet(remaining_tiles)
            new_table.append(new_set)

        return new_table

    def show_error(self, message: str):
        """
        Display error message.

        Args:
            message: Error message
        """
        print(f"\n{Fore.RED}ERROR: {message}{Style.RESET_ALL}\n")

    def show_success(self, message: str):
        """
        Display success message.

        Args:
            message: Success message
        """
        print(f"\n{Fore.GREEN}✓ {message}{Style.RESET_ALL}\n")

    def show_game_over(self, game: GameState):
        """
        Display game over screen.

        Args:
            game: Final game state
        """
        self.clear_screen()
        print("=" * 80)
        print(f"{Fore.CYAN}{Style.BRIGHT}GAME OVER{Style.RESET_ALL}".center(80))
        print("=" * 80)
        print()

        if game.winner:
            print(f"{Fore.GREEN}{Style.BRIGHT}Winner: {game.winner.name}!{Style.RESET_ALL}")
            print()

        print(f"{Fore.YELLOW}Final Scores:{Style.RESET_ALL}")
        sorted_players = sorted(game.players, key=lambda p: p.score, reverse=True)
        for i, player in enumerate(sorted_players, 1):
            print(f"  {i}. {player.name}: {player.score} points")
        print()

    def prompt_continue(self):
        """Wait for user to press enter."""
        input("Press Enter to continue...")

    def show_welcome(self):
        """Show welcome screen."""
        self.clear_screen()
        print("=" * 80)
        print(f"{Fore.CYAN}{Style.BRIGHT}WELCOME TO RUMMIKUB{Style.RESET_ALL}".center(80))
        print("=" * 80)
        print()
        print("A tile-based game where you create runs and groups to win!")
        print()
        print(f"{Fore.YELLOW}Rules:{Style.RESET_ALL}")
        print("  - Create RUNS: 3+ consecutive numbers in same color (e.g., 3-4-5 in red)")
        print("  - Create GROUPS: 3-4 tiles of same number in different colors")
        print("  - First meld must total at least 30 points")
        print("  - Win by emptying your rack!")
        print()
        print(f"{Fore.YELLOW}Tile Colors:{Style.RESET_ALL}")
        print(f"  {self.format_tile(Tile(1, Color.BLACK))} = Black")
        print(f"  {self.format_tile(Tile(1, Color.RED))} = Red")
        print(f"  {self.format_tile(Tile(1, Color.BLUE))} = Blue")
        print(f"  {self.format_tile(Tile(1, Color.ORANGE))} = Orange")
        print(f"  {self.format_tile(Tile(0, Color.JOKER, True))} = Joker (wild card)")
        print()
        self.prompt_continue()
