import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

# Load the model
model = load_model("typo_detection_model.h5")

tokenizer = Tokenizer()
max_len = 6

# Function to preprocess new sentences
def preprocess_sentence(sentence):
    sequence = tokenizer.texts_to_sequences([sentence])
    padded = pad_sequences(sequence, maxlen=max_len, padding="post")
    return padded


# Function to convert sequence back to text
def sequence_to_text(sequence):
    return "".join(tokenizer.index_word.get(i, "") for i in sequence)


# Function to apply model and detect typos
def detect_typos(sentence):
    preprocessed = preprocess_sentence(sentence)
    prediction = model.predict(preprocessed)[0]

    predicted_sequence = np.argmax(prediction, axis=-1)
    predicted_text = sequence_to_text(predicted_sequence)

    typos = []
    for i, (orig_char, pred_char) in enumerate(zip(sentence, predicted_text)):
        if orig_char != pred_char:
            typos.append((i, orig_char, pred_char))

    return typos


# Example usage
sentence = "Thiss is a test sentnce."
typo_detected = detect_typos(sentence)
print(typo_detected)
