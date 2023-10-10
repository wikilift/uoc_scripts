
from cisca_instruction_set import ADDRESSING_MODES,OPCODES
from operator_chooser import ARITHMETIC_OPERATIONS,execute_arithmetic_operation


def MOV(register1, value, registers):
    if isinstance(value, str):
        registers[register1] = registers[value]
    else:
        registers[register1] = value
   

def to_little_endian(hex_str, num_positions):
    padded_hex_str = hex_str.zfill(num_positions)
    segments = [padded_hex_str[i:i+2] for i in range(0, len(padded_hex_str), 2)]
    segments_reversed = reversed(segments)
    little_endian_str = ' '.join(segments_reversed)
    return little_endian_str


def calculate_offsets(instructions, initial_offset=0x00000100):
    offset = initial_offset
    offset_mapping = []
    
    for instruction, *operands in instructions:
        formatted_offset = f"{offset:08X}"
        label = None

        if 'LABEL' in operands[-1]:
            label = operands.pop().split(":")[1]

        if instruction == 'JMP':  
            offset += 1 + 1 + 4  
        elif instruction in ['JE', 'JNE', 'JGE', 'JG', 'JLE', 'JL']:  
            offset += 1 + 1 + 2  
        else:  
            operand_bytes = 0
            for op in operands:
                if isinstance(op, int):
                    operand_bytes += 5  
                elif str(op).startswith('[') and str(op).endswith(']'):
                    operand_bytes += 5  
                else:
                    operand_bytes += 1  
            offset += 1 + operand_bytes

        offset_mapping.append((formatted_offset, (f"{instruction} {operands}", label)))

    return offset_mapping

def translate_to_hex_with_labels(instructions, memory_values=None, initial_offset=0x00000100):
    offset_mapping = calculate_offsets(instructions, initial_offset)
    hex_translation = {}
    label_to_offset = {label: offset for offset, (instruction_str, label) in offset_mapping if label is not None}
    i=0
    for offset, (instruction_str, _) in offset_mapping:
        next_offset=None
        try:
            next_offset=offset_mapping[i + 1]
        except:
            pass
        if " " in instruction_str:
            instruction, operands_str = instruction_str.split(' ', 1)
        else:
            instruction, operands_str = instruction_str, ""
            
        opcode = OPCODES.get(instruction, "")
        
        if not opcode:
            print(f"The instruction {instruction} does not exist, the program cannot continue")
            exit()
            
        
        operands = eval(operands_str) 
        hex_operands = []
        

        for operand in operands:
            if isinstance(operand, str) and operand.startswith('R'):
                hex_operands.append(f" {ADDRESSING_MODES['Register']}{operand[1]} ")
            
            elif isinstance(operand, str) and operand.startswith('[') and operand.endswith(']'):
                if memory_values is None:
                    print(f"you don't defined the value for {operand}, the program cannot continue")
                    exit()
                if '+' in operand:
                    base, register = operand[1:-1].split('+')
                    num=int(base)
                    hex_str=hex(num)[2:]
                    hex_base = to_little_endian(hex_str=hex_str, num_positions=8)
                    hex_operands.append(f" {ADDRESSING_MODES['Indexed']}{register[1]} {hex_base}")
                else:
                    hex_operands.append(f" {ADDRESSING_MODES['Memory']}0 ")
                    addr = operand[1:-1]
                    hex_value =to_little_endian(hex_str= memory_values.get(addr, "00"),num_positions=8)
                    hex_operands.append(f"{hex_value}")
            elif isinstance(operand, int):
                hex_value = f"{operand:08X}"
                hex_operands.append(f" {ADDRESSING_MODES['Immediate']}4 {to_little_endian(hex_str=hex_value,num_positions=8)} ")
            elif isinstance(operand, str) and operand in label_to_offset:
                target_offset = label_to_offset[operand]               
                if opcode == '40': 
                    hex_operands.append(f" {ADDRESSING_MODES['Immediate']}0 {to_little_endian(hex_str=target_offset,num_positions=8)}")
                else: 
                    relative_offset = int(target_offset, 16) - int(next_offset[0], 16)
                    relative_offset_hex = format(relative_offset, 'x').upper()
                    hex_operands.append(f" {ADDRESSING_MODES['Relative_to_PC']}0 {to_little_endian(hex_str= relative_offset_hex,num_positions=4)}")
        if instruction in ARITHMETIC_OPERATIONS:
            
                operands = eval(operands_str)
                if instruction!='MOV': 
                    if len(operands) == 2:
                        execute_arithmetic_operation(instruction=instruction,operands=operands,memory=memory_values,registers=registers)              
                else:
                   
                    if len(operands) == 2:
                        dst, src = operands
                        if isinstance(dst, str) and dst.startswith('R'):
                            if isinstance(src, str) and src.startswith('R'):
                                registers[dst] = registers[src]
                            elif isinstance(src, int):
                                registers[dst] = src
                            elif isinstance(src, str) and src.startswith('[') and src.endswith(']'):
                                addr = src[1:-1]
                                registers[dst] = int(memory_values.get(addr, "0"), 16) 
                        elif isinstance(dst, str) and dst.startswith('[') and dst.endswith(']'):
                            addr = dst[1:-1]
                            if isinstance(src, str) and src.startswith('R'):
                                memory_values[addr] = hex(registers[src])[2:].zfill(8).upper()
                            elif isinstance(src, int):
                                memory_values[addr] = hex(src)[2:].zfill(8).upper()
     
        hex_instruction = f" {opcode}{''.join(hex_operands)}"
        data=f" {instruction} {','.join(map(str, operands))}\t "
        hex_translation[offset] = f"{data}{hex_instruction}"
        i+=1
    return hex_translation

registers = {
    'R1': 0x00000000,
    'R2': 0x00000000,
    'R3': 0x00000000,   
}


