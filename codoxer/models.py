import joblib
from pathlib import Path
import tensorflow as tf

class Tfidf(object):
    pass


def load_tfidf():
    path = Path(__file__).parent / 'models/tfidf'
    return joblib.load(path)

def load_selector():
    path = Path(__file__).parent / 'models/selector'
    return joblib.load(path)

def load_cnn():
    path = Path(__file__).parent / 'models/trained_model'
    return tf.keras.models.load_model(path)

'''
if __name__ == '__main__':
    load_tfidf()
'''
