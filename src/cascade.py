from matplotlib import pyplot as plt
from tqdm import tqdm
import os

from recognize_characters import recognize_characters
from segment_characters import segment_characters
from segment_lines import segment_lines
from segment_words import segment_words


def cascader(image, debug_segmentation=False, debug_recognition=False):
    """ Takes a skew-corrected, binarized image and cascades it into a string """
    characters = []

    if debug_segmentation or debug_recognition:
        folder_path = os.path.dirname(__file__)
        debug_folder_path = os.path.join(folder_path, 'debug_outputs')
        for file in os.listdir(debug_folder_path):
            os.remove(os.path.join(debug_folder_path, file))

    print("Segmenting image ...")
    lines = segment_lines(image, debug_segmentation)
    for line in tqdm(lines):
        words = segment_words(line, debug_segmentation)
        for word in words:
            characters.extend(segment_characters(word, debug_segmentation))
            characters.append(' ')
        characters.append('\n')

    predictions = recognize_characters(characters, debug_recognition)

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