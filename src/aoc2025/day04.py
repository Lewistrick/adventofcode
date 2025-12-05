from loguru import logger

from aoc_tools import DIR8, Grid, read_data


def is_reachable(grid: list[list[str]], x: int, y: int) -> bool:
    if grid[y][x] == ".":
        return False

    adjacent_rolls = 0
    for dx, dy in DIR8:
        if x + dx < 0 or x + dx >= len(grid[y]):
            continue
        if y + dy < 0 or y + dy >= len(grid):
            continue

        neighbor = grid[y + dy][x + dx]
        if neighbor == ".":
            continue
        elif neighbor == "@":
            adjacent_rolls += 1
        else:
            raise ValueError(f"Unexpected cell: {neighbor} at ({x + dx},{y + dy})")

    return adjacent_rolls < 4


def solve_part2(grid: Grid):
    """Use a new method to store rolls (in a set of (y,x) coordinates)."""
    rolls = set()
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col == "@":
                rolls.add((y, x))

    n_removed = 0
    while True:
        to_remove = set()
        for y, x in rolls:
            n_neighbors = 0
            for dy, dx in DIR8:
                if (y + dy, x + dx) in rolls:
                    n_neighbors += 1
            if n_neighbors < 4:
                to_remove.add((y, x))
        
        if to_remove:
            rolls -= to_remove
            n_removed += len(to_remove)
        else:
            break
    
    return n_removed


def solve():
    data = read_data(day=4, suffix="in").split("\n")
    grid = [list(row) for row in data]
    part1 = sum(1 for y in range(len(grid)) for x in range(len(grid[y])) if is_reachable(grid, x, y))
    logger.success(part1)

    part2 = solve_part2(grid)
    logger.success(part2)
