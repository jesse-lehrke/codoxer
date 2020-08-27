import pandas as pd
import regex as re
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler
from sklearn.multiclass import OneVsOneClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.exceptions import NotFittedError
from sklearn.model_selection import train_test_split

class CodingStyleFeatureExtractor(BaseEstimator, TransformerMixin):
    """Perform feature extraction for MVP

    Based on assumption that code provided is only C++, Java and Python

    """

    def __init__(self):
        pass

    def fit(self, X, y = None):
        return self

    def transform(self, X, y = None):

        def count_comments(language, code):
            """Counts number of comments based on language"""
            if language == 'cpp':
                return code.count('//') + code.count('/*') + code.count('*/')
            if language == 'python':
                return code.count('#') + code.count('"""')
            if language == 'java':
                return code.count('//') + code.count('/*') + code.count('*/') + code.count('/**') + code.count('/**')

        df = X.copy()
        # Length of code in character (including whitespaces and everything)
        df.loc[:, 'code_length'] = df['flines'].apply(lambda x: len(x))

        # Estimated number of loops
        df.loc[:, 'n_loops'] = df.flines.apply(lambda x: (x.count('for') + x.count('while')) / len(x) )

        # Estimated number of imports
        df.loc[:, 'n_imports'] = df.flines.apply(lambda x: (x.count('#include') + x.count('import')) / len(x) )

        # Estimated number of control statements excluding loops
        df.loc[:, 'n_contols'] = df.flines.apply(lambda x: (x.count('if') + x.count('else') + x.count('elif')) / len(x) )

        # Estimated nubmer of variable (re-)assignements and declarations
        df.loc[:, 'n_assigns'] = df.flines.apply(lambda x: (x.count('=') - x.count('==') - x.count('<=') - x.count('>=') - x.count('!=')) / len(x))

        # Estimated number of asserts
        df.loc[:, 'n_asserts'] = df.flines.apply(lambda x: x.count('assert') / len(x))

        # Whether main method is present in code
        df.loc[:, 'has_main'] = df.flines.apply(lambda x: min(x.count('main()'), 1))

        # Number of newlines
        df.loc[:, 'n_newlines'] = df.flines.apply(lambda x: x.count('\n') / len(x))

        # Estimated number od comments
        df.loc[:, 'n_comments'] = df.apply(lambda x: count_comments(x['language'], x['flines']) / len(x), axis = 1)

        # Relative Nmber of underscore in code
        df.loc[:, 'n_underscore'] = df.flines.apply(lambda x: x.count('_') / len(x))

        # Relative number of whitespaces
        df.loc[:, 'n_whitespace'] = df.flines.apply(lambda x: x.count(' ') / len(x))

        # Relative number of camel case uses
        df.loc[:, 'n_camelCase'] = df.flines.apply(lambda x: sum(1 for m in re.finditer(r'[a-z][A-Z]', x)) / len(x))

        # Relative use of snake case uses
        df.loc[:, 'n_snakeCase'] = df.flines.apply(lambda x: sum(1 for m in re.finditer(r'[a-zA-Z]_[a-zA-Z]', x)) / len(x))

        # Number of non-empty lines (code + comment + docstrings)
        #df['n_lines'] = df.flines.apply(lambda x: sum(1 for m in re.finditer(r'.+', x)) / len(x))

        # Number of lines of code (excluding empty and comment, DOES NOT exclude multiline and docstring)
        df.loc[:, 'n_lines'] = df.flines.apply(lambda x: sum(1 for m in re.finditer(r'[^#\/]+', x)) / len(x))

        # Relative number of print/output statements
        df.loc[:, 'outputs'] = df.flines.apply(lambda x: (x.count('cout') + x.count('print(') + x.count('print ') + x.count('.print')) / len(x))


        return df.drop(columns = ['language', 'flines'])


class MVP(object):

    def __init__(self, X, y):
        self.X_train = X
        self.y_train = y

    def get_estimator(self):
        return OneVsOneClassifier(LogisticRegression())

    def set_pipeline(self):
        fe = CodingStyleFeatureExtractor()

        cl = ColumnTransformer([('scaler', RobustScaler(), ['code_length', 'n_loops', 'n_imports', 'n_contols', 'n_assigns',
                'n_asserts', 'n_newlines', 'n_whitespace', 'n_comments',
                'n_camelCase', 'n_lines', 'outputs', 'n_snakeCase'])])

        est = self.get_estimator()

        self.pipe = make_pipeline(fe, cl, est)

    def train(self, cv = None):

        self.set_pipeline()

        self.pipe.fit(X_train, y_train)

    def predict(self, X):
        if self.pipe == None:
            raise NotFittedError('Model not fitted. Fit with .train() first.')

        return self.pipe.predict(X)

    def evaluate(self, X, y = None):
        return self.pipe.score(X, y)


if __name__ == '__main__':
    print('//Loading Data...')
    df = pd.read_csv('data/gcj_data_select.csv')
    print('//Preprocessing...')
    df = df[df.language.isin(['cpp', 'python', 'java'])]
    df = df[df.username.isin(list(df.username.value_counts().head(10).index))]
    X = df.drop(columns =  ['task', 'year'])
    y = df.username

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    print('//Initializig pipeline...')
    mvp_inst = MVP(X_train, y_train)

    print('//Training model...')
    mvp_inst.train()

    print('//Evaluating model...')

    print('Model accuracy: ' + str(mvp_inst.evaluate(X_test, y_test)))




