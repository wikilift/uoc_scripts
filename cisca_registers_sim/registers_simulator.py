from program import execute_program
      

registers = {
    'R0': 0x00000000,
    'R1': 0xFFFFFFFF,
    'R2': 0x08000080,
    'R3': 0x10000001,
    'R4': 0xEFFFFFFE,
    'R5': 0x00000001
}

memory = {       
    '00000000': 0x00000000,
    '10000001': 0x00001111,
    'EFFFFFFE': 0x11110000,
    '00100001': 0xFFFFF000,
    '00200002': 0xF000000F,
    'A':        0x00100001
}
program = [
   ('ADD', 'R5', 'R2')]

execute_program(registers=registers, memory=memory, program=program,pdf=False)

