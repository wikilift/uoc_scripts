from status_bits import update_status_bits
def ADD(register1, operand,memory,registers,status_bits):
    
    if isinstance(operand, str):
        if operand.startswith('[') and operand.endswith(']'):
                # It's a memory address
            mem_address = operand[1:-1]
            add_value = memory.get(mem_address, 0)
        else:
                # It's a register
            add_value = registers[operand]
    else:
        add_value = operand 
        
        # Handle negative numbers with Two's Complement
        if add_value < 0:
            add_value = 0xFFFFFFFF + add_value + 1
        
        result_unsigned = registers[register1] + add_value
        result = result_unsigned & 0xFFFFFFFF  # 32-bit result
        registers[register1] = result
        
        update_status_bits(result,status_bits=status_bits)
        status_bits['C'] = 1 if result_unsigned > 0xFFFFFFFF else 0
        
        status_bits['V'] = 0