from cisca_registers_sim.update_bits import update_status_bits

def AND(register1, operand2, registers, status_bits):
    if isinstance(operand2, str) and operand2 in registers:
        and_value = registers[operand2]
    else:
        and_value = operand2
    result = registers[register1] & and_value
    registers[register1] = result
    update_status_bits(result, status_bits)

def CMP(register1, register2, registers, status_bits):
    value1 = registers[register1]
    value2 = registers[register2]
    result = value1 - value2
    update_status_bits(result, status_bits)
    status_bits['C'] = 1 if result < 0 else 0
    status_bits['V'] = 0

def JE(label, index, status_bits, label_positions):
    if status_bits['Z'] == 1:
        return label_positions[label]
    return index


def JNE(label, index, status_bits, label_positions):
    if status_bits['Z'] == 0:
        return label_positions[label]
    return index


def JGE(label, index, status_bits, label_positions):
    if status_bits['S'] == 0:
        return label_positions[label]
    return index


def JG(label, index, status_bits, label_positions):
    if status_bits['S'] == 0 and status_bits['Z'] == 0:
        return label_positions[label]
    return index


def JLE(label, index, status_bits, label_positions):
    if status_bits['S'] == 1 or status_bits['Z'] == 1:
        return label_positions[label]
    return index


def JL(label, index, status_bits, label_positions):
    if status_bits['S'] == 1:
        return label_positions[label]
    return index

def SHL(register, bits, registers, status_bits):
    registers[register] <<= bits
    registers[register] &= 0xFFFFFFFF
    update_status_bits(registers[register], status_bits)


def SHR(register, bits, registers, status_bits):
    registers[register] >>= bits
    update_status_bits(registers[register], status_bits)
