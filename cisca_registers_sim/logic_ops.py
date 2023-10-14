from update_bits import update_status_bits

def AND(register1, operand2, registers):
    if isinstance(operand2, str) and operand2 in registers:
        and_value = registers[operand2]
    else:
        and_value = operand2
    result = registers[register1] & and_value
    registers[register1] = result
   
    update_status_bits(result,reset=True)

def CMP(register1, register2, registers, status_bits):
  
    value1 = registers[register1] & 0xFFFFFFFF
    if isinstance(register2, int):
        value2 = register2 & 0xFFFFFFFF
    else:
        value2 = registers.get(register2, 0) & 0xFFFFFFFF
    result = value1 - value2
    result_32bit = result & 0xFFFFFFFF
    status_bits['Z'] = 1 if result_32bit == 0 else 0 
    status_bits['S'] = 1 if result < 0 else 0
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

def SHL(register, bits, registers):
    registers[register] <<= bits
    registers[register] &= 0xFFFFFFFF
    update_status_bits(registers[register])


def SHR(register, bits, registers):
    registers[register] >>= bits
    update_status_bits(registers[register])
#     Changed Registers:
# R0: 0000X400h, (Decimal):1024
    
def SAR(register, bits, registers):
        sign_bit = registers[register] & 0x80000000
        registers[register] >>= bits
        if sign_bit:
            registers[register] |= (0xFFFFFFFF << (32 - bits))
        
        registers[register] &= 0xFFFFFFFF

        update_status_bits(registers[register])
    
def NOT(register, registers,memory):
    
        if register.startswith('[') and register.endswith(']'):
          
            actual_register = register[1:-1]
            mem_address = registers.get(actual_register, 0)
          
            memory[mem_address] = ~memory.get(mem_address, 0) & 0xFFFFFFFF
            update_status_bits(memory[mem_address],reset=True)
        else:
           
            registers[register] = ~registers[register] & 0xFFFFFFFF  
            update_status_bits(registers[register])
    
def MOV(register1, value,registers,memory):
        
        if isinstance(value, str):
            if value.startswith('[') and value.endswith(']'):
                # It's a memory address
                mem_address = value[1:-1]
                registers[register1] = memory.get(mem_address, 0)
            else:
                # It's a register
                registers[register1] = registers[value]
        else:
            registers[register1] = value
        
        update_status_bits(registers[register1])