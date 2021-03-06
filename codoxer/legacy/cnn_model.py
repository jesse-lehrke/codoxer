import pandas as pd
import numpy as np

from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping

from codoxer.utils import dictionary_target, token_y, inverse_dict


'''def dictionary_target(y):
    user_to_id = {'unseen_word': 0}
    i = 1
    for item in y:
        if item not in user_to_id:
            user_to_id[item] = i
            i+=1
    return user_to_id


def inverse_dict(dictonary):
    inv_dict = {v: k for k, v in dictonary.items()}
    return inv_dict


def token_y(y, dictionary):
    token = []
    for item in y:
        if item in dictionary:
            token.append(dictionary[item])
    return token'''


class CNN_model(object):

    def __init__(self, data):
        '''data is an instance of Tfidf Class
        methods of NB to be called before instantiate CNN_model:
        train_test_split -> split data
        get_vectorizer -> initialize tfidf
        fit_transform_Tfidf -> Tfidf on X
        reduce -> transform X into numpy array'''
        self.data = data
        self.X_train = data.features_train
        self.X_test = data.features_test
        self.y_train = data.labels_train
        self.y_test = data.labels_test
        self.input_shape = None
        self.classes = None
        self.model = None
        self.activation = ['relu', 'relu', 'softmax']
        self.es = EarlyStopping(patience = 30, monitor = 'loss', restore_best_weights = True)
        self.id_to_user = None


    def y_prep(self):
        index = len(self.y_train)
        y = pd.concat([self.y_train, self.y_test])
        user_to_id = dictionary_target(y)
        self.id_to_user = inverse_dict(user_to_id)
        y_t = token_y(y, user_to_id)
        y_cat = to_categorical(y_t)
        y_train_cat = y_cat[:index]
        y_test_cat = y_cat[index:]
        self.classes = y_train_cat.shape[1]
        self.y_train = y_train_cat
        self.y_test = y_test_cat

    def bin_y_prep(self):
        keys = self.y_train.unique()
        vals = [0, 1]
        bin_dict = dict(zip(keys, vals))
        self.classes = 2
        self.y_train = np.array(self.y_train.map(lambda x: bin_dict[x]))
        self.y_test = np.array(self.y_test.map(lambda x: bin_dict[x]))

    def X_prep(self):
        length = self.X_train.shape[0]
        width = self.X_train.shape[1]
        self.X_train = self.X_train.reshape(length, width, 1)
        self.X_test = self.X_test.reshape(self.X_test.shape[0], self.X_test.shape[1], 1)
        self.input_shape = self.X_train.shape

    def bin_X_prep(self):
        self.input_shape = self.X_train.shape

    def define_activations(self, *activations):
        ''' Define activation layers in the order of the layer for your model
        '''
        self.activation = [item for item in activations]
        if len(self.activation) != 3:
            print('Please enter 3 activations')
            pass
        return self.activation

    def early_stopping(self, patience=30, monitor='loss', restore_best_weights=True):
        ''' Defaults are patience=30, monitor='loss', restore_best_weights=True
        '''
        self.es = EarlyStopping(patience = patience, monitor = monitor, restore_best_weights = restore_best_weights)


    def init_model(self, loss='categorical_crossentropy', optim='adam', metrics=['accuracy']):
        '''initializes the model'''

        self.y_prep()
        self.X_prep()

        model = models.Sequential()

        model.add(layers.Conv1D(filters=32, kernel_size=8, activation=self.activation[0]))
        model.add(layers.MaxPooling1D(pool_size=16))
        model.add(layers.Flatten())
        model.add(layers.Dense(256, activation=self.activation[1]))
        model.add(layers.Dropout(.3))

        #model.add(layers.Conv1D(filters=8, kernel_size=8, activation=self.activation[0]))
        #model.add(layers.MaxPooling1D(pool_size=16))

        #model.add(layers.Flatten())

        model.add(layers.Dense(self.classes, activation=self.activation[2]))
        model.compile(loss=loss, optimizer=optim, metrics=metrics)

        self.model = model
        return model


    def init_bin_conv_model(self, loss='binary_crossentropy', optim='adam', metrics=['accuracy']):
        '''initializes the model'''

        self.bin_y_prep()
        self.X_prep()

        model = models.Sequential()

        model.add(layers.Conv1D(filters=32, kernel_size=8, activation=self.activation[0]))
        model.add(layers.MaxPooling1D(pool_size=16))
        model.add(layers.Flatten())
        model.add(layers.Dense(256, activation=self.activation[1]))
        model.add(layers.Dropout(.3))

        #model.add(layers.Conv1D(filters=8, kernel_size=8, activation=self.activation[0]))
        #model.add(layers.MaxPooling1D(pool_size=16))

        #model.add(layers.Flatten())

        model.add(layers.Dense(1, activation='sigmoid'))
        model.compile(loss=loss, optimizer=optim, metrics=metrics)

        self.model = model
        return model


    def init_bin_model(self, loss='binary_crossentropy', optim='adam', metrics=['accuracy']):
        '''initializes the model'''

        self.bin_y_prep()
        self.bin_X_prep()

        if self.classes != 2:
            print('binary classification only performs if there are 2 classes')

        model = models.Sequential()

        model.add(layers.Dense(256, input_dim=self.input_shape[1], activation='relu'))
        model.add(layers.Dropout(.4))
        model.add(layers.Dropout(0.3))
        model.add(layers.Dense(200, activation='relu'))
        model.add(layers.Dropout(0.3))
        model.add(layers.Dense(160, activation='relu'))
        model.add(layers.Dropout(0.3))
        model.add(layers.Dense(120, activation='relu'))
        model.add(layers.Dropout(0.3))
        model.add(layers.Dense(80, activation='relu'))
        model.add(layers.Dropout(0.3))

        model.add(layers.Dense(1, activation='sigmoid'))
        model.compile(loss=loss, optimizer=optim, metrics=metrics)

        self.model = model
        return model


    def init_rnn_model(self, loss='categorical_crossentropy', optim='rmsprop', metrics=['accuracy']):
        '''initializes the model'''

        self.y_prep()
        self.X_prep()

        model = models.Sequential()

        model.add(layers.SimpleRNN(units=16, activation='tanh'))

        model.add(layers.Dense(self.classes, activation=self.activation[2]))
        model.compile(loss=loss, optimizer=optim, metrics=metrics)

        self.model = model
        return model


    def init_lstm_model(self, loss='categorical_crossentropy', optim='rmsprop', metrics=['accuracy']):
        '''initializes the model'''

        self.y_prep()
        self.X_prep()

        model = models.Sequential()

        model.add(layers.LSTM(units=16, activation='tanh'))

        model.add(layers.Dense(self.classes, activation=self.activation[2]))
        model.compile(loss=loss, optimizer=optim, metrics=metrics)

        self.model = model
        return model


    def init_gru_model(self, loss='categorical_crossentropy', optim='rmsprop', metrics=['accuracy']):
        '''initializes the model'''

        self.y_prep()
        self.X_prep()

        model = models.Sequential()

        model.add(layers.GRU(units=16, activation='tanh'))

        model.add(layers.Dense(self.classes, activation=self.activation[2]))
        model.compile(loss=loss, optimizer=optim, metrics=metrics)

        self.model = model
        return model


    def model_summary(self):
        '''prints the model summary'''

        if self.model == None:
            print('model needs to be trained')
        else:
            self.model.build(input_shape=self.input_shape)
            print(self.model.summary())


    def model_fit(self, validation_split=.2, epochs=50, batch_size=16):
        '''fits the model'''
        if self.model == None:
            print('model needs to be trained')
        else:

            history = self.model.fit(self.X_train, self.y_train, validation_split=validation_split, callbacks=[self.es], batch_size=batch_size, epochs=epochs)
            return history


    def evaluate_model(self):

        self.model.evaluate(self.X_test, self.y_test)
        return result
