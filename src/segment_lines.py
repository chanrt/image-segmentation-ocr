from matplotlib import pyplot as plt
from numpy import zeros

from skimage import io
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from os import path


def segment_lines(image):
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
                line_start = index
            line_end = index
        elif line_start != -1:
            lines.append(image[line_start:line_end + 1, :])
            line_start, line_end = -1, -1

    if line_start != -1:
        lines.append(image[line_start:line_end + 1, :])

    return lines


if __name__ == '__main__':
    folder_path = path.dirname(__file__)
    image = rgb2gray(io.imread(path.join(folder_path, 'image.png')))
    threshold = threshold_otsu(image)
    image = image < threshold
    lines = segment_lines(image)

    for i, line in enumerate(lines):
        plt.subplot(1, len(lines), i + 1)
        plt.imshow(line)
    plt.show()