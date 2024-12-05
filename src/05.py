from utils import read_input, timer, setup_args
from collections import defaultdict

args = setup_args()

type Update = list[int]
type Rules = dict[int, set[int]]

def parse_input(test: bool) -> tuple[Rules, list[Update]]:
    rules: Rules = defaultdict(set)
    updates: list[Update] = []

    inpt = read_input("05", test=test)
    for row in inpt:
        if "|" in row:
            x, y = row.split("|")
            rules[int(x)].add(int(y))
        elif row != "":
            updates.append([int(x) for x in row.split(",")])

    return rules, updates


def find_invalid(update: Update, rules: Rules) -> tuple[int, int] | None:
    for i in range(len(update)):
        val = update[i]
        afters = update[i:]
        for after in afters:
            if val in rules[after]:
                return val, after
    return None


@timer
def get_first_solution(test: bool = False):
    rules, updates = parse_input(test=test)

    score = 0
    for update in updates:
        if find_invalid(update, rules) is None:
            score += update[len(update) // 2]

    return score


@timer
def get_second_solution(test: bool = False):
    rules, updates = parse_input(test=test)

    score = 0
    for update in updates:
        if find_invalid(update, rules) is None:
            continue
        while (error := find_invalid(update, rules)) is not None:
            i0 = update.index(error[0])
            i1 = update.index(error[1])
            update[i0] = error[1]
            update[i1] = error[0]

        score += update[len(update) // 2]
    return score


print(f" P1: {get_first_solution(test=args.test)}")
print(f" P2: {get_second_solution(test=args.test)}")
