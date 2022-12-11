from matplotlib import pyplot as plt
from multiprocessing import cpu_count, Pool
from numpy import arange, mean, pi, sum, var, zeros
from os import path
from skimage.io import imread
from skimage.color import rgb2gray, rgba2rgb
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


def image_preprocessor(image_name, skew_correction=False, denoising=False):
    # load image
    folder_path = path.dirname(__file__)
    original_image = imread(path.join(folder_path, 'inputs', image_name))
    num_rows, num_cols, num_channels = original_image.shape

    if num_channels == 4:
        original_image = rgba2rgb(original_image)
    image = rgb2gray(original_image)

    if settings.debug_preprocessor:
        plt.title("Grayscale image")
        plt.imshow(image, cmap='gray')
        plt.axis('off')
        plt.show()

    # thresholding
    otsu_threshold = threshold_otsu(image)
    image_otsu_1 = image > otsu_threshold
    image_otsu_2 = image < otsu_threshold

    if sum(image_otsu_1) > sum(image_otsu_2):
        threshold = threshold_local(image, settings.threshold_block_size, offset=settings.threshold_offset)
        image = image < threshold
    else:
        print("Dark image detected. Inverting image and recalculating local thresholds ...")
        image = 1 - image
        threshold = threshold_local(image, settings.threshold_block_size, offset=settings.threshold_offset)
        image = image < threshold

    if settings.debug_preprocessor:
        plt.title("Thresholded image")
        plt.imshow(image, cmap='gray')
        plt.axis('off')
        plt.show()
    
    if denoising:
        print("\nDenoising image ...")
        sigma = mean(estimate_sigma(image, channel_axis=-1))
        image = denoise_nl_means(original_image, h = 0.8 * sigma, fast_mode=True)

        if settings.debug_preprocessor:
            plt.title("Denoised image")
            plt.imshow(image, cmap='gray')
            plt.axis('off')
            plt.show()

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

        if settings.debug_preprocessor:
            plt.title("Skew corrected image")
            plt.imshow(image, cmap='gray')
            plt.axis('off')
            plt.show()
    
    return image


if __name__ == '__main__':
    image_preprocessor('polya_description.jpg', skew_correction=False, debug=True)