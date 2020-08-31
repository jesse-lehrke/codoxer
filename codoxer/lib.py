# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Jean Bizot <jean@styckr.io>
""" Main lib for codoxer Project
"""

from os.path import split
import pandas as pd
import datetime

pd.set_option('display.width', 200)

import pandas as pd
import random
​
class DataFilter(pd.DataFrame):
​
    ''' Class for filtering data in mulitple manners. Inherits from pandas dataframe.
​
    Attributes:
        user_dict = dictionary of username and count of code samples for that user
        username_list = simple list of usernames
        user_file_count = list of username and count of code samples for that user
​
    '''
​
    @property
    def _constructor(self):
        #self.df = df
        #self.df = DataFilter(*args, **kw)
        return DataFilter
​
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_dict = dict(self['username'].value_counts())
        self.username_list = self['username'].unique().tolist()
        self.user_file_count = self['username'].value_counts()
​
    def filter_user(self, username):
        ''' Filter by one username
        '''
        self = self.loc[self['username'] == username]
        return self
​
    def filter_top(self, n):
        '''Filter by a given n of the users with the most samples, e.g. top 10
        '''
        keeplist = self['username'].value_counts().index[:n].tolist()
        self = self[self['username'].isin(keeplist)]
        return self
​
    def filter_language(self, language):
        '''Filter by programming language: cpp, python, java
        '''
        self = self.loc[self['language'] == language]
        return self
​
    def filter_year(self, *year):
        '''Filter by a single given year
        '''
        year_list = [item for item in year]
        self = self[self['year'].isin(year_list)]
        #self = self.loc[self['year'] == year]
        return self
​
    def filter_n_greater_than(self, n):
        '''Filters and return only users with more samples than the given n
        '''
        self = self[self['username'].map(self['username'].value_counts()) > n]
        return self
​
    def select_random_users(self, n, minimum=100):
        '''Selects a random n number of users provided the have a minimum=number of samples
        '''
        #user_list = df1['username'].unique().tolist()
        self = self[self['username'].map(self['username'].value_counts()) > minimum]
        sampled_list = random.sample(self.username_list, n)
        self = self[self['username'].isin(sampled_list)]
        return self
​
    def make_oneone_sample(self):
        '''Returns dataframe with 1 code sample per user per task.
        Warning: Long runtime posssible!
        '''
        gb = self.groupby(['task', 'username'])
        blocks = [data.sample(n=1) for _,data in gb]
        self = pd.concat(blocks)
        return self


def clean_data(data):
    """ clean data
    """
    # Remove columns starts with vote
    cols = [x for x in data.columns if x.find('vote') >= 0]
    data.drop(cols, axis=1, inplace=True)
    # Remove special characteres from columns
    data.loc[:, 'civility'] = data['civility'].replace('\.', '', regex=True)
    # Calculate Age from day of birth
    actual_year = datetime.datetime.now().year
    data.loc[:, 'Year_Month'] = pd.to_datetime(data.birthdate)
    data.loc[:, 'Age'] = actual_year - data['Year_Month'].dt.year
    # Uppercase variable to avoid duplicates
    data.loc[:, 'city'] = data['city'].str.upper()
    # Take 2 first digits, 2700 -> 02700 so first two are region
    data.loc[:, 'postal_code'] = data.postal_code.str.zfill(5).str[0:2]
    # Remove columns with more than 50% of nans
    cnans = data.shape[0] / 2
    data = data.dropna(thresh=cnans, axis=1)
    # Remove rows with more than 50% of nans
    rnans = data.shape[1] / 2
    data = data.dropna(thresh=rnans, axis=0)
    # Discretize based on quantiles
    data.loc[:, 'duration'] = pd.qcut(data['surveyduration'], 10)
    # Discretize based on values
    data.loc[:, 'Age'] = pd.cut(data['Age'], 10)
    # Rename columns
    data.rename(columns={'q1': 'Frequency'}, inplace=True)
    # Transform type of columns
    data.loc[:, 'Frequency'] = data['Frequency'].astype(int)
    # Rename values in rows
    drows = {1: 'Manytimes', 2: 'Onetimebyday', 3: '5/6timesforweek',
             4: '4timesforweek', 5: '1/3timesforweek', 6: '1timeformonth',
             7: '1/trimestre', 8: 'Less', 9: 'Never'}
    data.loc[:, 'Frequency'] = data['Frequency'].map(drows)
    return data


if __name__ == '__main__':
    # For introspections purpose to quickly get this functions on ipython
    #import codoxer
    #folder_source, _ = split(codoxer.__file__)
    #df = pd.read_csv('{}/data/data.csv.gz'.format(folder_source))
    #clean_data = clean_data(df)
    #print(' dataframe cleaned')
