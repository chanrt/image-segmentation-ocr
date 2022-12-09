import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow import keras
from keras.models import load_model


if __name__ == '__main__':
    """ Loads the model and prints its summary """
    
    folder_path = os.path.dirname(__file__)
    model_path = os.path.join(folder_path, 'model')
    model = load_model(model_path)
    model.summary()

    # Model: "sequential"
    # _________________________________________________________________
    # Layer (type)                Output Shape              Param #   
    # =================================================================
    # conv2d (Conv2D)             (None, 26, 26, 64)        640       

    # max_pooling2d (MaxPooling2D  (None, 13, 13, 64)       0
    # )

    # conv2d_1 (Conv2D)           (None, 11, 11, 32)        18464     

    # max_pooling2d_1 (MaxPooling  (None, 5, 5, 32)         0
    # 2D)

    # flatten (Flatten)           (None, 800)               0

    # dense (Dense)               (None, 128)               102528

    # dense_1 (Dense)             (None, 62)                7998

    # =================================================================
    # Total params: 129,630
    # Trainable params: 129,630
    # Non-trainable params: 0
    # _________________________________________________________________