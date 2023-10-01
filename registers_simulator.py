
def execute_program(registers, memory, program):
    label_positions={}
    initial_registers = registers.copy()
    for idx, (instruction, *operands) in enumerate(program):
        if instruction == 'LABEL':
            label_positions[operands[0]] = idx
    
    status_bits = {
        'Z': 0,
        'S': 0,
        'C': 0,
        'V': 0
    }
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
    print("Initial Memory State")
    print("-" * 80) 
    for k, v in memory.items():
        print(f"Memory Address: {k}, Value (Decimal): {v}, Value (Hexadecimal): {hex(v)}")
    print("-" * 80)    
    for instruction, *operands in program:
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
             # Update status bits after MOV
            update_status_bits(registers[operands[0]]) 
        elif instruction == 'DEC':
            DEC(*operands)
             # Update status bits after DEC
            update_status_bits(registers[operands[0]]) 
        elif instruction == 'JE':
            index = JE(*operands, index)
        elif instruction == 'MUL':
            MUL(*operands)
             # Update status bits after MUL
            update_status_bits(registers[operands[0]]) 
        elif instruction == 'JMP':
            index = label_positions[operands[0]]   
        
        print("Current Status Bits:")
        for k, v in status_bits.items():
            print(f"{k}: {v}")
        print("-" * 80)
        print("Memory State")
        for k, v in memory.items():
            print(f"Memory Address: {k}, Value (Decimal): {v}, Value (Hexadecimal): {hex(v)}")
        print("-" * 80)
        
        changed_registers = {k: v for k, v in registers.items() if v != initial_registers.get(k, None)} 
        if changed_registers:
            print("Changed Registers:")
            for k, v in changed_registers.items():
                print(f"{k}: {hex(v)}")
        else:
            print("No registers modified")
            
        print("-" * 80)  

registers = {
    'R2': 0x00000004,
    'R5': 0x0000000A,
    'R6': 0x0000000C,
    'R7': 0x0000000C,
   
    
}

memory = {       
    'A13F00FC': 0xA13F0104,
    '00000256': 0x0000025E
}
program = [
   #('ADD', 'R5', 'R6'),
      ('ADD', 'R5', 'R2')
    # ('AND', 'R6',0xFFFFFFF8),
   # ('SUB', '[A13F00FC]','R6'),
    # ('JE', 'End_loop'),
    # ('MUL', 'R1', 'R2'),
    # ('JMP', 'Loop'),
    # ('LABEL', 'End_loop'),
    # ('MOV', '100', 'R1')
]
execute_program(registers=registers, memory=memory, program=program)