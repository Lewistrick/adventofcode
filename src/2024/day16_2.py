import random
import time
from functools import cache
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

@cache
def getprio(cx: int, cy: int, ex: int, ey: int) -> int:
    """Heuristic function accounting for turn and straight movement costs."""
    return abs(cx - ex) + abs(cy - ey)


def get_solutions(
    sx: int, sy: int, ex: int, ey: int, tiles: set[Pos]
) -> Generator[tuple[set[Pos], int], None, None]:
    queue = [(0, 0, sx, sy, 0, 0, {(sx, sy)})]  # (prio, score, cx, cy, dx, dy, seen)
    shortest_score = 220_000
    shortest_to = {}  # {(cx, cy, dx, dy): dist}

    t0 = time.perf_counter()
    stepx = 0
    next_print = 1
    while queue:
        stepx += 1
        prio, score, cx, cy, dx, dy, seen = heappop(queue)

        if stepx >= next_print:
            next_print *= random.random() / 2 + 1
            tx = time.perf_counter()
            logger.debug(f"{tx-t0:.1f} {stepx=} {len(queue)=} {score=}")

        if score > shortest_score:
            continue

        if (
            olddist := shortest_to.get((cx, cy, dx, dy), shortest_score)
        ) and olddist < score:
            continue
        shortest_to[(cx, cy, dx, dy)] = olddist

        # Reached the end position
        if (cx, cy) == (ex, ey):
            shortest_score = score
            tx = time.perf_counter()
            logger.debug(f"{tx-t0:.1f} {stepx=} {len(queue)=} {score=}")
            logger.success(f"Found new solution with score {score}")
            yield seen, score
            continue

        # Go straight
        newpos = (cx + dx, cy + dy)
        if newpos in tiles and newpos not in seen:
            if (
                olddist := shortest_to.get((*newpos, dx, dy), shortest_score)
            ) and olddist < score + 1:
                continue
            heappush(
                queue,
                (
                    score + getprio(*newpos, ex, ey),
                    score + 1,
                    newpos[0],
                    newpos[1],
                    dx,
                    dy,
                    seen | {newpos},
                ),
            )

        # Explore all valid moves
        for ndx, ndy in NESW:
            # Avoid straight or reverse movement
            if abs(ndx) == abs(dx) and abs(ndy) == abs(dy):
                continue
            newpos = (cx + ndx, cy + ndy)

            if (
                olddist := shortest_to.get((*newpos, ndx, ndy))
            ) and olddist < score + 1001:
                continue

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

    logger.info(f"Took {time.perf_counter() - t0} seconds")


sols = []
shortest = 999_999_999
for sol, score in get_solutions(sx, sy, ex, ey, tiles):
    sols.append((sol, score))
    shortest = min(score, shortest)

part1 = shortest
logger.info(f"Part 1: {part1}")

sols2 = [sol for sol, score in sols if score == shortest]

allseen = set()
for sol, score in sols:
    if score == shortest:
        allseen |= sol

part2 = len(allseen)
logger.info(f"Part 2: {part2}")