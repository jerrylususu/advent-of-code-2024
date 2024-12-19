with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

words_list = []
for w in lines[0].split(","):
    words_list.append(w.strip())

words_list.sort(key=lambda x: len(x), reverse=True)

target_list = []
for line in lines[1:]:
    if line.strip() == "":
        continue
    target_list.append(line.strip())

# print(words_list)
# print(target_list)


known_uncomposable = set()

def try_compose(target: str):
    if target == "":
        return True
    
    if target in known_uncomposable:
        return False

    for w in words_list:
        if target.startswith(w):
            remaining = target[len(w):]
            can_compose = try_compose(remaining)
            if can_compose:
                return True
            else:
                known_uncomposable.add(target)
                continue

    return False


can_compose_count = 0

for idx, target in enumerate(target_list):
    if try_compose(target):
        can_compose_count += 1

print(can_compose_count)
