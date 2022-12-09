from character_preprocessing import character_preprocessor
from character_recognition import character_recognizer
from image_preprocessing import image_preprocessor
from image_segmentation import image_segmenter
from post_processing import post_processor


if __name__ == "__main__":
    print("Program started")

    processed_image = image_preprocessor('para_text.png')
    raw_characters = image_segmenter(processed_image, debug=False)
    processed_characters = character_preprocessor(raw_characters)
    recognized_characters, details = character_recognizer(processed_characters, debug=False)
    final_output = post_processor(recognized_characters, details)

    print(f"\nFinal output:\n{final_output}")