from matplotlib import pyplot as plt
from tqdm import tqdm
import os

from segment_characters import segment_characters
from segment_lines import segment_lines
from segment_words import segment_words
from settings import settings


def image_segmenter(image, vertical_lines=False):
    """ Takes a processed binarized image and cascades it into an output string """
    characters = []

    print("\nSegmenting image ...")

    # divide image into lines
    lines = segment_lines(image, vertical_lines=vertical_lines)

    for line in tqdm(lines):
        # divide each line into words
        words = segment_words(line)

        for word in words:
            # divide each word into characters
            characters.extend(segment_characters(word))
            characters.append(' ')

        characters.append('\n')

    return characters