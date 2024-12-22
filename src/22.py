from utils import read_input, timer, setup_args
from collections import defaultdict, deque

args = setup_args()


def parse_input(test: bool = False) -> list[int]:
    inpt = read_input("22", test=test)
    return list(map(int, inpt))


def mix(secret: int, value: int) -> int:
    return secret ^ value


def prune(secret: int) -> int:
    return secret & (2**24 - 1)


def get_next_secret(secret: int) -> int:
    secret = prune(mix(secret, secret << 6))
    secret = prune(mix(secret, secret >> 5))
    secret = prune(mix(secret, secret << 11))

    return secret


@timer
def get_first_solution(test: bool = False) -> int:
    start_values = parse_input(test)

    score = 0

    for value in start_values:
        secret = value

        for _ in range(0, 2000):
            secret = get_next_secret(secret)

        score += secret

    return score


@timer
def get_second_solution(test: bool = False) -> int:
    start_values = parse_input(test)

    sequence_scores: dict[tuple[int, ...], int] = defaultdict(int)

    for value in start_values:
        price_changes: deque[int] = deque(maxlen=4)
        seen: set[tuple[int, ...]] = set()
        secret = value

        for _ in range(0, 2000):
            price = secret % 10

            next_secret = get_next_secret(secret)
            next_price = next_secret % 10

            price_change = next_price - price

            price_changes.append(price_change)

            if len(price_changes) == 4:
                sequence = tuple(price_changes)
                if sequence not in seen:
                    sequence_scores[sequence] += next_price
                    seen.add(sequence)

            secret = next_secret

    max_score = max(sequence_scores.values())

    return max_score


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
