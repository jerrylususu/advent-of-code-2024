with open("input.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

last_direction = None

count = 0

def check_arr(arr):
    arr = line.split()
    arr = [int(i) for i in arr]
    ok = True
    last_direction = None
    for i in range(len(arr) - 1):
        a1, a2 = arr[i], arr[i+1]
        diff = a1 - a2
        diff_abs = abs(diff)
        if diff_abs < 1 or diff_abs > 3:
            ok = False
            break
        sign = diff / diff_abs
        if last_direction == None:
            last_direction = sign
        if sign != last_direction:
            ok = False
            break

    return ok

for line in lines:
    if check_arr(line):
        count += 1

print(count)
