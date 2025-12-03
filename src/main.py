from argparse import ArgumentParser
from datetime import datetime

today = datetime.now()

def run_day():
    parser = ArgumentParser()
    parser.add_argument("-y", "--year", type=int, default=today.year)
    parser.add_argument("-d", "--day", type=int, default=today.day)
    args = parser.parse_args()

    print(args)
    