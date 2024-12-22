from utils import read_input, timer, setup_args
from functools import cache
from collections import deque
import heapq

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
def shortest_path(start: str, end: str, numpad: bool) -> int:
    queue: deque[tuple[str, list[str]]] = deque()

    queue.append((start, []))

    while queue:
        pos, path = queue.popleft()

        if pos == end:
            return len(path)

        if numpad:
            neighbours = get_neighbours_numpad(pos)
        else:
            neighbours = get_neighbours_keypad(pos)

        for direction, button in neighbours.items():
            queue.append((button, path + [direction]))

    return -1


@cache
def get_best_path(start: str, end: str, numpad: bool) -> list[str]:
    queue: list[tuple[int, str, str, list[str]]] = []
    costs: dict[str, int] = {}

    heapq.heapify(queue)
    heapq.heappush(queue, (0, start, "A", []))

    costs[start] = 0

    while queue:
        cost, pos, current_button, path = heapq.heappop(queue)

        if pos == end:
            return path

        if numpad:
            neighbours = get_neighbours_numpad(pos)
        else:
            neighbours = get_neighbours_keypad(pos)

        for direction, button in neighbours.items():
            heapq.heappush(
                queue,
                (
                    (
                        cost
                        + shortest_path(current_button, direction, False)
                        + 1,
                        button,
                        direction,
                        path + [direction],
                    )
                ),
            )

    return []


def press_instructions(instructions: str, numpad: bool) -> str:
    path = ""
    for b1, b2 in zip(f"A{instructions}", instructions):
        path += "".join(get_best_path(b1, b2, numpad=numpad))
        path += "A"

    return path


def solve(n_robots: int, test: bool) -> int:
    codes = parse_input(test)

    score = 0

    for code in codes:
        instruction = press_instructions(code, numpad=True)

        for i in range(n_robots):
            print(f"Code: {code}, Robot nr {i + 1}")
            instruction = press_instructions(instruction, numpad=False)

        score += int(code.replace("A", "")) * len(instruction)
        print(f"Code: {code}, Length: {len(instruction)}")

    return score


@timer
def get_first_solution(test: bool = False) -> int:
    get_best_path("A", "1", True)

    return solve(2, test)


@timer
def get_second_solution(test: bool = False):
    return solve(25, test)


get_best_path("3", "7", True)

print(f"P1: {get_first_solution(test=args.test)}")
# print(f"P2: {get_second_solution(test=args.test)}")
