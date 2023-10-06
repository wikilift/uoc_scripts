from cisca_instruction_set import OPCODES,ADRESSING_MODES
# Ajuste en la función de conversión para manejar decimales y hexadecimales
def convert_to_little_endian(value):
    if 'h' in value:
        hex_value = value.replace('h', '')
    else:
        hex_value = hex(int(value))[2:]
    hex_value = hex_value.zfill(8)  # Rellenar con ceros a la izquierda para tener 8 dígitos
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



# Prueba de la función
print("MOV R1,R2 -->", calculate_bk_complete('MOV', ['R1', 'R2']))  # Debería ser 10 11 12
print("JE E2 -->", calculate_bk_complete('JE', ['E2']))  # Debería ser 41 (desplazamiento se añadirá más tarde)
print("MUL R1,R2 -->", calculate_bk_complete('MUL', ['R1', 'R2']))  # Debería ser 22 11 12
print("MOV R3,4 -->", calculate_bk_complete('MOV', ['R3', '4']))  # Debería ser 10 13 00 04 00 00 00
print("MOV [100+R3],R1 -->", calculate_bk_complete('MOV', ['[100+R3]', 'R1']))  # Debería ser 10 53 64 00 00 00 11


program = [
    "MOV R1 R2",
    "DEC R2",
    "JE E2",
    "MUL R1 R2",
    "JMP E1",
    "MOV R3 4",
    "MOV [100+R3] R1"
]



start_address = 0x00010000
