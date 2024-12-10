import os
import operator

here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, 'input.txt')

with open(filepath, mode='r', encoding='utf8') as f:
    data = f.read()
equations = data.splitlines()


def isValidEq(result: int, operands: list[int], operators: list):
    n = len(operands)

    def solveEq(idx: int, current: int):
        nonlocal result, operands, operators, n

        if idx == n:
            return current == result
        if current > result:
            return False
        
        return any(solveEq(idx+1, op(current, operands[idx])) for op in operators)
    
    return solveEq(0, 0)

operators_p1 = [operator.add, operator.mul]

concat = lambda a, b: int(str(a) + str(b))
operators_p2 = [operator.add, operator.mul, concat]

total = 0
for equation in equations:
    _s_result, _s_operands = equation.split(": ")
    result = int(_s_result)
    operands = list(map(int, _s_operands.split(" ")))

    if isValidEq(result, operands, operators_p2):
        total += result
    else:
        pass

print(f"{total=}")
