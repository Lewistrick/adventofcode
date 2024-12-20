from collections import defaultdict
from functools import cache
from heapq import heappop, heappush
from aoc_tools import NESW, read_data

data = read_data(suffix="ex").split("\n")

tiles = set()
walls = set()
for y, line in enumerate(data):
    for x, val in enumerate(line):
        if val == "#":
            walls.add((x, y))
            continue

        tiles.add((x, y))

        if val == "S":
            sx, sy = x, y
        if val == "E":
            ex, ey = x, y


@cache
def get_prio(x1, y1, x2, y2, cheats):
    return abs(x1 - x2) + abs(y1 - y2)


def solve(tiles, walls, sx, sy, ex, ey, cheats_left):
    heap = [(1, sx, sy, cheats_left)]

    cheat_counter = defaultdict(int)
    while heap:
        prio, (cx, cy), seen = heappop(heap)

        if (cx, cy) == (ex, ey):
            if cheats_left:
                continue
            cheat_counter[len(seen)] += 1

        for dx, dy in NESW:
            nx, ny = cx + dx, cy + dy

            # it costs one cheat to collide
            if (nx, ny) in walls:
                if not cheats_left:
                    continue
                cheats_left -= 1

            if (nx, ny) in tiles:
                # it costs one cheat to uncollide
                if (cx, cy) in walls:
                    if not cheats_left:
                        continue
                    cheats_left -= 1

                heappush(
                    get_prio(cx, cy, ex, ey, cheats_left),
                    (nx, ny),
                    seen & {(nx, ny)},
                )


"""
1. calculate shortest route from every tile
2. for every point, try to create all cheats
3. 
"""
