import tensorflow as tf
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Sequential
# from keras.optimizers import gradient_descent_v2
from tensorflow.keras.optimizers import SGD
from keras.callbacks import Callback
import numpy as np


def get_model():
    generate_model = Sequential()

    # create the dense input layer
    generate_model.add(Dense(15, input_shape=(4,), input_dim=4))
    generate_model.add(Activation('sigmoid'))

    # create second layer (first hidden layer)
    generate_model.add(Dense(16))
    generate_model.add(Activation('sigmoid'))

    # create third and last layer
    generate_model.add(Dense(4))
    generate_model.add(Activation('softmax'))
    sgd = SGD(lr=0.01, decay=0.0, momentum=0.0, nesterov=False)
    # Use mean squared error loss and SGD as optimizer
    generate_model.compile(loss='mse', optimizer=sgd)
    generate_model.summary()
    return generate_model


# model = get_model()

