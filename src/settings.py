

class Settings:
    def __init__(self):
        # debug modes
        self.debug_preprocessor = False
        self.debug_line_segmenter = False
        self.debug_word_segmenter = False
        self.debug_character_segmenter = False
        self.debug_character_preprocessor = False
        self.debug_character_recognizor = False
        self.debug_post_processor = False

        # adaptive thresholding parameters
        self.threshold_block_size = 51
        self.threshold_offset = 0.1

        # the range (-theta, theta) across which skew correction is performed (in degrees)
        self.skew_correction_range = 90

        # the fine-angle tuning used for skew correction (in degrees)
        self.skew_correction_step = 1

        # the minimum ratio of pixels in a row (with respect to total number of pixels) for it to be considered a horizontal line
        self.horizontal_line_threshold = 0.4

        # rows around each horizontal line to be remove
        self.line_surround_remove = 2

        # the minimum ratio of pixels in a row (with respect to the maximum) for it to be considered the starting of a line of text
        self.line_segmentation_threshold = 0.1

        # minimum spacing between two lines (in pixels)
        self.line_segmentation_min_height = 5

        # the ratio of height (wrt line height) of a character if it is to be ignored
        # this is useful for ignoring commas and periods
        self.ignore_character_height_ratio = 0.4

        # the minimum number of pixels a feature above a short connected component must have
        # to be considered a tittle
        self.min_tittle_pixels = 5

        # if connectivtiy is 1, then only the 4 Von Neumann neighbours are considered as 'neighbours' of a pixel
        # if connectivity is 2, then all 7 adjacent pixels are considered as 'neighbours'
        # for eroded images, keep connectivity = 2 to prevent the connected components from being broken
        self.connectivity = 2

        # the amount of padding (in pixels) inserted around the square image of each character
        # before image is passed to neural network for recongition
        self.padding = 4

        # skeletonization of character processed image, beofre it is passed to neural network
        # required only if the writing is very thick, or thickness is uneven
        self.skeletonize = False

        # dilation of character processed image, before it is passed to neural network
        # required only if the writing is very thin and the characters have been eroded
        self.dilate = True

        # in a word with both letters and numbers
        # the ratio of num_numbers / num_total below which number correction will be applied
        self.max_number_ratio = 0.5

        # minimum length of word for which autocorrected can be applied
        self.min_word_length_autocorrect = 3

        # maximum ratio of erraneous characters to total characters in a word for which autocorrect can be applied
        self.max_error_ratio = 0.8

        # maximum number of prospective words to be returned by autocorrect
        self.max_autocorrected_words = 4


settings = Settings()