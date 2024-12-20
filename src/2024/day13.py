from dataclasses import dataclass

from aoc_tools import nums, read_data

data = read_data(day=13, suffix="in")

puzzles = data.split("\n\n")


@dataclass
class Puzzle:
    ax: int
    ay: int
    bx: int
    by: int
    x: int
    y: int

    @classmethod
    def from_lines(cls, lines):
        a, b, p = lines.strip().split("\n")
        ax, ay = nums(a)
        bx, by = nums(b)
        x, y = nums(p)
        return cls(ax, ay, bx, by, x, y)

    def solve(self, part2=False) -> tuple[int, int]:
        if part2:
            self.x += 10000000000000
            self.y += 10000000000000

        # draw a line from (0, 0) with slope (ay/ax)
        a_slope = self.ay / self.ax

        # draw a line with slope (by/bx) that crosses (X, Y)
        b_slope = self.by / self.bx
        # solve for c: y = (by/bx)x + c
        # c = y - (by/bx) * x
        c = self.y - b_slope * self.x

        # now if the line for a and the line for b cross each other
        # between x=0 and x=self.x, this is solvable

        # note that below, x is used to make the formula,
        # which is different from the X in the puzzle (self.x)

        # y1 = sa * x
        # y2 = sb * x + c
        # y1=y2, so: sa * x = sb * x + c
        # (sa - sb) * x = c
        # x = c / (sa - sb)
        solx = c / (a_slope - b_slope)
        if not 0 <= solx <= self.x:
            return 0, 0

        a_presses = solx / self.ax
        b_presses = (self.x - solx) / self.bx

        # number of presses has to be an integer number
        if abs(round(a_presses) - a_presses) > 0.01:
            return 0, 0

        if abs(round(b_presses) - b_presses) > 0.01:
            return 0, 0

        return (round(a_presses), round(b_presses))


p1 = 0
p2 = 0
for lines in puzzles:
    puzzle = Puzzle.from_lines(lines)

    a_presses, b_presses = puzzle.solve()
    p1 += 3 * a_presses + b_presses

    a_presses, b_presses = puzzle.solve(True)
    p2 += 3 * a_presses + b_presses


print(p1)
print(p2)
