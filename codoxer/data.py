import pandas as pd
import random
import os
class DataBunch(object):

    ''' Loads and filters data based on filter arguments

    Parameters
    ----------
    file_path : string, mandatory
        Path to data file
    languages : list, optional, default = None
        Default is ['cpp, java, python']
        Programming languages to be considered.
    top_n : int, optional, default = None
        Default is 10
        Must be between 2 and number of coders in sample
        i.e data['username'].nunqiue()
    one_sample : boolean, optional, default = None
        Default is True.
        If True only one sample per round per user will be considered. This helps
        to make sure there is no duplicate of very similar code by a coder that
        might end up being split between training and test data leading to data
        leakage.
    years : list, optional, default = None
        List of years to be considered. Years not in dataset will be ignored.
        If None is specified all years present in dataset will be used.

    '''

    def __init__(self, file_path, **kwargs):

        self.data_list = []
        # Load data
        if os.path.isdir(file_path):
            for file in os.listdir(file_path):
                if file.endswith('.csv'):
                    data_list.append(pd.read_csv(file))

        else:
            self.data = pd.read_csv(file_path)

        # Get params from kwargs
        self.languages = kwargs.get('languages', ['cpp', 'java', 'python'])
        self.top_n = kwargs.get('top_n', 10)
        self.one_sample = kwargs.get('one_sample', True)
        self.years = kwargs.get('years', [2020])


    """
    def filter_user(self, username):
        ''' Filter by one username
        '''
        self = self.loc[self['username'] == username]
        return self
    """

    def clean_data(self):


        # If path is a file only do for one file
        if len(self.data_list) == 0:

            # If no NaN in full path use full path column for extracting language
            if self.data['full_path'].isna().sum() != len(list(self.data['full_path'])):
                self.data = self.data[['year','username', 'task', 'full_path', 'flines']]
                self.data[['drop','language']] = self.data.full_path.str.split('.', expand=True)
                self.data = self.data.drop(columns=['full_path', 'drop'])

            # Else use file columns for extracting language
            else:
                self.data = self.data[['year','username', 'task', 'file', 'flines']]
                print(self.data.file.str.split('.', expand=True))
                self.data[['drop','language']] = self.data.file.str.split('.', expand=True)
                self.data = self.data.drop(columns=['file', 'drop'])

            self.data.loc[:, 'language'] = self.data.language.str.lower()

        # If path is directory do for each .csv file in path
        else:
            data_clean_list = []
            for df in data_list:

                # If no NaN in full path use full path column for extracting language
                if self.data['full_path'].isna().sum() != 0:
                    self.data = self.data[['year','username', 'task', 'full_path', 'flines']]
                    self.data[['drop','language']] = self.data.full_path.str.split('.', expand=True)
                    self.data = self.data.drop(columns=['full_path', 'drop'])

                # Else use file columns for extracting language
                else:
                    self.data = self.data[['year','username', 'task', 'file', 'flines']]
                    self.data[['drop','language']] = self.data.file.str.split('.', expand=True)
                    self.data = self.data.drop(columns=['file', 'drop'])
                df.loc[:, 'language'] = df.language.str.lower()

            self.data = pd.concat(data_clean_list)

            # Language remapping
        python = ['py', 'python3', 'python', 'pypy2', 'ipynb']
        cpp = ['cpp', 'cxx', 'cc', 'c++']

        self.data.language = [x if x not in python else 'python' for x in self.data.language]
        self.data.language = [x if x not in cpp else 'cpp' for x in self.data.language]




    def filter_top(self, n):
        '''Filter by a given n of the users with the most samples, e.g. top 10
        '''
        keeplist = self.data['username'].value_counts().index[:n].tolist()
        self.data = self.data[self['username'].isin(keeplist)]

    def filter_years(self, *year):
        '''Filter by given years
        '''
        year_list = [item for item in year]
        self.data = self.data[self.data['year'].isin(year_list)]


    """
    def filter_n_greater_than(self, n):
        '''Filters and return only users with more samples than the given n
        '''
        self = self[self['username'].map(self['username'].value_counts()) > n]
        return self
    """

    """
    def select_random_users(self, n, minimum=100):
        '''Selects a random n number of users provided the have a minimum=number of samples
        '''
        #user_list = df1['username'].unique().tolist()
        self = self[self['username'].map(self['username'].value_counts()) > minimum]
        sampled_list = random.sample(self.username_list, n)
        self = self[self['username'].isin(sampled_list)]
        return self
    """


    def make_oneone_sample(self):
        '''Returns dataframe with 1 code sample per user per task.
        Warning: Long runtime posssible!
        '''
        if self.one_sample:
            gb = self.data.groupby(['task', 'username'])
            blocks = [data.sample(n=1) for _,data in gb]
            #blocks = [data.iloc[-1] for _,data in gb]
            self.data = pd.concat(blocks)


    """
    def truncate(self, min_samples):
        '''Undersamples classes with more the the given min_samples
        '''
        self = self[self['username'].map(self['username'].value_counts()) > min_samples]
        gb = self.groupby(['username'])
        blocks = [data.sample(n=min_samples) for _,data in gb]
        self = pd.concat(blocks)
        return self
    """

    def filter_languages(self, *languages):
        '''Filter by given languages
        '''
        print(self.data.columns)
        language_list = [item for item in languages]
        self.data = self.data[self.data['language'].isin(language_list)]


    def filter_data(self):
        #self.filter_years(self.years)
        self.filter_languages(self.languages)
        self.make_oneone_sample()
        self.filter_top(self.top_n)

    def load_data(self):
        self.clean_data()
        self.filter_data()
        return self.data

if __name__ == '__main__':
    df = DataBunch('data/gcj-dataset-master/gcj2020.csv')
    df.load_data()

