#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import from the standard library
import os
import argparse
import numpy as np
import tensorflow as tf
import scipy

# Import from codoxer
from codoxer import models
from codoxer.transformers import CxxTokenizer

#from sklearn.feature_extraction import TfidfVectorizer

class Tfidf(object):
    pass


if __name__ == '__main__':



    # Arguemtn parser duh
    parser = argparse.ArgumentParser()

    # arguments
    parser.add_argument('code', help = 'code for which the author is to be predicted')
    parser.add_argument('-v', '--verbose', help = 'make output verbose', action = 'store_true')
    parser.add_argument('-p', '--probability', help = 'return probability of prediction', action = 'store_true')
    parser.add_argument('-n', '--n_best', type = int, choices = range(1,11), default = 1, help = 'return n most likely authors (best to combine with -p to get probabilities)')

    args = parser.parse_args()
    #print(args)

    file = args.code


    # open file
    if args.verbose == True:
        print('// Loading data...')
    with open(file, 'r') as open_file:
        code = open_file.read()
    if args.verbose == True:
        print('// DONE')


    # Check for correct input

    # Tokenize code
    if args.verbose == True:
        print('// Tokenizing...')

    tokenizer = CxxTokenizer()

    code_tokenized = tokenizer.fit_transform(code)

    if args.verbose == True:
        print('// DONE')



    # Run through Tf-Idf

    if args.verbose == True:
        print('// Running Tf-Idf...')

    tfidf = models.load_tfidf()
    code_tfidf = tfidf.transform([code_tokenized])

    if args.verbose == True:
        print('// DONE')



    # Run through Selector

    if args.verbose == True:
        print('// Running Percentil Selector...')

    code_tfidf = code_tfidf.reshape(1,-1)


    selector = models.load_selector()
    code_selected = selector.transform(code_tfidf)

    if args.verbose == True:
        print('// DONE')



    # Run trough CNN

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    if args.verbose == True:
        print('// Computing prediction...')


    def convert_sparse_matrix_to_sparse_tensor(X):
        coo = X.tocoo()
        indices = np.mat([coo.row, coo.col]).transpose()
        return tf.SparseTensor(indices, coo.data, coo.shape)

    #code_reordered = tf.sparse.reorder(code_selected)
    code_reordered = code_selected.sort_indices()

    cnn = models.load_cnn()

    #code_selected = code_selected.reshape(code_selected.shape[0], code_selected.shape[1], 1)
    code_final = tf.sparse.to_dense(tf.sparse.reshape(convert_sparse_matrix_to_sparse_tensor(code_selected), (code_selected.shape[0], code_selected.shape[1], 1)))

    predictions = cnn.predict(code_final)

    if args.verbose == True:
        print('// DONE...')

    # Load dict to map id to user
    id_to_user = models.load_dict()

    # OUTPUT
    print(id_to_user[str(predictions.argmax())])



