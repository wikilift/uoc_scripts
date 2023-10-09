
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
ARITHMETIC_OPERATIONS = ['ADD',
    'SUB',
    'MUL',
    'DIV',
    'DEC',
    'INC',
    'MOV']


def ADD(register1, operand, registers, memory):
    add_value = None  
    if isinstance(operand, str):
        if operand.startswith('[') and operand.endswith(']'):
            mem_address = operand[1:-1]
            add_value = int(memory.get(mem_address, 0), 16)
        else:
            add_value = registers.get(operand, 0)
    else:
        add_value = operand

    if register1.startswith('[') and register1.endswith(']'):
        mem_address = register1[1:-1]
        original_value = int(memory.get(mem_address, 0), 16)
        result = (original_value + add_value) & 0xFFFFFFFF  
        memory[mem_address] = f"{result:08X}"  
    else:
        original_value = registers.get(register1, 0)
        result = (original_value + add_value) & 0xFFFFFFFF  
        registers[register1] = result  
   
def DEC(operand, registers, memory):
    dec_value = None
    
    if operand.startswith('[') and operand.endswith(']'):
        mem_address = operand[1:-1]
        dec_value = int(memory.get(mem_address, 0), 16)
    else:
        dec_value = registers.get(operand, 0)

    result = (dec_value - 1) & 0xFFFFFFFF 

    if operand.startswith('[') and operand.endswith(']'):
        mem_address = operand[1:-1]
        memory[mem_address] = f"{result:08X}" 
    else:
        registers[operand] = result  

def INC(operand, registers, memory):
    
    inc_value = None
    
    if operand.startswith('[') and operand.endswith(']'):
        mem_address = operand[1:-1]
        inc_value = int(memory.get(mem_address, 0), 16)
    else:
        inc_value = registers.get(operand, 0)

    result = (inc_value + 1) & 0xFFFFFFFF  

    if operand.startswith('[') and operand.endswith(']'):
        mem_address = operand[1:-1]
        memory[mem_address] = f"{result:08X}" 
    else:
        registers[operand] = result  

def MUL(operand1, operand2, registers, memory):
    mul_value1, mul_value2 = None, None

    if operand1.startswith('[') and operand1.endswith(']'):
        mem_address = operand1[1:-1]
        mul_value1 = int(memory.get(mem_address, 0), 16)
    else:
        mul_value1 = registers.get(operand1, 0)
    if operand2.startswith('[') and operand2.endswith(']'):
        mem_address = operand2[1:-1]
        mul_value2 = int(memory.get(mem_address, 0), 16)
    else:
        mul_value2 = registers.get(operand2, 0)
    result = (mul_value1 * mul_value2) & 0xFFFFFFFF 
    if operand1.startswith('[') and operand1.endswith(']'):
        mem_address = operand1[1:-1]
        memory[mem_address] = f"{result:08X}" 
    else:
        registers[operand1] = result    
    
def SUB(operand1, operand2, registers, memory):
    sub_value1, sub_value2 = None, None
    if operand1.startswith('[') and operand1.endswith(']'):
        mem_address = operand1[1:-1]
        sub_value1 = int(memory.get(mem_address, 0), 16)
    else:
        sub_value1 = registers.get(operand1, 0)

    if operand2.startswith('[') and operand2.endswith(']'):
        mem_address = operand2[1:-1]
        sub_value2 = int(memory.get(mem_address, 0), 16)
    else:
        sub_value2 = registers.get(operand2, 0) if operand2 in registers else operand2
        
    result = (sub_value1 - sub_value2) & 0xFFFFFFFF 
    if operand1.startswith('[') and operand1.endswith(']'):
        mem_address = operand1[1:-1]
        memory[mem_address] = f"{result:08X}"  
    else:
        registers[operand1] = result 

def DIV(operand1, operand2, registers, memory):
    div_value1, div_value2 = None, None

    if operand1.startswith('[') and operand1.endswith(']'):
        mem_address = operand1[1:-1]
        div_value1 = int(memory.get(mem_address, 0), 16)
    else:
        div_value1 = registers.get(operand1, 0)

    if operand2.startswith('[') and operand2.endswith(']'):
        mem_address = operand2[1:-1]
        div_value2 = int(memory.get(mem_address, 0), 16)
    else:
        div_value2 = registers.get(operand2, 0)

    if div_value2 == 0:
        print("Division by zero error. The program cannot continue.")
        exit()

    result = div_value1 // div_value2  
    if operand1.startswith('[') and operand1.endswith(']'):
        mem_address = operand1[1:-1]
        memory[mem_address] = f"{result:08X}"
    else:
        registers[operand1] = result 

   
def execute_arithmetic_operation(instruction, operands, registers, memory):
    if instruction == "ADD":
        ADD(*operands, registers, memory)
    elif instruction == "DEC":
        DEC(*operands,registers=registers,memory=memory)
    elif instruction == "INC":
        INC(*operands,registers=registers,memory=memory)
    elif instruction == "MUL":
        MUL(*operands, registers=registers, memory=memory)
    elif instruction == "SUB":
        SUB(*operands, registers, memory)
    elif instruction == "DIV":
        DIV(*operands, registers, memory)