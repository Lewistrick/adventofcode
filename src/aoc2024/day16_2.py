from heapq import heappop, heappush
from typing import Generator

from aoc_tools import NESW, read_data
from loguru import logger

Pos = tuple[int, int]

data = read_data(day=16, suffix="in").split("\n")

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


def getprio(cx: int, cy: int, ex: int, ey: int) -> int:
    """Heuristic function accounting for turn and straight movement costs."""
    return abs(cx - ex) + abs(cy - ey)


def get_solutions(
    sx: int, sy: int, ex: int, ey: int, tiles: set[Pos]
) -> Generator[tuple[set[Pos], int], None, None]:
    queue = [(0, 0, sx, sy, 0, 0, {(sx, sy)})]  # (prio, score, cx, cy, dx, dy, seen)
    shortest_score = float("inf")
    shortest_to = {}  # {(cx, cy, dx, dy): dist}

    while queue:
        _, score, cx, cy, dx, dy, seen = heappop(queue)

        # Prune states with worse priorities
        if olddist := shortest_to.get((cx, cy, dx, dy)):
            if score > olddist:
                continue
        shortest_to[(cx, cy, dx, dy)] = score

        # Stop exploring if score exceeds known shortest solution
        if score > shortest_score:
            continue

        # Reached the end position
        if (cx, cy) == (ex, ey):
            shortest_score = score
            yield seen, score
            continue

        # Go straight
        newpos = (cx + dx, cy + dy)
        if newpos in tiles and newpos not in seen:
            heappush(
                queue,
                (
                    score + getprio(*newpos, ex, ey),
                    score + 1,
                    *newpos,
                    dx,
                    dy,
                    seen | {newpos},
                ),
            )

        # Explore valid turns
        for ndx, ndy in NESW:
            # Avoid straight or reverse movement
            if abs(ndx) == abs(dx) and abs(ndy) == abs(dy):
                continue
            newpos = (cx + ndx, cy + ndy)
            if newpos in tiles and newpos not in seen:
                heappush(
                    queue,
                    (
                        score + getprio(*newpos, ex, ey),
                        score + 1001,
                        *newpos,
                        ndx,
                        ndy,
                        seen | {newpos},
                    ),
                )


sols = []
shortest = 999_999_999
for sol, score in get_solutions(sx, sy, ex, ey, tiles):
    sols.append((sol, score))
    shortest = min(score, shortest)

part1 = shortest
logger.info(f"Part 1: {part1}")

allseen = set()
for sol, score in sols:
    if score == shortest:
        allseen |= sol

part2 = len(allseen)
logger.info(f"Part 2: {part2}")  # too low: 625
