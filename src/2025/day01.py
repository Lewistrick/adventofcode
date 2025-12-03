from aoc_tools import read_data
from loguru import logger

data = read_data(day=1, suffix="ex").split("\n")

curr = 50
maxval = 100
part1 = 0
part2 = 0
for ii, instruction in enumerate(data, 1):
    direction, amount = instruction[0], int(instruction[1:])
    ticker = -1 if direction == "L" else 1
    for click in range(amount):
        curr += ticker
        if curr == -1:
            curr = 99
        elif curr == 100:
            curr = 0
        
        if curr == 0:
            part2 += 1
    if curr == 0:
        part1 += 1

logger.success(part1)  # 984 correct
logger.success(part2)  # 4632|4720 te laag, 5750|6156 te hoog, 5660|5662 incorrect
