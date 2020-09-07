import pandas as pd
import os
from collections import defaultdict
from pathlib import Path
import shutil

class Tokenizer(object):

    def __init__(self, data, column=3):
        self.data = pd.read_csv(data)
        self.column =  column
        if not os.path.exists('./data/'):
            os.makedirs('./data/')
        if not os.path.exists('./data/output'):
            os.makedirs('./data/output')
        if not os.path.exists('./data/input'):
            os.makedirs('./data/input')

    def tokenize(self):

        i = 0
        for index, row in self.data.iterrows():
            if i > len(self.data):
                break
            else:
                f = open('./data/input/'+str(i)+'.txt', 'w')
                f.write(row[self.column])
                f.close()
                i+=1

        filenames = list(range(0, i, 1))
        for file in filenames:
            cmd = 'tokenizer -l C++ -t c ./data/input/{}.txt > ./data/output/{}'.format(file, file)
            os.system(cmd)

        my_dir_path = "./data/output"

        results = defaultdict(list)
        for file in Path(my_dir_path).iterdir():
            with open(file, "r") as file_open:
                #results["file_name"] = file.name # not needed anymore ?
                filename = file.name
                filename = filename.split('.')
                results["index"].append(filename[0])
                results["text"].append(file_open.read())
        df_x = pd.DataFrame(results)

        #clean up
        shutil.rmtree("./data/input")
        shutil.rmtree("./data/output")
        #os.remove('./data/input')
        #os.remove('./data/output')

        #indexing to merge
        df_x = df_x.set_index('index')
        df_x.index.astype(float)
        df_x.index = pd.to_numeric(df_x.index, errors='coerce')
        df_x = df_x.sort_index()

        #final split and saveing
        df_x = df_x.text.str.split('\n')
        df_4 = self.data.merge(df_x, right_index=True, left_index=True)
        df_4.rename(columns={'text':'tokens'},
                 inplace=True)
        self.data = df_4.to_csv('./data/tokens.csv')

        return self.data
