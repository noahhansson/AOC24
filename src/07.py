from utils import read_input, timer, setup_args

args = setup_args()


def parse_input(test: bool) -> tuple[list[int], list[list[int]]]:
    inpt = read_input("07", test=test)

    targets: list[int] = []
    terms: list[list[int]] = []

    for row in inpt:
        target = int(row.split(":")[0])
        term_lst = [int(x) for x in row.split(":")[1].strip(" ").split(" ")]

        targets.append(target)
        terms.append(term_lst)

    return targets, terms


def try_solve(target: int, current_val: int, terms: list[int], p2: bool = False) -> bool:
    if (current_val == target) and (len(terms) == 0):
        return True
    elif (current_val > target) or (len(terms) == 0):
        return False
    else:
        if current_val == 0:
            return try_solve(target, current_val + terms[0], terms[1:], p2)
        else:
            return (
                try_solve(target, current_val + terms[0], terms[1:], p2)
                or try_solve(target, current_val * terms[0], terms[1:], p2)
                or (p2 and try_solve(target, int(f"{current_val}{terms[0]}"), terms[1:], p2))
            )


@timer
def get_first_solution(test: bool = False):
    targets, terms = parse_input(test)

    score = 0
    for target, term_lst in zip(targets, terms):
        if try_solve(target, 0, term_lst):
            score += target

    return score


@timer
def get_second_solution(test: bool = False):
    targets, terms = parse_input(test)

    score = 0
    for target, term_lst in zip(targets, terms):
        if try_solve(target, 0, term_lst, p2=True):
            score += target

    return score


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
