import heapq
import time
from copy import deepcopy

from aoc_tools import NESW, read_data

data = read_data(suffix="in").split("\n")

tiles = set()
walls = set()
for y, row in enumerate(data):
    for x, tile in enumerate(row):
        if tile == "#":
            walls.add((x, y))
            continue

        if tile == "S":
            sx, sy = x, y
        if tile == "E":
            ex, ey = x, y

        tiles.add((x, y))

heap = [(0, sx, sy, 1, 0, [(sx, sy, 1, 0)])]  # score, (pos), (dir), {route}
# heap = [(0, sx, sy, 1, 0)]  # score, (pos), (dir)
# seen = {(sx, sy, 1, 0)}
part1 = 0
t0 = time.perf_counter()
all_solution_coords = set()
maxscore = 0
while heap:
    score, cx, cy, dx, dy, route = heapq.heappop(heap)
    # if score > maxscore:
    #     print(f"\r{len(heap)} {score}", end=" ")

    if part1 and score > part1:
        continue

    if cx == ex and cy == ey:
        all_solution_coords |= {(x, y) for x, y, *_ in route}
        part1 = score
        break

    # first, try to add the same direction
    if (cx + dx, cy + dy) in tiles:
        newroute = deepcopy(route)
        newroute.append((cx + dx, cy + dy, dx, dy))
        straight = (score + 1, cx + dx, cy + dy, dx, dy, newroute)
        # straight = (score + 1, cx + dx, cy + dy, dx, dy)
        heapq.heappush(heap, straight)
        # seen.add((cx + dx, cy + dy, dx, dy))

    for ndx, ndy in NESW:
        nx, ny = cx + ndx, cy + ndy

        if nx == ndx and ny == ndy:
            # straight direction already added
            continue

        if (nx, ny) == (-ndx, -ndy):
            # turning around isn't allowed
            continue

        if (nx, ny) in walls:
            # this is a wall piece
            continue

        if (nx, ny, ndx, ndy) in route:
            continue

        newroute = deepcopy(route)
        newroute.append((nx, ny, ndx, ndy))
        heapq.heappush(heap, (score + 1001, nx, ny, ndx, ndy, newroute))
        # heapq.heappush(heap, (score + 1001, nx, ny, ndx, ndy))
        # seen.add((cx + ndx, cy + ndy, ndx, ndy))

tx = time.perf_counter() - t0
print(f"{tx:.3f}")
print(len(heap))
print(part1)

seen = all_solution_coords
for y in range(len(data)):
    for x in range(len(data[0])):
        if (x, y) == (sx, sy):
            print("S", end="")
        elif (x, y) == (ex, ey):
            print("E", end="")
        elif (x, y) in tiles:
            print(".", end="")
        else:
            print("#", end="")
    print(" --> ", end="")
    for x in range(len(data[0])):
        if (x, y) in seen:
            print("O", end="")
        elif (x, y) in tiles:
            print(".", end="")
        elif (x, y) in walls:
            print("#", end="")
        else:
            raise ValueError(f"{(x,y)} not found")
    print()

print(part1)
part2 = len(all_solution_coords)
print(part2)