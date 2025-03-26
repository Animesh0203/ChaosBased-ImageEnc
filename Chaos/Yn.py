# Importing all the functions from YInitial module for testing
from Chaos.YInitial import *


# This module generates yn values

# This function takes initial value of y0 (as 'YInitial') generated using YInitial module
# and number of values to be generated (as 'number_of_values') and computes a chaotic value

def yn(YInitial, number_of_values=16):
    yn=YInitial
    yn_values = []
    while len(yn_values)<number_of_values:
        y_n_plus_1 = (3.9999)*yn*(1-yn)
        yn = y_n_plus_1
        yn_values.append(y_n_plus_1)


    return yn_values





