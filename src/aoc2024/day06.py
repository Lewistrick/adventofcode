from copy import deepcopy
from aoc_tools import read_data

lines = read_data(day=6, suffix="in").split()

occupied = set()
for y in range(len(lines)):
    for x in range(len(lines[y])):
        if lines[y][x] == "#":
            occupied.add((x, y))
        elif lines[y][x] in "^<>v":
            startx = x
            starty = y


# dx/dy
directions = ((0, -1), (1, 0), (0, 1), (-1, 0))


def part1(occupied):
    currx, curry = startx, starty
    diridx = 0

    visited = set()  # x, y, diridx
    is_loop = False

    while True:
        visited.add((currx, curry, diridx))

        dx, dy = directions[diridx]
        newx, newy = currx + dx, curry + dy

        if (newx, newy, diridx) in visited:
            is_loop = True
            break

        if (newx, newy) in occupied:
            diridx = (diridx + 1) % 4
            continue

        if newx < 0 or newx >= len(lines[0]):
            break

        if newy < 0 or newy >= len(lines):
            break

        currx, curry = newx, newy

    seen = {(x, y) for (x, y, _) in visited}

    return seen, is_loop


seen, _ = part1(occupied)
p1 = len(seen)
print(p1)

p2 = 0
for x, y in seen - occupied:
    if (x, y) == (startx, starty):
        continue

    occ2 = deepcopy(occupied)
    occ2.add((x, y))
    _, is_loop = part1(occ2)
    p2 += is_loop

print(p2)
