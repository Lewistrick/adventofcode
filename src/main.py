import importlib
import shutil
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

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

def start_day():
    parser = ArgumentParser()
    parser.add_argument("-y", "--year", type=int, default=today.year)
    parser.add_argument("-d", "--day", type=int, default=today.day)
    args = parser.parse_args()

    day_file = Path.cwd() / f"src/aoc{args.year}/day{args.day:02d}.py"
    if day_file.is_file():
        raise OSError(f"Can't start day - file already exists: {day_file}")

    base_file = day_file.parent / "dayxx.py"
    shutil.copy(base_file, day_file)
    logger.success(f"Created day file: {day_file}")

    data_dir = Path.cwd() / f"data/{args.year}"
    for ext in ("in", "ex"):
        data_file = data_dir / f"{args.day:02d}.{ext}"
        data_file.touch()
        logger.success(f"Created empty data file: {data_file}")