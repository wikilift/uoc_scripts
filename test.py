import pandas as pd
from cisca_instruction_set import OPCODES,ADRESSING_MODES

def format_address(address):
    return f"{address:08X}"
# Function to convert values to little-endian format
def convert_to_little_endian(value):
    if 'h' in value:
        hex_value = value.replace('h', '')
    else:
        hex_value = hex(int(value))[2:]
    hex_value = hex_value.zfill(8)
    little_endian = ''.join(reversed([hex_value[i:i+2] for i in range(0, len(hex_value), 2)]))
    return little_endian

# Function to calculate the BK (hex values) for a complete instruction
def calculate_bk_complete(instruction, operands):
    opcode = OPCODES.get(instruction, '??')
    bk_values = [opcode]

    # Primer operando
    operand1 = operands[0]
    if operand1.startswith('R'):
        bk_values.append(ADRESSING_MODES['Register'] + operand1[1])
    elif operand1.startswith('[') and operand1.endswith(']'):
        if '+' in operand1:
            mode = 'Indexed' if 'R' in operand1.split('+')[1] else 'Relative'
            bk_values.append(ADRESSING_MODES[mode] + '3')
            hex_value = operand1.strip('[]').split('+')[0]
            little_endian = convert_to_little_endian(hex_value)
            bk_values.append(little_endian)
        else:
            # This is the case where operand is something like [A] or [B]
            bk_values.append(ADRESSING_MODES['Memory'] + '0')
    elif operand1 in ['E1', 'E2']:  # estas son etiquetas
        bk_values.append(ADRESSING_MODES['EN PC'] + '0')
    else:
        bk_values.append(ADRESSING_MODES['Immediate'] + '0')
        little_endian = convert_to_little_endian(operand1)
        bk_values.append(little_endian)

    # Segundo operando, si existe
    if len(operands) > 1:
        operand2 = operands[1]
        if operand2.startswith('R'):
            bk_values.append(ADRESSING_MODES['Register'] + operand2[1])
        elif operand2.startswith('[') and operand2.endswith(']'):
            bk_values.append(ADRESSING_MODES['Memory'] + '0')
        else:
            little_endian = convert_to_little_endian(operand2)
            bk_values.append(little_endian)

    return ' '.join(bk_values)


# Sample assembly program
#!exercise 1
# program = [
#     {'label': None, 'instruction': 'MOV', 'operands': ['R1', 'R2']},
#     {'label': 'E1', 'instruction': 'DEC', 'operands': ['R2']},
#     {'label': None, 'instruction': 'JE', 'operands': ['E2']},
#     {'label': None, 'instruction': 'MUL', 'operands': ['R1', 'R2']},
#     {'label': None, 'instruction': 'JMP', 'operands': ['E1']},
#     {'label': 'E2', 'instruction': 'MOV', 'operands': ['R3', '4']},
#     {'label': None, 'instruction': 'MOV', 'operands': ['[100+R3]', 'R1']}
# ]
#!exercise 2
program = [
    {'label': None, 'instruction': 'MOV', 'operands': ['R0', '[A]']},
    {'label': None, 'instruction': 'CMP', 'operands': ['R0', '[B]']},
    {'label': None, 'instruction': 'JLE', 'operands': ['E1']},
    {'label': None, 'instruction': 'DEC', 'operands': ['R0']},
    {'label': None, 'instruction': 'JMP', 'operands': ['E2']},
    {'label': 'E1', 'instruction': 'ADD', 'operands': ['[B]', '4']},
    {'label': 'E2', 'instruction': 'MUL', 'operands': ['[B]', 'R0']},
    {'label': None, 'instruction': 'MOV', 'operands': ['[A]', 'R0']},
]
import pandas as pd

# Create a DataFrame to hold the information
df = pd.DataFrame(columns=['Instruction', 'BK'])

# Populate the DataFrame
for instr in program:
    instruction_str = f"{instr['instruction']} {' '.join(instr['operands'])}"
    bk_str = calculate_bk_complete(instr['instruction'], instr['operands'])
    df = df.append({'Instruction': instruction_str, 'BK': bk_str}, ignore_index=True)

print(df)
