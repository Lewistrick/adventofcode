from loguru import logger

from aoc_tools import read_data


def solve():
    fresh_ranges, available_ids = read_data(suffix="in").split("\n\n")
    fresh: set[range] = set()
    for new_rng in fresh_ranges.split("\n"):
        rfrom, rto = new_rng.split("-")
        fresh.add(range(int(rfrom), int(rto) + 1))

    part1 = sum(1 for id in available_ids.split("\n") if any(int(id) in rng for rng in fresh))
    logger.success(part1)

    new_ranges = []
    curr_rng = range(0, 0)
    # sort the fresh ranges by start index
    # and create new ranges by merging overlapping/connecting ranges
    for new_rng in sorted(fresh, key=lambda r: r.start):
        if new_rng.start in curr_rng:
            # ranges overlap; extend the current range
            curr_rng = range(curr_rng.start, max(new_rng.stop, curr_rng.stop))
        elif new_rng.start == curr_rng.stop:
            # ranges connect; extend the current range
            curr_rng = range(curr_rng.start, new_rng.stop)
        else:
            # ranges have a gap between them, create a new range
            new_ranges.append(curr_rng)
            curr_rng = new_rng

    # don't forget to add the last range
    new_ranges.append(curr_rng)

    part2 = sum(len(r) for r in new_ranges)
    logger.success(part2)
