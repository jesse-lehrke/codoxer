from time import time
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif
#from sklearn.naive_bayes import GaussianNB
#from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import numpy as np
#from sklearn import metrics

class Tfidf(object):

    def __init__ (self, df):
        self.X = df.tokens
        self.y = df.username
        self.vocabulary = None
        self.features_train = None

    def train_test_split(self, test_s=.3):
        '''train test split function
        test_s is test_size and set to default set to .3
        '''
        self.features_train, self.features_test, self.labels_train, self.labels_test = train_test_split(self.X,
                                                                            self.y,
                                                                            test_size=test_s,
                                                                            random_state=1)
        return self.features_train, self.features_test, self.labels_train, self.labels_test

    def get_vectorizer(self, ngrams=3, max_df=1., min_df=1):
        '''ngrams = enter integer what to range up to, default is 3 for trigrams
        max_df and min_df set to sklearn defaults 1. and 1 respectively
        '''
        self.vectorizer = TfidfVectorizer(ngram_range=(1, ngrams), max_df=max_df, min_df=min_df)

    def fit_transform_tfidf(self, reduce=10):
        '''fit and transforms train set, transforms test set.
        Also reduce the amount of features so text does not have too many features, default reduce = 10.
        '''
        if self.features_train is None:
            t0 = time()
            print('Running train_test_split first with default values')
            self.train_test_split()
            print(f"Complete... fitting and transforming: {round(time()-t0, 3)}s")
        else:
            t0 = time()
            self.features_train = self.vectorizer.fit_transform(self.features_train) #partial_fit
            self.features_test = self.vectorizer.transform(self.features_test)
            self.vocabulary = self.vectorizer.get_feature_names()
            print(f"Fit and transform complete time: {round(time()-t0, 3)}s")

        selector = SelectPercentile(f_classif, percentile=reduce)
        selector.fit(self.features_train, self.labels_train)

        self.features_train = selector.transform(self.features_train).toarray()
        self.features_test = selector.transform(self.features_test).toarray()
