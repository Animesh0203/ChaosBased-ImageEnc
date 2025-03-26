import streamlit as st
import os
from PIL import Image
import base64
import io
from keyGen import generate_key as keyGen
from de import encrypt
from de import decrypt
from Chaos.Encode_key import secure_key_export
# Placeholder functions (you'll replace these with your actual implementations)
def generate_key():
    """
    Placeholder function for key generation.
    Replace with your actual key generation logic.
    """
    seed = ""
    key = keyGen(seed)
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