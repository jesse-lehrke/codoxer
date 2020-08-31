import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class LanguagePicker(BaseEstimator, TransformerMixin):

    def __init__(self, language_list):
        self.language_list = language_list

    def fit(self, X, y = None):
        return self

    def transform(self, X, y = None):
        return X[['language'].isin(language_list)]


class TopNPicker(BaseEstimator, TransformerMixin):

    def __init__(self, top_n):
        self.top_n = top_n

    def fit(self, X, y = None):
        return self

    def transform(self, X, y = None):
        if y not is None:
            keeplist = y['username'].value_counts().index[:n].tolist()
            self = self[self['username'].isin(keeplist)]
            return self

