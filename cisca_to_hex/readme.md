### CISCA to Hex Translator

🖥️ A Python script to translate CISCA assembly language instructions to hexadecimal format. Useful for understanding how different assembly operations are represented in machine code.

#### 📋 Usage

- Navigate to the `scripts` directory and run the script.
  cd cisca_to_hex
  python cisca_to_hex.py

#### ✨ Features

- Translates basic assembly operations like `MOV`, `ADD`, `SUB`, `MUL`, etc., to hexadecimal.
- Displays the state of the program counter, instructions, and their hexadecimal representations.
- Supports exporting the translation to an Excel sheet.

#### 📖 Documentation

##### How to Run with Different Options

- Open `cisca_to_hex.py` in your text editor.
- You can run the `printResult` function with different options to get various outputs.
  printResult(xlsOutput=True, graphic=True)
  
- `xlsOutput=True` will export the translation to an Excel sheet in the `output` directory.
- `graphic=True` will display the translation using matplotlib.

## Example:
```python
from memory_ops import translate_to_hex_with_labels

program = [
    ('MOV', 'R1', 'R2'),
    ('DEC', 'R2', 'LABEL:E1'),
    ('JE', 'E2'),
    ('MUL', 'R1', 'R2'),
    ('JMP', 'E1'),
    ('MOV', 'R3', 4, 'LABEL:E2'),
    ('MOV', '[100+R3]', 'R1')
]

memory_values= {
    "A": "20",
    "B": "200",
    "100":"0"
}

printResult(xlsOutput=False, graphic=True)
```