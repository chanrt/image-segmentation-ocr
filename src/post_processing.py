from tqdm import tqdm


def check_word(i, string):
    length = len(string)
    start, end = -1, -1

    for j in range(i, length):
        if string[j] == ' ' or string[j] == '\n':
            end = j - 1
            break

    for j in range(i, -1, -1):
        if string[j] == ' ' or string[j] == '\n':
            start = j + 1
            break

    word = string[start:end + 1]

    num_letters = 0
    num_numbers = 0

    for char in word:
        if char.isalpha():
            num_letters += 1
        elif char.isdigit():
            num_numbers += 1

    return num_letters, num_numbers


def post_processing(string):
    """ Accepts a string and corrects common mistakes """
    new_string = ""
    length = len(string)

    print("Post processing ...")
    for i in tqdm(range(length)):
        if string[i].isdigit():
            num_letters, num_numbers = check_word(i, string)
            if num_letters > 1:
                if string[i] == '0':
                    new_string += 'o'
                elif string[i] == '1':
                    new_string += 'l'
                elif string[i] == '2':
                    new_string += 'z'
                elif string[i] == '5':
                    new_string += 's'
                elif string[i] == '6':
                    new_string += 'b'
                elif string[i] == '8':
                    new_string += 'g'
                elif string[i] == '9':
                    new_string += 'g'
                else:
                    new_string += string[i]
            else:
                new_string += string[i]
        else:
            new_string += string[i]

    return new_string