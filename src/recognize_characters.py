from matplotlib import pyplot as plt
from numba import njit
from numpy import array, argmax, c_, r_, transpose, zeros
from pickle import load
from skimage.transform import resize
from skimage.morphology import skeletonize
from tqdm import tqdm

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow import keras
from keras.models import load_model


def get_character(label, mapping):
    for item in mapping:
        if item[0] == label:
            return chr(item[1])


def get_most_probable_chars(predictions, mapping):
    most_prob_alpha, most_prob_num = "", ""
    alpha_prob, num_prob = 0, 0

    highest_prob_label = argmax(predictions)
    char = get_character(highest_prob_label, mapping)

    if char.isdigit():
        most_prob_num = char
        num_prob = predictions[highest_prob_label]

        while True:
            predictions[highest_prob_label] = 0
            highest_prob_label = argmax(predictions)
            char = get_character(highest_prob_label, mapping)

            if char.isdigit():
                continue
            else:
                most_prob_alpha = char
                alpha_prob = predictions[highest_prob_label]
                break
    else:
        most_prob_alpha = char
        alpha_prob = predictions[highest_prob_label]
        
        while True:
            predictions[highest_prob_label] = 0
            highest_prob_label = argmax(predictions)
            char = get_character(highest_prob_label, mapping)

            if char.isdigit():
                most_prob_num = char
                num_prob = predictions[highest_prob_label]
                break
            else:
                continue
        
    return most_prob_alpha, most_prob_num, alpha_prob, num_prob


def pad_character(character, padding):
    padding_row = zeros((padding, character.shape[1]))
    character = r_[padding_row, character, padding_row]
    
    padding_column = zeros((character.shape[0], padding))
    character = c_[padding_column, character, padding_column]

    return character


def prepare_character(character):
    if str(character) == ' ' or str(character) == '\n':
        return str(character)
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

        standard_padding = 4
        required_size = 28 - 2 * standard_padding
        character = resize(character, (required_size, required_size))
        character = pad_character(character, standard_padding)
        # character = skeletonize(character)
        
        return character


def recognize_characters(characters, debug=False):
    """ Takes a binary image containing a single character, resizes it, and passes it to the neural network for recognition """
    folder_path = os.path.dirname(__file__)
    model = load_model(os.path.join(folder_path, 'model'))
    mapping = load(open(os.path.join(folder_path, 'data', 'mapping.pkl'), 'rb'))

    print("\nPreparing characters ...")
    prepared_characters = [prepare_character(character) for character in tqdm(characters)]

    print("\nPredicting characters ...\n")
    punctuations = []
    actual_characters = []

    for i, prepared_character in enumerate(prepared_characters):
        if isinstance(prepared_character, str):
            punctuations.append({'index': i, 'character': prepared_character})
        else:
            actual_characters.append(transpose(prepared_character))

    predictions = [0 for _ in characters]

    for punctuation in punctuations:
        predictions[punctuation['index']] = punctuation['character']

    actual_characters = array(actual_characters)
    model_predictions = model.predict(actual_characters, verbose=0)

    index = 0
    for i in range(len(predictions)):
        if predictions[i] == 0:
            most_prob_alpha, most_prob_num, alpha_prob, num_prob = get_most_probable_chars(model_predictions[index], mapping)
            predictions[i] = {'alpha': most_prob_alpha, 'alpha prob': alpha_prob, 'num': most_prob_num, 'num prob': num_prob}
            index += 1
            print(predictions[i])

            # predictions[i] = get_character(argmax(model_predictions[index]), mapping)
            # index += 1

    # if debug:
    #     print("Generating debug data ...")
    #     num = 0
    #     for actual_character in tqdm(actual_characters):
    #         plt.title(f"Predictions: {model_predicted_characters[num]}")
    #         plt.imshow(transpose(actual_character))
    #         plt.savefig(os.path.join(folder_path, 'debug_outputs', f'character_{num}.png'))
    #         num += 1

    return predictions