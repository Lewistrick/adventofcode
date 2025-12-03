import importlib
from argparse import ArgumentParser
from datetime import datetime

from loguru import logger

today = datetime.now()


def run_day():
    parser = ArgumentParser()
    parser.add_argument("-y", "--year", type=int, default=today.year)
    parser.add_argument("-d", "--day", type=int, default=today.day)
    args = parser.parse_args()

    module_name = f"aoc{args.year}.day{args.day:02d}"

    day_module = importlib.import_module(module_name)

    if hasattr(day_module, "solve"):
        logger.info(f"--- Running {args.year} Day {args.day} ---")
        day_module.solve()
    else:
        raise NameError(f"Error: Module '{module_name}' exists but has no 'solve()' function.")
