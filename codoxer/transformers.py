import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import os
from collections import defaultdict
from pathlib import Path
import shutil



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

class CxxTokenizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        if not os.path.exists('./data/'):
            os.makedirs('./data/')
        if not os.path.exists('./data/output'):
            os.makedirs('./data/output')
        if not os.path.exists('./data/input'):
            os.makedirs('./data/input')

    def fit(self, X, y = None):
        return self

    def transform(self, X, y = None)
        i = 0
        for row in X
            if i > len(X):
                break
            else:
                f = open('./data/input/'+str(i)+'.txt', 'w')
                f.write(row)
                f.close()
                i+=1

        filenames = list(range(0, i, 1))
        for file in filenames:
            cmd = 'tokenizer -l C++ -t c ./data/input/{}.txt > ./data/output/{}'.format(file, file)
            os.system(cmd)

        my_dir_path = "./data/output"

        results = []
        for file in Path(my_dir_path).iterdir():
            with open(file, "r") as file_open:
                #results["file_name"] = file.name # not needed anymore ?
                filename = file.name
                filename = filename.split('.')
                #results["index"].append(filename[0])
                results.append(file_open.read())
        token_x = np.array(results)

        #clean up
        shutil.rmtree("./data/input")
        shutil.rmtree("./data/output")
        #os.remove('./data/input')
        #os.remove('./data/output')

        #indexing to merge
        #df_x = df_x.set_index('index')
        #df_x.index.astype(float)
        #df_x.index = pd.to_numeric(df_x.index, errors='coerce')
        #df_x = df_x.sort_index()

        #final split and saveing
        #df_x = df_x.text.str.split('\n')
        #df_4 = self.data.merge(df_x, right_index=True, left_index=True)
        #df_4.rename(columns={'text':'tokens'},
        #         inplace=True)
        #self.data = df_4.to_csv('./data/tokens.csv')

        return token_x
