from typing import Iterable, Literal

Char = Literal["X", "M", "A", "S"] | str
Row = list[Char]
Grid = list[Row]


with open("data/04.in") as handle:
    lines = handle.read().split()
    grid: Grid = [list(line) for line in lines]

# sample = """MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX"""
# grid = [list(line) for line in sample.split()]


def rotate_grid_cw(grid: Grid) -> Grid:
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
    return horizontals(rotate_grid_cw(grid), reverse)


def diagonals(grid: Grid) -> Iterable[str]:
    # y=     x=
    # ###0## ###3##
    # ##1### ##2###
    # #2#### #1####
    # 3##### 0#####
    # ###### ######
    for _ in range(4):
        for row in range(len(grid)):
            ys_up = range(row, -1, -1)
            xs_up = range(0, len(ys_up))
            diag = "".join(grid[y][x] for y, x in zip(ys_up, xs_up))
            yield diag
            if len(diag) > 1 and row < len(grid) - 1:
                yield diag[::-1]
            # ys_dn = range(row, len(grid))
            # xs_dn = range(0, len(ys_dn))
            # yield "".join(grid[y][x] for y, x in zip(ys_dn, xs_dn))

        grid = rotate_grid_cw(grid)


part1 = 0
tgt = "XMAS"
for lines in [horizontals(grid), verticals(grid), diagonals(grid)]:
    for line in lines:
        words = [
            "".join(line[i : i + len(tgt)]) for i in range(len(line) - len(tgt) + 1)
        ]
        part1 += sum(1 for w in words if w == tgt)

print(part1)


def get_blocks(grid, width, height) -> Iterable[Grid]:
    for _ in range(4):
        for y0 in range(len(grid) - height + 1):
            for x0 in range(len(grid[0]) - width + 1):
                block = []
                for y in range(y0, y0 + height):
                    block.append(grid[y][x0 : x0 + width])
                yield block
        grid = rotate_grid_cw(grid)


def is_mas_cross(block: Grid):
    return (
        block[0][0] == "M"
        and block[0][2] == "M"
        and block[1][1] == "A"
        and block[2][0] == "S"
        and block[2][2] == "S"
    )


part2 = 0
for block in get_blocks(grid, 3, 3):
    part2 += is_mas_cross(block)

print(part2)
