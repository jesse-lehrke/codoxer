import pandas as pd
import random

class DataFilter(pd.DataFrame):

    ''' Class for filtering data in mulitple manners. Inherits from pandas dataframe.

    Attributes:
        user_dict = dictionary of username and count of code samples for that user
        username_list = simple list of usernames
        user_file_count = list of username and count of code samples for that user

    '''

    @property
    def _constructor(self):
        #self.df = df
        #self.df = DataFilter(*args, **kw)
        return DataFilter

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_dict = dict(self['username'].value_counts())
        self.username_list = self['username'].unique().tolist()
        self.user_file_count = self['username'].value_counts()

    def filter_user(self, username):
        ''' Filter by one username
        '''
        self = self.loc[self['username'] == username]
        return self

    def filter_top(self, n):
        '''Filter by a given n of the users with the most samples, e.g. top 10
        '''
        keeplist = self['username'].value_counts().index[:n].tolist()
        self = self[self['username'].isin(keeplist)]
        return self

    def filter_language(self, language):
        '''Filter by programming language: cpp, python, java
        '''
        self = self.loc[self['language'] == language]
        return self

    def filter_years(self, *years):
        '''Filter by given years, comma seperated
        '''
        year_list = [item for item in years]
        self = self[self['year'].isin(year_list)]
        #self = self.loc[self['year'] == year]
        return self

    def filter_n_greater_than(self, n):
        '''Filters and return only users with more samples than the given n
        '''
        self = self[self['username'].map(self['username'].value_counts()) > n]
        return self

    def select_random_users(self, n, minimum=100):
        '''Selects a random n number of users provided the have a minimum=number of samples
        '''
        #user_list = df1['username'].unique().tolist()
        self = self[self['username'].map(self['username'].value_counts()) > minimum]
        sampled_list = random.sample(self.username_list, n)
        self = self[self['username'].isin(sampled_list)]
        return self

    def make_oneone_sample(self):
        '''Returns dataframe with 1 code sample per user per task.
        Warning: Long runtime posssible!
        '''
        gb = self.groupby(['task', 'username'])
        blocks = [data.sample(n=1) for _,data in gb]
        self = pd.concat(blocks)
        return self
