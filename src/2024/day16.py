from copy import deepcopy
from aoc_tools import NESW, read_data

data = read_data(suffix="ex").split("\n")

tiles = set()
for y, row in enumerate(data):
    for x, val in enumerate(row):
        if val == "#":
            continue

        if val == "S":
            sx, sy = x, y
        if val == "E":
            ex, ey = x, y

        tiles.add((x, y))

seen = {(sx, sy)}
stack = [(sx, sy, 1, 0)]
while stack:
    cx, cy, dx, dy, seen = stack.pop(0)

    # first, try to add the same direction
