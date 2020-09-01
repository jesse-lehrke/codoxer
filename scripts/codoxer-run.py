#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import from the standard library
import argparse


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
        print('DONE')

    # Run trough CNN
    if args.verbose == True:
        print('// Computing prediction...')

    cnn = models.load_cnn()
    print(cnn.predict(code_tfidf))

    if args.verbose == True:
        print('// DONE...')


