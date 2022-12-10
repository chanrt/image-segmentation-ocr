"""
This program requires handwritten_dataset.pkl and printedchar_dataset.pkl to be in the data folder.
You can download them from here:
1) handwritten_dataset.pkl (~550 MB): https://indianinstituteofscience-my.sharepoint.com/:u:/g/personal/chandanrt_iisc_ac_in/EaUa37ifvlpLlJv01iw9K1gB__t3h5qthJeodg4lF3RxGw?e=mPSpBf
2) printedchar_dataset.pkl (~200 MB): https://indianinstituteofscience-my.sharepoint.com/:u:/g/personal/chandanrt_iisc_ac_in/EfKPg_oMfXlAhHo_W_1bN8ABPs9_OUfbon0XSiGKf7BrVA?e=v2Vemt
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow import keras
from keras.layers import Dense, InputLayer, Conv2D, MaxPooling2D, Flatten
from keras.losses import SparseCategoricalCrossentropy
from keras.models import Sequential
from keras.optimizers import Adam

from data_loader import load_handwritten_dataset, load_printedchar_dataset


if __name__ == '__main__':
    data, labels, mapping = load_handwritten_dataset()

    data = data.reshape(-1, 28, 28, 1)

    length_data = len(data)
    train_data = data[:int(length_data * 0.8)] / 255.0
    train_labels = labels[:int(length_data * 0.8)]

    test_data = data[int(length_data * 0.8):] / 255.0
    test_labels = labels[int(length_data * 0.8):]

    print("Separated data set")

    model = Sequential([
        Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(28, 28, 1)),
        Conv2D(64, (3, 3), padding='same', activation='relu'),
        Conv2D(128, (3, 3), padding='same', activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(100, activation='relu'),
        Dense(62, activation='softmax')
    ])

    model.summary()
    model.compile(loss=SparseCategoricalCrossentropy(), optimizer=Adam(learning_rate=0.003), jit_compile=True, metrics=['accuracy'])
    model.fit(train_data, train_labels, epochs=5, batch_size=256, shuffle=True)

    model.save('cnn_model_handwritten')

    print("Evaluation on test set:")
    print(model.evaluate(test_data, test_labels))