# Rummikub with AI Opponents

A single-player Rummikub game where you play against 3 sophisticated AI opponents powered by Google OR-Tools constraint programming.

## Features

- **Full Rummikub Implementation**: All standard rules including runs, groups, and jokers
- **Sophisticated AI**: Uses constraint programming (CP-SAT solver) to find optimal tile placements
- **Three Difficulty Levels**: Easy, Medium, and Hard AI opponents
- **Terminal-Based UI**: Colorful, interactive command-line interface
- **Complete Rule Validation**: Enforces all Rummikub rules including initial meld requirement

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies

```bash
cd rummikub
pip install -r requirements.txt
```

This will install:
- `ortools` - Google's optimization library for constraint programming
- `colorama` - Cross-platform colored terminal text

## How to Play

### Starting the Game

```bash
python main.py
```

Or make it executable:

```bash
chmod +x main.py
./main.py
```

### Game Setup

When you start the game, you'll be prompted to:
1. Choose the number of AI opponents (1-3)
2. Select AI difficulty level (Easy/Medium/Hard)

### Game Rules

#### Objective
Be the first player to empty your rack of tiles by forming valid sets on the table.

#### Valid Sets

1. **Runs**: 3 or more consecutive numbers in the same color
   - Example: Red 3-4-5-6

2. **Groups**: 3 or 4 tiles of the same number in different colors
   - Example: 7 in Black, Red, Blue

#### Initial Meld Requirement

Your first play must total at least **30 points** using only tiles from your rack. After your initial meld, you can freely manipulate existing table sets.

#### On Your Turn

You can:
- Play tiles from your rack to form new sets
- Add tiles to existing sets on the table
- Manipulate existing sets (after initial meld)
- Draw a tile if unable or unwilling to play

#### Jokers

- Jokers can substitute for any tile
- Worth 30 points if left on your rack
- Can be retrieved by replacing with the actual tile

#### Winning

The game ends when a player empties their rack. Points are scored based on tiles remaining on other players' racks.

### Controls

During your turn:
1. **Play tiles** - Select tiles from your rack to play
2. **Draw a tile** - Take a tile from the pool
3. **View table** - See current table sets
4. **Quit game** - Exit the game

## AI Implementation

### Constraint Programming Approach

The AI uses Google OR-Tools' CP-SAT solver to find optimal moves:

#### Decision Variables
- Tile-to-set assignments for all tiles (rack + table)
- Active/inactive status for potential sets
- Tile positions within sets

#### Constraints
1. **Set Validity**: Each active set must be a valid run or group
2. **Tile Usage**: Each tile appears in at most one set
3. **Table Integrity**: All table tiles must remain in valid sets
4. **Initial Meld**: First plays must sum to ≥30 points

#### Objective Function
Maximize: (tiles played from rack) × 100 + (sum of tile values played)

### Difficulty Levels

**Easy**
- 0.5 second time limit
- Only adds tiles to existing sets
- No complex manipulations

**Medium**
- 1.5 second time limit
- Can manipulate up to 3 existing sets
- Basic strategic play

**Hard**
- 3.0 second time limit
- Full table manipulation
- Optimal tile placements
- Strategic joker use

## Project Structure

```
rummikub/
├── __init__.py          # Package initialization
├── tiles.py             # Tile, Set, and Player classes
├── validation.py        # Set validation logic
├── ai_player.py         # AI using OR-Tools constraint programming
├── game.py              # Game state and logic
├── ui.py                # Terminal-based user interface
├── main.py              # Game entry point
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Code Architecture

### Core Classes

**Tile** (`tiles.py`)
- Represents a single tile with value, color, and joker status
- Includes unique tile_id for tracking

**TileSet** (`tiles.py`)
- Represents a set of tiles on the table
- Manages tile collections

**Player** (`tiles.py`)
- Tracks rack, score, and meld status
- Handles both human and AI players

**GameState** (`game.py`)
- Manages overall game state
- Handles turn progression and move validation
- Tracks pool, players, and table sets

**RummikubAI** (`ai_player.py`)
- Implements constraint programming solver
- Finds optimal tile placements
- Handles different difficulty levels

**RummikubUI** (`ui.py`)
- Terminal-based interface
- Colored tile display
- Interactive move building

## Performance Notes

The constraint programming solver typically finds solutions in:
- Easy: < 0.5 seconds
- Medium: 0.5-1.5 seconds
- Hard: 1.0-3.0 seconds

For very complex board states, the solver may timeout and fall back to simpler moves or drawing a tile.

## Known Limitations

1. Human player interface is simplified - advanced table manipulations require manual set reconstruction
2. AI explanation mode not yet implemented
3. No save/load game functionality
4. No undo for human players after confirming move

## Future Enhancements

- [ ] Visual move animations
- [ ] AI move explanations
- [ ] Hint system for human players
- [ ] Game replay functionality
- [ ] More sophisticated table manipulation UI
- [ ] Online multiplayer support
- [ ] Tournament mode with multiple rounds

## Troubleshooting

### Import Errors

If you get import errors, ensure all dependencies are installed:

```bash
pip install --upgrade ortools colorama
```

### Slow AI Performance

If the AI takes too long:
1. Reduce difficulty level to Easy or Medium
2. Check that OR-Tools is properly installed
3. Ensure you're using Python 3.8+

### Display Issues

If colors don't display correctly:
- Windows: Install colorama
- Linux/Mac: Most terminals support colors by default
- If issues persist, the game will fall back to non-colored output

## License

MIT License - Feel free to use and modify as needed.

## Credits

Built using:
- [Google OR-Tools](https://developers.google.com/optimization) for constraint programming
- [Colorama](https://github.com/tartley/colorama) for cross-platform colored terminal output

Based on the classic Rummikub tile game.
