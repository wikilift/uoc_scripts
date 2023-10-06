#from cisca_instruction_set import OPCODES,ADRESSING_MODES
OPCODES = {
    'MOV': '10',
    'DEC': '25',
    'JE': '41',
    'MUL': '22',
    'JMP': '40'
}

ADRESSING_MODES = {
    'Immediate': '0',
    'Register': '1',
    'Memory': '2',
    'Indirect': '3',
    'Relative': '4',
    'Indexed': '5',
    'EN PC': '6'
}

def convert_to_little_endian(value, is_offset=False):
    if 'h' in value:
        hex_value = value.replace('h', '')
    elif value.startswith('0x'):
        hex_value = value[2:]
    elif is_offset and value.startswith('-'):
        hex_value = hex(0x10000 + int(value))  # Convert negative offset to 2's complement
        hex_value = hex_value[2:]
    else:
        hex_value = hex(int(value))[2:]
    hex_value = hex_value.zfill(8)  # Fill with leading zeros to ensure 8 digits
    little_endian = ''.join(reversed([hex_value[i:i+2] for i in range(0, len(hex_value), 2)]))
    return little_endian

# Ajuste en la función calculate_bk_complete
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
        else:
            little_endian = convert_to_little_endian(operand2)
            bk_values.append(little_endian)

    return ' '.join(bk_values)

def format_address(address):
    return f"{address:08X}h"


# Prueba de la función
print("MOV R1,R2 -->", calculate_bk_complete('MOV', ['R1', 'R2']))  # Debería ser 10 11 12
print("JE E2 -->", calculate_bk_complete('JE', ['E2']))  # Debería ser 41 (desplazamiento se añadirá más tarde)
print("MUL R1,R2 -->", calculate_bk_complete('MUL', ['R1', 'R2']))  # Debería ser 22 11 12
print("MOV R3,4 -->", calculate_bk_complete('MOV', ['R3', '4']))  # Debería ser 10 13 00 04 00 00 00
print("MOV [100+R3],R1 -->", calculate_bk_complete('MOV', ['[100+R3]', 'R1']))  # Debería ser 10 53 64 00 00 00 11


program = [
    {'label': None, 'instruction': 'MOV', 'operands': ['R1', 'R2']},
    {'label': 'E1', 'instruction': 'DEC', 'operands': ['R2']},
    {'label': None, 'instruction': 'JE', 'operands': ['E2']},
    {'label': None, 'instruction': 'MUL', 'operands': ['R1', 'R2']},
    {'label': None, 'instruction': 'JMP', 'operands': ['E1']},
    {'label': 'E2', 'instruction': 'MOV', 'operands': ['R3', '4']},
    {'label': None, 'instruction': 'MOV', 'operands': ['[100+R3]', 'R1']}
]

import pandas as pd
# Corregir la generación del DataFrame
df = pd.DataFrame(columns=['Offset', 'Eti', 'Instruction', 'Bk'])

# Calcular los bk values para cada instrucción y añadirlos al DataFrame
initial_address = 0x00010000
current_address = initial_address

label_addresses = {}

for instr in program:
    instr['address'] = current_address
    bk_value = calculate_bk_complete(instr['instruction'], instr['operands'])
    
    # Añadir al diccionario de etiquetas si existe una
    if instr['label']:
        label_addresses[instr['label']] = current_address

    # Calcular el tamaño de la instrucción en bytes
    instr_size = len(bk_value.split())
    
    # Actualizar la dirección actual
    current_address += instr_size
    
    # Guardar el bk value en el diccionario de la instrucción
    instr['bk'] = bk_value

    # Añadir la nueva fila al DataFrame
    new_row = {'Offset': None, 'Eti': instr['label'], 
               'Instruction': f"{instr['instruction']} {' '.join(instr['operands'])}", 
               'Bk': bk_value}
    df = df.append(new_row, ignore_index=True)

print(df)
# label_addresses = {}
# initial_address = 0x00010000
# current_address = initial_address

# for instr in program:
#     instr['address'] = current_address
#     bk_value = calculate_bk_complete(instr['instruction'], instr['operands'])
    
#     if instr['label']:
#         label_addresses[instr['label']] = current_address
    
#     instr_size = len(bk_value.split())
#     current_address += instr_size
#     instr['bk'] = bk_value
# for instr in program:
#     if instr['instruction'] in ['JE', 'JMP']:
#         # Calcular el desplazamiento del salto
#         target_label = instr['operands'][0]
#         target_address = label_addresses.get(target_label, 0)
#         offset = target_address - (instr['address'] + len(instr['bk'].split()))
        
#         # Convertir el desplazamiento a formato little-endian
#         little_endian_offset = convert_to_little_endian(str(offset))
        
#         # Actualizar el bk value de la instrucción
#         instr['bk'] += f" {little_endian_offset}"
# for instr in program:
#     instr['formatted_address'] = format_address(instr['address'])        
# for p in program:
#     for l,v in p.items():
#         print(f"{l}:{v}")

