from sympy import *

def limit_calc(function: str, variable: str, value_to_aproximate: str) -> str:
    
    if value_to_aproximate == 'oo':
        value_to_aproximate = oo
    elif value_to_aproximate == '-oo':
        value_to_aproximate = -oo
    else:
        value_to_aproximate = S(value_to_aproximate)  
    
    x = symbols(variable)
    func = S(function) 
    
    print(f"1: Original: {func}")
    
    
    func_simplified = func.simplify()
    if func != func_simplified:
        print(f"2: Simplified: {func_simplified}")
    
    if func.is_rational_function(x):
        highest_power = degree(func.as_numer_denom()[1], gen=x)
        print(f"Step 3: The highest power of x in the denominator is {highest_power}.")
       
        numer, denom = func.as_numer_denom()
        func_divided = cancel((numer / (x ** highest_power)) / (denom / (x ** highest_power)))
        print(f"Step 4: Function after dividing by x^{highest_power}: {func_divided}")
    
    lim = limit(func_simplified, x, value_to_aproximate)
    return f"3: Limit is: {lim}"


result = limit_calc("(4*x**2 - 3*x + 2) / (2*x**2 - 7*x - 5)", "x", "oo")


print(result)
