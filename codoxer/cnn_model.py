from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping

from codoxer.embedding_prep import dictionary_target, token_y


'''def dictionary_target(y):
    user_to_id = {'unseen_word': 0}
    i = 1
    for item in y:
        if item not in user_to_id:
            user_to_id[item] = i
            i+=1
    return user_to_id


def token_y(y, dictionary):
    token = []
    for item in y:
        if item in dictionary:
            token.append(dictionary[item])
    return token'''


class CNN_model(object):

    def __init__(self, data):
        '''data is an instance of NB Class
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


    def y_prep(self):
        y = pd.concat([self.y_train, self.y_test])
        user_to_id = dictionary_target(y)
        y_t = token_y(y, user_to_id)
        y_cat = to_categorical(y_t)
        y_train_cat = y_cat[:9240]
        y_test_cat = y_cat[9240:]
        self.classes = y_train_cat.shape[1]
        self.y_train = y_train_cat
        self.y_test = y_test_cat

    def X_prep(self):
        length = self.X_train.shape[0]
        width = self.X_train.shape[1]
        self.X_train = self.X_train.reshape(length, width, 1)
        self.X_test = self.X_test.reshape(self.X_test.shape[0], self.X_test.shape[1], 1)
        self.input_shape = self.X_train.shape


    def init_model(self):
        '''initializes the model'''

        self.y_prep()
        self.X_prep()

        model = models.Sequential()

        model.add(layers.Conv1D(filters=8, kernel_size=8, activation='relu'))
        model.add(layers.MaxPooling1D(pool_size=16))

        model.add(layers.Flatten())

        model.add(layers.Dense(self.classes, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        self.model = model


    def model_summary(self):
        '''prints the model summary'''

        if self.model == None:
            print('model needs to be trained')
        else:
            self.model.build(input_shape=self.input_shape)
            print(self.model.summary())


    def model_fit(self):
        '''fits the model'''
        if self.model == None:
            print('model needs to be trained')
        else:
            es = EarlyStopping(patience=5, restore_best_weights=True)

            history = self.model.fit(self.X_train, self.y_train, validation_split=0.3, callbacks=[es], batch_size=16, epochs=50)
            return history


    def evaluate_model(self):

        self.model.evaluate(self.X_test, self.y_test)
