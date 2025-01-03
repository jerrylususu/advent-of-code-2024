with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

order_set = set()

total = 0

def get_middle_of_list(list):
    n = len(list)
    if n % 2 == 0:
        raise Exception("List length must be odd")
    return list[(n - 1) // 2]


def list_is_in_order(list, order_set):
    n = len(list)
    for i in range(n):
        for j in range(i + 1, n):
            if (list[j], list[i]) in order_set:
                return False
    return True

for line in lines:
    if "|" in line:
        a, b = line.split("|")
        a, b = int(a), int(b)
        order_set.add((a, b))

    if "," in line:
        list = [int(x) for x in line.split(",")]
        if list_is_in_order(list, order_set):
            total += get_middle_of_list(list)

print(total)
