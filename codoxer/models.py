import joblib
from pathlib import Path
import tensorflow as tf

def load_tfidf():
    path = Path(__file__).parent / 'models/tfidf.pkl'
    return joblib.load(path)

def load_cnn():
    path = Path(__file__).parent / 'models/trained_model'
    return tf.keras.models.load_model(path)


'''
if __name__ == '__main__':
    load_cnn()
'''
