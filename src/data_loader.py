"""
This program requires handwritten_dataset.pkl and printedchar_dataset.pkl to be in the data folder.
You can download them from here:
1) handwritten_dataset.pkl (~550 MB): https://indianinstituteofscience-my.sharepoint.com/:u:/g/personal/chandanrt_iisc_ac_in/EaUa37ifvlpLlJv01iw9K1gB__t3h5qthJeodg4lF3RxGw?e=mPSpBf
2) printedchar_dataset.pkl (~200 MB): https://indianinstituteofscience-my.sharepoint.com/:u:/g/personal/chandanrt_iisc_ac_in/EfKPg_oMfXlAhHo_W_1bN8ABPs9_OUfbon0XSiGKf7BrVA?e=v2Vemt
"""


from numpy import array
from numpy.random import seed, shuffle
from pickle import load
import os


def load_handwritten_dataset():
    print("Loading handwritten dataset ...")
    data_folder_path = os.path.join(os.path.dirname(__file__), 'data')
    dataset = load(open(os.path.join(data_folder_path, 'handwritten_dataset.pkl'), 'rb'))

    data = array(dataset['data'])
    labels = array([dataset['labels']]).T
    mapping = load(open('data/mapping.pkl', 'rb'))

    print(data.shape)
    print(labels.shape)
    print(data[0])

    seed(42)
    shuffle(data)

    seed(42)
    shuffle(labels)

    return data, labels, mapping


def load_printedchar_dataset():
    print("Loading printedchar dataset ...")
    data_folder_path = os.path.join(os.path.dirname(__file__), 'data')
    dataset = load(open(os.path.join(data_folder_path, 'printedchar_dataset.pkl'), 'rb'))

    data = array(dataset['data'])
    labels = array([dataset['labels']]).T
    mapping = load(open('data/mapping.pkl', 'rb'))

    print(data.shape)
    print(labels.shape)
    print(data[0])

    seed(42)
    shuffle(data)

    seed(42)
    shuffle(labels)

    return data, labels, mapping


if __name__ == '__main__':
    load_handwritten_dataset()
    load_printedchar_dataset()