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
            # get most probable alphabet
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
            # get most probable number
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


def character_recognizer(characters, use_cnn=True, printed_chars=True, debug=False):
    """ Takes binary images containing single characters and passes it to the neural network for recognition """
    folder_path = os.path.dirname(__file__)
    mapping = load(open(os.path.join(folder_path, 'data', 'mapping.pkl'), 'rb'))

    model_name = ""
    if use_cnn:
        model_name += "cnn_model"
    else:
        model_name += "ann_model"

    if printed_chars:
        model_name += "_printedchar"
    else:
        model_name += "_handwritten"

    model = load_model(os.path.join(folder_path, model_name))
    
    special_chars = []
    actual_characters = []

    # separate input into (spaces, new lines) and actual characters
    for i, character in enumerate(characters):
        if isinstance(character, str):
            special_chars.append({'index': i, 'character': character})
        else:
            if use_cnn:
                actual_characters.append(character)
            else:
                actual_characters.append(character.reshape(784))

    # final output
    predictions = [0 for _ in characters]

    # add spaces and lines
    for special_char in special_chars:
        predictions[special_char['index']] = special_char['character']

    actual_characters = array(actual_characters)
    model_predictions = model.predict(actual_characters, verbose=0)
    most_probable_characters = []

    print("\nPredicting characters ...")
    index = 0
    for i in tqdm(range(len(predictions))):
        if predictions[i] == 0:
            most_prob_alpha, most_prob_num, alpha_prob, num_prob = get_most_probable_chars(model_predictions[index], mapping)
            predictions[i] = {'alpha': most_prob_alpha, 'alpha prob': alpha_prob, 'num': most_prob_num, 'num prob': num_prob}
            index += 1

            if alpha_prob > num_prob:
                most_probable_characters.append(most_prob_alpha)
            else:
                most_probable_characters.append(most_prob_num)

    if debug:
        print("Generating debug data ...")
        num = 0
        for actual_character in tqdm(actual_characters):
            plt.title(f"Prediction: {most_probable_characters[num]}")
            plt.imshow(transpose(actual_character))
            plt.savefig(os.path.join(folder_path, 'debug_outputs', f'character_{num}.png'))
            num += 1

    # format final output
    string = ""
    for prediction in predictions:
        if str(prediction) == ' ' or str(prediction) == '\n':
            string += prediction
        else:
            if prediction['alpha prob'] > prediction['num prob']:
                string += prediction['alpha']
            else:
                string += prediction['num']

    return string.lower(), predictions