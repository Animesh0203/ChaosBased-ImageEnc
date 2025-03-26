from PIL import Image
import os
import time
from Chaos.Yn import *
from Chaos.Check import *

# Ensure key is 80-bit ASCII (10 characters, each 8-bit)
def validate_key(key):
    if len(key) != 10:
        raise ValueError("Key must be exactly 10 ASCII characters (80 bits).")

# Encrypts an image file and returns an encrypted image object
def encrypt(image_file, secret_key_80bits):
    validate_key(secret_key_80bits)
    print(f"🔑 Using Secret Key: {secret_key_80bits}")
    start_time = time.time()
    
    image = Image.open(image_file).convert("RGB")
    pixels = image.load()
    width, height = image.size

    # Convert secret key to binary and hex
    binary_keys = to_8bit_keys(secret_key_80bits)
    print(f"🔑 Using Binary Keys: {binary_keys}")

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


# Decrypts an encrypted image file and returns a decrypted image object
def decrypt(encrypted_image_file, secret_key_80bits):
    validate_key(secret_key_80bits)
    print(f"🔑 Using Secret Key: {secret_key_80bits}")
    start_time = time.time()
    
    image = Image.open(encrypted_image_file).convert("RGB")
    pixels = image.load()
    width, height = image.size

    # Convert secret key to binary and hex
    binary_keys = to_8bit_keys(secret_key_80bits)
    print(f"🔑 Using Binary Keys: {binary_keys}")

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


# **Run the encryption and decryption process**
if __name__ == "__main__":
    # Change this to the image path you want to encrypt
    image_path = "Picture3.jpg"  
    secret_key = "abcdefghij"  # Must be exactly 10 characters (80 bits)

    if not os.path.exists(image_path):
        print(f"❌ Error: File '{image_path}' not found.")
    else:
        try:
            encrypted_path = encrypt(image_path, secret_key)
            decrypted_path = decrypt(encrypted_path, secret_key)

            # Verify if the decrypted image matches the original
            original = Image.open(image_path)
            decrypted = Image.open(decrypted_path)
            if list(original.getdata()) == list(decrypted.getdata()):
                print("✅ SUCCESS: The decrypted image matches the original!")
            else:
                print("❌ WARNING: The decrypted image does NOT match the original.")
        except Exception as e:
            print(f"❌ ERROR: An exception occurred: {str(e)}")