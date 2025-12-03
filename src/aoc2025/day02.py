from functools import cache
from math import log10

from loguru import logger

from aoc_tools import read_data

data = read_data(suffix="in").split(",")

@cache
def get_divisors(n):
    divisors = []
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            divisors.append(i)

    return divisors

def solve():
    part1 = 0
    part2 = 0
    for rng in data:
        logger.debug(f"{rng=}")
        breakpoint()
        low, high = rng.split("-")

        for n in range(int(low), int(high) + 1):
            ndigits = int(log10(n)) + 1
            if ndigits == 1:
                continue

            added = False
            for sublen in get_divisors(ndigits):
                s = str(n)
                parts = {s[i * sublen : i * sublen + sublen] for i in range(ndigits//sublen)}
                if len(parts) == 1:
                    if not added:
                        part2 += n
                        # logger.success(f"Invalid (part 2): {n} {parts=}")

                    added = True
                    if sublen == ndigits / 2:
                        # logger.info(f"Invalid (part 1): {n} {parts=}")
                        part1 += n


    logger.success(part1)
    logger.success(part2)
