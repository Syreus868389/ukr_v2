from numpy import real
from sympy import symbols, Eq, solve
from datetime import datetime
from math import ceil

def resolve_interval(start: str, end: str, portion_size: int):
    '''
    Args:
    Dates should be strings.
    Interval should be an integer.
    '''
    f_start = datetime.strptime(start, "%Y-%m-%d")
    f_end = datetime.strptime(end, "%Y-%m-%d")
    delta = (f_end  - f_start )
    delta_days = delta.days
    x = symbols('x', real=True)
    eq = Eq(delta_days/x, portion_size)
    solution = solve(eq, x)
    interval = solution[0]

    chunk = delta/float(interval)
    
    for i in range(ceil(interval)):
          
        # using generator function to solve problem
        # returns intermediate result
        yield (f_start + chunk * i).strftime("%Y-%m-%d")

    yield f_end.strftime("%Y-%m-%d")