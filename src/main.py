from cascade import cascader
from pre_processing import pre_processor
from post_processing import post_processor


if __name__ == "__main__":
    print("Program started")

    processed_image = pre_processor('para_text.png')
    raw_output, predictions = cascader(processed_image, debug_segmentation=False, debug_recognition=False)
    final_output = post_processor(raw_output, predictions)

    print(final_output)