

class Settings:
    def __init__(self):
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
        self.skeletonize = False


settings = Settings()