from recognize_character import recognize_characters
from segment_characters import segment_characters
from segment_words import segment_words

from skimage import io
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from os import path


if __name__ == '__main__':
    """ Use this to run generic tasks """
    folder_path = path.dirname(__file__)
    image = rgb2gray(io.imread(path.join(folder_path, 'image.png')))
    threshold = threshold_otsu(image)
    image = image < threshold

    words = segment_words(image)
    for word in words:
        characters = segment_characters(word)
        print(recognize_characters(characters))