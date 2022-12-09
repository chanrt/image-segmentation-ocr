from character_preprocessing import character_preprocessor
from character_recognition import character_recognizer
from image_preprocessing import image_preprocessor
from image_segmentation import image_segmenter
from post_processing import post_processor


def main(image_name):
    print("Program started")

    # preprocess the image before segmenting it
    # skew_correction = True will try to correct the skew of the image
    # debug = True will show the result at intermediate steps
    processed_image = image_preprocessor(image_name, skew_correction=False, debug=True)

    # segment the image into lines, words and characters
    # debug = True will show all the intermediate segmentation steps
    raw_characters = image_segmenter(processed_image, debug=False)

    # process each character before inputting it to the neural network
    processed_characters = character_preprocessor(raw_characters)

    # recognize each character, and provide details of most probable alphabet and most probable number
    # if debug = False, then each character, along with it's prediction, will be saved in the debug_outputs folder
    recognized_characters, details = character_recognizer(processed_characters, debug=False)

    # run post processing on the recognized characters
    # number_correction = True will try to replace each number with the most probable character
    # english_correction = True will try to correct words that are not in the English dictionary
    final_output = post_processor(recognized_characters, details, number_correction=True, english_correction=True)

    print(f"\nFinal output:\n{final_output}")

    return final_output


if __name__ == '__main__':
    main('polya_description.jpg')