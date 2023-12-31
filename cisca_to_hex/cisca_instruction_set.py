OPCODES = {
    'NOP': '00',
    'STI': '01',
    'CLI': '02',
    'MOV': '10',
    'PUSH': '11',
    'POP': '12',
    'ADD': '20',
    'SUB': '21',
    'MUL': '22',
    'DIV': '23',
    'INC': '24',
    'DEC': '25',
    'CMP': '26',
    'NEG': '27',
    'AND': '30',
    'OR': '31',
    'XOR': '32',
    'TEST': '33',
    'NOT': '34',
    'SAL': '35',
    'SAR': '36',
    'JMP': '40',
    'JE': '41',
    'JNE': '42',
    'JL': '43',
    'JLE': '44',
    'JG': '45',
    'JGE': '46',
    'CALL': '47',
    'RET': '48',
    'INT': '49',
    'IRET': '4A',
    'IN': '50',
    'OUT': '51'
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