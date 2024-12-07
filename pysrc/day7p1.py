from itertools import combinations

with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()



def eval_expr(expr):
    if len(expr) == 1:
        return expr[0]
    op1, op, op2, remaining = expr[0], expr[1], expr[2], expr[3:]
    res = 0
    if op == "+":
        res = op1 + op2
    elif op == "*":
        res = op1 * op2
    new_expr = [res] + remaining
    return eval_expr(new_expr)


def make_expr(values):
    n_value = len(values)
    n_space = n_value - 1
    for mult_count in range(0, n_space + 1):
        for comb in combinations(range(n_space), mult_count):
            ops = []
            for i in range(n_space):
                if i in comb:
                    ops.append("*")
                else:
                    ops.append("+")
            expr = []
            for i in range(n_value):
                expr.append(values[i])
                if i < n_space:
                    expr.append(ops[i])
            yield expr


total = 0

for line in lines:
    target, values = line.split(":")
    values = list(map(int, values.split()))
    target = int(target)
    for expr in make_expr(values):
        if eval_expr(expr) == target:
            total += target
            break

print(total)
    
    
