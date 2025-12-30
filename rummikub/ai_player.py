"""AI player using Google OR-Tools constraint programming."""

from typing import List, Optional, Tuple, Dict, Set as PySet
from ortools.sat.python import cp_model
from tiles import Tile, TileSet, Player, Color
from validation import is_valid_run, is_valid_group
import time


class Difficulty:
    """AI difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class AIMove:
    """Represents an AI's move."""

    def __init__(self, new_table_sets: List[TileSet], tiles_played: List[Tile]):
        """
        Initialize AI move.

        Args:
            new_table_sets: New configuration of table sets after move
            tiles_played: Tiles played from rack
        """
        self.new_table_sets = new_table_sets
        self.tiles_played = tiles_played

    def __repr__(self):
        return f"AIMove(played={len(self.tiles_played)} tiles, sets={len(self.new_table_sets)})"


class RummikubAI:
    """AI player using constraint programming to find optimal moves."""

    def __init__(self, player: Player, difficulty: str = Difficulty.MEDIUM):
        """
        Initialize AI player.

        Args:
            player: The player object this AI controls
            difficulty: AI difficulty level
        """
        self.player = player
        self.difficulty = difficulty
        self.time_limit = self._get_time_limit()
        self.max_sets_to_manipulate = self._get_max_manipulation()

    def _get_time_limit(self) -> float:
        """Get time limit based on difficulty."""
        if self.difficulty == Difficulty.EASY:
            return 0.5
        elif self.difficulty == Difficulty.MEDIUM:
            return 1.5
        else:  # HARD
            return 3.0

    def _get_max_manipulation(self) -> int:
        """Get max number of table sets to manipulate."""
        if self.difficulty == Difficulty.EASY:
            return 1  # Only add to existing sets
        elif self.difficulty == Difficulty.MEDIUM:
            return 3
        else:  # HARD
            return 999  # Unlimited

    def find_best_move(self, table_sets: List[TileSet]) -> Optional[AIMove]:
        """
        Find the best move using constraint programming.

        Args:
            table_sets: Current sets on the table

        Returns:
            Best move found, or None if should draw a tile
        """
        # Try simple greedy approach first for speed
        simple_move = self._try_simple_move(table_sets)
        if simple_move and len(simple_move.tiles_played) >= 3:
            return simple_move

        # Use constraint programming for complex moves
        if self.difficulty != Difficulty.EASY:
            cp_move = self._find_move_with_cp(table_sets)
            if cp_move:
                return cp_move

        # Return simple move if found, otherwise None (draw)
        return simple_move if simple_move else None

    def _try_simple_move(self, table_sets: List[TileSet]) -> Optional[AIMove]:
        """
        Try simple greedy moves (add tiles to existing sets).

        Args:
            table_sets: Current table sets

        Returns:
            Simple move if found
        """
        rack = self.player.rack.copy()
        new_sets = [s.copy() for s in table_sets]
        tiles_played = []

        # Try to add tiles to existing runs
        for tile in rack[:]:
            if tile.is_joker:
                continue

            for tile_set in new_sets:
                test_tiles = tile_set.get_tiles() + [tile]
                if is_valid_run(test_tiles):
                    tile_set.add_tile(tile)
                    tiles_played.append(tile)
                    rack.remove(tile)
                    break

        # Check if initial meld requirement is met
        if not self.player.has_melded:
            total = sum(t.get_points() for t in tiles_played)
            if total < 30:
                return None

        if tiles_played:
            return AIMove(new_sets, tiles_played)

        return None

    def _find_move_with_cp(self, table_sets: List[TileSet]) -> Optional[AIMove]:
        """
        Use constraint programming to find optimal move.

        Args:
            table_sets: Current table sets

        Returns:
            Best move found using CP solver
        """
        # Get all available tiles
        rack_tiles = self.player.rack.copy()
        table_tiles = []
        for s in table_sets[:self.max_sets_to_manipulate]:
            table_tiles.extend(s.get_tiles())

        all_tiles = rack_tiles + table_tiles

        if len(all_tiles) < 3:
            return None

        # Build and solve constraint model
        model = cp_model.CpModel()

        # Create tile-to-set assignment variables
        max_sets = min(len(all_tiles) // 3 + 2, 15)  # Limit to prevent explosion
        tile_to_set = {}

        for i, tile in enumerate(all_tiles):
            # -1 means not in any set (on rack or returned to table)
            tile_to_set[i] = model.NewIntVar(-1, max_sets - 1, f'tile_{i}_set')

        # Create set active variables
        set_active = [model.NewBoolVar(f'set_{i}_active') for i in range(max_sets)]

        # Track which tiles are in each set
        tiles_in_set = {}
        for set_id in range(max_sets):
            tiles_in_set[set_id] = []
            for i in range(len(all_tiles)):
                in_set = model.NewBoolVar(f'tile_{i}_in_set_{set_id}')
                model.Add(tile_to_set[i] == set_id).OnlyEnforceIf(in_set)
                model.Add(tile_to_set[i] != set_id).OnlyEnforceIf(in_set.Not())
                tiles_in_set[set_id].append(in_set)

        # Constraint: Set size must be >= 3 if active, 0 if not active
        for set_id in range(max_sets):
            set_size = sum(tiles_in_set[set_id])
            model.Add(set_size >= 3).OnlyEnforceIf(set_active[set_id])
            model.Add(set_size == 0).OnlyEnforceIf(set_active[set_id].Not())
            model.Add(set_size <= 13)  # Max possible run length

        # Constraint: All table tiles must be in some set
        for i in range(len(rack_tiles), len(all_tiles)):
            model.Add(tile_to_set[i] >= 0)

        # Add valid set constraints (simplified)
        for set_id in range(max_sets):
            self._add_set_validity_constraints(
                model, set_id, all_tiles, tiles_in_set[set_id], set_active[set_id]
            )

        # Initial meld constraint
        if not self.player.has_melded:
            tiles_played_value = sum(
                all_tiles[i].get_points() * tiles_in_set[set_id][i]
                for i in range(len(rack_tiles))
                for set_id in range(max_sets)
            )
            model.Add(tiles_played_value >= 30)

        # Objective: Maximize tiles played from rack
        tiles_played_count = sum(
            model.NewBoolVar(f'tile_{i}_played')
            for i in range(len(rack_tiles))
        )

        for i in range(len(rack_tiles)):
            played = model.NewBoolVar(f'tile_{i}_played')
            model.Add(tile_to_set[i] >= 0).OnlyEnforceIf(played)
            model.Add(tile_to_set[i] == -1).OnlyEnforceIf(played.Not())
            tiles_played_count += played * 100  # Weight heavily

        model.Maximize(tiles_played_count)

        # Solve
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = self.time_limit
        solver.parameters.num_search_workers = 4

        status = solver.Solve(model)

        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return self._extract_solution(solver, all_tiles, tile_to_set, rack_tiles, max_sets)

        return None

    def _add_set_validity_constraints(
        self,
        model: cp_model.CpModel,
        set_id: int,
        all_tiles: List[Tile],
        tiles_in_set: List,
        set_active
    ):
        """
        Add constraints to ensure set is valid (run or group).

        This is a simplified version that relies on post-validation.
        """
        # For simplicity, we'll validate solutions after solving
        # A full implementation would add explicit run/group constraints
        pass

    def _extract_solution(
        self,
        solver: cp_model.CpSolver,
        all_tiles: List[Tile],
        tile_to_set: Dict,
        rack_tiles: List[Tile],
        max_sets: int
    ) -> Optional[AIMove]:
        """
        Extract solution from solver.

        Args:
            solver: Solved CP solver
            all_tiles: All tiles (rack + table)
            tile_to_set: Tile assignment variables
            rack_tiles: Tiles from rack
            max_sets: Maximum number of sets

        Returns:
            AIMove if solution is valid
        """
        # Build new table sets
        sets_dict = {}
        tiles_played = []

        for i, tile in enumerate(all_tiles):
            set_id = solver.Value(tile_to_set[i])
            if set_id >= 0:
                if set_id not in sets_dict:
                    sets_dict[set_id] = []
                sets_dict[set_id].append(tile.copy())

                # Track if from rack
                if i < len(rack_tiles):
                    tiles_played.append(tile)

        # Create TileSet objects and validate
        new_table_sets = []
        for tiles in sets_dict.values():
            tile_set = TileSet(tiles)
            # Validate the set
            if not (is_valid_run(tiles) or is_valid_group(tiles)):
                return None  # Invalid solution
            new_table_sets.append(tile_set)

        if tiles_played:
            return AIMove(new_table_sets, tiles_played)

        return None
