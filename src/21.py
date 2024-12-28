from utils import read_input, timer, setup_args
from functools import cache
from collections import deque

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
def get_path(key_from: str, key_to: str, numpad: bool = False) -> str:
    if numpad:
        neighbour_f = get_neighbours_numpad
    else:
        neighbour_f = get_neighbours_keypad

    queue: deque[tuple[str, str]] = deque()
    queue.append(("", key_from))

    while queue:
        path, curr_position = queue.popleft()

        if curr_position == key_to:
            return path

        # Add moves to queue in order of priority: "<v^>" due to distance from "A"-key
        for direction, position in sorted(
            neighbour_f(curr_position).items(), key=lambda x: "<v^>".find(x[0])
        ):
            if (direction not in path) or (direction == path[-1]):
                queue.append((path + direction, position))

    return ""


@cache
def count_presses(
    key_from: str, key_to: str, n_robots: int, numpad: bool
) -> int:
    path = get_path(key_from, key_to, numpad)
    keys = f"A{path}A"

    if n_robots == 0:
        return len(f"{path}A")
    else:
        score = 0
        for k_from, k_to in zip(keys, keys[1:]):
            score += count_presses(k_from, k_to, n_robots - 1, False)

        return score


def solve(n_robots: int, test: bool) -> int:
    codes = parse_input(test)

    total = 0

    for code in codes:
        score = 0
        keys = f"A{code}"
        for key_from, key_to in zip(keys, keys[1:]):
            score += count_presses(key_from, key_to, n_robots, True)

        total += int(code.replace("A", "")) * score

    return total


@timer
def get_first_solution(test: bool = False) -> int:
    return solve(2, test)


@timer
def get_second_solution(test: bool = False):
    return solve(25, test)


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
