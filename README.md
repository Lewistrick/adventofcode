# Advent of Code solutions, by Lewistrick

## Setup
- Code is in the `src/` folder
    - The `src/aoc_tools.py` is a living document that should be used as much as possible
    - Every edition has its own folder, indicated by the year name (i.e. `src/2024`)
    - Daily solutions are named `day<day>.py`
        - Where `<day>` is the zero-padded day number, e.g. 01 or 24.
- Daily inputs are in the `data/` folder
    - Puzzle inputs are named `<day>.in` (zero-padded again)
    - Example inputs are named `<day>.ex<n>` (n is an indexing number)

## Run
- To create a starter script and two empty data files for a day, run `uv run start`.
- To execute a script for a given day, run `uv run today`.
- For both of the scripts above, you can specify one or both of these:
    - `-y 2025` to specify the year (in this case, 2025)
    - `-d 1` to specify the day (in this case the 1st day of advent)
