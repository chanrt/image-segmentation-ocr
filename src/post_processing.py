from os import path


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
        # if letter == '0':
        #     corrected_word += 'o'
        # elif letter == '1':
        #     corrected_word += 'l'
        # elif letter == '2':
        #     corrected_word += 'z'
        # elif letter == '5':
        #     corrected_word += 's'
        # elif letter == '6':
        #     corrected_word += 'b'
        # elif letter == '9':
        #     corrected_word += 'g'
        # else:
        #     corrected_word += letter

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

    if length < 5 and min_error < 2:
        return prospective_words
    elif length < 8 and min_error < 3:
        return prospective_words
    elif length < 10 and min_error < 4:
        return prospective_words
    else:
        return word


def apply_extra_correction(word, english_words):
    length = len(word)
    prospective_words = []

    for i in range(length):
        prospective_word = word[:i] + word[i + 1:]
        if prospective_word in english_words:
            prospective_words.append(prospective_word)

    return prospective_words


def post_processing(string, predictions, number_correction=True, english_correction=False):
    """ Accepts a string and corrects common mistakes """
    folder_path = path.dirname(__file__)
    english_words = open(path.join(folder_path, 'data', 'english_words.txt'), 'r').read().split('\n')

    length = len(string)

    words = []
    word = ""

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

    index = 0
    for word in words:
        if word == ' ' or word == '\n':
            corrected_words.append(word)
            index += 1
        else:
            num_letters, num_numbers = get_stats(word)

            if number_correction and (num_numbers > 0 and num_letters > 0):
                corrected_word = apply_number_correction(word, predictions[index: index + len(word)])
            else:
                corrected_word = word[:]
            
            if english_correction:
                if corrected_word in english_words:
                    corrected_words.append(corrected_word)
                else:
                    corrections = apply_spelling_correction(corrected_word, english_words)
                    corrected_words.append("/".join(corrections))
            else:
                corrected_words.append(corrected_word)

            index += len(word)

    corrected_words = "".join(corrected_words)

    return corrected_words