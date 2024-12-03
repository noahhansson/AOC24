from utils import read_input, timer, setup_parser

parser = setup_parser()
args = parser.parse_args()
test_run = args.test


def parse_errors(row: list[int], p2: bool = False) -> bool:

    prev_increment = 0

    for i, (x, x_lag) in enumerate(zip(row[1:], row)):
        increment = x - x_lag
        if (
            ((abs(increment) > 3) or (abs(increment) < 1))
            or ((prev_increment < 0) and (increment > 0))
            or ((prev_increment > 0) and (increment < 0))
        ):
            if p2:
                # When error is encountered the faulty level is either in place,
                # ahead, or behind. Try again for all cases
                row_fix_a = row[: i - 1] + row[i:]
                row_fix_b = row[:i] + row[i + 1 :]
                row_fix_c = row[: i + 1] + row[i + 2 :]
                return (
                    parse_errors(row_fix_a, p2=False)
                    or parse_errors(row_fix_b, p2=False)
                    or parse_errors(row_fix_c, p2=False)
                )
            else:
                return False

        prev_increment = increment

    return True


@timer
def get_first_solution(test: bool = test_run):
    inpt = read_input("02", test=test)
    n_safe = 0

    for row in inpt:
        row_fix = [int(x) for x in row.split(" ")]
        if parse_errors(row_fix):
            n_safe += 1

    return n_safe


@timer
def get_second_solution(test: bool = test_run):
    inpt = read_input("02", test=test)
    n_safe = 0

    for row in inpt:
        row_fix = [int(x) for x in row.split(" ")]
        if parse_errors(row_fix, p2=True):
            n_safe += 1

    return n_safe


print(f" P1: {get_first_solution(test=args.test)}")
print(f" P2: {get_second_solution(test=args.test)}")
