from matplotlib import pyplot as plt
from tqdm import tqdm
import os

from segment_characters import segment_characters
from segment_lines import segment_lines
from segment_words import segment_words


def image_segmenter(image, debug=False):
    """ Takes a processed binarized image and cascades it into an output string """
    characters = []

    if debug:
        folder_path = os.path.dirname(__file__)
        debug_folder_path = os.path.join(folder_path, 'debug_outputs')

        # check if debug folder exists
        if not os.path.exists(debug_folder_path):
            # create debug folder
            os.mkdir(debug_folder_path)
        else:
            # empty debug folder contents
            for file in os.listdir(debug_folder_path):
                os.remove(os.path.join(debug_folder_path, file))

    print("\nSegmenting image ...")

    # divide image into lines
    lines = segment_lines(image, debug)

    for line in tqdm(lines):
        # divide each line into words
        words = segment_words(line, debug)

        for word in words:
            # divide each word into characters
            characters.extend(segment_characters(word, debug))
            characters.append(' ')

        characters.append('\n')

    return characters