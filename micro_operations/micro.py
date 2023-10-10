
def to_big_endian(s: str) -> str: 
    chunks = [s[i:i + 2] for i in range(0, len(s), 2)]
    reversed_chunks = reversed(chunks)
    reversed_s = ''.join(reversed_chunks)
    return reversed_s


def simulate_instruction_cycle(instruction, initial_offset_hex, instruction_bytes):
    steps = []
    offset_hex = initial_offset_hex.replace("h", "") 
    offset_decimal = int(offset_hex, 16)

  
    steps.append(f"Fase 1 para instrucción {instruction[0]} {', '.join(map(str, instruction[1:]))} en offset {offset_hex}h:")
    steps.append(f"(MAR={offset_hex.zfill(8)}h) ← (PC={offset_hex.zfill(8)}h), read")

    mbr_content = instruction_bytes.replace(" ", "")
    steps.append(f"(MBR={to_big_endian(mbr_content).zfill(8)}h) ← Memoria")
    
    instruction_size = len(instruction_bytes.split())
    new_offset_decimal = offset_decimal + instruction_size
    new_offset_hex = f"{new_offset_decimal:08X}"
    steps.append(f"(PC={new_offset_hex.zfill(8)}h) ← (PC={offset_hex.zfill(8)}h) + {instruction_size}")
    
    steps.append(f"(IR={to_big_endian(mbr_content).zfill(8)}) ← (MBR={to_big_endian(mbr_content).zfill(8)})")


    steps.append(f"Fase 2:")
    operands_are_registers = all(isinstance(op, str) and op.startswith("R") for op in instruction[1:])
    if operands_are_registers:
        steps.append("(No es necesario hacer nada, los operandos fuente son registros)")
    else:
        for operand in instruction[1:]:
            if isinstance(operand, str) and operand.startswith("[") and operand.endswith("]"):
                steps.append(f"(Leer el valor en memoria {operand})")
            elif isinstance(operand, str) and operand in known_labels:
                steps.append(f"(no hay que hacer nada la etiqueta {operand} será resuelta durante la ejecución,se entiende como op. fuente)")
            elif isinstance(operand, str):
                steps.append(f"(No es necesario hacer nada {operand} es un valor que ya está en un registro)")
            elif isinstance(operand, int):
                steps.append(f"(No es necesario hacer nada {operand} es un valor inmediato está en la propia instrucción)")

    steps.append(f"Fase 3:")
    if instruction[0] == "MOV":
        steps.append(f"{instruction[1]} ← {instruction[2]}")
    elif instruction[0] == "MUL":
        steps.append(f"{instruction[1]} ← {instruction[1]} * {instruction[2]}")
    elif instruction[0] == "ADD":
        steps.append(f"{instruction[1]} ← {instruction[1]} + {instruction[2]}")
    elif instruction[0] == "SUB":
        steps.append(f"{instruction[1]} ← {instruction[1]} - {instruction[2]}")
    elif instruction[0] == "JMP":
        steps.append(f"(PC={instruction[1]}) ← {instruction[1]}")
    elif instruction[0] == "JE":
        steps.append(f"Si Z=1, (PC={instruction[1]}) ← {instruction[1]}")
    elif instruction[0] == "JNE":
        steps.append(f"Si Z=0, (PC={instruction[1]}) ← {instruction[1]}")
    elif instruction[0] == "JL":
        steps.append(f"Si L=1, (PC={instruction[1]}) ← {instruction[1]}")
    elif instruction[0] == "JLE":
        steps.append(f"Si LE=1, (PC={instruction[1]}) ← {instruction[1]}")
    elif instruction[0] == "JG":
        steps.append(f"Si G=1, (PC={instruction[1]}) ← {instruction[1]}")
    elif instruction[0] == "JGE":
        steps.append(f"Si GE=1, (PC={instruction[1]}) ← {instruction[1]}")
    elif instruction[0] == "CALL":
        steps.append(f"MBR ← PC")
        steps.append("SP ← SP - 4")
        steps.append("MAR ← SP, write")
        steps.append("Memoria ← MBR")
        steps.append(f"PC ← {instruction[1]}")
    elif instruction[0] == "RET":
        steps.append("MAR ← SP, read")
        steps.append("MBR ← Memoria")
        steps.append("SP ← SP + 4")
        steps.append("PC ← MBR")
    steps.append("_"*80)
    return steps

offsets = ["00010009h", "0001000Ch", "00010012h", "00010019h"]
instructions = [
    ("MUL", "R1", "R2"),
    ("JMP", "loop"),
    ("MOV", "R3", 4),
    ("MOV", "[100+R3]", "R1")
]
instruction_bytes = [
    "22 11 12",
    "40 00 03 00 01 00",
    "10 13 00 04 00 00 00",
    "10 53 64 00 00 00 11"
]
known_labels = ["loop", "start", "end"] 

for offset, instruction, instr_bytes in zip(offsets, instructions, instruction_bytes):
    for r in simulate_instruction_cycle(instruction, offset, instr_bytes):
        print(r)

