from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler
from sklearn.multiclass import OneVsOneClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline


class CodingStyleFeatureExtractor(BaseEstimator, TransformerMixin):
    """Perform feature extraction for MVP

    Based on assumption that code provided is only C++, Java and Python

    """

    def __init__(self):
        pass

    def fit(self, X, y = None):
        return self

    def transform(self, X, y = None):

        df = X
        # Length of code in character (including whitespaces and everything)
        df['code_length'] = df['flines'].apply(lambda x: len(x))

        # Estimated number of loops
        df['n_loops'] = df.flines.apply(lambda x: (x.count('for') + x.count('while')) / len(x) )

        # Estimated number of imports
        df['n_imports'] = df.flines.apply(lambda x: (x.count('#include') + x.count('import')) / len(x) )

        # Estimated number of control statements excluding loops
        df['n_contols'] = df.flines.apply(lambda x: (x.count('if') + x.count('else') + x.count('elif')) / len(x) )

        # Estimated nubmer of variable (re-)assignements and declarations
        df['n_assigns'] = df.flines.apply(lambda x: (x.count('=') - x.count('==') - x.count('<=') - x.count('>=') - x.count('!=')) / len(x))

        # Estimated number of asserts
        df['n_asserts'] = df.flines.apply(lambda x: x.count('assert') / len(x))

        # Whether main method is present in code
        df['has_main'] = df.flines.apply(lambda x: min(x.count('main()'), 1))

        # Number of newlines
        df['n_newlines'] = df.flines.apply(lambda x: x.count('\n') / len(x))

        # Estimated number od comments
        df['n_comments'] = df.apply(lambda x: count_comments(x['lan'], x['flines']) / len(x), axis = 1)

        # Relative Nmber of underscore in code
        df['n_underscore'] = df.flines.apply(lambda x: x.count('_') / len(x))

        # Relative number of whitespaces
        df['n_whitespace'] = df.flines.apply(lambda x: x.count(' ') / len(x))

        # Relative number of camel case uses
        df['n_camelCase'] = df.flines.apply(lambda x: sum(1 for m in re.finditer(r'[a-z][A-Z]', x)) / len(x))

        # Relative use of snake case uses
        df['n_snakeCase'] = df.flines.apply(lambda x: sum(1 for m in re.finditer(r'[a-zA-Z]_[a-zA-Z]', x)) / len(x))

        # Number of non-empty lines (code + comment + docstrings)
        #df['n_lines'] = df.flines.apply(lambda x: sum(1 for m in re.finditer(r'.+', x)) / len(x))

        # Number of lines of code (excluding empty and comment, DOES NOT exclude multiline and docstring)
        df['n_lines'] = df.flines.apply(lambda x: sum(1 for m in re.finditer(r'[^#\/]+', x)) / len(x))

        # Relative number of print/output statements
        df['outputs'] = df.flines.apply(lambda x: (x.count('cout') + x.count('print(') + x.count('print ') + x.count('.print')) / len(x))

        def count_comments(language, code):
            """Counts number of comments based on language"""
            if language == 'cpp':
                return code.count('//') + code.count('/*') + code.count('*/')
            if language == 'python':
                return code.count('#') + code.count('"""')
            if language == 'java':
                return code.count('//') + code.count('/*') + code.count('*/') + code.count('/**') + code.count('/**')

        return df


    class Trainer(object):

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

            est = get_estimator()

            self.pipe = make_pipeline(fe, cl, est)

        def train(self):

            self.set_pipeline()

            self.pipe.fit(X_train, y_train)

        def






