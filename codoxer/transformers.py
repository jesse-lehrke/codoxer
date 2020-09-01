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

'''
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
'''

class CxxTokenizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y = None):
        return self

    def transform(self, X, y = None):
        print('transform()')

        # If input is a single tring -> when called from command line
        if isinstance(X, str):

            # Write code to txt file in current? folder
            with open('code.txt', 'w') as file:
                file.write(X)

            # Execute tokenizer in command line
            cmd = 'tokenizer -l C++ -t c ./data/input/code.txt > ./data/output/code'
            os.system(cmd)

            # Read tokenized text from file
            out = ''
            with open('code.txt', 'r') as file:
                out = file.read

            # Cleanup
            os.remove('code.txt')

            return out

        if not os.path.exists('./data/'):
            os.makedirs('./data/')
        if not os.path.exists('./data/output'):
            os.makedirs('./data/output')
        if not os.path.exists('./data/input'):
            os.makedirs('./data/input')


        i = 0
        for row in X:
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
        print(token_x.shape)
        token_x = np.reshape(token_x, (token_x.shape[0], 1))
        print(token_x.shape)
        return token_x

if __name__ == '__main__':

    data = pd.read_csv('data/coder_data_prepped.csv')

    from sklearn.compose import ColumnTransformer

    print('line 110')
    ct = ColumnTransformer([('token', CxxTokenizer(), 'flines')])
    print('line 112')
    ct = ct.fit(data)
    print('line 114')
    data_out = ct.transform(data)
    print(data_out)
