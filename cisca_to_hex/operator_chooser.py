
ARITHMETIC_OPERATIONS = ['ADD',
    'SUB',
    'MUL',
    'DIV',
    'DEC',
    'INC',
    'MOV','XOR']


def ADD(register1, operand, registers, memory):
    add_value = None  
    if isinstance(operand, str):
        if operand.startswith('[') and operand.endswith(']'):
            mem_address = operand[1:-1]
            add_value = int(str(memory.get(mem_address, 0)), 16)

        else:
            add_value = registers.get(operand, 0)
    else:
        add_value = operand

    if register1.startswith('[') and register1.endswith(']'):
        mem_address = register1[1:-1]
        original_value = int(str(memory.get(mem_address, 0)), 16)

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

    def get_value(value, source):
        if isinstance(value, str) and value.startswith('[') and value.endswith(']'):
            mem_address = value[1:-1]
            return int(source.get(mem_address, "0"), 16)
        else:
            return source.get(value, 0)

    sub_value1 = get_value(operand1, memory if operand1.startswith('[') and operand1.endswith(']') else registers)
    sub_value2 = get_value(operand2, memory if operand2.startswith('[') and operand2.endswith(']') else registers)

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

def XOR(register1, operand, registers, memory):
    xor_value = None
    if isinstance(operand, str):
        if operand.startswith('[') and operand.endswith(']'):
            mem_address = operand[1:-1]
            xor_value = int(memory.get(mem_address, 0), 16)
        else:
            xor_value = registers.get(operand, 0)
    else:
        xor_value = operand

    if register1.startswith('[') and register1.endswith(']'):
        mem_address = register1[1:-1]
        original_value = int(memory.get(mem_address, 0), 16)
        result = original_value ^ xor_value
        memory[mem_address] = f"{result:08X}"
    else:
        original_value = registers.get(register1, 0)
        result = original_value ^ xor_value
        registers[register1] = result

   
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
    elif instruction == "XOR":
        XOR(*operands, registers, memory)