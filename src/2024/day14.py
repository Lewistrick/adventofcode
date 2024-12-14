from collections import defaultdict
from itertools import count

from aoc_tools import NESW, nums, product, read_data

data = read_data(suffix="in").split("\n")

bots = []
for line in data:
    bot = tuple(nums(line))
    bots.append(bot)

t = 100
w, h = 101, 103
# w, h = 11, 7
quadrants = [0, 0, 0, 0]
positions = defaultdict(int)
for x0, y0, vx, vy in bots:
    xt, yt = (x0 + t * vx) % w, (y0 + t * vy) % h
    positions[(xt, yt)] += 1

    # print(x0, y0, vx, vy)
    # print((xt, yt))

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

# print(quadrants)
print(product(quadrants))

bestscore = 0
for t in count():
    positions = defaultdict(int)
    for x0, y0, vx, vy in bots:
        xt, yt = (x0 + t * vx) % w, (y0 + t * vy) % h
        positions[(xt, yt)] += 1

    score = 0
    for x, y in positions:
        for dx, dy in NESW:
            nx, ny = x + dx, y + dy
            if (nx, ny) in positions:
                score += 1

    if score > bestscore:
        bestscore = score
        print(f"{t=} {score=}")
        for y in range(h):
            for x in range(w):
                if (x, y) in positions:
                    print("##", end="")
                else:
                    print("  ", end="")
            print()

        input("-" * 80)
