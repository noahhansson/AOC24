from utils import read_input, timer, setup_args
from collections import defaultdict
from functools import cache

args = setup_args()


def parse_input(test: bool = False) -> dict[int, int]:
    inpt = read_input("11", test=test)

    stones: dict[int, int] = defaultdict(int)
    for stone in inpt[0].split(" "):
        stones[int(stone)] += 1

    return stones


@cache
def blink(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    elif (stone_len := len(str(stone))) % 2 == 0:
        return [
            int(str(stone)[: stone_len // 2]),
            int(str(stone)[stone_len // 2 :]),
        ]
    else:
        return [stone * 2024]


def blink_all(stones: dict[int, int]) -> dict[int, int]:
    new_stones: dict[int, int] = defaultdict(int)

    for stone, freq in stones.items():
        for new_stone in blink(stone):
            new_stones[new_stone] += freq

    return new_stones


@timer
def get_first_solution(test: bool = False) -> int:
    stones = parse_input(test)

    for _ in range(25):
        stones = blink_all(stones)

    score = 0
    for value in stones.values():
        score += value

    return score


@timer
def get_second_solution(test: bool = False) -> int:
    stones = parse_input(test)

    for _ in range(75):
        stones = blink_all(stones)

    score = 0
    for value in stones.values():
        score += value

    return score


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
