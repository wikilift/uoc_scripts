### CISCA to Hex Translator

🖥️ A Python script to simulate the CPU instruction cycle for a hypothetical CPU. This script provides insights into the fetch, decode, and execute phases of the instruction cycle for basic assembly language instructions.

#### 📋 Usage

- Navigate to the `scripts` directory and run the script.
  ```bash
   cd cpu_instruction_cycle_simulation
 
```
   cpu_instruction_cycle_simulation.py 


#### ✨ Features

:gear: Simulates the instruction cycle for a hypothetical CPU.

:book: Supports basic assembly language instructions like MOV, ADD, SUB, MUL, etc.

:loudspeaker: Provides a detailed explanation of each step in the instruction cycle.

#### 📖 Documentation

##### How to Run with Different Options

- Open cpu_instruction_cycle_simulation.py in your text editor.
- You can run the simulate_instruction_cycle function with different instruction sets to simulate various cycles.

## Example:
```python
from cpu_instruction_cycle_simulation import simulate_instruction_cycle

instructions = [
    ('MOV', 'R1', 'R2'),
    ('JMP', 'loop'),
    ('MOV', 'R3', 4),
    ('MOV', '[100+R3]', 'R1')
]

offsets = ['00010009h', '0001000Ch', '00010012h', '00010019h']
instruction_bytes = [
    '22 11 12',
    '40 00 03 00 01 00',
    '10 13 00 04 00 00 00',
    '10 53 64 00 00 00 11'
]

for offset, instruction, instr_bytes in zip(offsets, instructions, instruction_bytes):
    for step in simulate_instruction_cycle(instruction, offset, instr_bytes):
        print(step)

```

## 📜 License

[MIT](https://choosealicense.com/licenses/mit/)