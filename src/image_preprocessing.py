from matplotlib import pyplot as plt
from multiprocessing import cpu_count, Pool
from numpy import arange, mean, pi, sum, var, zeros
from os import path
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.filters import threshold_local, threshold_otsu
from skimage.restoration import denoise_nl_means, estimate_sigma
from skimage.transform import rotate
from tqdm import tqdm

from settings import settings


def get_rotated_image_variance(data):
    image, angle = data
    rotated_image = rotate(image, angle)
    horizontal_profile = sum(rotated_image, axis=1)
    return var(horizontal_profile)


def image_preprocessor(image_name, skew_correction=False, debug=False):
    # load image
    folder_path = path.dirname(__file__)
    original_image = imread(path.join(folder_path, 'inputs', image_name))
    image = rgb2gray(original_image)
    num_rows, num_cols = image.shape

    if debug:
        plt.title("Grayscale image")
        plt.imshow(image, cmap='gray')
        plt.axis('off')
        plt.show()

    # thresholding
    threshold = threshold_local(image, settings.threshold_block_size, offset=settings.threshold_offset)
    # threshold = threshold_otsu(image)
    image = image < threshold

    if debug:
        plt.title("Thresholded image")
        plt.imshow(image, cmap='gray')
        plt.axis('off')
        plt.show()
    
    # noise removal
    # print("\nDenoising image ...")
    # sigma = mean(estimate_sigma(image, channel_axis=-1))
    # image = denoise_nl_means(original_image, h = 0.8 * sigma, fast_mode=True)

    # if debug:
    #     plt.title("Denoised image")
    #     plt.imshow(image, cmap='gray')
    #     plt.axis('off')
    #     plt.show()

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


if __name__ == '__main__':
    image_preprocessor('polya_description.jpg', skew_correction=False, debug=True)