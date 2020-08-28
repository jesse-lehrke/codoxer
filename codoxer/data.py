import pandas as pd
import random
import os
import gc
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
    verbose : int, optional, default = 0

    '''

    def __init__(self, file_path, **kwargs):

        # Get params from kwargs
        self.languages = kwargs.get('languages', ['cpp', 'java', 'python'])
        self.top_n = kwargs.get('top_n', 10)
        self.one_sample = kwargs.get('one_sample', True)
        self.years = kwargs.get('years', [2020])
        self.verbose = kwargs.get('verbose', 0)

        # Load data

        self.data_list = []

        if self.verbose == 1:
            print('// Loading Data...')

        if os.path.isdir(file_path):
            for file in os.listdir(file_path):
                if file.endswith('.csv'):
                    self.data_list.append(pd.read_csv(file_path + '/' +file))

        else:
            self.data = pd.read_csv(file_path)



    """
    def filter_user(self, username):
        ''' Filter by one username
        '''
        self = self.loc[self['username'] == username]
        return self
    """

    def clean_data(self):

        if self.verbose == 1:
            print('// CLEANING DATA...')

        # If path is a file only do for one file
        if len(self.data_list) == 0:

            # If no NaN in full path use full path column for extracting language
            if self.data['file'].str.endswith('.cpp').sum() == 0:
                self.data = self.data[['year','username', 'task', 'full_path', 'flines']]
                self.data[['drop','language']] = self.data.full_path.str.split('.', expand=True)
                self.data = self.data.drop(columns=['full_path', 'drop'])

            # Else use file columns for extracting language
            else:
                self.data = self.data[['year','username', 'task', 'file', 'flines']]
                self.data[['drop','language']] = self.data.file.str.split('.', expand=True)
                self.data = self.data.drop(columns=['file', 'drop'])

            self.data.loc[:, 'language'] = self.data.language.str.lower()

        # If path is directory do for each .csv file in path
        else:
            data_clean_list = []
            for df in self.data_list:
                if self.verbose == 1:
                    print('...')

                # If files dont have extensions use full path column for extracting language
                file_not_str = False
                try:
                    df['file'].str.endswith('.cpp')
                except:
                    file_not_str = True

                if file_not_str or df['file'].str.lower().str.endswith('.cpp').sum() == 0:
                    df = df[['year','username', 'task', 'full_path', 'flines']]
                    #print(df.year)
                    #print(df.full_path.str.split('.', expand=True))
                    df[['drop','language']] = df.full_path.str.split('.', expand=True)
                    df = df.drop(columns=['full_path', 'drop'])

                # Else use file columns for extracting language
                else:
                    #print(df.year.unique())
                    #print(df.file.str.split('.', expand=True))
                    df = df[['year','username', 'task', 'file', 'flines']]
                    df['language'] = df.file.apply(lambda x: x.split('.')[-1])
                    df = df.drop(columns='file')

                df.loc[:, 'language'] = df.language.str.lower()

                data_clean_list.append(df)

            self.data = pd.concat(data_clean_list)

        # Language remapping
        if self.verbose == 1:
            print('/ Language remapping in progress...')

        python = ['py', 'python3', 'python', 'pypy2', 'ipynb']
        cpp = ['cpp', 'cxx', 'cc', 'c++']

        self.data.language = [x if x not in python else 'python' for x in self.data.language]
        self.data.language = [x if x not in cpp else 'cpp' for x in self.data.language]

        self.data.dropna()
        self.data['task'] = self.data.task.astype('category')

        print('// Collecting Garbage...')
        gc.collect()
        print('Done.')



    def filter_top(self, n):
        '''Filter by a given n of the users with the most samples, e.g. top 10
            !!! also fairly slow
        '''
        if self.verbose == 1:
            print(f'// Filtering top {self.top_n}...')

        keeplist = self.data['username'].value_counts().index[:n].tolist()

        self.data = self.data[self.data['username'].isin(keeplist)]


    def filter_years(self, *year):
        '''Filter by given years
        '''
        if self.verbose == 1:
            print(f'// Filtering for years...')

        year_list = [item for item in year]
        self.data = self.data[self.data['year'].isin(year_list)]

        print('// Collecting Garbage...')
        gc.collect()
        print('Done.')


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

            # Verbose output
            if self.verbose == 1:
                print('// Choosing one sample per task...')


            # groupby
            #gb = self.data.groupby(['task', 'username'])
            #print('groupy done')

            # use last code for user for task -> slow
            #blocks = [data.sample(n=1) for _,data in gb]
            #blocks = [data.iloc[-1] for _,data in gb]
            #print('picking last code done')

            # Concat
            #self.data = pd.concat(blocks)
            #print('concat done')


            self.data = pd.concat([data.sample(n=1) for _,data in self.data.groupby(['task', 'username'])])

            print('// Collecting Garbage...')
            gc.collect()
            print('Done.')
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

    def filter_languages(self, language_list):
        '''Filter by given languages
        '''
        if self.verbose == 1:
            print('// Filtering language...')

        #language_list = [item for item in languages]
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

    def save_data(self, path):
        self.data.to_csv(path)

if __name__ == '__main__':
    import time
    t0= time.clock()
    df = DataBunch('data/gcj-dataset-master', verbose = 1)
    print(df.load_data())
    df.save_data('data/coder_data_prepped.csv')
    t1 = time.clock() - t0
    print("Time elapsed: ", t1) # CPU seconds elapsed (floating point)


