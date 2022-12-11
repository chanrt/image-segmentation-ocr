from tqdm import tqdm

from segment_characters import segment_characters
from segment_lines import segment_lines
from segment_words import segment_words


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

            # add space after every word
            characters.append(' ')

        # add newline after every line
        characters.append('\n')

    # the characters returned here, are connected components of alphanumeric characters isolated from the image (2D numpy arrays
    # however, newlines and spaces are also incorporated into the list, in the form of strings
    # the downstream functions will be able to handle this
    return characters