def validate_key(key):
    if len(key) != 10:
        raise ValueError("Key must be exactly 10 ASCII characters (80 bits).")