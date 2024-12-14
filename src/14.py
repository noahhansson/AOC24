from utils import read_input, timer, setup_args
import re
from dataclasses import dataclass
from collections import defaultdict

args = setup_args()


@dataclass
class Robot:
    x: int
    y: int
    dx: int
    dy: int

    def move(self, steps: int, xmax: int, ymax: int) -> None:
        self.x = (self.x + self.dx * steps) % xmax
        self.y = (self.y + self.dy * steps) % ymax

    @property
    def position(self) -> tuple[int, int]:
        return (self.x, self.y)


def parse_input(test: bool = False) -> list[Robot]:
    inpt = read_input("14", test=test)
    robots = []
    for row in inpt:
        x, y, dx, dy = map(int, re.findall("-?\d{1,3}", row))
        robots.append(Robot(x, y, dx, dy))
    return robots


def print_state(robots: list[Robot], xmax: int, ymax: int) -> str:
    positions: dict[tuple[int, int], int] = defaultdict(int)
    for robot in robots:
        positions[robot.position] += 1

    return "\n".join(
        [
            "".join([str(positions[(x, y)]) if (x, y) in positions else " " for x in range(0, xmax)])
            for y in range(0, ymax)
        ]
    )


def calculate_score(robots: list[Robot], xmax: int, ymax: int) -> int:
    positions: dict[tuple[int, int], int] = defaultdict(int)
    for robot in robots:
        positions[robot.position] += 1

    quadrants: dict[tuple[int, int], int] = defaultdict(int)

    score = 1

    x_mid = xmax // 2
    y_mid = ymax // 2

    for robot in robots:
        pos = robot.position
        if (pos[0] < x_mid) and (pos[1] < y_mid):
            quadrants[(0, 0)] += 1
        if (pos[0] > x_mid) and (pos[1] < y_mid):
            quadrants[(1, 0)] += 1
        if (pos[0] < x_mid) and (pos[1] > y_mid):
            quadrants[(0, 1)] += 1
        if (pos[0] > x_mid) and (pos[1] > y_mid):
            quadrants[(1, 1)] += 1

    for quadrant_score in quadrants.values():
        score *= quadrant_score

    return score


def calc_entropy(robots: list[Robot]) -> int:
    positions: dict[tuple[int, int], int] = defaultdict(int)
    for robot in robots:
        positions[robot.position] += 1

    score = 0
    for position in positions:
        for direction in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            if (position[0] + direction[0], position[1] + direction[1]) in positions:
                score += 1

    return score


@timer
def get_first_solution(test: bool = False):
    if test:
        xmax, ymax = (11, 7)
    else:
        xmax, ymax = (101, 103)

    robots = parse_input(test)

    for robot in robots:
        robot.move(100, xmax, ymax)

    return calculate_score(robots, xmax, ymax)


@timer
def get_second_solution(test: bool = False):
    if test:
        xmax, ymax = (11, 7)
    else:
        xmax, ymax = (101, 103)

    robots = parse_input(test)

    seen = set()

    i = 1

    max_entropy = 0
    max_entropy_i = 0
    max_entropy_str = ""

    while True:
        for robot in robots:
            robot.move(1, xmax, ymax)

        if tuple([r.position for r in robots]) in seen:
            print(f"Loop detected at iteration {i}")
            break

        if (entropy := calc_entropy(robots)) > max_entropy:
            max_entropy = entropy
            max_entropy_i = i
            max_entropy_str = print_state(robots, xmax, ymax)

        seen.add(tuple([r.position for r in robots]))
        i += 1

    print(max_entropy_str)

    return max_entropy_i


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
