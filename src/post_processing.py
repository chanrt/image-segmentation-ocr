from os import path
from tqdm import tqdm

from settings import settings


def get_stats(word):
    num_letters, num_numbers = 0, 0

    for letter in word:
        if letter.isalpha():
            num_letters += 1
        elif letter.isdigit():
            num_numbers += 1

    return num_letters, num_numbers


def apply_number_correction(word, predictions):
    corrected_word = ""
                
    for i, letter in enumerate(word):
        if letter.isdigit():
            corrected_word += predictions[i]['alpha']
        else:
            corrected_word += letter

    return corrected_word


def apply_spelling_correction(word, english_words):
    length = len(word)
    min_error = 100
    prospective_words = []

    for english_word in english_words:
        if len(english_word) == length:
            error = 0
            for letter1, letter2 in zip(word, english_word):
                if letter1 != letter2:
                    error += 1
            
            if error < min_error:
                prospective_words = [english_word]
                min_error = error
            elif error == min_error:
                prospective_words.append(english_word)

    if min_error / length < settings.max_error_ratio and len(prospective_words) <= settings.max_autocorrected_words:
        return prospective_words
    else:
        return word


def post_processor(string, predictions, number_correction=True, english_correction=False, debug=False):
    """ Accepts a string and corrects common mistakes """
    folder_path = path.dirname(__file__)
    english_words = open(path.join(folder_path, 'data', 'english_words.txt'), 'r').read().split('\n')

    length = len(string)

    words = []
    word = ""

    if debug:
        print("\nText received for post-processing:")
        print(string)

    # break string into words
    for i in range(length):
        if string[i] != ' ' and string[i] != '\n':
            if word == "":
                word = string[i]
            else:
                word += string[i]
        else:
            words.append(word)
            words.append(string[i])
            word = ""

    corrected_words = []

    print("\nCarrying out post processing ...")
    index = 0
    for word in tqdm(words):
        if word == ' ' or word == '\n':
            corrected_words.append(word)
            index += 1
        else:
            num_letters, num_numbers = get_stats(word)

            if number_correction and (num_numbers > 0 and num_letters > 0):
                corrected_word = apply_number_correction(word, predictions[index: index + len(word)])
            else:
                corrected_word = word[:]
            
            if english_correction and len(word) >= settings.min_word_length_autocorrect:
                if corrected_word in english_words:
                    corrected_words.append(corrected_word)
                else:
                    corrections = apply_spelling_correction(corrected_word, english_words)

                    if corrections == corrected_word:
                        corrected_words.append(corrected_word)
                    else:
                        corrected_words.append("/".join(corrections))
            else:
                corrected_words.append(corrected_word)

            index += len(word)

    string = "".join(corrected_words)

    if debug:
        print("\nText after post-processing:")
        print(string)

    return string.lower()