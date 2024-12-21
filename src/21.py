from utils import read_input, timer, setup_args
from functools import cache
from collections import deque
from itertools import product

args = setup_args()


def parse_input(test: bool = False) -> list[str]:
    inpt = read_input("21", test=test)
    return inpt


def get_neighbours_numpad(key: str) -> dict[str, str]:
    adjacent = {
        "9": {"<": "8", "v": "6"},
        "8": {"<": "7", "v": "5", ">": "9"},
        "7": {"v": "4", ">": "8"},
        "6": {"<": "5", "v": "3", "^": "9"},
        "5": {"<": "4", "v": "2", ">": "6", "^": "8"},
        "4": {"v": "1", ">": "5", "^": "7"},
        "3": {"<": "2", "v": "A", "^": "6"},
        "2": {"<": "1", "v": "0", ">": "3", "^": "5"},
        "1": {">": "2", "^": "4"},
        "0": {">": "A", "^": "2"},
        "A": {"<": "0", "^": "3"},
    }

    return adjacent[key]


def get_neighbours_keypad(key: str) -> dict[str, str]:
    adjacent = {
        "^": {"v": "v", ">": "A"},
        "v": {"<": "<", "^": "^", ">": ">"},
        "<": {">": "v"},
        ">": {"<": "v", "^": "A"},
        "A": {"<": "^", "v": ">"},
    }

    return adjacent[key]


@cache
def get_path(start: str, end: str, numpad: bool) -> list[list[str]]:
    queue: deque[tuple[str, list[str]]] = deque()

    max_len: int | None = None
    paths: list[list[str]] = []

    queue.append((start, []))

    while queue:
        position, path = queue.popleft()

        if max_len is not None and len(path) > max_len:
            return paths

        if position == end:
            paths.append(path)
            max_len = len(path)

        if numpad:
            neighbours = get_neighbours_numpad(position)
        else:
            neighbours = get_neighbours_keypad(position)

        for direction, button in neighbours.items():
            queue.append((button, path + [direction]))

    return []


def press_instructions(instructions: str, numpad: bool) -> list[str]:
    path_alternatives = []
    for b1, b2 in zip(f"A{instructions}", instructions):
        path_alternatives.append(get_path(b1, b2, numpad=numpad))

    paths = product(*path_alternatives)
    paths_formatted: list[str] = []
    for path in paths:
        path_formatted = []
        for instruction in path:
            path_formatted += instruction
            path_formatted += "A"
        paths_formatted.append("".join(path_formatted))

    return paths_formatted


def prune_instructions(instructions: list[str]) -> list[str]:
    lenghts = {i: len(i) for i in instructions}
    min_len = min(lenghts.values())
    return [i for i, length in lenghts.items() if length == min_len]


def solve(n_robots: int, test: bool) -> int:
    codes = parse_input(test)
    get_path("A", "<", False)

    score = 0

    for code in codes:
        instructions = press_instructions(code, numpad=True)

        for i in range(n_robots):
            print(f"Code: {code}, Robot nr {i + 1}")
            print(f"Number of instructions to parse: {len(instructions)}")
            instructions_next: list[str] = []
            for instruction in prune_instructions(instructions):
                instructions_next += press_instructions(
                    instruction, numpad=False
                )

            instructions = instructions_next

        min_len = len(prune_instructions(instructions_next)[0])
        score += int(code.replace("A", "")) * min_len
        print(f"Code: {code}, min length: {min_len}")

    return score


@timer
def get_first_solution(test: bool = False) -> int:
    return solve(2, test)


@timer
def get_second_solution(test: bool = False):
    return solve(25, test)


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
