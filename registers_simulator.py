
def execute_program(registers, memory, program):
    label_positions={}
    index=0
    initial_registers = registers.copy()
    initial_memory = memory.copy()
    for idx, (instruction, *operands) in enumerate(program):
        if instruction == 'LABEL':
            label_positions[operands[0]] = idx
    
    status_bits = {
        'Z': 0,
        'S': 0,
        'C': 0,
        'V': 0
    }
    
    def SHL(register, bits):
        registers[register] <<= bits
        registers[register] &= 0xFFFFFFFF  
        update_status_bits(registers[register])
          
    def SHR(register, bits):
        registers[register] >>= bits
        update_status_bits(registers[register])
        
    def update_status_bits(result):
    
        status_bits['Z'] = 1 if result == 0 else 0  # Zero flag
        status_bits['S'] = 1 if (result >> 31) & 1 else 0  # Sign flag
        # Carry and Overflow are updated during operations

    def ADD(register1, operand):
    
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
        
        update_status_bits(result)
        status_bits['C'] = 1 if result_unsigned > 0xFFFFFFFF else 0
        
        status_bits['V'] = 0

    def CMP(register1, register2):
    
        value1 = registers[register1]
        value2 = registers[register2]
        
        # Perform the subtraction
        result = value1 - value2
        
        # Update status bits
        update_status_bits(result)
        status_bits['C'] = 1 if result < 0 else 0  # Carry flag
        status_bits['V'] = 0 

    def MOV(register1, value):
        
        if isinstance(value, str):
            registers[register1] = registers[value]
        else:
            registers[register1] = value
        update_status_bits(registers[register1])

    def DEC(register):
        
        registers[register] -= 1
        update_status_bits(registers[register])

    def JE(label, index):
    
        if status_bits['Z'] == 1:
            return label_positions[label]
        return index

    def JNE(label, index):
         # Jump if not equal (Z = 0)
        if status_bits['Z'] == 0: 
            return label_positions[label]
        return index

    def JGE(label, index):
         # Jump if greater or equal (S = 0)
        if status_bits['S'] == 0: 
            return label_positions[label]
        return index

    def JG(label, index):
         # Jump if greater (S = 0 and Z = 0)
        if status_bits['S'] == 0 and status_bits['Z'] == 0: 
            return label_positions[label]
        return index

    def JLE(label, index):
        # Jump if less or equal (S = 1 or Z = 1)
        if status_bits['S'] == 1 or status_bits['Z'] == 1:  
            return label_positions[label]
        return index

    def JL(label, index):
        # Jump if less (S = 1)
        if status_bits['S'] == 1:  
            return label_positions[label]
        return index

    def MUL(register1, register2):
        
        result = registers[register1] * registers[register2]
        registers[register1] = result & 0xFFFFFFFF  # 32-bit result
        update_status_bits(result)
        
    def SUB(operand1, operand2):
        if operand1.startswith('[') and operand1.endswith(']'):
           
            mem_address1 = operand1[1:-1]
            value1 = memory.get(mem_address1, 0)
            # operand2 should be a register
            value2 = registers[operand2]
            
            result = value1 - value2
            result_32bit = result & 0xFFFFFFFF  # 32-bit result
            # Updating the memory with the new value
            memory[mem_address1] = result_32bit 
        else:
            # Assuming operand1 is a register and operand2 can be either a register or a numerical constant
            value1 = registers[operand1]
            if operand2 in registers:
                value2 = registers[operand2]
            else:
                value2 = operand2  
                
            result = value1 - value2
            result_32bit = result & 0xFFFFFFFF  # 32-bit result AND
            # Updating the register with the new value
            registers[operand1] = result_32bit
            
        update_status_bits(result_32bit)
        status_bits['C'] = 1 if result < 0 else 0
        status_bits['V'] = 0  # imposible overflow on sub

    def AND(register1, operand2):
        # Check if operand2 is a register name or a numerical constant
        if isinstance(operand2, str) and operand2 in registers:
            and_value = registers[operand2]
        else:
             # It's a numerical constant
            and_value = operand2 
        
       
        result = registers[register1] & and_value
        registers[register1] = result
        
        
        update_status_bits(result)
    
    
    
    while index < len(program):  # Changed to a while loop
        instruction, *operands = program[index]
        print(f"Executing: {instruction} {operands}")
        print("-" * 80)
        
        if instruction == 'ADD':
            ADD(*operands)
        elif instruction == 'SUB':
            SUB(*operands)
        elif instruction == 'AND':
            AND(*operands)
        elif instruction == 'CMP':
            CMP(*operands)
        elif instruction == 'MOV':
            MOV(*operands)
            if operands[0].startswith('[') and operands[0].endswith(']'):
                mem_address = operands[0][1:-1]
                update_status_bits(memory.get(mem_address, 0))
            else:
                update_status_bits(registers[operands[0]]) 
        elif instruction == 'SHL':
            SHL(*operands)
        elif instruction == 'SHR':
            SHR(*operands)
        elif instruction == 'DEC':
            DEC(*operands)
            update_status_bits(registers[operands[0]]) 
        elif instruction == 'JE':
            index = JE(*operands, index)          
        elif instruction == 'MUL':
            MUL(*operands)
            update_status_bits(registers[operands[0]]) 
        elif instruction == 'JMP':
            index = label_positions[operands[0]]   
        elif instruction == 'JNE':
            index = JNE(*operands, index)
        elif instruction == 'JGE':
            index = JGE(*operands, index)
        elif instruction == 'JG':
            index = JG(*operands, index)
        elif instruction == 'JLE':
            index = JLE(*operands, index)
        elif instruction == 'JL':
            index = JL(*operands, index)
            
        index+=1
        print("Current Status Bits:")
        for k, v in status_bits.items():
            print(f"{k}: {v}")
        print("-" * 80)
        changed_memory = {k: v for k, v in memory.items() if v != initial_memory.get(k, None)}

        if changed_memory:
            print("Changed Memory State")
            print("-" * 80)
            for k, v in changed_memory.items():
                print(f"Memory Address: {k}, Initial Value (Decimal): {initial_memory.get(k, None)}, Current Value (Decimal): {v}, Current Value (Hexadecimal): {hex(v)}")
            print("-" * 80)
        else:
            print("No memory positions changed")
            print("-" * 80)
        changed_registers = {k: v for k, v in registers.items() if v != initial_registers.get(k, None)} 
        if changed_registers:
            print("Changed Registers:")
            for k, v in changed_registers.items():
                print(f"{k}: {hex(v)}Hex, (Decimal):{v}")
        else:
            print("No registers modified")
            
        print("-" * 80)  

registers = {
    'R2': 0x00000004,
    'R5': 0x0000000A,
    'R6': 0x0000000C,
    'R7': 0x0000000E,
   
    
}

memory = {       
    'A13F00FC': 0xA13F0104,
    '00000256': 0x00000025
}
program = [
    #('ADD', 'R5', 'R6'),
    ('MOV', 'R1', 'R2'),
    ('LABEL', 'Loop'),
    ('DEC', 'R2'),
    ('JE', 'End_loop'),
    ('MUL', 'R1', 'R2'),
    ('JMP', 'Loop'),
    ('LABEL', 'End_loop'),
    ('MOV', '[100]', 'R1')
]
execute_program(registers=registers, memory=memory, program=program)