from utils import read_input, timer, setup_args
import re

args = setup_args()


def parse_input(test: bool = False):
    inpt = read_input("13", test=test)

    equations = []

    equation: dict[str, int] = {}
    for row in inpt:
        if row == "":
            equations.append(equation)
            equation = {}
        elif "A" in row:
            a, c = re.findall("\d{1,}", row)
            equation["a"] = int(a)
            equation["c"] = int(c)
        elif "B" in row:
            b, d = re.findall("\d{1,}", row)
            equation["b"] = int(b)
            equation["d"] = int(d)
        elif "Prize" in row:
            x, y = re.findall("\d{1,}", row)
            equation["x"] = int(x)
            equation["y"] = int(y)

    if equation:
        equations.append(equation)

    return equations


def det(a: int, b: int, c: int, d: int) -> int:
    return a * d - b * c


def solve(a: int, b: int, c: int, d: int, x: int, y: int) -> tuple[float, float]:
    return 1 / det(a, b, c, d) * (d * x - b * y), 1 / det(a, b, c, d) * (-c * x + a * y)


def get_solution(equation: dict[str, int]) -> tuple[int, int] | None:
    solution = solve(**equation)
    solution_rounded = (round(solution[0]), round(solution[1]))
    if all(
        [
            solution_rounded[0] * equation["a"] + solution_rounded[1] * equation["b"] == equation["x"],
            solution_rounded[0] * equation["c"] + solution_rounded[1] * equation["d"] == equation["y"],
        ]
    ):
        return solution_rounded
    else:
        return None


@timer
def get_first_solution(test: bool = False):
    equations = parse_input(test)

    score = 0

    for equation in equations:
        if solution := get_solution(equation):
            score += solution[0] * 3 + solution[1]

    return score


@timer
def get_second_solution(test: bool = False):
    equations = parse_input(test)

    score = 0

    for equation in equations:
        equation["x"] += 10000000000000
        equation["y"] += 10000000000000
        if solution := get_solution(equation):
            score += solution[0] * 3 + solution[1]

    return score


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
