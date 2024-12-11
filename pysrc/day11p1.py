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

total_step = 25

for i in range(total_step):
    values = get_next_state_list(values)
    # print(i, len(values), values)

print(len(values))

