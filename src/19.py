from utils import read_input, timer, setup_args
from functools import cache

args = setup_args()


def parse_input(test: bool = False) -> tuple[frozenset[str], list[str]]:
    inpt = read_input("19", test=test)
    patterns = frozenset(inpt[0].split(", "))
    designs = inpt[2:]
    return patterns, designs


@cache
def dfs(design: str, patterns: frozenset[str], max_l: int) -> int:
    if design == "":
        return 1

    score = 0
    for pattern_length in range(1, min(max_l, len(design)) + 1):
        if design[:pattern_length] in patterns:
            score += dfs(design[pattern_length:], patterns, max_l)
    return score


@timer
def get_first_solution(test: bool = False):
    patterns, designs = parse_input(test)

    max_l = max([len(p) for p in patterns])

    score = 0

    for design in designs:
        if dfs(design, patterns, max_l) > 0:
            score += 1

    return score


@timer
def get_second_solution(test: bool = False):
    patterns, designs = parse_input(test)

    max_l = max([len(p) for p in patterns])

    score = 0

    for design in designs:
        score += dfs(design, patterns, max_l)

    return score


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
