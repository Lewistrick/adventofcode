from typing import Any, Generator

from aoc_tools import NESW, read_data

Pos = tuple[int, int]

data = read_data(suffix="ex").split("\n")

tiles = set()
for y, row in enumerate(data):
    for x, tile in enumerate(row):
        if tile == "#":
            continue

        if tile == "S":
            sx, sy = x, y
        if tile == "E":
            ex, ey = x, y

        tiles.add((x, y))

part1 = 0


def get_solutions(
    score: int, cx: int, cy: int, dx: int, dy: int, seen: set[Pos]
) -> Generator[tuple[set[Pos], int], Any, None]:
    global part1

    if part1 and score > part1:
        # print(f"Returning with too high score {score}")
        return

    # if (cx, cy) == (9, 7):
    #     breakpoint()

    if (cx, cy) == (ex, ey):
        part1 = score
        yield (seen, score)

    # turns
    for ndx, ndy in NESW:
        if abs(ndx) == abs(dx) and abs(ndy == abs(dy)):
            # don't go straight or reverse
            continue

        if (newpos := (cx + ndx, cy + ndy)) not in tiles:
            # don't go through walls
            continue

        if newpos in seen:
            # don't revisit
            continue

        newseen = seen | {newpos}
        yield from get_solutions(score + 1001, *newpos, ndx, ndy, newseen)

    # straight
    if (newpos := (cx + dx, cy + dy)) in tiles:
        if newpos not in seen:
            newseen = seen | {newpos}
            yield from get_solutions(score + 1, *newpos, dx, dy, newseen)


allseen = set()
for sol, score in get_solutions(0, sx, sy, 1, 0, {sx, sy}):
    allseen |= sol

    # print()
    # print("   ", end="")
    # for x in range(len(data[0])):
    #     print(x % 10, end="")
    # print()

    # for y in range(len(data)):
    #     print(f"{y:2d}", end=" ")
    #     for x in range(len(data[0])):
    #         if (x, y) in sol:
    #             print("O", end="")
    #         elif (x, y) in tiles:
    #             print(".", end="")
    #         else:
    #             print("#", end="")
    #     print()

    # print(score)

print(score)
print(len(allseen) - 1)
