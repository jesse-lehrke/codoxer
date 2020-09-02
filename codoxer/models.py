import json
import joblib
from pathlib import Path
import tensorflow as tf

class Tfidf(object):
    pass


def load_tfidf():
    path = Path(__file__).parent / 'models/vectorizer_132'
    return joblib.load(path)

def load_selector():
    path = Path(__file__).parent / 'models/selector_132'
    return joblib.load(path)

def load_cnn():
    path = Path(__file__).parent / 'models/trained_model_132'
    return tf.keras.models.load_model(path)

def load_dict():
    path = Path(__file__).parent / 'models/user_id_dict_132.json'
    with open(path) as file:
        return json.load(file)


if __name__ == '__main__':
    print(load_dict())
