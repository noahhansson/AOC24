from utils import read_input, timer, setup_args

args = setup_args()


@timer
def get_first_solution(test: bool = False):
    inpt = read_input("01", test=test)
    return inpt


@timer
def get_second_solution(test: bool = False):
    inpt = read_input("01", test=test)
    return inpt


# print(f"P1: {get_first_solution(test=args.test)}")
# print(f"P2: {get_second_solution(test=args.test)}")
