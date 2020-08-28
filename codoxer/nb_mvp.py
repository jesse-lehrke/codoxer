#!/usr/bin/env python
# coding: utf-8

from time import time
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif
#from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import numpy as np
from sklearn import metrics


class NB(object):

    def __init__ (self, df):
        self.X = df.tokens
        self.y = df.username
        self.vocabulary = None

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

    def fit_transform_tfidf(self):
        '''fit and transforms train set, transforms test set
        '''
        self.features_train = self.vectorizer.fit_transform(self.features_train) #partial_fit
        self.features_test = self.vectorizer.transform(self.features_test)
        self.vocabulary = self.vectorizer.get_feature_names()

    def reduce(self):
        '''Reduce the amount of features so text does not have too many features
        '''
        selector = SelectPercentile(f_classif, percentile=10)
        selector.fit(self.features_train, self.labels_train)

        self.features_train = selector.transform(self.features_train).toarray()
        self.features_test = selector.transform(self.features_test).toarray()

    def initialize_fit_nb(self, alpha=0):
        ''' Initializes and fits NB model.
        Alpha default is zero and can range up to 1 as a float
        '''
        t0 = time()
        self.model = MultinomialNB(alpha)
        self.model.fit(self.features_train, self.labels_train)

        print(f"\nTraining time: {round(time()-t0, 3)}s")

    def score_train_test(self):
        '''Score
        '''
        t0 = time()
        score_train = self.model.score(self.features_train, self.labels_train)
        print(f"Prediction time (train): {round(time()-t0, 3)}s")

        t0 = time()
        score_test = self.model.score(self.features_test, self.labels_test)
        print(f"Prediction time (test): {round(time()-t0, 3)}s")

        print("\nTrain set score:", score_train)
        print("Test set score:", score_test)

    def get_reports(self):
        '''prints a classification report with precision, recall, f1, support
        and macro averages plus accuracy
        '''

        y_pred = self.model.predict(self.features_test)

        # compute the performance measures
        score1 = metrics.accuracy_score(self.labels_test, y_pred)
        print("accuracy:   %0.3f" % score1)

        print(metrics.classification_report(self.labels_test, y_pred))

        print("confusion matrix:")
        print(metrics.confusion_matrix(self.labels_test, y_pred))

        print('------------------------------')

    def get_top_features(self, number):
        '''Extract top features. WARNING: large RAM requirements
        '''
        feature_array = np.array(self.vectorizer.get_feature_names())
        tfidf_sorting = np.argsort(self.features_train).flatten()[::-1]

        n = number
        top_n = feature_array[tfidf_sorting][:n]
        print(top_n)




