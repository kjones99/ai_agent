from functions.write_file import write_file
from functions.run_python_file import run_python_file

def test():
    result = run_python_file("calculator", "main.py")
    print(f'Result for main.py file:')
    print(result, '\n')

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(f'Result for main.py [3 + 5] file:')
    print(result, '\n')

    result = run_python_file("calculator", "tests.py")
    print(f'Result for tests.py file:')
    print(result, '\n')

    result = run_python_file("calculator", "../main.py")
    print(f'Result for ../main.py file:')
    print(result, '\n')

    result = run_python_file("calculator", "nonexistent.py")
    print(f'Result for nonexistent.py file:')
    print(result, '\n')

    result = run_python_file("calculator", "lorem.txt")
    print(f'Result for lorem.txt file:')
    print(result, '\n')

if __name__ == "__main__":
    test()
