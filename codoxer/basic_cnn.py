from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras import callbacks
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier

class TfidfCNN(object):

    def __init__(self, data):
        self.inputd = data.features_train.shape[1]
        self.target_len = data.labels_train.nunique()
        self.model = None
        self.features_train = data.features_train
        self.features_test = data.features_test
        self.labels_train = data.labels_train
        self.labels_test = data.labels_test
        self.activation_list = ['tanh', 'tanh', 'relu', 'relu', 'tanh', 'softmax']
        self.es = callbacks.EarlyStopping(patience = 30, monitor = 'loss', restore_best_weights = True)

    def early_stopping(self, patience=30, monitor='loss', restore_best_weights=True):
        ''' Defaults are patience=30, monitor='loss', restore_best_weights=True
        '''
        self.es = callbacks.EarlyStopping(patience = patience, monitor = monitor, restore_best_weights = restore_best_weights)

    def define_activations(self, *activations):
        ''' Define 6 activation layers in the order of the layer for your model
        '''
        self.activation_list = [item for item in activations]
        if len(self.activation_list) != 6:
            print('Please enter 6 activations')
            pass
        return self.activation_list


    def build_fit_model(self, optim='RMSprop', validation_split=.2, epochs=20, batch_size=64):
        ''' Defaults: optim='adam', validation_split=.2, epochs=20, batch_size=64
        '''
        def build_model(optim=optim):

            model = Sequential()
            model.add(Dense(256, input_dim=self.inputd, activation=self.activation_list[0]))
            model.add(layers.Dropout(.4))
            model.add(Dropout(0.3))
            model.add(Dense(200, activation=self.activation_list[1]))
            model.add(Dropout(0.3))
            model.add(Dense(160, activation=self.activation_list[2]))
            model.add(Dropout(0.3))
            model.add(Dense(120, activation=self.activation_list[3]))
            model.add(Dropout(0.3))
            model.add(Dense(80, activation=self.activation_list[4]))
            model.add(Dropout(0.3))
            model.add(Dense(self.target_len, activation=self.activation_list[5]))
            model.compile(loss='categorical_crossentropy', optimizer=optim, metrics=['accuracy'])
            model.summary()

            return model

        self.estimator = KerasClassifier(build_fn=build_model, validation_split= validation_split,epochs=epochs, batch_size=batch_size, callbacks=[self.es])
        self.estimator.fit(self.features_train, self.labels_train)

    def score_train(self):
        '''Scores the train set
        '''
        return self.estimator.score(self.features_test, self.labels_test)
