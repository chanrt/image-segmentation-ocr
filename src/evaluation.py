from Levenshtein import distance
import os

from main import main


def evaluator(image_name):
    folder_path = os.path.dirname(__file__)
    program_output = main(image_name).replace('\n', '')

    file_name = image_name.split('.')[0] + '.txt'
    
    expected_output_file = os.path.join(folder_path, 'expected_outputs', file_name)
    expected_output = open(expected_output_file, 'r').read().replace('\n', ' ')

    print(f"\nProgram output:\n{program_output}")
    print(f"\nExpected output:\n{expected_output}")

    # program has a tendency to add a space at the end of every line
    # hence replace every newline with nothing will suffice
    program_output = program_output.replace('\n', '')

    # the Levenshtein distance is a metric for string similarity
    # it is based on the lowest number of single-character edits required to transform one string into the other
    levenshtein_distance = distance(program_output, expected_output)
    error = levenshtein_distance * 100 / len(expected_output)

    print(f"\nLevenshtein distance: {levenshtein_distance}")
    print(f"Error: {error:.2f} %")


if __name__ == '__main__':
    evaluator('para_text_rotated.png')