from matplotlib import pyplot as plt
from skimage import io
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from os import path

from recognize_characters import recognize_characters
from segment_characters import segment_characters
from segment_lines import segment_lines
from segment_words import segment_words


def cascade(image, debug=False):
    """ Takes a binarized image and cascades it into a string """
    characters = []

    lines = segment_lines(image, debug)
    for i, line in enumerate(lines):
        print(f"Segmenting line {i + 1} of {len(lines)}", end='\r')
        words = segment_words(line, debug)
        for word in words:
            characters.extend(segment_characters(word, debug))
            characters.append(' ')
        characters.append('\n')
    print("")

    predictions = recognize_characters(characters, debug)
    string = ("".join(predictions)).lower()
    print(string)


if __name__ == '__main__':
    folder_path = path.dirname(__file__)
    image = rgb2gray(io.imread(path.join(folder_path, 'inputs', 'quick_brown_fox_written.jpg')))
    threshold = threshold_otsu(image)
    image = image < threshold
    cascade(image, debug=True)