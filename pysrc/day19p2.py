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
next_word_to_comb_count = {}

def try_get_all_combination(w: str):

    def try_compose(target: str, parts: list[str]) -> int:
        if target == "":
            return 1
        
        if target in known_uncomposable:
            return 0

        if target in next_word_to_comb_count:
            return next_word_to_comb_count[target]

        sum_of_comb_count = 0

        for w in words_list:
            if target.startswith(w):
                remaining = target[len(w):]
                comb_count = try_compose(remaining, parts + [w])
                if comb_count > 0:
                    sum_of_comb_count += comb_count

        if sum_of_comb_count == 0:
            known_uncomposable.add(target)

        next_word_to_comb_count[target] = sum_of_comb_count
        return sum_of_comb_count
    return try_compose(w, [])


total_count = 0

for idx, target in enumerate(target_list):
    combinations = try_get_all_combination(target)
    print(idx, target, combinations)
    total_count += combinations

print(total_count)
