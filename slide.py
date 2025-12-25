#!/usr/bin/env python3
"""
sliding_puzzle.py - 3x3 sliding puzzle (8-puzzle) playable in terminal.

Controls:
- Type a tile number (1-8) to move that tile if it's adjacent to the blank.
- Or use w/a/s/d to move the blank up/left/down/right.
- Type "solve" to run the A* solver and show the solution.
- Type "shuffle" to reshuffle the board.
- Type "quit" or "q" to exit.

Requires Python 3.6+
"""
import random
import heapq
import sys
from typing import List, Tuple, Dict, Optional

Goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def index_to_rc(idx: int, size: int = 3) -> Tuple[int, int]:
    return divmod(idx, size)


def rc_to_index(r: int, c: int, size: int = 3) -> int:
    return r * size + c


def manhattan_distance(state: Tuple[int, ...], goal: Tuple[int, ...] = Goal, size: int = 3) -> int:
    # Sum of Manhattan distances of tiles (ignore blank)
    pos_goal = {val: i for i, val in enumerate(goal)}
    dist = 0
    for i, val in enumerate(state):
        if val == 0:
            continue
        gi = pos_goal[val]
        r1, c1 = index_to_rc(i, size)
        r2, c2 = index_to_rc(gi, size)
        dist += abs(r1 - r2) + abs(c1 - c2)
    return dist


def is_solvable(state: Tuple[int, ...]) -> bool:
    arr = [x for x in state if x != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    # For 3x3, solvable iff inversions even
    return inv % 2 == 0


def get_neighbors_blank(idx_blank: int, size: int = 3) -> List[int]:
    r, c = index_to_rc(idx_blank, size)
    neighbors = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < size and 0 <= nc < size:
            neighbors.append(rc_to_index(nr, nc, size))
    return neighbors


def shuffle_state(moves: int = 100, size: int = 3) -> Tuple[int, ...]:
    # Start from goal and make random legal moves -> always solvable
    state = list(Goal)
    blank = state.index(0)
    for _ in range(moves):
        nbrs = get_neighbors_blank(blank, size)
        swap_with = random.choice(nbrs)
        state[blank], state[swap_with] = state[swap_with], state[blank]
        blank = swap_with
    return tuple(state)


def print_board(state: Tuple[int, ...], size: int = 3) -> None:
    print("+---+---+---+")
    for r in range(size):
        row = []
        for c in range(size):
            v = state[rc_to_index(r, c, size)]
            row.append(" " if v == 0 else str(v))
        print("| " + " | ".join(f"{x}" for x in row) + " |")
        print("+---+---+---+")


def move_tile(state: Tuple[int, ...], tile: int) -> Optional[Tuple[int, ...]]:
    # Move tile by value if adjacent to blank, else None
    if tile == 0 or tile not in state:
        return None
    arr = list(state)
    i_tile = arr.index(tile)
    i_blank = arr.index(0)
    if i_tile in get_neighbors_blank(i_blank):
        arr[i_blank], arr[i_tile] = arr[i_tile], arr[i_blank]
        return tuple(arr)
    return None


def move_blank_direction(state: Tuple[int, ...], direction: str) -> Optional[Tuple[int, ...]]:
    # direction in 'w','a','s','d' corresponds to moving blank up/left/down/right
    dir_map = {
        "w": (-1, 0),
        "s": (1, 0),
        "a": (0, -1),
        "d": (0, 1),
    }
    if direction not in dir_map:
        return None
    size = 3
    arr = list(state)
    i_blank = arr.index(0)
    r, c = index_to_rc(i_blank, size)
    dr, dc = dir_map[direction]
    nr, nc = r + dr, c + dc
    if 0 <= nr < size and 0 <= nc < size:
        swap_i = rc_to_index(nr, nc, size)
        arr[i_blank], arr[swap_i] = arr[swap_i], arr[i_blank]
        return tuple(arr)
    return None


def a_star(start: Tuple[int, ...], goal: Tuple[int, ...] = Goal) -> Optional[List[Tuple[int, ...]]]:
    # A* search returning list of states from start to goal (inclusive) or None if failure
    if start == goal:
        return [start]
    open_heap = []
    heapq.heappush(open_heap, (manhattan_distance(start), 0, start))
    came_from: Dict[Tuple[int, ...], Optional[Tuple[int, ...]]] = {start: None}
    g_score: Dict[Tuple[int, ...], int] = {start: 0}
    visited = 0
    while open_heap:
        _, g, current = heapq.heappop(open_heap)
        visited += 1
        if current == goal:
            # reconstruct path
            path = []
            cur = current
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            path.reverse()
            # print(f"A* visited {visited} nodes.")
            return path
        i_blank = current.index(0)
        for nbr in get_neighbors_blank(i_blank):
            arr = list(current)
            arr[i_blank], arr[nbr] = arr[nbr], arr[i_blank]
            neighbor = tuple(arr)
            tentative_g = g + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f = tentative_g + manhattan_distance(neighbor)
                heapq.heappush(open_heap, (f, tentative_g, neighbor))
                came_from[neighbor] = current
    return None


def interactive_loop():
    print("3x3 Sliding Puzzle (8-puzzle). Type 'help' for commands.")
    state = shuffle_state(50)
    while not is_solvable(state):
        state = shuffle_state(50)  # Should always be solvable, but safety
    moves = 0
    while True:
        print_board(state)
        if state == Goal:
            print(f"Congratulations! Solved in {moves} moves.")
            cmd = input("Type 'shuffle' to play again or 'quit' to exit: ").strip().lower()
            if cmd in ("shuffle", "s"):
                state = shuffle_state(80)
                moves = 0
                continue
            else:
                break
        cmd = input("Enter tile (1-8) to move, w/a/s/d to move blank, 'solve', 'shuffle', 'quit': ").strip().lower()
        if cmd in ("q", "quit", "exit"):
            print("Goodbye.")
            break
        if cmd in ("help", "h", "?"):
            print("Commands: tile number (1-8), w/a/s/d to move blank, 'solve' to auto-solve, 'shuffle', 'quit'")
            continue
        if cmd == "shuffle":
            state = shuffle_state(80)
            moves = 0
            continue
        if cmd == "solve":
            print("Running A* solver (may take some seconds)...")
            path = a_star(state, Goal)
            if path is None:
                print("No solution found (unexpected for 3x3).")
            else:
                print(f"Solution found in {len(path)-1} moves. Showing steps:")
                for step in path[1:]:
                    print_board(step)
                    input("Press Enter for next step...")
                state = path[-1]
            continue
        if cmd in ("w", "a", "s", "d"):
            new = move_blank_direction(state, cmd)
            if new:
                state = new
                moves += 1
            else:
                print("Can't move blank that direction.")
            continue
        # try parse as tile number
        if cmd.isdigit():
            tile = int(cmd)
            if 1 <= tile <= 8:
                new = move_tile(state, tile)
                if new:
                    state = new
                    moves += 1
                else:
                    print("Tile not adjacent to blank; can't move.")
                continue
        print("Unknown command. Type 'help' for commands.")


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    try:
        interactive_loop()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye.")


if __name__ == "__main__":
    main()
