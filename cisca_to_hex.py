# Importing required modules and libraries
import pandas as pd
from collections import defaultdict

# Defining constants for OPCODES and ADDRESSING_MODES
OPCODES = {
    'MOV': '10',
    'DEC': '25',
    'JE': '41',
    'MUL': '22',
    'JMP': '40',
    'CMP': '26',
    'JLE': '44',
    'ADD': '20'
}

ADDRESSING_MODES = {
    'Immediate': '0',
    'Register': '1',
    'Memory': '2',
    'Indirect': '3',
    'Relative': '4',
    'Indexed': '5',
    'Relative_to_PC': '6'
}

# Function to convert to little endian format
def convert_to_little_endian(value):
    try:
        int_value = int(value)
        hex_value = hex(int_value)[2:]
    except ValueError:
        hex_value = value

    hex_value = hex_value.zfill(8)
    little_endian = ''.join(reversed([hex_value[i:i + 2] for i in range(0, len(hex_value), 2)]))
    return little_endian

# Function to calculate the BK (bytecode) of the instruction
def calculate_bk_complete(instruction, operands, labels, next_address):
    opcode = OPCODES.get(instruction, '??')
    bk_values = [opcode]
    offset_jump = None

    for operand in operands:
        if operand.startswith('R'):
            bk_values.append(ADDRESSING_MODES['Register'] + operand[1])
        elif operand.startswith('[') and operand.endswith(']'):
            bk_values.append(ADDRESSING_MODES['Memory'] + "0")
            bk_values.append(operand[1:-1])
        elif operand in labels:
            if instruction in ['JE', 'JLE']:
                bk_values.append(ADDRESSING_MODES['Relative_to_PC'] + '0')
                offset_jump = labels[operand] - next_address
                offset_jump = convert_to_little_endian(str(offset_jump))
            elif instruction == 'JMP':
                bk_values.append(ADDRESSING_MODES['Immediate'] + '0')
                offset_jump = labels[operand]
                offset_jump = convert_to_little_endian(str(offset_jump))
        else:
            bk_values.append(ADDRESSING_MODES['Immediate'] + '0')
            little_endian = convert_to_little_endian(operand)
            bk_values.append(little_endian)

    if offset_jump:
        bk_values.append(offset_jump)

    return ' '.join(bk_values)


# Main function to assemble the program
def assemble_program(program, start_address=0x00010000, memory_values=None):
    assembled_program = []
    current_address = start_address
    labels = {}
    temp_program = []

    # Initialize memory values
    memory_dict = defaultdict(str)
    if memory_values:
        for address, value in memory_values.items():
            memory_dict[address] = convert_to_little_endian(value)

    for line in program:
        label = line.get('label')
        instruction = line.get('instruction')
        operands = line.get('operands', [])
        
        if label:
            labels[label] = current_address

        if instruction:
            temp_program.append({
                'label': label,
                'instruction': instruction,
                'operands': operands,
                'current_address': current_address
            })

            # Calculate instruction length
            instruction_length = 1 + len(operands)
            for operand in operands:
                if operand.isnumeric() or ('h' in operand and operand.replace('h', '').isnumeric()):
                    instruction_length += 4
            current_address += instruction_length

    for line in temp_program:
        label = line.get('label')
        instruction = line.get('instruction')
        operands = line.get('operands', [])
        current_address = line.get('current_address')

        if not instruction:
            continue

        next_instruction_address = current_address + 1 + len(operands)
        
        operands = [
            operand if operand not in memory_dict else '[' + operand + ']'
            for operand in operands
        ]

        bk_complete = calculate_bk_complete(instruction, operands, labels, next_instruction_address)
        assembled_program.append({
            'offset': format_address(current_address),
            'label': label,
            'instruction': f"{instruction} {' '.join(operands)}",
            'BK': bk_complete
        })

    return pd.DataFrame(assembled_program)

# Function to format the address
def format_address(address):
    return f"{address:08X}"


program_ex2=new_program = [
    {'label': None, 'instruction': 'MOV', 'operands': ['R0', '[A]']},
    {'label': None, 'instruction': 'CMP', 'operands': ['R0', '[B]']},
    {'label': None, 'instruction': 'JLE', 'operands': ['E1']},
    {'label': None, 'instruction': 'DEC', 'operands': ['R0']},
    {'label': None, 'instruction': 'JMP', 'operands': ['E2']},
    {'label': 'E1', 'instruction': 'ADD', 'operands': ['[B]', '4']},
    {'label': 'E2', 'instruction': 'MUL', 'operands': ['[B]', 'R0']},
    {'label': None, 'instruction': 'MOV', 'operands': ['[A]', 'R0']},
]


memory_values_example = {
    "A": "32",
    "B": "512"
}

df = assemble_program(program_ex2,start_address=0x000010F8,memory_values=memory_values_example)
print(df)