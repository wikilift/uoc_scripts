# Limit Calculator

## Description

This Python script uses SymPy to calculate limits of rational functions and visualizes the step-by-step process with Matplotlib. The script is designed to handle both finite and infinite limits.

## Features

- 📊 Visualizes each step of the calculation process.
- 📝 Handles both finite and infinite limits.
- 🧮 Supports rational functions.

## Requirements

- Python 3.x
- SymPy
- Matplotlib

To install the required packages, run:

```bash
pip install -r requirements.txt
```
## Usage
```python
#Import the limit_calc function from the script.
from limit_calculator import limit_calc
#Call limit_calc with the function, variable, and value to approximate as arguments.
limit_calc("(x**2 - 3*x + 1) / (4*x**2 + 2)", "x", "oo")
```
