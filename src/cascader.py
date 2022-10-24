from recognize_character import recognize_characters
from segment_characters import segment_characters
from segment_lines import segment_lines
from segment_words import segment_words

from skimage import io
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from os import path


def cascade(image):
    """ Takes a binarized image and cascades it into a string """
    characters = []

    lines = segment_lines(image)
    for i, line in enumerate(lines):
        print(f"Segmenting line {i + 1} of {len(lines)}")
        words = segment_words(line)
        for word in words:
            characters.extend(segment_characters(word))
            characters.append(' ')
        characters.append('\n')

    print("Predicting ...")
    predictions = recognize_characters(characters)
    string = ("".join(predictions)).lower()
    print(string)


if __name__ == '__main__':
    folder_path = path.dirname(__file__)
    image = rgb2gray(io.imread(path.join(folder_path, 'inputs', 'para_written.png')))
    threshold = threshold_otsu(image)
    image = image < threshold
    cascade(image)