from codoxer.transformers import CxxTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.exceptions import NotFittedError
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from codoxer.utils import dictionary_target, token_y, inverse_dict


class CodoxerModel(BaseEstimator):

    def __init__(self):
        self.tokenizer = CxxTokenizer()

        self.tfidf = TfidfVectorizer(ngram_range=(1, ngrams))

        self.selector = SelectPercentile(f_classif, percentile=reduce)

        self.estimator = models.Sequential()

        self.es = EarlyStopping(patience = 30, monitor = 'loss', restore_best_weights = True)


    def fit(self, X, y):

        # Tokenize
        X = self.tokenizer.fit(X, y)

        # Tfidf
        X = self.tfidf.fit_transform(X, y)

        # Select
        X = self.selector.fit_transform(X, y)

        # prepare target
        user_to_id = dictionary_target(y)
        self.id_to_user = inverse_dict(user_to_id)
        y_t = token_y(y, user_to_id)
        y_cat = to_categorical(y_t)
        self.classes = y_t_cat.shape[1]

        # Construct and compile CNN
        self.estimator.add(layers.Conv1D(filters=32, kernel_size=8, activation='relu'))
        self.estimator.add(layers.MaxPooling1D(pool_size=16))
        self.estimator.add(layers.Flatten())
        self.estimator.add(layers.Dense(256, activation='relu'))
        self.estimator.add(layers.Dropout(.3))
        self.estimator.add(layers.Dense(self.classes,   activation='softmax'))
        self.estimator.compile(loss=loss, optimizer=optim, metrics=metrics)

        # Fit CNN
        self.estimator.fit(X, y_cat, validation_split=.25, callbacks=[self.es], batch_size=16, epochs=50)


    def predict(self, X):
        preds = self.predict_proba(X)
        return self.user_to_id[preds.argmax()]

    def predict_proba(self, X):
        if self.user_to_id is None:
            raise NotFittedError('Model not fitted. Fit with CodoxerModel.fit(X, y).')

        X = self.tokenizer.transform(X)

        X = self.tfidf.transform(X)

        X = self.selector.transform(X)

        return self.estimator.predict(X)



