from matplotlib import pyplot as plt
from numpy import sum, zeros
from skimage.measure import label
from os import path

from settings import settings


def get_bounding_rows(vertical_histogram):
    num_rows = len(vertical_histogram)

    top_row = 0
    for i in range(num_rows):
        if vertical_histogram[i] != 0:
            top_row = i
            break

    bottom_row = num_rows - 1
    for i in range(num_rows - 1, -1, -1):
        if vertical_histogram[i] != 0:
            bottom_row = i
            break

    return top_row, bottom_row


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
    num_rows, _ = image.shape
    vertical_histogram = zeros(num_rows, dtype=int)

    for row in range(num_rows):
        vertical_histogram[row] = sum(image[row, :])

    top_line, bottom_line = get_bounding_rows(vertical_histogram)

    if top_line == bottom_line:
        return []

    labelled_image = label(image, background=0, connectivity=1)

    num_features = labelled_image.max()
    segments = []

    # isolate segments
    for i in range(1, num_features + 1):
        segmented_region = (labelled_image == i)

        # this is the bounding rect
        top_row, bottom_row, left_col, right_col = get_bounding_rect(labelled_image, i)
        width, height = right_col - left_col, bottom_row - top_row

        if height / abs(top_line - bottom_line) < settings.ignore_character_height_ratio:
            continue
        
        # check for tittle above the rect
        tittle_segment = image[top_line:top_row, left_col:right_col]
        if sum(tittle_segment) > settings.min_tittle_pixels:
            # extend top limit to include tittle
            top_limit = top_line
        else:
            # ignore
            top_limit = top_row
        bottom_limit = bottom_row

        segment = {
            'image': segmented_region[top_limit:bottom_limit + 1, left_col:right_col + 1],
            'x': left_col
        }
        segments.append(segment)

    # sort segments left to right
    segments = sorted(segments, key=lambda segment: segment['x'])

    # extract images
    segments = [segment['image'] for segment in segments]

    if debug:
        for i, segment in enumerate(segments):
            plt.subplot(1, len(segments), i + 1)
            plt.imshow(segment, cmap='gray')
        plt.axis('off')
        plt.show()

    return segments