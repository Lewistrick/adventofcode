from aoc_tools import Grid, grid_blocks, grid_lines, read_data

data = read_data(day=4)
lines = data.split()
grid: Grid = [list(line) for line in lines]


part1 = 0
tgt = "XMAS"
for line in grid_lines(grid):
    words = ["".join(line[i : i + len(tgt)]) for i in range(len(line) - len(tgt) + 1)]
    part1 += sum(1 for w in words if w == tgt)

print(part1)


def is_mas_cross(block: Grid) -> bool:
    """Check if a block (a 3x3 grid) is a X of 'MAS', i.e. it looks like this:

    M.M
    .A.
    S.S

    Where '.' can be any character.

    Note that we don't check for rotated versions because grid_blocks already does this.
    Also note that we don't check for mirrored versions because they equal the original.
    """
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
