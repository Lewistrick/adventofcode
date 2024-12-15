from collections import defaultdict
from itertools import count

from aoc_tools import NESW, nums, product, read_data

data = read_data(day=14).split("\n")

bots = []
for line in data:
    bot = tuple(nums(line))
    bots.append(bot)

p2 = 100
w, h = 101, 103
quadrants = [0, 0, 0, 0]
positions = defaultdict(int)
for x0, y0, vx, vy in bots:
    xt, yt = (x0 + p2 * vx) % w, (y0 + p2 * vy) % h
    positions[(xt, yt)] += 1


    if xt == w // 2 or yt == h // 2:
        continue

    match xt <= w // 2, yt <= h // 2:
        case True, True:  # upper left
            quadrants[0] += 1
        case False, True:  # upper right
            quadrants[1] += 1
        case True, False:  # lower left
            quadrants[2] += 1
        case False, False:  # lower right
            quadrants[3] += 1

p1 = product(quadrants)

most_adjacencies = 0
for p2 in count():
    positions = defaultdict(int)
    for x0, y0, vx, vy in bots:
        xt, yt = (x0 + p2 * vx) % w, (y0 + p2 * vy) % h
        positions[(xt, yt)] += 1

    adjacencies = 0
    for x, y in positions:
        for dx, dy in NESW:
            nx, ny = x + dx, y + dy
            if (nx, ny) in positions:
                adjacencies += 1

    if adjacencies > most_adjacencies:
        most_adjacencies = adjacencies
        print(f"{p2=} {adjacencies=}")
        for y in range(h):
            for x in range(w):
                if (x, y) in positions:
                    print("##", end="")
                else:
                    print("  ", end="")
            print()

        print("-" * 80)
        ans = input("Stop searching (y/n) >> ")
        if ans == "y":
            break

print(f"part 1: {p1}")
print(f"part 2: {p2}")
