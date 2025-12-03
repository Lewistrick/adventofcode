import datetime
import re
from functools import reduce
from typing import Any, Iterable

Grid = list[list[Any]]

TODAY = datetime.datetime.now()
YEAR = TODAY.year
DAY = TODAY.day

NESW = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def read_data(year: int = YEAR, day: int = DAY, suffix="in") -> str:
    with open(f"data/{year}/{day:02d}.{suffix}") as handle:
        return handle.read()


def rotate_grid_ccw(grid: Grid) -> Grid:
    newgrid: Grid = [[] for _ in grid[0]]
    for col in range(len(grid[0])):
        for row in grid:
            newgrid[len(grid[0]) - col - 1].append(row[col])

    return newgrid


def show_grid(grid: Grid):
    for row in grid:
        print("".join(row))


def horizontals(grid, reverse=True) -> Iterable[str]:
    for row in grid:
        yield "".join(row)
        if reverse:
            yield "".join(row[::-1])


def verticals(grid, reverse=True) -> Iterable[str]:
    for col in horizontals(rotate_grid_ccw(grid), reverse):
        yield col


def diagonals(grid: Grid) -> Iterable[str]:
    """Return all diagonals of a grid.

    Example grid:
        abc
        def
        ghi

    This will return these diagonals:
        a   c   g   i
        db  bd  bf  fb  dh  hd  fh  hf
        aei iea gec ceg
    """
    for _ in range(4):
        for row in range(len(grid)):
            # Find all diagonals starting on the left side of the grid
            ys_up = range(row, -1, -1)
            xs_up = range(0, len(ys_up))
            diag = "".join(grid[y][x] for y, x in zip(ys_up, xs_up))
            yield diag

            # Reversing corner diagonals (length 1) is of no use
            if len(diag) == 1:
                continue

            # Don't reverse corner diagonals, these are covered by rotations
            if row == len(grid) - 1:
                continue

            # Also return the reversed diagonal
            yield diag[::-1]

        # Rotate the grid to find diagonals starting from all sides
        grid = rotate_grid_ccw(grid)


def grid_lines(grid: Grid) -> Iterable[Any]:
    """Return all lines in a grid: horizontal, vertical, and diagonal."""
    for lines in (horizontals(grid), verticals(grid), diagonals(grid)):
        for line in lines:
            yield (line)


def grid_blocks(grid: Grid, width: int, height: int, rotate=True) -> Iterable[Grid]:
    """Get all sub-blocks of a grid. Returns mini-grids.

    Example grid:
        123
        456
        789

    Given width=height=2, this will yield these four subgrids:
        12  23  45  56
        45  56  78  89
    """
    for _ in range(4):
        for y0 in range(len(grid) - height + 1):
            for x0 in range(len(grid[0]) - width + 1):
                block = []
                for y in range(y0, y0 + height):
                    block.append(grid[y][x0 : x0 + width])
                yield block
        if rotate:
            grid = rotate_grid_ccw(grid)
        else:
            return

def nums(s):
    return map(int, re.findall("-?\\d+", s))


def product(ns):
    return reduce(lambda a, b: a * b, ns, 1)