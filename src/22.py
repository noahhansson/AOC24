from utils import read_input, timer, setup_args

args = setup_args()


def parse_input(test: bool = False) -> list[int]:
    inpt = read_input("22", test=test)
    return list(map(int, inpt))


def mix(secret: int, value: int) -> int:
    return secret ^ value


def prune(secret: int) -> int:
    return secret & (2**24 - 1)


def next_secret(secret: int) -> int:
    secret = prune(mix(secret, secret << 6))
    secret = prune(mix(secret, secret >> 5))
    secret = prune(mix(secret, secret << 11))

    return secret


@timer
def get_first_solution(test: bool = False):
    start_values = parse_input(test)

    score = 0

    for value in start_values:
        secret = value

        for _ in range(0, 2000):
            secret = next_secret(secret)

        score += secret

    return score


@timer
def get_second_solution(test: bool = False):
    start_values = parse_input(test)

    score = 0

    # {(Monkey, step): price}
    prices: dict[tuple[int, int], int] = {}
    # {(Monkey, step): change}
    price_changes: dict[tuple[int, int], int] = {}

    for i, value in enumerate(start_values):
        secret = value

        prices[i, 0] = secret % 10

        for j in range(0, 2000):
            secret = next_secret(secret)
            prices[i, j + 1] = secret % 10
            price_changes[i, j + 1] = prices[i, j + 1] - prices[i, j]

    # {sequence: {monkey: value}}
    sequence_values: dict[tuple[int, ...], dict[int, int]] = {}

    for i in range(4, 2001):
        sequence_idx = [i - 3, i - 2, i - 1, i]
        for monkey in range(len(start_values)):
            sequence = tuple([price_changes[monkey, x] for x in sequence_idx])

            if sequence not in sequence_values:
                sequence_values[sequence] = {}

            if monkey not in sequence_values[sequence]:
                sequence_values[sequence][monkey] = prices[monkey, i]

    max_value = 0

    for sequence in sequence_values.keys():
        monkey_prices = sequence_values[sequence]
        if (score := sum(monkey_prices.values())) > max_value:
            max_value = score

    return max_value


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
