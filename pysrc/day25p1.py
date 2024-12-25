with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

in_pattern = True
all_patterns = []
last_pattern = []

for line in lines:
    if line.strip() == "":
        in_pattern = False
        all_patterns.append(last_pattern)
        last_pattern = []
        continue
    
    in_pattern = True
    line = [i for i in line.strip()]
    last_pattern.append(line)

all_patterns.append(last_pattern)

locks = []
keys = []

def count_hash_in_col(pattern):
    n_row = len(pattern)
    n_col = len(pattern[0])
    li = []
    for i in range(n_col):
        cnt = 0
        for j in range(n_row):
            if pattern[j][i] == "#":
                cnt += 1
        # base
        cnt -= 1
        li.append(cnt)
    return li

for pattern in all_patterns:
    if all([i == "." for i in pattern[0]]):
        keys.append(count_hash_in_col(pattern))
    else:
        locks.append(count_hash_in_col(pattern))

# print(locks)
# print(keys)
def can_fit(lock, key):
    for l, k in zip(lock, key):
        if l + k >= 6:
            return False
    return True

all_can_fit_count = 0

for lock in locks:
    for key in keys:
        if can_fit(lock, key):
            all_can_fit_count += 1

print(all_can_fit_count)    





    
