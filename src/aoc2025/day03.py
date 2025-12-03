from loguru import logger

from aoc_tools import read_data

data = read_data(suffix="in").split("\n")


def solve_part(vals: list[int], n=2) -> int:
    """Find the maximum joltage of a bank."""
    if n == 1:
        if vals:
            return max(vals)
        return 0

    maxval = max(vals[:-n+1])
    maxval_idx = next(idx for idx, val in enumerate(vals) if val == maxval)
    sol = (10 ** (n-1)) * maxval + solve_part(vals[maxval_idx + 1 :], n - 1)
    return sol

def solve():
    part1 = 0
    part2 = 0
    for bank in data:
        joltages = [int(val) for val in bank]
        part1 += solve_part(joltages)
        part2 += solve_part(joltages, 12)

    logger.success(f"{part1=}")
    logger.success(f"{part2=}")
