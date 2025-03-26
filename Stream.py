import streamlit as st
import os
from PIL import Image
import base64
import io

import base64
import os

def secure_key_export(key):
    """
    Securely export the encryption key
    
    Args:
        key (str): The encryption key to export
    
    Returns:
        bytes: Encrypted/encoded key for secure download
    """
    # Base64 encode the key for initial obfuscation
    encoded_key = base64.b64encode(key.encode('utf-8'))
    
    # Optional: Add an extra layer of security
    # Here you could add additional encryption if needed
    
    return encoded_key


import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Dropout
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Define character set and mapping
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"
char_to_idx = {c: i + 1 for i, c in enumerate(chars)}  # Start index from 1
idx_to_char = {i: c for c, i in char_to_idx.items()}
vocab_size = len(chars) + 1  # Including 0 for padding

# Function to generate random keys
def generate_keys(num_keys=1000, key_length=10):
    return [''.join(np.random.choice(list(chars), key_length)) for _ in range(num_keys)]

# Encode keys into numerical format
def encode_keys(keys):
    return [[char_to_idx[c] for c in key] for key in keys]

# Prepare dataset
keys = generate_keys()
encoded_keys = encode_keys(keys)
max_length = max(map(len, encoded_keys))

X = pad_sequences(encoded_keys, maxlen=max_length, padding='post', value=0)
y = np.roll(X, shift=-1, axis=-1)

# One-hot encoding labels
y = keras.utils.to_categorical(y, num_classes=vocab_size)

# Define LSTM Model
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=64, input_length=max_length),
    LSTM(128, return_sequences=True),
    Dropout(0.2),
    LSTM(256, return_sequences=True),
    Dropout(0.2),
    Dense(vocab_size, activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam')

# Train the model
model.fit(X, y, epochs=50, batch_size=32, verbose=1)

# Function to generate keys based on seed input
def generate_key(seed, length=10):
    generated = seed
    for _ in range(length - len(seed)):
        seed_encoded = pad_sequences([[char_to_idx.get(c, 0) for c in generated]], maxlen=max_length, padding='post')
        pred_probs = model.predict(seed_encoded, verbose=0)[0][len(generated) - 1]
        pred_idx = np.argmax(pred_probs)
        generated += idx_to_char.get(pred_idx, '?')  # Fallback to '?' for unknown indices
    return generated



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


def generate_key():
    """
    Placeholder function for key generation.
    Replace with your actual key generation logic.
    """
    seed = ""
    key = generate_key(seed)
    return key

def encrypt_image(image_path, key):
    """
    Placeholder function for image encryption.
    Replace with your actual encryption logic.
    """
    encrypted_image = encrypt(image_path, key)
    return encrypted_image

def decrypt_image(encrypted_image_path, key):
    """
    Placeholder function for image decryption.
    Replace with your actual decryption logic.
    """
    decrypted_image = decrypt(encrypted_image_path, key)
    return decrypted_image

def secure_key_import(encrypted_key_file):
    """
    Import and decrypt the secure key
    
    Args:
        encrypted_key_file (bytes): Encrypted key file data
    
    Returns:
        str: Decrypted original key
    """
    try:
        # Decode the base64 encoded key
        decoded_key = base64.b64decode(encrypted_key_file).decode('utf-8')
        return decoded_key
    except Exception as e:
        st.error(f"Error importing key: {e}")
        return None

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Image Encryption App", 
        page_icon="🔐", 
        layout="wide"
    )

    # Custom CSS for modern, elegant design
    st.markdown("""
    <style>
    .main-container {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #4e73df;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #3a5cd8;
        transform: scale(1.05);
    }
    .upload-box {
        border: 2px dashed #4e73df;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .upload-box:hover {
        background-color: #e6eaf5;
    }
    </style>
    """, unsafe_allow_html=True)

    # Main container    
    # Title
    st.title("🔐 Image Encryption Utility")
    st.write("Secure your images with easy encryption and decryption")

    # Columns for better layout


    # Image Upload
    uploaded_file = st.file_uploader(
        "Choose an image to encrypt", 
        type=['png', 'jpg', 'jpeg', 'bmp', 'gif'],
        help="Upload an image file you want to encrypt"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Key Generation
    if st.button("🔑 Generate Encryption Key"):
        key = generate_key()
        st.success(f"Key Generated: {key}")
        st.session_state.encryption_key = key
        
        # Secure key export
        secure_exported_key = secure_key_export(key)
        
        # Download button with secure key
        st.download_button(
            label="Download Encryption Key",
            data=secure_exported_key,
            file_name="secure_encryption_key.enc",  # .enc extension suggests encrypted file
            mime="application/octet-stream"  # Generic binary file
        )



    # Encryption Section
    if uploaded_file is not None:
        # Save uploaded file temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Display uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Encrypt Button
        if st.button("🔒 Encrypt Image"):
            if 'encryption_key' in st.session_state:
                encrypted_path = encrypt_image(temp_path, st.session_state.encryption_key)
                st.success("Image Encrypted Successfully!")
                
                # Provide download option for encrypted image
                with open(encrypted_path, "rb") as file:
                    st.download_button(
                        label="Download Encrypted Image",
                        data=file.read(),
                        file_name="encrypted_image.enc",
                        mime="application/octet-stream"
                    )
            else:
                st.warning("Please generate an encryption key first!")

    st.sidebar.header("🔑 Key Management")
    uploaded_key_file = st.sidebar.file_uploader(
        "Load Encryption Key", 
        type=['enc'],
        help="Upload your previously generated secure encryption key"
    )

    if uploaded_key_file is not None:
        # Read the uploaded key file
        key_file_contents = uploaded_key_file.read()
        
        # Import the key
        imported_key = secure_key_import(key_file_contents)
        
        if imported_key:
            # Store the imported key in session state
            st.session_state.decryption_key = imported_key
            st.sidebar.success("Key Successfully Imported!")
            
            # Optional: Show first few characters of the key (for verification)
            st.sidebar.info(f"Key Preview: {imported_key[:10]}...")

    # Decryption Section
    st.markdown("---")
    st.subheader("🔓 Decryption")
    
    decrypt_col1, decrypt_col2 = st.columns(2)
    
    with decrypt_col1:
        # Encrypted Image Upload
        encrypted_file = st.file_uploader(
            "Choose an encrypted image", 
            type=['enc'],
            help="Upload an encrypted image file"
        )

    with decrypt_col2:
        # Decryption Options
        if encrypted_file is not None:
            # Temporary save of encrypted file
            temp_encrypted_path = f"temp_encrypted_{encrypted_file.name}"
            with open(temp_encrypted_path, "wb") as f:
                f.write(encrypted_file.getvalue())
            
            # Decrypt Button
            decrypt_key = st.text_input("Enter Decryption Key", type="password")
            
            if st.button("🔓 Decrypt Image"):
                if decrypt_key:
                    decrypted_path = decrypt_image(temp_encrypted_path, decrypt_key)
                    st.success("Image Decrypted Successfully!")
                    
                    # Display decrypted image
                    st.image(decrypted_path, caption="Decrypted Image", use_column_width=True)
                    
                    # Provide download option for decrypted image
                    with open(decrypted_path, "rb") as file:
                        st.download_button(
                            label="Download Decrypted Image",
                            data=file.read(),
                            file_name="decrypted_image.png",
                            mime="image/png"
                        )
                else:
                    st.warning("Please enter the decryption key!")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()