from matplotlib import pyplot as plt
from numpy import zeros
from os import path


def segment_lines(image, debug=False):
    """ Takes a binarized image containing a paragraph and segments it into lines  """
    num_rows, _ = image.shape
    horizontal_histogram = zeros(num_rows, dtype=int)

    for row in range(num_rows):
        horizontal_histogram[row] = sum(image[row, :])

    lines = []
    line_start, line_end = -1, -1

    index = 0
    for index in range(num_rows):
        if horizontal_histogram[index] > 0:
            if line_start == -1:
                # new line started
                line_start = index
            # line continues
            line_end = index
        elif line_start != -1:
            # line ended
            lines.append(image[line_start:line_end + 1, :])
            line_start, line_end = -1, -1

    # add last line
    if line_start != -1:
        lines.append(image[line_start:line_end + 1, :])

    if debug:
        for i, line in enumerate(lines):
            plt.subplot(len(lines), 1, i + 1)
            plt.imshow(line, cmap='gray')
        plt.axis('off')
        plt.show()

    return lines