
def to_big_endian(s: str) -> str: 
    chunks = [s[i:i + 2] for i in range(0, len(s), 2)]
    reversed_chunks = reversed(chunks)
    reversed_s = ''.join(reversed_chunks)
    return reversed_s


def simulate_instruction_cycle(instruction, initial_offset_hex, instruction_bytes, known_labels=[]):
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
    
    elif instruction[0] == "XOR":
       
        if isinstance(instruction[2], str) and instruction[2].startswith("[") and instruction[2].endswith("]"):
            steps.append(f"(Leer el valor en memoria {instruction[2]})")
        else:
            steps.append(f"(No es necesario hacer nada, el operando fuente es {instruction[2]})")
    elif instruction[0] in ["ADD", "SUB","MUL","DIV"]:
       
        if isinstance(instruction[2], str) and instruction[2].startswith("[") and instruction[2].endswith("]"):
            steps.append(f"(Leer el valor en memoria {instruction[2]})")
        else:
            steps.append(f"(No es necesario hacer nada, el operando fuente es {instruction[2]})")
    elif instruction[0] == "CMP":
        
        if isinstance(instruction[2], int):
            steps.append(f"(Cargar el valor inmediato {instruction[2]})")
        elif isinstance(instruction[2], str) and instruction[2].startswith("[") and instruction[2].endswith("]"):
            steps.append(f"(Leer el valor en memoria {instruction[2]})")
        else:
            steps.append(f"(No es necesario hacer nada, el operando fuente es {instruction[2]})")
        
    elif instruction[0] in ["JLE", "JE", "JNE", "JL", "JLE", "JG", "JGE"]:
        steps.append(f"Evaluación de las condiciones para el salto utilizando los flags apropiados.")   
    
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
    elif instruction[0] == "CMP":
        steps.append(f"Comparar el valor en el registro {instruction[1]} con el valor {instruction[2]}")
        steps.append(f"Ajustar los flags de estado (Z, L, G) según el resultado de la comparación")

    elif instruction[0] == "XOR":
        steps.append(f"{instruction[1]} ← {instruction[1]} XOR {instruction[2]}") 
        steps.append(f"Realizar la operación XOR entre el registro {instruction[1]} y el valor/registro {instruction[2]}")
        steps.append(f"Guardar el resultado en el registro {instruction[1]}")

    elif instruction[0] == "ADD":
        steps.append(f"{instruction[1]} ← {instruction[1]} + {instruction[2]}")
        steps.append(f"Sumar el valor en el registro {instruction[1]} y el valor/registro {instruction[2]}")
        steps.append(f"Guardar el resultado en el registro {instruction[1]}")

    elif instruction[0] == "SUB":
        steps.append(f"{instruction[1]} ← {instruction[1]} - {instruction[2]}")
        steps.append(f"Restar el valor/registro {instruction[2]} del registro {instruction[1]}")
        steps.append(f"Guardar el resultado en el registro {instruction[1]}")

    elif instruction[0] == "MUL":
        steps.append(f"{instruction[1]} ← {instruction[1]} * {instruction[2]}")
        steps.append(f"Multiplicar el valor en el registro {instruction[1]} por el valor/registro {instruction[2]}")
        steps.append(f"Guardar el resultado en el registro {instruction[1]}")

    elif instruction[0] in ["JMP", "JE", "JNE", "JL", "JLE", "JG", "JGE"]:
        condition = {
            "JMP": "incondicionalmente",
            "JE": "si el flag Z es 1",
            "JNE": "si el flag Z es 0",
            "JL": "si el flag L es 1",
            "JLE": "si el flag LE es 1",
            "JG": "si el flag G es 1",
            "JGE": "si el flag GE es 1",
        }[instruction[0]]
        steps.append(f"Evaluar la condición {condition}")
        steps.append(f"Si la condición se cumple, actualizar el registro del contador del programa (PC) con el valor {instruction[1]}")

    elif instruction[0] == "CALL":
        steps.append(f"Guardar el valor actual del PC en el registro MBR")
        steps.append(f"Decrementar el puntero de pila SP en 4")
        steps.append(f"Escribir el valor del MBR en la dirección apuntada por SP")
        steps.append(f"Actualizar el registro del contador del programa (PC) con el valor {instruction[1]}")

    elif instruction[0] == "RET":
        steps.append(f"Leer el valor en la dirección apuntada por SP en el registro MBR")
        steps.append(f"Incrementar el puntero de pila SP en 4")
        steps.append(f"Actualizar el registro del contador del programa (PC) con el valor almacenado en MBR")

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

