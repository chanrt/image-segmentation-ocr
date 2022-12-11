from matplotlib import pyplot as plt
from numpy import c_, r_, zeros
from skimage.morphology import dilation, skeletonize
from skimage.transform import resize
from tqdm import tqdm

from settings import settings


def pad_character(character, padding):
    padding_row = zeros((padding, character.shape[1]))
    character = r_[padding_row, character, padding_row]
    
    padding_column = zeros((character.shape[0], padding))
    character = c_[padding_column, character, padding_column]

    return character


def character_preprocessor(characters, debug=True):
    """ Takes binarized images containing single characters and processes them for input to neural network """

    processed_characters = []
    print("\nProcessing characters ...")

    for character in tqdm(characters):
        if str(character) == ' ' or str(character) == '\n':
            processed_characters.append(character)
        else:
            original_character = character.copy()
            num_rows, num_cols = character.shape

            # make sure image is square
            if num_rows > num_cols:
                # add extra columns
                num_either_side = (num_rows - num_cols) // 2
                padding_column = zeros((num_rows, 1))

                for _ in range(num_either_side):
                    character = c_[padding_column, character]

                for _ in range(num_either_side):
                    character = c_[character, padding_column]
            else:
                # add extra rows
                num_either_side = (num_cols - num_rows) // 2
                padding_row = zeros((1, num_cols))

                for _ in range(num_either_side):
                    character = r_[padding_row, character]

                for _ in range(num_either_side):
                    character = r_[character, padding_row]

            # add padding to square image
            standard_padding = settings.padding
            required_size = 28 - 2 * standard_padding
            character = resize(character, (required_size, required_size))
            character = pad_character(character, standard_padding)

            if settings.dilate:
                character = dilation(character)
            if settings.skeletonize:
                character = skeletonize(character)
            
            processed_characters.append(character)

            if settings.debug_character_preprocessor:
                plt.figure(figsize=(10, 5))
                plt.subplot(1, 2, 1)
                plt.title("Original character")
                plt.imshow(original_character, cmap='gray')
                plt.axis('off')

                plt.subplot(1, 2, 2)
                plt.title("Processed character")
                plt.imshow(character, cmap='gray')
                plt.axis('off')

                plt.show()

    return processed_characters