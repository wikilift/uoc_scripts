from cisca_registers_sim.update_bits import *

def ADD(register1, operand, registers, memory, status_bits):
    if isinstance(operand, str):
        if operand.startswith('[') and operand.endswith(']'):
            mem_address = operand[1:-1]
            add_value = memory.get(mem_address, 0)
        else:
            add_value = registers[operand]
    else:
        add_value = operand

    result_unsigned = registers[register1] + add_value
    result = result_unsigned & 0xFFFFFFFF  # 32-bit result
    registers[register1] = result

    update_status_bits(result, status_bits)
    status_bits['C'] = 1 if result_unsigned > 0xFFFFFFFF else 0
    status_bits['V'] = 0
    
def DEC(register, registers, status_bits):
    registers[register] -= 1
    update_status_bits(registers[register], status_bits)

def MUL(register1, register2, registers, status_bits):
    result = registers[register1] * registers[register2]
    registers[register1] = result & 0xFFFFFFFF  # 32-bit result
    update_status_bits(result, status_bits)
    
def SUB(operand1, operand2, registers, memory, status_bits):
    if operand1.startswith('[') and operand1.endswith(']'):
        mem_address1 = operand1[1:-1]
        value1 = memory.get(mem_address1, 0)
        value2 = registers[operand2]
        result = value1 - value2
        result_32bit = result & 0xFFFFFFFF  # 32-bit result
        memory[mem_address1] = result_32bit
    else:
        value1 = registers[operand1]
        if operand2 in registers:
            value2 = registers[operand2]
        else:
            value2 = operand2
        result = value1 - value2
        result_32bit = result & 0xFFFFFFFF  # 32-bit result
        registers[operand1] = result_32bit
    update_status_bits(result_32bit, status_bits)
    status_bits['C'] = 1 if result < 0 else 0
    status_bits['V'] = 0
    
