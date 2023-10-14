from update_bits import *

def ADD(register1, operand, registers, memory, status_bits):
    if isinstance(operand, str):
        if operand.startswith('[') and operand.endswith(']'):
            mem_register = operand[1:-1] 
            if mem_register in registers:
                add_value = registers[mem_register]
            else:
                mem_address = registers.get(mem_register, 0)
                hex_mem_address = format(mem_address, '08X')
                add_value = memory.get(hex_mem_address, 0)
        else:
            add_value = registers[operand]
    else:
        add_value = operand

    result_unsigned = registers[register1] + add_value
    result = result_unsigned & 0xFFFFFFFF  
    registers[register1] = result
    status_bits['S'] = 1 if result & 0x80000000 else 0
    status_bits['C'] = 1 if result_unsigned > 0xFFFFFFFF else 0
    status_bits['V'] = 0
    status_bits['Z'] = 1 if result == 0 else 0


    
def DEC(register, registers):
    registers[register] -= 1
    update_status_bits(registers[register],reset=True)
    
def INC(register, registers):
    registers[register] += 1
    update_status_bits(registers[register],reset=True)

def MUL(register1, register2, registers):
    result = registers[register1] * registers[register2]
    registers[register1] = result & 0xFFFFFFFF  # 32-bit result
    update_status_bits(result)
    
def SUB(operand1, operand2, registers, memory):
    if operand2.startswith('[') and operand2.endswith(']'):
        mem_address2 = operand2[1:-1]
        value2 = registers.get(mem_address2, memory.get(mem_address2, 0)) 
    elif operand2 in registers:
        value2 = registers[operand2]
    else:
        value2 = int(operand2, 16) if operand2.startswith("0x") else int(operand2)

    if operand1 in registers:
        value1 = registers[operand1]
        result = value1 - value2
        result_32bit = result & 0xFFFFFFFF  
        registers[operand1] = result_32bit
        # status_bits['S'] = 1 if (result_32bit >> 31) & 1 else 0
        status_bits['S'] = 1 if result < 0 else 0
        status_bits['C'] = 1 if result < 0 else 0
        status_bits['V'] = 0  # impossible overflow on sub
        status_bits['Z'] =1 if result == 0 else 0
       
    else:
        raise ValueError("Invalid operand1")


    
