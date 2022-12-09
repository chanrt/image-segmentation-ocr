from os import path
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu


def pre_processor(image_name):
    folder_path = path.dirname(__file__)
    image = rgb2gray(imread(path.join(folder_path, 'inputs', image_name)))
    threshold = threshold_otsu(image)
    image = image < threshold
    
    return image