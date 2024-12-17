with open("input.txt", "r") as f:
    lines = f.readlines()

reg_a, reg_b, reg_c = 0, 0, 0
program = []

for line in lines:
    if line.startswith("Register A"):
        reg_a = int(line.split(":")[1].strip())
    elif line.startswith("Register B"):
        reg_b = int(line.split(":")[1].strip())
    elif line.startswith("Register C"):
        reg_c = int(line.split(":")[1].strip())
    elif line.startswith("Program"):
        program = list(map(int, line.split(":")[1].strip().split(",")))


def run_program(program, reg_a, reg_b, reg_c, max_iter=100000):
    vm_state = {
        "reg_a": reg_a,
        "reg_b": reg_b,
        "reg_c": reg_c,
        "pc": 0,
    }
    output = []

    def get_combo_operand(vm_state, operand):
        if operand in [0,1,2,3]:
            return operand
        
        if operand == 4:
            return vm_state["reg_a"]
        
        if operand == 5:
            return vm_state["reg_b"]
        
        if operand == 6:
            return vm_state["reg_c"]
        
        if operand == 7:
            raise Exception("Invalid operand")

    step_used = 0
    for _ in range(max_iter):
        step_used += 1
        vm_state["reg_a"] = int(vm_state["reg_a"])
        vm_state["reg_b"] = int(vm_state["reg_b"])
        vm_state["reg_c"] = int(vm_state["reg_c"])


        # break if exceed program length
        if vm_state["pc"] >= len(program):
            break

        opcode = program[vm_state["pc"]]
        operand = program[vm_state["pc"] + 1]
        # print("pc=", vm_state["pc"], "opcode=", opcode, "operand=", operand, "vm_state_before=", vm_state)

        if opcode == 0:
            # adv, combo
            numerator = vm_state["reg_a"]
            denominator = int(2 ** get_combo_operand(vm_state, operand))
            vm_state["reg_a"] = numerator // denominator
            vm_state["pc"] += 2
            continue

        elif opcode == 1:
            # bxl, literal
            op1 = vm_state["reg_b"]
            op2 = operand
            res = op1 ^ op2
            vm_state["reg_b"] = res
            vm_state["pc"] += 2
            continue

        elif opcode == 2:
            # bst, combo
            op1 = get_combo_operand(vm_state, operand)
            res = op1 % 8
            vm_state["reg_b"] = res
            vm_state["pc"] += 2
            continue
        
        elif opcode == 3:
            # jnz
            if vm_state["reg_a"] == 0:
                # don't jump
                vm_state["pc"] += 2
            else:
                vm_state["pc"] = operand
            continue
            

        elif opcode == 4:
            # bxc
            op1 = vm_state["reg_b"]
            op2 = vm_state["reg_c"]
            res = op1 ^ op2
            vm_state["reg_b"] = res
            vm_state["pc"] += 2
            continue


        elif opcode == 5:
            # out, combo
            op1 = get_combo_operand(vm_state, operand)
            res = op1 % 8
            output.append(res)
            vm_state["pc"] += 2
            continue

        
        elif opcode == 6:
            # bdv combo
            numerator = vm_state["reg_a"]
            denominator = 2 ** get_combo_operand(vm_state, operand)
            vm_state["reg_b"] = numerator // denominator
            vm_state["pc"] += 2
            continue


        elif opcode == 7:
            # cdv combo
            numerator = vm_state["reg_a"]
            denominator = 2 ** get_combo_operand(vm_state, operand)
            vm_state["reg_c"] = numerator // denominator
            vm_state["pc"] += 2
            continue


        else:
            raise Exception("Invalid opcode")


    return output, step_used

# for i in range(117435, 117488):
#     output, step_used = run_program(program, i, 0, 0)
#     if output == program:
#         print(i, step_used)
new_reg_a = 5157141799986
new_reg_a = 35184372088832
lower_limit = 2 ** 45
upper_limit = 2 ** 48 
# new_reg_a = 35000000000000 # min?
# new_reg_a = 70368744177664 * 2 * 2 -1 
# new_reg_a = 138000000000000 # min?

# for i in range(lower_limit, upper_limit):
#     output, step_used = run_program(program, i, reg_b, reg_c)
#     print(i, step_used, output)
#     if output == program:
#         print("hit", i, step_used)
#         break


# 2,4 reg_b = reg_a % 8
# 1,1 reg_b = reg_b xor 1
# 7,5 reg_c = reg_a // 2**reg_b
# 0,3 reg_a = reg_a // 8      <-- iter count
# 1,4 reg_b = reg_b xor 4
# 4,5 reg_b = reg_b xor reg_c
# 5,5 output (reg_b % 8)      <-- output
# 3,0 jump to 0 if reg_a != 0



def find_consecutive_index_ranges(nums):
    if not nums:
        return []
    
    result = []
    start_idx = 0
    
    for i in range(1, len(nums)):
        if nums[i] != nums[i-1] + 1:
            if start_idx == i-1:
                result.append((start_idx, start_idx))
            else:
                result.append((start_idx, i-1))
            start_idx = i
    
    if start_idx == len(nums)-1:
        result.append((start_idx, start_idx))
    else:
        result.append((start_idx, len(nums)-1))
    
    return result

def check_backward_until_index(target_index, program, output):
    for i in range(len(program) - 1, target_index - 1, -1):
        if program[i] != output[i]:
            return False
    return True

precision = 12
seg_count = 2 ** precision

all_founds = []

def recursive_check(lower_limit, upper_limit, index):
    print("enter", lower_limit, upper_limit, index)
    if index == -1:
        # found:
        return True, (lower_limit, upper_limit)
    
    if upper_limit - lower_limit < 10000:
        # brute force
        print("enter", lower_limit, upper_limit, index, "brute force")
        for i in range(lower_limit, upper_limit):
            output, step_used = run_program(program, i, reg_b, reg_c)
            hitted = program == output
            if hitted:
                print("found at", i)
                all_founds.append(i)
                break
        # continue dfs
        return False, None


    range_len = upper_limit - lower_limit
    range_len_div_by_seg_count = range_len // seg_count

    hit_index_list = []

    for j in range(seg_count + 1):
        new_reg_a = lower_limit + range_len_div_by_seg_count * j
        output, step_used = run_program(program, new_reg_a, reg_b, reg_c)

        hitted = check_backward_until_index(index, program, output)
        # print(j, new_reg_a, step_used, output, hitted)
        if hitted:
            hit_index_list.append(j)
    
    if len(hit_index_list) == 0:
        print("finish", lower_limit, upper_limit, index, "no hit")
        return False, None
    
    consecutive_index_ranges = find_consecutive_index_ranges(hit_index_list)
    print("finish", lower_limit, upper_limit, index, "ranges", consecutive_index_ranges)


    for r in consecutive_index_ranges:
        found, result = recursive_check(lower_limit + range_len_div_by_seg_count * hit_index_list[r[0]], lower_limit + range_len_div_by_seg_count * hit_index_list[r[1]], index - 1)
        if found:
            return True, result

    return False, None

recursive_check(lower_limit, upper_limit, len(program) - 1)

print("all_founds", all_founds)
print("min", min(all_founds))

# for i in range(len(program)):
#     trying_to_hit_index = len(program) - i - 1

#     range_len = last_upper_limit - last_lower_limit
#     range_len_div_by_seg_count = range_len // seg_count

#     hit_index_list = []

#     for j in range(seg_count + 1):
#         new_reg_a = last_lower_limit + range_len_div_by_seg_count * j
#         output, step_used = run_program(program, new_reg_a, reg_b, reg_c)

#         hitted = check_backward_until_index(trying_to_hit_index, program, output)
#         print(i, j, new_reg_a, step_used, output, hitted)
#         if hitted:
#             hit_index_list.append(j)

#     print(i, hit_index_list)
#     next_index_ranges = get_next_index_range(hit_index_list)
#     print(i, next_index_range)

#     last_lower_limit = last_lower_limit + range_len_div_by_seg_count * next_index_range[0]
#     last_upper_limit = last_lower_limit + range_len_div_by_seg_count * next_index_range[1]

