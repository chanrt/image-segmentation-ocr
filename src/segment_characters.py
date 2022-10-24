from matplotlib import pyplot as plt
from skimage import io
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from skimage.measure import label
from os import path


def get_bounding_rect(labelled_image, label):
    num_rows, num_cols = labelled_image.shape
    top_row, bottom_row, left_col, right_col = num_rows, 0, num_cols, 0

    for i in range(num_rows):
        for j in range(num_cols):
            if labelled_image[i, j] == label:
                if i < top_row:
                    top_row = i
                if i > bottom_row:
                    bottom_row = i
                if j < left_col:
                    left_col = j
                if j > right_col:
                    right_col = j

    return top_row, bottom_row, left_col, right_col


def segment_characters(image, debug=False):
    """ Takes a binarized image of a word and segments it into characters """
    labelled_image = label(image, background=0)

    num_features = labelled_image.max()
    segments = []

    for i in range(1, num_features + 1):
        segmented_region = (labelled_image == i)
        top_row, bottom_row, left_col, right_col = get_bounding_rect(labelled_image, i)
        segment = {
            'image': segmented_region[top_row:bottom_row + 1, left_col:right_col + 1],
            'x': left_col
        }
        segments.append(segment)

    segments = sorted(segments, key=lambda segment: segment['x'])
    segments = [segment['image'] for segment in segments]

    if debug:
        for i, segment in enumerate(segments):
            plt.subplot(1, len(segments), i + 1)
            plt.imshow(segment, cmap='gray')
        plt.axis('off')
        plt.show()

    return segments


if __name__ == '__main__':
    folder_path = path.dirname(__file__)
    image = rgb2gray(io.imread(path.join(folder_path, 'inputs', 'word_written.png')))
    threshold = threshold_otsu(image)
    image = image < threshold
    characterss = segment_characters(image)

    for i, characters in enumerate(characterss):
        plt.subplot(1, len(characterss), i + 1)
        plt.imshow(characters)
    plt.show()