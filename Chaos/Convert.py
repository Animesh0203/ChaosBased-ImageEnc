

## Converts an integer value directly to a 8-bit binary string
def int_to_binary_string(int_value):
    return '00000000'[len(bin(int_value)[2:]):]+bin(int_value)[2:]

# Converts an integer value directly to a 8-bit binary array
def int_to_binary_list(int_value):
    return list('00000000'[len(bin(int_value)[2:]):]+bin(int_value)[2:])

# Converts a 8-bit binary string value directly to a 8-bit binary array
def binary_string_to_binary_list(binary_string):
    return list(binary_string)

# Converts a 8-bit binary array directly to a 8-bit binary string
def binary_list_to_binary_string(list_of_binary_values):
    return (''.join(list_of_binary_values))

# Converts a 8-bit binary array directly to integer value
def binary_list_to_int(list_of_binary_values):
    return int(''.join(list_of_binary_values), 2)

# Converts a 8-bit binary string directly to integer value
def binary_string_to_int(binary_string):
    return int((binary_string),2)


