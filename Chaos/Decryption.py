
from PIL import Image
from Chaos.Yn import *
from Chaos.Check import *
from Chaos.Encryption import *
import numpy as np
from Chaos.ValidateKey import *


## This function uses all the functions of previous modules, takes an encrypted image file and a 80 bit ascii key provided by the user
## and returns an decrypted image object

def decrypt(encrypted_image_file, secret_key_80bits):
    validate_key(secret_key_80bits)
    start_time = time.time()
    
    image = Image.open(encrypted_image_file).convert("RGB")
    pixels = image.load()
    width, height = image.size

    # Convert secret key to binary and hex
    binary_keys = to_8bit_keys(secret_key_80bits)

    hex_keys = to_hex_keys(secret_key_80bits)

    # Generate chaotic sequences
    x_knot = x0(x01(binary_keys), x02(hex_keys))
    f24 = xn(x_knot, 24)
    p24 = pk(f24)
    y_knot = y0(y01(binary_keys), y02(binary_keys, p24))

    print(f"🔑 Initial x_knot: {x_knot}, y_knot: {y_knot}")
    
    # Process pixels in the same order as encryption
    processing_order = []
    for y in range(height):
        for x in range(width):
            processing_order.append((x, y))
    
    # Reverse the processing order for decryption
    processing_order.reverse()
    
    pixel_count = 0
    # Initialize session keys and chaotic sequences at the beginning
    binary_keys_states = []
    y_knot_states = []
    
    # First pass: compute all states
    temp_binary_keys = binary_keys.copy()
    temp_f24 = f24.copy()
    temp_p24 = p24.copy()
    temp_y_knot = y_knot
    
    for i in range(len(processing_order)):
        if i % 16 == 0:
            temp_binary_keys = modifying_session_keys(temp_binary_keys)
            temp_f24 = xn(temp_f24[23])
            temp_p24 = pk(temp_f24)
            temp_y_knot = y0(y01(temp_binary_keys), y02(temp_binary_keys, temp_p24))
        
        binary_keys_states.append(temp_binary_keys.copy())
        temp_yn_values = yn(temp_y_knot, 20)
        y_knot_states.append(temp_yn_values)
        temp_y_knot = temp_yn_values[-1]
    
    # Second pass: actual decryption
    for i, (x, y) in enumerate(processing_order):
        current_binary_keys = binary_keys_states[len(processing_order) - 1 - i]
        yn_values = y_knot_states[len(processing_order) - 1 - i]
        
        r, g, b = pixels[x, y]  # Extract pixel values
        
        # Apply operations in reverse order
        for value in reversed(yn_values):
            r, g, b = check_operations_to_be_performed(value, r, g, b, current_binary_keys, decryption=True)
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
        pixels[x, y] = (r, g, b)
        pixel_count += 1

    decrypted_file = "decrypted_image.png"
    image.save(decrypted_file)
    print(f"🛠 Decryption complete! Saved as {decrypted_file}")
    print(f"⏱ Time taken: {time.time() - start_time:.2f} seconds")
    return decrypted_file



