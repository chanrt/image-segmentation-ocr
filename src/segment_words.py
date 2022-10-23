from kmeans1d import cluster
from matplotlib import pyplot as plt
from numpy import zeros

from skimage import io
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from os import path


def get_first(histogram):
    for i in range(len(histogram)):
        if histogram[i] != 0:
            return i
    return -1


def get_last(histogram):
    for i in range(len(histogram) - 1, -1, -1):
        if histogram[i] != 0:
            return i
    return -1


def get_space_around(histogram, i):
    space = 0
    for j in range(i, len(histogram)):
        if histogram[j] == 0:
            space += 1
        else:
            return space


def segment_words(image):
    """ Takes a binarized image of a line and segments it into words """
    num_rows, num_cols = image.shape
    vertical_histogram = zeros(num_cols, dtype=int)

    for col in range(num_cols):
        vertical_histogram[col] = sum(image[:, col])

    plt.plot(vertical_histogram)
    plt.show()

    spaces = []
    in_space = False
    current_space_length = 0
    start, end = get_first(vertical_histogram), get_last(vertical_histogram)

    for i in range(start, end):
        if vertical_histogram[i] == 0:
            if not in_space:
                in_space = True
                current_space_length = 1
            else:
                current_space_length += 1
        elif in_space:
            in_space = False
            spaces.append(current_space_length)

    clusters, centroids = cluster(spaces, 2)

    words = []
    word_start, word_end = -1, -1
    
    index = start
    while index < end:
        if vertical_histogram[index] > 0:
            if word_start == -1:
                word_start = index
                word_end = index
            else:
                word_end = index
        else:
            spacing = get_space_around(vertical_histogram, index)
            if abs(spacing - centroids[0]) > abs(spacing - centroids[1]):
                if word_start != -1:
                    words.append(image[:, word_start:word_end + 1])
                    word_start, word_end = -1, -1
            index += spacing

        index += 1

    if word_start != -1:
        words.append(image[:, word_start:end + 1])

    return words


if __name__ == '__main__':
    folder_path = path.dirname(__file__)
    image = rgb2gray(io.imread(path.join(folder_path, 'image.png')))
    threshold = threshold_otsu(image)
    image = image < threshold
    words = segment_words(image)

    for i, word in enumerate(words):
        plt.subplot(1, len(words), i + 1)
        plt.imshow(word)
    plt.show()