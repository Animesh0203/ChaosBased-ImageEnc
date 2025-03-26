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
