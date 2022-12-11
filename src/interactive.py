from numpy import array, transpose
from pickle import load
from skimage.morphology import dilation

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow import keras
from keras.models import load_model
import pygame as pg


def get_character(label, mapping):
    for item in mapping:
        if item[0] == label:
            return chr(item[1])


def interactive():
    """ Allows the user to draw a character on a canvas and have it recognized by the neural network """
    use_cnn = True
    handwritten = True

    model_name = ""
    if use_cnn:
        model_name += "cnn_model"
    else:
        model_name += "ann_model"

    if not handwritten:
        model_name += "_printedchar"
    else:
        model_name += "_handwritten"

    print("Loading model ...")

    folder_path = os.path.dirname(__file__)
    model = load_model(os.path.join(folder_path, model_name))
    mapping = load(open(os.path.join(folder_path, 'data', 'mapping.pkl'), 'rb'))

    pg.init()
    screen = pg.display.set_mode((800, 600))
    cell_length = 600 // 28
    grid = [[0 for _ in range(28)] for _ in range(28)]
    big_font = pg.font.SysFont('Arial', 50)
    small_font = pg.font.SysFont('Arial', 20)

    mouse_down = False
    text = None

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == pg.MOUSEBUTTONUP:
                mouse_down = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    return
                if event.key == pg.K_c:
                    grid = [[0 for _ in range(28)] for _ in range(28)]
                    text = None

        if mouse_down:
            mouse_x, mouse_y = pg.mouse.get_pos()
            x = mouse_x // cell_length
            y = mouse_y // cell_length

            if 0 <= x < 28 and 0 <= y < 28:
                grid[y][x] = 1

            if use_cnn:
                nn_input = dilation(array(grid)).reshape(-1, 28, 28, 1)
            else:
                nn_input = dilation(array(grid)).reshape(-1, 784)
            prediction = model.predict(nn_input, verbose=0)
            character = get_character(prediction.argmax(), mapping)
            text = big_font.render(character, True, (255, 255, 255)) 

        screen.fill((0, 0, 0))

        for i in range(28):
            for j in range(28):
                pg.draw.rect(screen, (255, 255, 255), (i * cell_length, j * cell_length, cell_length, cell_length), 1)

                if grid[j][i] == 1:
                    pg.draw.rect(screen, (255, 255, 255), (i * cell_length, j * cell_length, cell_length, cell_length))

        if text is not None:
            screen.blit(text, (680, 250))

        clear_instruction = small_font.render("Press C to clear", True, (255, 255, 255))
        screen.blit(clear_instruction, (640, 400))

        pg.display.flip()


if __name__ == '__main__':
    interactive()