
### Registers Simulator

🖥️ A Python script to simulate register operations in assembly language. Useful for understanding how different operations affect register states and memory.

#### 📋 Usage

- Navigate to the `scripts` directory and run the script.

  cd registers_simulator
  python registers_simulator.py

#### ✨ Features

- Simulates basic assembly operations like `ADD`, `SUB`, `AND`, etc.
- Displays the state of registers and memory before and after each operation.
- Customizable register and memory initial states.

#### 📖 Documentation

##### How to Customize Initial States

- Open `registers_simulator.py` in your text editor.
- Locate the `registers` and `memory` dictionaries.
- Modify the key-value pairs to set your own initial states for registers and memory.

##### Adding New Operations

- Open `registers_simulator.py` in your text editor.
- Locate the main loop where the operations are executed.
- Add your new operation using Python syntax.

Example:

```python

registers = {
    'R2': 0x00000004,
    'R5': 0x0000000A,     
}
memory = {       
    'A13F00FC': 0xA13F0104,
    '00000256': 0x0000025E
}
program = [
   ('ADD', 'R5', 'R2')]
execute_program(registers=registers, memory=memory, program=program)
```
```bash
OUTPUT:
Initial Memory State
--------------------------------------------------------------------------------
Memory Address: A13F00FC, Value (Decimal): 2705260804, Value (Hexadecimal): 0xa13f0104
Memory Address: 00000256, Value (Decimal): 606, Value (Hexadecimal): 0x25e
--------------------------------------------------------------------------------
Executing: ADD ['R5', 'R2']
--------------------------------------------------------------------------------
Current Status Bits:
Z: 0
S: 0
C: 0
V: 0
--------------------------------------------------------------------------------
Memory State
Memory Address: A13F00FC, Value (Decimal): 2705260804, Value (Hexadecimal): 0xa13f0104
Memory Address: 00000256, Value (Decimal): 606, Value (Hexadecimal): 0x25e
--------------------------------------------------------------------------------
Changed Registers:
R5: 0xe
--------------------------------------------------------------------------------
```