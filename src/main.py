from character_preprocessing import character_preprocessor
from character_recognition import character_recognizer
from image_preprocessing import image_preprocessor
from image_segmentation import image_segmenter
from post_processing import post_processor


def main(image_name):
    print("Program started")

    # preprocess the image before segmenting it
    # skew_correction = True will try to correct the skew of the image
    # denoising = True will denoise the image using non-local means (time consuming)
    processed_image = image_preprocessor(image_name, skew_correction=False, denoising=False, horizontal_lines=False)

    # segment the image into lines, words and characters
    raw_characters = image_segmenter(processed_image, vertical_lines=True)

    # process each character before inputting it to the neural network
    processed_characters = character_preprocessor(raw_characters)

    # recognize each character, and provide details of most probable alphabet and most probable number
    # use_cnn = True will use the CNN model, otherwise the ANN model will be used
    # printed_chars = True will use the model trained on printed characters, otherwise the model trained on handwritten characters will be used
    recognized_characters, details = character_recognizer(processed_characters, use_cnn=True, printed_chars=True)

    # run post processing on the recognized characters
    # number_correction = True will try to replace each number with the most probable character, in places where a number is not likely
    # english_correction = True will try to correct words that are not in the English dictionary
    final_output = post_processor(recognized_characters, details, number_correction=True, english_correction=False)

    print(f"\nFinal output:\n{final_output}")

    return final_output


if __name__ == '__main__':
    main('lorem_ipsum.png')