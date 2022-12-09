

class Settings:
    def __init__(self):
        # the range (-theta, theta) across which skew correction is performed (in degrees)
        self.skew_correction_range = 90

        # the fine-angle tuning used for skew correction (in degrees)
        self.skew_correction_step = 1

        # the ratio of height (wrt line height) of a character if it is to be ignored
        # this is useful for ignoring commas and periods
        self.ignore_character_height_ratio = 0.4

        # the minimum number of pixels a feature above a short connected component must have
        # to be considered a tittle
        self.min_tittle_pixels = 5

        # the amount of padding (in pixels) inserted around the square image of each character
        # before image is passed to neural network for recongition
        self.padding = 4

        # skeletonization of character processed image, beofre it is passed to neural network
        # required only if the writing is very thick
        self.skeletonize = True

        # dilation of character processed image, before it is passed to neural network
        # required only if the writing is very thin and the characters have been eroded
        self.dilate = False

        # minimum length of word for which autocorrected can be applied
        self.min_word_length_autocorrect = 4

        # maximum ratio of erraneous characters to total characters in a word for which autocorrect can be applied
        self.max_error_ratio = 0.8

        # maximum number of prospective words to be returned by autocorrect
        self.max_autocorrected_words = 4


settings = Settings()