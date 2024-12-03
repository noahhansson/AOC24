import os
import time
from typing import Callable
import argparse

def read_input(file_name: str, test: bool = False) -> list[str]:
    """Function for navigating to data folder and reading input.

    Args:
        file_name (str): File name to read. Do not include .txt suffix

    Returns:
        list[str]: Returns the input where each row is a list element
    """

    if test:
        file_name = f"{file_name}-test"

    input_file = os.path.join(os.getcwd(), "..", "input", f"{file_name}.txt")
    with open(input_file, 'r') as file:
        contents = [val.strip() for val in file.readlines()]

    return contents

def timer(func: Callable):
    """Decorator for printing time taken for a function call
    """    
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        
        if execution_time < 1e-6:
            time_taken = f"{execution_time * 1e9:.2f} ns"
        elif execution_time < 1e-3:
            time_taken = f"{execution_time * 1e6:.2f} μs"
        elif execution_time < 1:
            time_taken = f"{execution_time * 1e3:.2f} ms"
        else:
            time_taken = f"{execution_time:.4f} s"
        
        print(f"Execution time of {func.__name__}: {time_taken}")
        return result
    return wrapper

def setup_parser():
    """Setup argument parser. Used to allow for easily running on test input
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--test",
        action="store_true",
        help="If set, run on test input"
    )
    
    return parser