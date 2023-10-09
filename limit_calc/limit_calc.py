from sympy import symbols, limit, oo, S, degree, latex
import matplotlib.pyplot as plt

def limit_calc(function: str, variable: str, value_to_aproximate: str) -> str:
    steps = []
    
    if value_to_aproximate == 'oo':
        value_to_aproximate = oo
    elif value_to_aproximate == '-oo':
        value_to_aproximate = -oo
    else:
        value_to_aproximate = S(value_to_aproximate)
    
    x = symbols(variable)
    func = S(function)
    
    steps.append(f"1: Original: ${latex(func)}$")
    
    if func.is_rational_function(x):
        numer, denom = func.as_numer_denom()
        
       
        highest_power = degree(denom, gen=x)
        steps.append(f"2: The highest power of x in the denominator is {highest_power}.")
        
        
        numer_divided = numer / x**highest_power
        denom_divided = denom / x**highest_power
        
        
        numer_divided = numer_divided.simplify()
        denom_divided = denom_divided.simplify()
        
        func_divided = numer_divided / denom_divided

        steps.append(f"3: Function after dividing by x^{highest_power}: ${latex(func_divided)}$")
        
        func_to_use_for_limit = func_divided
    
    else:
        func_to_use_for_limit = func
    
    lim = limit(func_to_use_for_limit, x, value_to_aproximate)
    steps.append(f"4: The limit is: ${latex(lim)}$")
    
    fig, ax = plt.subplots()
    ax.axis('off')
    for i, step in enumerate(reversed(steps)):
        ax.annotate(step, xy=(0.5, 0.1 + i * 0.2), xycoords='axes fraction', fontsize=16,
                    horizontalalignment='center', verticalalignment='center')
    
    plt.show()
                      #! operation                   "var""tendence"
#limit_calc("(4*x**2 - 3*x + 2) / (2*x**2 - 7*x - 5)", "x", "oo")
limit_calc("(x**2 - 3*x + 1) / (4*x**2 + 2)", "x", "oo")#? indeterminate test

