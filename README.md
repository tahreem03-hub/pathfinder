## Overview

This project is a step-by-step visual simulation of six classic uninformed (blind) search algorithms navigating a 15×15 grid from a **Start (S)** node to a **Target (T)** node while avoiding static walls. Every frame of the visualization shows exactly which nodes are being explored, which are waiting in the frontier, and what the final path looks like once found.

---

## Requirements

- Python 3.7 or higher
- Pygame

Install the dependency with:

```
pip install pygame
```

---

## How to Run

```
python pathfinder.py
```

---

## Controls

| Key | Action |
|-----|--------|
| `1` | Select BFS |
| `2` | Select DFS |
| `3` | Select UCS |
| `4` | Select DLS |
| `5` | Select IDDFS |
| `6` | Select Bidirectional Search |
| `ENTER` | Run the selected algorithm |
| `C` | Clear the grid (keep walls, reset visualization) |
| `ESC` | Stop the algorithm mid-execution |

The currently selected algorithm, status, and explored node count are always shown in the **bottom bar** of the window.

---

## Grid Layout

| Property | Value |
|----------|-------|
| Grid Size | 15 × 15 |
| Cell Size | 45 × 45 px |
| Start | Top-left `(0, 0)` — Green |
| Target | Bottom-right `(14, 14)` — Red |
| Walls | Fixed static obstacles — Black |

---

## Color Legend

| Color | Meaning |
|-------|---------|
| Green | Start node (S) |
| Red | Target node (T) |
| Black | Wall (impassable) |
| Orange | Explored node (already visited) |
| Cyan | Frontier node (in queue/stack, waiting) |
| Yellow | Final path from Start to Target |
| Light gray | Unvisited empty cell |

> **UCS only:** Small gray numbers on empty cells show the random edge weights (1–9). Bold numbers on explored cells show the cumulative path cost to reach that node.

---

## Movement Order

When expanding a node, neighbors are added in this strict **clockwise order** as required by the assignment:

| Direction | Row Δ | Col Δ |
|-----------|-------|-------|
| Up | -1 | 0 |
| Right | 0 | +1 |
| Down | +1 | 0 |
| Bottom-Right (diagonal) | +1 | +1 |
| Left | 0 | -1 |
| Top-Left (diagonal) | -1 | -1 |

Note: Top-Right and Bottom-Left diagonals are **not** included.

---

## Algorithms Implemented

### 1. Breadth-First Search (BFS)
Uses a **queue (FIFO)**. Explores all nodes level by level, guaranteeing the **shortest path** in terms of number of steps.

- **Data structure:** `collections.deque`
- **Complete:** Yes
- **Optimal:** Yes (unweighted)
- **Pros:** Always finds shortest path
- **Cons:** High memory usage; explores many nodes

---

### 2. Depth-First Search (DFS)
Uses a **stack (LIFO)**. Dives as deep as possible before backtracking.

- **Data structure:** Python list as stack
- **Complete:** No (can loop in infinite spaces)
- **Optimal:** No
- **Pros:** Low memory usage
- **Cons:** Can explore far-away nodes before finding nearby target; path may not be optimal

---

### 3. Uniform-Cost Search (UCS)
Uses a **priority queue** ordered by cumulative path cost. Each edge has a random weight (1–9). Expands the cheapest node first.

- **Data structure:** `heapq`
- **Complete:** Yes
- **Optimal:** Yes (finds minimum cost path)
- **Pros:** Finds cheapest path even with varying edge costs
- **Cons:** Slower than BFS if costs are uniform; high memory

---

### 4. Depth-Limited Search (DLS)
DFS with a **hard depth limit of 12**. Will not explore nodes beyond this depth.

- **Data structure:** Recursive stack
- **Depth Limit:** 12
- **Complete:** No (may miss target if it's deeper than the limit)
- **Optimal:** No
- **Pros:** Prevents infinite loops; controlled memory
- **Cons:** Incomplete if the target is beyond the limit

---

### 5. Iterative Deepening DFS (IDDFS)
Runs DLS repeatedly, increasing the depth limit by 1 each iteration (1, 2, 3, ...) until the target is found. Combines the memory efficiency of DFS with the completeness of BFS.

- **Data structure:** Recursive stack (reset each iteration)
- **Complete:** Yes
- **Optimal:** Yes (in terms of steps)
- **Pros:** Uses very little memory; guaranteed to find the shallowest solution
- **Cons:** Revisits nodes many times; slower in practice due to repeated work

---

### 6. Bidirectional Search (BiDir)
Runs two simultaneous **BFS searches** — one forward from Start, one backward from Target — until they meet in the middle.

- **Data structure:** Two `collections.deque` queues
- **Complete:** Yes
- **Optimal:** Yes (BFS from both ends)
- **Pros:** Much faster than single BFS in many cases; explores far fewer nodes
- **Cons:** More complex to implement; requires knowing the goal state in advance
- **Path construction:** When the two frontiers meet at a node, the forward path and reversed backward path are joined at the meeting point

---

## Project Structure

```
pathfinder.py    — Main source file (all code in one file)
README.md        — This file
```

---

## Implementation Notes

- All six algorithms are implemented as methods inside the `App` class.
- The `tick()` method handles drawing and event polling between each step, creating the step-by-step animation.
- `DLS` and `IDDFS` use a **local visited set** (not shared with global state) so that depth-limited backtracking works correctly — nodes are not permanently blocked across depth iterations.
- `UCS` uses random integer weights (regenerated each run) stored in a 15×15 matrix called `WEIGHTS`.
- Bidirectional search stores full paths in dictionaries (`vF`, `vB`) and reconstructs the complete path by joining and reversing at the meeting node.

---

### Best Case
Select **BiDir** or **BFS** — these find the target quickly when a clear, short path exists near the diagonal.

### Worst Case
Select **DFS** or **DLS** — DFS may explore most of the grid before finding the target. DLS will fail entirely if the target is deeper than the limit of 12.

---

## Dependencies

```
pygame
```

Install via:
```
pip install pygame
```
