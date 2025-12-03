from loguru import logger

from aoc_tools import read_data

data = read_data(day=1, suffix="in").split("\n")

def solve():
    curr = 50
    part1 = 0
    part2 = 0
    for instruction in data:
        direction, amount = instruction[0], int(instruction[1:])
        ticker = -1 if direction == "L" else 1
        for _ in range(amount):
            curr += ticker
            if curr == -1:
                curr = 99
            elif curr == 100:
                curr = 0
            
            if curr == 0:
                part2 += 1
        if curr == 0:
            part1 += 1

    logger.success(part1)
    logger.success(part2)
