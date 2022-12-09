from os import path
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu


def image_preprocessor(image_name):
    # load image
    folder_path = path.dirname(__file__)
    image = rgb2gray(imread(path.join(folder_path, 'inputs', image_name)))

    # thresholding
    threshold = threshold_otsu(image)
    image = image < threshold
    
    return image