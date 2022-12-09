from matplotlib import pyplot as plt
from multiprocessing import cpu_count, Pool
from numpy import arange, pi, sum, var, zeros
from os import path
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from skimage.transform import rotate
from tqdm import tqdm

from settings import settings


def get_rotated_image_variance(data):
    image, angle = data
    rotated_image = rotate(image, angle)
    horizontal_profile = sum(rotated_image, axis=1)
    return var(horizontal_profile)


def image_preprocessor(image_name, skew_correction=False):
    # load image
    folder_path = path.dirname(__file__)
    image = rgb2gray(imread(path.join(folder_path, 'inputs', image_name)))
    num_rows, num_cols = image.shape

    # thresholding
    threshold = threshold_otsu(image)
    image = image < threshold

    # skew correction
    if skew_correction:
        skew_range = settings.skew_correction_range
        angles = arange(-skew_range, +skew_range, settings.skew_correction_step)

        data = [(image, angle) for angle in angles]
        pool = Pool(cpu_count() - 1)

        print("Performing skew correction (will take a few seconds to initialize multiprocessing) ...")
        variances = list(tqdm(pool.imap(get_rotated_image_variance, data), total=len(data)))

        best_angle = angles[variances.index(max(variances))]
        image = rotate(image, best_angle, mode='constant', cval=0)
    
    return image