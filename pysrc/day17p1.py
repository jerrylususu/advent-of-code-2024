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


for i in range(1000):
    # break if exceed program length
    # print(vm_state)
    if vm_state["pc"] >= len(program):
        break

    opcode = program[vm_state["pc"]]
    operand = program[vm_state["pc"] + 1]
    # print("pc=", vm_state["pc"], "opcode=", opcode, "operand=", operand)

    if opcode == 0:
        # adv, combo
        numerator = vm_state["reg_a"]
        denominator = 2 ** get_combo_operand(vm_state, operand)
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


print(output)
print(",".join(map(str, output)))