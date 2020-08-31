#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import from the standard library
from os.path import split
import argparse
import pandas as pd

# Import from codoxer
import codoxer
from codoxer.transformers import CxxTokenizer

if __name__ == '__main__':

    # Arguemtn parser duh
    parser = argparse.ArgumentParser()

    # arguments
    parser.add_argument('code', help = 'code for which the author is to be predicted')
    parser.add_argument('-v', '--verbose', help = 'make output verbose', action = 'store_true')
    parser.add_argument('-p', '--probability', help = 'return probability of prediction', action = 'store_true')
    parser.add_argument('-n', '--n_best', type = int, choices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], help = 'return n most likely authors (best to combine with -p to get probabilities)')

    args = parser.parse_args()
    print(args)

    file = args.code


    # open file
    with open(file, 'r') as open_file:
        code = open_file.read()


    # Tokenize code
    tokenizer = CxxTokenizer()

    code_tokenized = tokenizer.fit_transform(code)
