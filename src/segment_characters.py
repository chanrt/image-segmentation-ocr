from matplotlib import pyplot as plt
from skimage.measure import label


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


def segment_characters(image):
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

    return segments