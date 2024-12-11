with open("input.txt", "r", encoding="utf-8") as f:
    data = f.readlines()

values = [int(i) for i in data[0].split(" ")]

def get_next_state(value):
    if value == 0:
        return [1]
    if len(str(value)) % 2 == 0:
        s = str(value)
        left, right = s[:len(s)//2], s[len(s)//2:]
        return [int(left), int(right)]
    return [value * 2024]
    
def get_next_state_list(values):
    new_values = []
    for value in values:
        new_values.extend(get_next_state(value))
    return new_values


def get_list_after_step(value, step):
    values = [value]
    for i in range(step):
        values = get_next_state_list(values)
    return values

# key = (value, remaining_step)
# value = count

memo = {}

def solve(value, remaining_step):
    if remaining_step == 0:
        return 1
    if (value, remaining_step) in memo:
        return memo[(value, remaining_step)]
    next_values = get_next_state(value)
    count = 0
    for next_value in next_values:
        count += solve(next_value, remaining_step - 1)
    memo[(value, remaining_step)] = count
    return count

total = 0
for v in values:
    total += solve(v, 75)

print(total)