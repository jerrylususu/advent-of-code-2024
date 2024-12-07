from itertools import product

with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()



def eval_expr(expr, early_break=None):
    if len(expr) == 1:
        return expr[0]
    op1, op, op2, remaining = expr[0], expr[1], expr[2], expr[3:]
    if early_break is not None and op1 > early_break:
        return None
    res = 0
    if op == "+":
        res = op1 + op2
    elif op == "*":
        res = op1 * op2
    elif op == "|":
        res = int(str(op1) + str(op2))
    new_expr = [res] + remaining
    return eval_expr(new_expr)


def make_expr(values):
    n_value = len(values)
    n_space = n_value - 1

    for comb in product(["+", "*", "|"], repeat=n_space):
        expr = []
        for i in range(n_value):
            expr.append(values[i])
            if i < n_space:
                expr.append(comb[i])
        yield expr

total = 0

for i, line in enumerate(lines):
    target, values = line.split(":")
    values = list(map(int, values.split()))
    target = int(target)
    print(i)
    for expr in make_expr(values):
        if eval_expr(expr, target) == target:
            total += target
            break

print(total)
    
    
