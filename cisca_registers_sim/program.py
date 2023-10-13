from arithmetic_ops import *
from update_bits import update_status_bits,status_bits
from logic_ops import *
from  pdf_helper import PDF

def generate_pdf(output_lines,initial_registers,initial_memory):
    pdf = PDF()
    pdf.add_page()

    pdf.chapter_title('Initial Registers:')
    pdf.chapter_body_dict(initial_registers)

    pdf.chapter_title('Initial Memory:')
    pdf.chapter_body_dict(initial_memory)

    pdf.chapter_title('Program Output:')
    pdf.set_auto_page_break(auto=1, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.chapter_title("Program Execution Output")
    
    for line in output_lines:
        q=line.split("\n")
        for i in q:
            
            pdf.cell(0, 10, i, ln=True)
    
    pdf.output("output/assembly_output.pdf")

def execute_program(registers, memory, program,pdf=False):
    result=[]
    label_positions=set_labels(program=program)
    index=0
    initial_registers = registers.copy()
    initial_memory = memory.copy()

    while index < len(program):  # Changed to a while loop
        instruction, *operands = program[index]
        result.append(f"Executing: {instruction} {operands}")
        print(f"Executing: {instruction} {operands}")
        result.append("-" * 80)
        print("-" * 80)
        
        if instruction == 'ADD':
            ADD(*operands)
        elif instruction == 'SUB':
            SUB(*operands,memory=memory,registers=registers)
        elif instruction == 'AND':
            AND(*operands,registers=registers)
        elif instruction == 'CMP':
            CMP(*operands)
        elif instruction == 'MOV':
            MOV(*operands,memory=memory,registers=registers)
            if operands[0].startswith('[') and operands[0].endswith(']'):
                mem_address = operands[0][1:-1]
                update_status_bits(memory.get(mem_address, 0))
            else:
                update_status_bits(registers[operands[0]]) 
        elif instruction == 'SHL':
            SHL(*operands)
        elif instruction == 'SHR':
            SHR(*operands)
        elif instruction == 'DEC':
            DEC(*operands)
            update_status_bits(registers[operands[0]]) 
        elif instruction == 'JE':
            index = JE(*operands, index)          
        elif instruction == 'MUL':
            MUL(*operands)
            update_status_bits(registers[operands[0]]) 
        elif instruction == 'JMP':
            index = label_positions[operands[0]]   
        elif instruction == 'JNE':
            index = JNE(*operands, index)
        elif instruction == 'JGE':
            index = JGE(*operands, index)
        elif instruction == 'JG':
            index = JG(*operands, index)
        elif instruction == 'JLE':
            index = JLE(*operands, index)
        elif instruction == 'JL':
            index = JL(*operands, index)
        elif instruction == 'NOT':
            NOT(*operands, registers, memory)

        elif instruction == 'SAR':
            SAR(*operands, registers)
            
        index+=1
        result.append("Current Status Bits:")
        print("Current Status Bits:")
        for k, v in status_bits.items():
            result.append(f"{k}: {v}")
            print(f"{k}: {v}")
        print("-" * 80)
        result.append("-" * 80)
        changed_memory = {k: v for k, v in memory.items() if v != initial_memory.get(k, None)}
        

        if changed_memory:
            result.append("Changed Memory State")
            print("Changed Memory State")
            print("-" * 80)
            for k, v in changed_memory.items():
                result.append(f"Memory Address: 0x{str(k).zfill(8)}h\nInitial Value (Decimal): {initial_memory.get(k, None)}\nCurrent Value (Decimal): {v}\nCurrent Value (Hexadecimal): {str(hex(v)).upper().zfill(8)}\n")
                print(f"Memory Address: 0x{str(k).zfill(8)}h, Initial Value (Decimal): {initial_memory.get(k, None)}, Current Value (Decimal): {v}, Current Value (Hexadecimal): {str(hex(v)).upper().zfill(8)}")
            print("-" * 80)
            initial_memory.update(changed_memory)
        else:
            result.append("No memory positions changed")
            print("No memory positions changed")
            print("-" * 80)
            result.append("-" * 80)
        changed_registers = {k: v for k, v in registers.items() if v != initial_registers.get(k, None)} 
        if changed_registers:
            result.append("Changed Registers:")
            print("Changed Registers:")
            for k, v in changed_registers.items():
                result.append(f"{k}: {str(hex(v)).upper().zfill(8)}Hex, (Decimal):{v}")
                print(f"{k}: {str(hex(v)).upper().zfill(8)}h, (Decimal):{v}")
        else:
            result.append("No registers modified")
            print("No registers modified")
        result.append("-" * 80)
        print("-" * 80)  
        print("*" * 80)
        if pdf:
            generate_pdf(output_lines=result,initial_memory=initial_memory,initial_registers=initial_registers)  