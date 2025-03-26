
from PIL import Image
from Chaos.Yn import *
from Chaos.Check import *
import time
from Chaos.ValidateKey import *
#from numba import jit

## Importing all the previous modules



## This function uses all the functions of previous modules, takes an image file and a 80 bit ascii key provided by the user
## and returns an encrypted image object
def encrypt(image_file, secret_key_80bits):
    validate_key(secret_key_80bits)
    start_time = time.time()
    
    image = Image.open(image_file).convert("RGB")
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

    # Store the processing order to ensure decryption follows the same pattern
    processing_order = []
    
    pixel_count = 0
    for y in range(height):
        for x in range(width):
            processing_order.append((x, y))
            if pixel_count % 16 == 0:
                binary_keys = modifying_session_keys(binary_keys)
                f24 = xn(f24[23])
                p24 = pk(f24)
                y_knot = y0(y01(binary_keys), y02(binary_keys, p24))

            r, g, b = pixels[x, y]  # Extract pixel values
            yn_values = yn(y_knot, 20)

            # Keep track of the sequence of operations
            for value in yn_values:
                # Apply bounds checking to ensure valid RGB values (0-255)
                r, g, b = check_operations_to_be_performed(value, r, g, b, binary_keys, decryption=False)
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))

            pixels[x, y] = (r, g, b)
            y_knot = yn_values[-1]
            pixel_count += 1

    encrypted_file = "encrypted_image.png"
    image.save(encrypted_file)
    
    # Save processing order for decryption
    with open("processing_order.txt", "w") as f:
        for x, y in processing_order:
            f.write(f"{x},{y}\n")
    
    print(f"🛠 Encryption complete! Saved as {encrypted_file}")
    print(f"⏱ Time taken: {time.time() - start_time:.2f} seconds")
    return encrypted_file