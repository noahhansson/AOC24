from utils import read_input, timer, setup_parser
from collections import defaultdict

parser = setup_parser()
args, _= parser.parse_known_args()


@timer
def get_first_solution(test: bool = False):
    inpt = read_input("01", test=test)

    l1 = [int(s.split("   ")[0]) for s in inpt]
    l2 = [int(s.split("   ")[1]) for s in inpt]

    l1 = sorted(l1)
    l2 = sorted(l2)

    total = 0

    for x, y in zip(l1, l2):
        total += abs(x - y)

    return total


@timer
def get_second_solution(test: bool = False):
    inpt = read_input("01", test=test)

    l1 = [int(s.split("   ")[0]) for s in inpt]
    l2 = [int(s.split("   ")[1]) for s in inpt]

    val_count: dict = defaultdict(int)

    for val in l2:
        val_count[str(val)] += 1

    score = 0

    for val in l1:
        score += val * val_count[str(val)]

    return score


print(f" P1: {get_first_solution(test=args.test)}")
print(f" P2: {get_second_solution(test=args.test)}")
