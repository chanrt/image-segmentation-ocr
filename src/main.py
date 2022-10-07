from matplotlib import pyplot as plt
from numpy import sum, transpose
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from skimage.measure import label
from skimage.morphology import binary_dilation
import cv2
import pygame as pg


def main():
    # initialize opencv to capture webcam output
    capture = cv2.VideoCapture()
    capture.open(0, cv2.CAP_DSHOW)
    _, frame = capture.read()
    num_rows, num_cols, num_channels = frame.shape

    # initialize pygame
    pg.init()
    screen = pg.display.set_mode((num_cols, num_rows))
    pg.display.set_caption("Webcam")
    clock = pg.time.Clock()

    # initialize parameters
    width_percent = 0.7
    height_percent = 0.35

    # calculated parameters
    width = int(num_cols * width_percent)
    height = int(num_rows * height_percent)
    size = width * height
    x = int((num_cols - width) / 2)
    y = int((num_rows - height) / 2)

    # bools
    show_graphs = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_g:
                    show_graphs = not show_graphs
                if event.key == pg.K_w and height_percent < 1:
                    height_percent += 0.05
                    height = int(num_rows * height_percent)
                    size = width * height
                    y = int((num_rows - height) / 2)
                if event.key == pg.K_s and height_percent > 0.05:
                    height_percent -= 0.05
                    height = int(num_rows * height_percent)
                    size = width * height
                    y = int((num_rows - height) / 2)
                if event.key == pg.K_d and width_percent < 1:
                    width_percent += 0.05
                    width = int(num_cols * width_percent)
                    size = width * height
                    x = int((num_cols - width) / 2)

        _, bgr_image = capture.read()
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

        cropped_image = rgb_image[y:y + height, x:x + width]
        grayscale_image = rgb2gray(cropped_image)
        binary_image = binary_dilation(grayscale_image > threshold_otsu(grayscale_image))

        if show_graphs:
            plt.imshow(binary_image, cmap='gray')
            plt.show()

        num_true = sum(binary_image)
        background_value = 1 if num_true > size / 2 else 0
        labeled_image = label(binary_image, background=background_value)
        superimposed_surface = pg.surfarray.make_surface(transpose(labeled_image))

        if show_graphs:
            plt.imshow(labeled_image)
            plt.show()
            show_graphs = False

        pg.surfarray.blit_array(screen, transpose(rgb_image, (1, 0, 2)))
        screen.blit(superimposed_surface, (x, y))

        pg.draw.rect(screen, (255, 0, 0), (x, y, width, height), 2)
        pg.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()