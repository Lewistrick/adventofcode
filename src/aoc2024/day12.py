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


def get_n_borders(region: set[tuple[int, int]]) -> int:
    """Get the number of borders of a region.

    For example, this region A has 8 borders:

    AA.
    .AA

    This is done by adding the number of borders in each direction,
    in this case 2+2+2+2. The north direction has one border that spans
    the two plots on the north row, and one border that spans the plot
    in the southeast.

    We check every plot in a region, going left-right, top-bottom, so starting
    northwest. If it's a sidbordere (there is no region plot to the north), we
    also check adjacent directions (east and west are adjacent to north). In
    this case, there is a plot to the east. This is not counted as an extra
    border, because it's part of the same border.
    Going further in the left-right/top-bottom checking, we see that the second
    plot is already checked and we move on. The third plot is not a border,
    because there's a region plot to the north, and the fourth is a border that
    has no neighbors we need to check again.

    Next, we go to east; the adjacent directions are north and south. You could
    also see it as checking a rotated map for north borders.
    """
    n_borders = 0
    # directions are denoted by (dx, dy), e.g. north is (0, -1) because the x
    # value doesn't change and the y value goes closer to 0.
    for diri, (dx, dy) in enumerate(NESW):
        # get the adjacent directions (l and r mean left and right)
        ldx, ldy = NESW[(diri - 1) % 4]
        rdx, rdy = NESW[(diri + 1) % 4]

        # keep track of the region plots we checked for this direction
        checked = set()
        for x, y in region:
            if (x, y) in checked:
                continue
            checked.add((x, y))

            if (x + dx, y + dy) not in region:
                # this is a border
                n_borders += 1
                checked.add((x, y))

                # check left whether it belongs to the same border piece
                for nl in count(1):
                    # first go `nl` spaces left
                    lx, ly = (x + nl * ldx, y + nl * ldy)
                    # if it's in the region, go one straight from there
                    if (lx, ly) in region and (lx + dx, ly + dy) not in region:
                        # if that's not in the region, it's the same border
                        checked.add((lx, ly))
                    else:
                        # otherwise, stop checking left
                        break

                # check right (clockwise) in the same way
                for nr in count(1):
                    rx, ry = (x + nr * rdx, y + nr * rdy)
                    if (rx, ry) in region and (rx + dx, ry + dy) not in region:
                        checked.add((rx, ry))
                    else:
                        break

    return n_borders


part1 = sum(get_perimeter(region) * len(region) for region in regions)
print(part1)

part2 = sum(get_n_borders(region) * len(region) for region in regions)
print(part2)
