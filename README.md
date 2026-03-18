# ♟️ Chess Engine (Minimax + Alpha-Beta Pruning)

## Overview
This project is a custom-built chess engine that uses the **Minimax algorithm** with a **custom board evaluation function** to determine the best move for a given board state. The engine supports configurable search depth and optional **alpha-beta pruning** to improve performance.

It includes multiple gameplay modes (Human vs Human, Human vs Engine, Engine vs Engine) and allows users to request move suggestions using a built-in hint system.

---

## Features

### 🧠 AI Engine
- Minimax-based decision making
- Custom board evaluation function
- Configurable search depth
- Optional **alpha-beta pruning** (toggle ON/OFF)

---

## Game Modes

### 1. Human vs Human
- Two players can play against each other
- Move validation ensures only legal moves are executed

**Hint System:**
- Type `hint`
- You will be prompted to enter a depth
- The engine will return the best move found at that depth

Example:
```text
hint
Enter depth: 3
Best move: e2e4
```

---

### 2. Human vs Engine
- Play against the chess engine
- The engine calculates the best move based on:
  - Selected depth
  - Alpha-beta pruning setting

---

### 3. Engine vs Engine (Performance Mode)
- Both sides are controlled by the engine
- Used for testing and comparison
- Outputs:
  - Time taken per move
  - Useful for comparing:
    - Alpha-beta pruning ON vs OFF
    - Different search depths

---

## 📝 Move Input Format

Moves must be entered in standard coordinate notation:

```text
<start_square><end_square>
```

### Examples:
```text
e2e4
g1f3
```

- Moves are validated before execution
- Invalid moves are rejected

---

## ⚙️ Configuration

Key parameters can be adjusted in the code and through prompts:
- Search depth
- Alpha-beta pruning (enabled/disabled)
- Engine vs Engine test settings (set in code)

---

## 📊 Performance Insights

The Engine vs Engine mode is designed to:
- Measure move computation time
- Compare optimization techniques
- Demonstrate efficiency gains from alpha-beta pruning

---

## How to Run

1. Ensure all files are in the same folder and run `main.py`
2. Select a game mode:
   - Human vs Human
   - Human vs Engine
   - Engine vs Engine
3. Enter moves using the correct format (`e2e4`)
4. Use hints in Human vs Human or Human vs Engine mode:

```text
hint
Enter depth: 4
```

---

## Future Improvements

- Opening book integration
- Improved evaluation heuristics
- GUI interface
- Dynamic depth adjustment

---

## Key Concepts Demonstrated

- Minimax algorithm
- Alpha-beta pruning
- Game tree search
- Heuristic evaluation functions
- Performance benchmarking
