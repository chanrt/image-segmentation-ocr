from matplotlib import pyplot as plt
from numpy import zeros

from settings import settings


def segment_lines(image, vertical_lines=False):
    """ Takes a binarized image containing a paragraph and segments it into lines  """
    num_rows, num_cols = image.shape
    horizontal_histogram = zeros(num_rows, dtype=int)

    for row in range(num_rows):
        horizontal_histogram[row] = sum(image[row, :])

    max_pixels = max(horizontal_histogram)
    minimas_considered = []
    
    if not vertical_lines:
        # naive method (line start swhen a row has atleast one pixel)
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
                minimas_considered.append(index)
                line_start, line_end = -1, -1

        if line_start != -1:
            lines.append(image[line_start:line_end + 1, :])
    else:
        # improved method (line starts at the centre of contiguous line spaces)

        # get empty line location according to threshold
        empty_line_locations = zeros(num_rows, dtype=bool)
        for row in range(num_rows):
            ratio = horizontal_histogram[row] / max_pixels
            if ratio < settings.line_segmentation_threshold:
                empty_line_locations[row] = True
            else:
                empty_line_locations[row] = False

        # find contiguous empty line spaces
        contiguous_empty_line_locations = []
        consider_row = 0
        while consider_row < num_rows:
            if empty_line_locations[consider_row]:
                # start of line spacing
                start_row, end_row = consider_row, consider_row

                for next_row in range(start_row + 1, num_rows):
                    if not empty_line_locations[next_row]:
                        # end of line spacing
                        break
                    else:
                        # line spacing continues
                        end_row = next_row

                if end_row - start_row > settings.line_segmentation_min_height:
                    # valid line spacing
                    contiguous_empty_line_locations.append((start_row, end_row))

                # skip to end of line spacing
                consider_row = end_row + 1
            else:
                # skip to next row
                consider_row += 1

        # locate line separation indices
        line_separation_indices = []
        for start_row, end_row in contiguous_empty_line_locations:
            line_separation_index = (start_row + end_row) // 2
            line_separation_indices.append(line_separation_index)

        # separate lines
        lines = []
        line_start = 0
        for line_separation_index in line_separation_indices:
            lines.append(image[line_start:line_separation_index + 1, :])
            minimas_considered.append(line_separation_index)
            line_start = line_separation_index + 1

    if settings.debug_line_segmenter:
        for i, line in enumerate(lines):
            plt.subplot(len(lines), 1, i + 1)
            plt.imshow(line, cmap='gray')
        plt.axis('off')
        plt.show()

        plt.plot(horizontal_histogram)
        for minima in minimas_considered:
            plt.plot([minima, minima], [0, max_pixels], 'r')
        plt.show()

    return lines