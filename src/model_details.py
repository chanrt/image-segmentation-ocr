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