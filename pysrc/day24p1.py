with open("input.txt", "r", encoding="u8") as f:
    lines = f.readlines()

state_map = {}
target_to_source_map = {}
node_set = set()

for line in lines:
    if ":" in line:
        node, value = line.strip().split(":")
        value = int(value.strip())
        state_map[node] = value
        node_set.add(node)

    if "->" in line:
        operation, target = line.strip().split("->")
        target = target.strip()
        source1, op, source2 = operation.strip().split(" ")
        target_to_source_map[target] = (source1, op, source2)
        node_set.add(target)
        node_set.add(source1)
        node_set.add(source2)


# print(state_map)
# print(target_to_source_map)


def do_and(input1, input2):
    return input1 & input2

def do_or(input1, input2):
    return input1 | input2

def do_xor(input1, input2):
    return input1 ^ input2


def find_calculable_targets(target_to_source_map):
    calculable = []
    for target, (source1, op, source2) in target_to_source_map.items():
        if source1 in state_map and source2 in state_map:
            calculable.append(target)
    return calculable

def do_operation(op, source1, source2):
    if op == "AND":
        return do_and(source1, source2)
    elif op == "OR":
        return do_or(source1, source2)
    elif op == "XOR":
        return do_xor(source1, source2)
    else:
        raise ValueError(f"Unknown operation: {op}")

while len(state_map) != len(node_set):
    can_be_calculated_targets = find_calculable_targets(target_to_source_map)
    for target in can_be_calculated_targets:
        source1, op, source2 = target_to_source_map[target]
        result_state = do_operation(op, state_map[source1], state_map[source2])
        state_map[target] = result_state

count_of_z = len([i for i in state_map if i.startswith("z")])

final_result = 0

for i in range(count_of_z):
    final_result += state_map[f"z{i:02d}"] * (2 ** i)

print(final_result)