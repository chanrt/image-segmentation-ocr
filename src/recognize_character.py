from matplotlib import pyplot as plt
from numpy import argmax, c_, r_, transpose, zeros
from pickle import load
from skimage.transform import resize

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow import keras
from keras.models import load_model


def get_character(label, mapping):
    for item in mapping:
        if item[0] == label:
            return chr(item[1])


def pad_character(character, padding):
    padding_row = zeros((padding, character.shape[1]))
    character = r_[padding_row, character, padding_row]
    
    padding_column = zeros((character.shape[0], padding))
    character = c_[padding_column, character, padding_column]

    return character


def recognize_characters(characters):
    """ Takes a binary image containing a single character, resizes it, and passes it to the neural network for recognition """
    folder_path = os.path.dirname(__file__)
    model = load_model(os.path.join(folder_path, 'model'))
    mapping = load(open(os.path.join(folder_path, 'mapping.pkl'), 'rb'))
    predictions = []

    for character in characters:
        if str(character) == ' ' or str(character) == '\n':
            predictions.append(character)
        else:
            num_rows, num_cols = character.shape

            if num_rows > num_cols:
                num_either_side = (num_rows - num_cols) // 2
                padding_column = zeros((num_rows, 1))

                for _ in range(num_either_side):
                    character = c_[padding_column, character]

                for _ in range(num_either_side):
                    character = c_[character, padding_column]
            else:
                num_either_side = (num_cols - num_rows) // 2
                padding_row = zeros((1, num_cols))

                for _ in range(num_either_side):
                    character = r_[padding_row, character]

                for _ in range(num_either_side):
                    character = r_[character, padding_row]

            standard_padding = 3
            required_size = 28 - 2 * standard_padding
            character = resize(character, (required_size, required_size))
            character = pad_character(character, standard_padding)

            input_vector = transpose(character).reshape(-1, 784)
            prediction = get_character(argmax(model.predict(input_vector, verbose=0)), mapping)
            predictions.append(prediction)

    return predictions