from dataclasses import dataclass

from aoc_tools import nums, read_data

data = read_data(suffix="in")

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

    def solve_hard(self) -> tuple[int, int]:
        

    def solve_easy(self, part2=False):
        if part2:
            self.x += 10000000000000
            self.y += 10000000000000

        max_a_presses = min((self.x // self.ax), (self.y // self.ay))

        # start with a=0 (pressing a costs more)
        for a_presses in range(max_a_presses + 1):
            xa = a_presses * self.ax

            b_presses, rest = divmod(self.x - xa, self.bx)
            if rest:
                continue

            ya = a_presses * self.ay
            yb = b_presses * self.by

            if part2 and a_presses > 100 or b_presses > 100:
                continue

            if ya + yb == self.y:
                print(f"{a_presses=} {b_presses=}")
                return a_presses, b_presses

        print(f"Not possible: X={self.x}, Y={self.y}")
        return 0, 0


p1 = 0
p2 = 0
for lines in puzzles:
    puzzle = Puzzle.from_lines(lines)
    a_presses, b_presses = puzzle.solve_easy()
    p1 += 3 * a_presses + b_presses

    a_presses, b_presses = puzzle.solve_easy(True)
    p2 += 3 * a_presses + b_presses

print(p1)  # 25754 too low
print(p2)
