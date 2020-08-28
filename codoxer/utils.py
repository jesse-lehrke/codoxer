import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

def dictionary_ids(X):
    '''takes in a list of words
    returns a dictionay assigning an id to each word'''
    word_to_id = {}
    i = 0
    for item in X:
        for word in item:
            if word not in word_to_id:
                word_to_id[word] = i
                i+=1
    return word_to_id

def dictionary_target(y):
    user_to_id = {'unseen_word': 0}
    i = 1
    for item in y:
        if item not in user_to_id:
            user_to_id[item] = i
            i+=1
    return user_to_id

def tokens(sentence, dictionary):
    '''takes in a list of lists containing tokens
    returns a list of lists with matching ids'''
    token = []
    vocab_size = len(dictionary)
    for item in sentence:
        sub_token = []
        for word in item:
            if word in dictionary:
                sub_token.append(dictionary[word]/vocab_size)
        token.append(sub_token)
    return token

def y_tokens(y_train, y_test):
    new_y = []
    for item in y_test:
        if item not in y_train:
            new_y.append('unseen_word')
        else:
            new_y.append(item)
    return y_train, new_y

def token_y(y, dictionary):
    token = []
    for item in y:
        if item in dictionary:
            token.append(dictionary[item])
    return token

def string_to_token(X):
    X = X[2:-2]
    X = X.split("\', \'")
    return X

def series_to_tokens(X):
    X = X.apply(string_to_token)
    return X


def embedding_prep_X_y(X, y, pad_len=1000):
    #prepare X
    X = series_to_tokens(X)

    #split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    #prepare a dictionary for X and y
    word_to_id = dictionary_ids(X_train)
    vocab_size = len(word_to_id)
    user_to_id = dictionary_target(y_train)

    #convert words to ids
    token_train = tokens(X_train, word_to_id)
    token_test = tokens(X_test, word_to_id)

    #pad X
    X_train_pad = pad_sequences(token_train, maxlen=pad_len)
    X_test_pad = pad_sequences(token_test, maxlen=pad_len)

    s = X_train_pad.shape

    #prepare y
    y_train = y_train.tolist()
    y_test = y_test.tolist()
    y_train, new_y_test = y_tokens(y_train, y_test)
    user_train = token_y(y_train, user_to_id)
    user_test = token_y(new_y_test, user_to_id)
    user_train = np.array(user_train).astype(np.int32)
    user_test = np.array(user_test).astype(np.int32)
    y_train_cat = to_categorical(user_train)
    y_test_cat = to_categorical(user_test)

    return vocab_size, s, X_train_pad, X_test_pad, y_train_cat, y_test_cat
