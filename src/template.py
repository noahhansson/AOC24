from utils import read_input, timer_decorator, setup_parser

parser = setup_parser()
args = parser.parse_args()

@timer_decorator
def get_first_solution(test: bool = args.test):
    inpt = read_input("01", test=test)
    return inpt

@timer_decorator
def get_second_solution(test: bool = args.test):
    inpt = read_input("01", test=test)
    return inpt

print(f" P1: {get_first_solution()}")
print(f" P2: {get_second_solution()}")