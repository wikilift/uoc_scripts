from update_bits import *

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
    
def DEC(register, registers):
    registers[register] -= 1
    update_status_bits(registers[register])

def MUL(register1, register2, registers):
    result = registers[register1] * registers[register2]
    registers[register1] = result & 0xFFFFFFFF  # 32-bit result
    update_status_bits(result)
    
def SUB(operand1, operand2, registers, memory):
    if operand2.startswith('[') and operand2.endswith(']'):
        mem_address2 = operand2[1:-1]
        if mem_address2 in registers:
            mem_address2 = hex(registers[mem_address2])[2:].upper()
        value2 = memory.get(mem_address2, 0)
      
    elif operand2 in registers:
        value2 = registers[operand2]
    else:
        value2 = int(operand2, 16) if operand2.startswith("0x") else int(operand2)

    if operand1 in registers:
        value1 = registers[operand1]
        result = value1 - value2
        result_32bit = result & 0xFFFFFFFF  # 32-bit result AND
        registers[operand1] = result_32bit
        status_bits['C'] = 1 if result < 0 else 0
        status_bits['V'] = 0  # impossible overflow on sub
        update_status_bits(result_32bit)
    else:
        raise ValueError("Invalid operand1")

    
