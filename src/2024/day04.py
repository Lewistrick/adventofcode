from typing import Literal

from aoc_tools import grid_blocks, grid_lines

Char = Literal["X", "M", "A", "S"] | str
Row = list[Char]
Grid = list[Row]


with open("data/04.in") as handle:
    lines = handle.read().split()
    grid: Grid = [list(line) for line in lines]


part1 = 0
tgt = "XMAS"
for line in grid_lines(grid):
    words = ["".join(line[i : i + len(tgt)]) for i in range(len(line) - len(tgt) + 1)]
    part1 += sum(1 for w in words if w == tgt)

print(part1)


def is_mas_cross(block: Grid):
    return (
        block[0][0] == "M"
        and block[0][2] == "M"
        and block[1][1] == "A"
        and block[2][0] == "S"
        and block[2][2] == "S"
    )


part2 = 0
for block in grid_blocks(grid, 3, 3):
    part2 += is_mas_cross(block)

print(part2)
