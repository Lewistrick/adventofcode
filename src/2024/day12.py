from itertools import count
from aoc_tools import NESW, read_data

grid = read_data(suffix="in").split("\n")
plots = {}  # (x, y): letter
for y, row in enumerate(grid):
    for x, plot in enumerate(row):
        plots[(x, y)] = plot

seen = set()
regions: list[set[tuple[int, int]]] = []


def get_region(x, y) -> set[tuple[int, int]]:
    tgtval = plots[(x, y)]
    stack = [(x, y)]
    region: set[tuple[int, int]] = {(x, y)}
    while stack:
        px, py = stack.pop()
        for dx, dy in NESW:
            xx, yy = px + dx, py + dy
            if (xx, yy) in seen or (xx, yy) in region:
                continue
            if plots.get((xx, yy)) != tgtval:
                continue
            region.add((xx, yy))
            seen.add((xx, yy))
            stack.append((xx, yy))

    return region


for y in range(len(grid)):
    for x in range(len(grid[0])):
        if (x, y) in seen:
            continue

        regions.append(get_region(x, y))


def get_perimeter(region: set[tuple[int, int]]) -> int:
    perimeter = 0
    for x, y in region:
        n_neighbors = sum(1 for dx, dy in NESW if (x + dx, y + dy) in region)
        n_fences = 4 - n_neighbors
        perimeter += n_fences

    return perimeter


def get_sides(region: set[tuple[int, int]]) -> int:
    sides = 0
    for side_idx, (dx, dy) in enumerate(NESW):
        ldx, ldy = NESW[(side_idx - 1) % 4]
        rdx, rdy = NESW[(side_idx + 1) % 4]

        checked = set()
        for x, y in region:
            if (x, y) in checked:
                continue
            if (x + dx, y + dy) not in region:
                # this is a side
                sides += 1
                checked.add((x, y))
                # check left
                for nl in count(1):
                    lx, ly = (x + nl * ldx, y + nl * ldy)
                    if (lx, ly) in region and (lx + dx, ly + dy) not in region:
                        checked.add((lx, ly))
                    else:
                        break
                # check right
                for nr in count(1):
                    rx, ry = (x + nr * rdx, y + nr * rdy)
                    if (rx, ry) in region and (rx + dx, ry + dy) not in region:
                        checked.add((rx, ry))
                    else:
                        break

    return sides


part1 = sum(get_perimeter(region) * len(region) for region in regions)
print(part1)

part2 = sum(get_sides(region) * len(region) for region in regions)
print(part2)
