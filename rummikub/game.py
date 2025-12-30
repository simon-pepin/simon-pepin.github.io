"""Game state and logic for Rummikub."""

from typing import List, Optional, Tuple
from tiles import Tile, TileSet, Player, create_tile_pool, shuffle_tiles
from validation import validate_all_sets, validate_initial_meld
from ai_player import RummikubAI, AIMove, Difficulty
import random


class GameState:
    """Manages the state of a Rummikub game."""

    def __init__(self, num_ai_players: int = 3, ai_difficulty: str = Difficulty.MEDIUM):
        """
        Initialize a new game.

        Args:
            num_ai_players: Number of AI opponents (1-3)
            ai_difficulty: Difficulty level for AI players
        """
        self.pool: List[Tile] = []
        self.players: List[Player] = []
        self.table_sets: List[TileSet] = []
        self.current_player_idx: int = 0
        self.ai_difficulty = ai_difficulty
        self.ai_players: dict = {}  # player -> AI instance
        self.game_over = False
        self.winner: Optional[Player] = None

        # Setup game
        self._setup_game(num_ai_players)

    def _setup_game(self, num_ai_players: int):
        """Setup the initial game state."""
        # Create players
        human_player = Player("You", is_human=True)
        self.players.append(human_player)

        for i in range(num_ai_players):
            ai_name = f"AI {i+1}"
            ai_player = Player(ai_name, is_human=False)
            self.players.append(ai_player)
            self.ai_players[ai_player] = RummikubAI(ai_player, self.ai_difficulty)

        # Create and shuffle tiles
        all_tiles = create_tile_pool()
        self.pool = shuffle_tiles(all_tiles)

        # Deal 14 tiles to each player
        for player in self.players:
            for _ in range(14):
                if self.pool:
                    tile = self.pool.pop()
                    player.add_tile(tile)
            player.sort_rack()

        # Randomly choose starting player
        self.current_player_idx = random.randint(0, len(self.players) - 1)

    def get_current_player(self) -> Player:
        """Get the current player."""
        return self.players[self.current_player_idx]

    def draw_tile(self, player: Player) -> Optional[Tile]:
        """
        Draw a tile from the pool for a player.

        Args:
            player: Player drawing the tile

        Returns:
            The drawn tile, or None if pool is empty
        """
        if self.pool:
            tile = self.pool.pop()
            player.add_tile(tile)
            player.sort_rack()
            return tile
        return None

    def next_turn(self):
        """Move to the next player's turn."""
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def validate_move(
        self,
        player: Player,
        tiles_played: List[Tile],
        new_table_sets: List[TileSet]
    ) -> Tuple[bool, str]:
        """
        Validate a player's move.

        Args:
            player: Player making the move
            tiles_played: Tiles being played from rack
            new_table_sets: New configuration of table sets

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if all new sets are valid
        if not validate_all_sets(new_table_sets):
            return False, "Invalid sets on table"

        # Check if all played tiles are from player's rack
        for tile in tiles_played:
            if tile not in player.rack:
                return False, "Cannot play tiles not in your rack"

        # Check initial meld requirement
        if not player.has_melded and tiles_played:
            is_valid, total = validate_initial_meld(tiles_played)
            if not is_valid:
                return False, f"Initial meld must be at least 30 points (you have {total})"

        return True, ""

    def apply_move(
        self,
        player: Player,
        tiles_played: List[Tile],
        new_table_sets: List[TileSet]
    ) -> bool:
        """
        Apply a validated move to the game state.

        Args:
            player: Player making the move
            tiles_played: Tiles being played from rack
            new_table_sets: New configuration of table sets

        Returns:
            True if move was applied successfully
        """
        # Validate first
        is_valid, error = self.validate_move(player, tiles_played, new_table_sets)
        if not is_valid:
            return False

        # Remove played tiles from rack
        for tile in tiles_played:
            player.remove_tile(tile)

        # Update table sets
        self.table_sets = new_table_sets

        # Mark player as having melded
        if tiles_played:
            player.has_melded = True

        # Check for win
        if len(player.rack) == 0:
            self._end_game(player)

        return True

    def player_draws(self, player: Player):
        """
        Player draws a tile (can't or won't play).

        Args:
            player: Player drawing
        """
        tile = self.draw_tile(player)
        return tile

    def execute_ai_turn(self, ai_player: Player) -> Tuple[bool, Optional[AIMove]]:
        """
        Execute an AI player's turn.

        Args:
            ai_player: The AI player

        Returns:
            Tuple of (played_tiles, ai_move or None if drew)
        """
        ai = self.ai_players[ai_player]
        move = ai.find_best_move(self.table_sets)

        if move:
            # Apply the move
            success = self.apply_move(ai_player, move.tiles_played, move.new_table_sets)
            if success:
                return True, move
            else:
                # Fallback: draw a tile
                self.player_draws(ai_player)
                return False, None
        else:
            # Draw a tile
            self.player_draws(ai_player)
            return False, None

    def _end_game(self, winner: Player):
        """
        End the game and calculate scores.

        Args:
            winner: The player who won
        """
        self.game_over = True
        self.winner = winner

        # Calculate scores
        total_points = 0
        for player in self.players:
            if player != winner:
                points = player.get_rack_value()
                player.score -= points
                total_points += points

        winner.score += total_points

    def get_game_status(self) -> dict:
        """
        Get current game status.

        Returns:
            Dictionary with game state information
        """
        return {
            'current_player': self.get_current_player().name,
            'pool_size': len(self.pool),
            'table_sets': len(self.table_sets),
            'game_over': self.game_over,
            'winner': self.winner.name if self.winner else None,
            'scores': {p.name: p.score for p in self.players}
        }


class Move:
    """Represents a human player's move being constructed."""

    def __init__(self, player: Player, table_sets: List[TileSet]):
        """
        Initialize a move.

        Args:
            player: Player making the move
            table_sets: Current table sets (will be copied)
        """
        self.player = player
        self.original_rack = player.rack.copy()
        self.working_rack = player.rack.copy()
        self.working_table = [s.copy() for s in table_sets]
        self.tiles_played: List[Tile] = []

    def play_tile(self, tile: Tile, set_index: Optional[int] = None):
        """
        Play a tile from rack to table.

        Args:
            tile: Tile to play
            set_index: Index of set to add to, or None for new set
        """
        if tile in self.working_rack:
            self.working_rack.remove(tile)
            self.tiles_played.append(tile)

            if set_index is not None and set_index < len(self.working_table):
                self.working_table[set_index].add_tile(tile)
            else:
                # Create new set
                self.working_table.append(TileSet([tile]))

    def undo(self):
        """Undo all changes and reset to original state."""
        self.working_rack = self.original_rack.copy()
        self.tiles_played = []

    def get_new_table_sets(self) -> List[TileSet]:
        """Get the new table configuration."""
        return self.working_table

    def get_tiles_played(self) -> List[Tile]:
        """Get tiles played from rack."""
        return self.tiles_played
