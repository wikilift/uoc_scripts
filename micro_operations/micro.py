
def to_big_endian(s: str) -> str: 
    chunks = [s[i:i + 2] for i in range(0, len(s), 2)]
    reversed_chunks = reversed(chunks)
    reversed_s = ''.join(reversed_chunks)
    return reversed_s


def simulate_instruction_cycle(instruction, initial_offset_hex, instruction_bytes, known_labels=[]):
    steps = []
    offset_hex = initial_offset_hex.replace("h", "") 
    offset_decimal = int(offset_hex, 16)

    # Phase 1
    steps.append(f"Fase 1 para instrucción {instruction[0]} {', '.join(map(str, instruction[1:]))} en offset {offset_hex}h:")
    steps.append(f"(MAR={offset_hex.zfill(8)}h) ← (PC={offset_hex.zfill(8)}h), read")

    mbr_content = instruction_bytes.replace(" ", "")
    steps.append(f"(MBR={to_big_endian(mbr_content).zfill(8)}h) ← Memoria")
    
    instruction_size = len(instruction_bytes.split())
    new_offset_decimal = offset_decimal + instruction_size
    new_offset_hex = f"{new_offset_decimal:08X}"
    steps.append(f"(PC={new_offset_hex.zfill(8)}h) ← (PC={offset_hex.zfill(8)}h) + {instruction_size}")
    steps.append(f"(IR={to_big_endian(mbr_content).zfill(8)}) ← (MBR={to_big_endian(mbr_content).zfill(8)})")

    # Phase 2
    steps.append(f"Fase 2:")
    

    if instruction[0] == "MOV":
        source_operand = instruction[2]
        dest_operand = instruction[1]
        if isinstance(source_operand, str) and source_operand.startswith("[") and source_operand.endswith("]"):
            steps.append(f"(Leer el valor en memoria {source_operand})")
        elif isinstance(dest_operand, str) and dest_operand.startswith("[") and dest_operand.endswith("]"):
            steps.append("(No es necesario hacer nada, el operando destino es una dirección de memoria)")
        else:
            steps.append(f"(No es necesario hacer nada, el operando fuente es {source_operand})")
    elif instruction[0]=="JMP":
        steps.append(f"(no hay que hacer nada la etiqueta {instruction[1]} será resuelta durante la ejecución,se entiende como op. fuente)")
    # Phase 3
    steps.append(f"Fase 3:")
    if instruction[0] == "MOV":
        if instruction[1].startswith("[") and instruction[1].endswith("]"):
            steps.append(f"MBR ← {instruction[2]}")
            addr_operand = instruction[1][1:-1].split('+')
            if len(addr_operand) == 2:
                steps.append(f"(MAR=IR(dirección operando) + {addr_operand[1]}) ← {addr_operand[0]} + {addr_operand[1]}, write")
            else:
                steps.append(f"(MAR={addr_operand[0]}h) ← {addr_operand[0]}h, write")
            steps.append("Memoria ← MBR")
        else:
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

