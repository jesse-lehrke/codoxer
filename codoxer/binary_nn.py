import numpy as np
import pandas as pd

from codoxer.utils import n_samples #couples,
from codoxer.filter import DataFilter
from codoxer.tfidf import Tfidf
from codoxer.cnn_model import CNN_model

class BinaryNN():

    def __init__(self, df):
        self.dffilter = DataFilter(df)
        self.model_df = None

    def n_users(self, n):
        top_n = self.dffilter.filter_top(n)
        return top_n

    def couples(self, lst):
        if type(lst) == np.ndarray:
            lst = lst.tolist()
        couples = []
        iters = len(lst)
        for j in range(iters):
            i = 0
            user1 = lst.pop(i)
            for item in lst:
                couples.append((user1, item))
        return couples

    def n_samples(self, df):
        users = df['username'].unique()
        samples = {}
        for user in users:
            samples[user] = df[df.username==user].shape[0]
        return samples

    def fit(self, n, model='model', couples=None, epochs=30, name='binary_nn_df'):
        df = self.n_users(n)
        users = df['username'].unique()
        couples_list = self.couples(users)
        samples = self.n_samples(df)

        if couples==None:
            couples = (0, len(couples_list))

        cols = ['user1', 'user2', 'sample1', 'sample2', 'accuracy_train', 'accuracy_val', 'accuracy_test']
        binary_stats_df = pd.DataFrame(columns=cols)

        for item in couples_list[couples[0]:couples[1]]:
            row = {'user1': item[0], 'user2': item[1], 'sample1': samples[item[0]], 'sample2': samples[item[1]]}
            test_df = df.loc[df.username.isin(item)]
            print('tfidf')
            tfidf = Tfidf(test_df)
            tfidf.train_test_split()
            tfidf.get_vectorizer()
            tfidf.fit_transform_tfidf()
            print('model')
            cnn = CNN_model(tfidf)
            if model=='model':
                cnn.init_bin_model()
            elif model=='cnn':
                cnn.init_bin_conv_model()
            else:
                print('invalid model')
                return None
            history = cnn.model_fit(epochs=epochs)
            row['accuracy_train'] = history.history['accuracy'][-1]
            row['accuracy_val'] = history.history['val_accuracy'][-1]
            test = cnn.evaluate_model()
            row['accuracy_test'] = test[1]
            binary_stats_df = binary_stats_df.append(row, ignore_index=True)

        self.model_df = binary_stats_df
        binary_stats_df.to_csv(f'{name}.csv', index=False)
        print(binary_stats_df.head())
        print(binary_stats_df.accuracy_test.describe())
        return binary_stats_df
