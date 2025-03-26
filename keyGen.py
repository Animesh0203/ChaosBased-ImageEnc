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

