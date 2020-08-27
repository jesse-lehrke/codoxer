import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class LanguagePicker(BaseEstimator, TransformerMixin):

    def __init__(self, language_list):
        self.language_list = language_list

    def fit(self, X, y = None):
        return self

    def transform(self, X, y = None):
        return X[['language'].isin(language_list)]
