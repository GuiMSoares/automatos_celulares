"""Core WireWorld cellular automaton logic and grid operations."""

from typing import List
from constants import EMPTY, CONDUCTOR, ELECTRON_HEAD, ELECTRON_TAIL, CHAR_TO_STATE, STATE_CHARS


def clamp(v, lo, hi):
    """Clamp a value between lo and hi."""
    return max(lo, min(hi, v))


def new_grid(w: int, h: int, fill: int = EMPTY) -> List[List[int]]:
    """Create a new grid filled with the specified value."""
    return [[fill for _ in range(w)] for _ in range(h)]


def copy_grid(g: List[List[int]]) -> List[List[int]]:
    """Create a deep copy of a grid."""
    return [row[:] for row in g]


def load_state(path: str) -> List[List[int]]:
    """Load a WireWorld state from a text file."""
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]
    maxlen = max((len(line) for line in lines), default=0)
    grid = []
    for line in lines:
        row = [CHAR_TO_STATE.get(ch, EMPTY) for ch in line]
        if len(row) < maxlen:
            row.extend([EMPTY] * (maxlen - len(row)))
        grid.append(row)
    return grid


def save_state(path: str, grid: List[List[int]]):
    """Save a WireWorld state to a text file."""
    with open(path, 'w', encoding='utf-8') as f:
        for row in grid:
            f.write(''.join(STATE_CHARS.get(cell, '.') for cell in row) + '\n')


def count_head_neighbors(grid: List[List[int]], x: int, y: int) -> int:
    """Count the number of electron heads neighboring the given cell."""
    h = len(grid)
    w = len(grid[0]) if h else 0
    cnt = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                if grid[ny][nx] == ELECTRON_HEAD:
                    cnt += 1
    return cnt


def step_wireworld(grid: List[List[int]]) -> List[List[int]]:
    """Perform one step of the WireWorld cellular automaton."""
    h = len(grid)
    w = len(grid[0]) if h else 0
    nextg = new_grid(w, h, EMPTY)
    for y in range(h):
        for x in range(w):
            cell = grid[y][x]
            if cell == EMPTY:
                nextg[y][x] = EMPTY
            elif cell == ELECTRON_HEAD:
                nextg[y][x] = ELECTRON_TAIL
            elif cell == ELECTRON_TAIL:
                nextg[y][x] = CONDUCTOR
            elif cell == CONDUCTOR:
                heads = count_head_neighbors(grid, x, y)
                nextg[y][x] = ELECTRON_HEAD if heads in (1, 2) else CONDUCTOR
    return nextg

