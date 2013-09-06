#!/usr/bin/env python
import sys
import cPickle as pkl

try:
    input_path = sys.argv[1]
except:
    input_path = 'data/metagenome_list.pkl'

try:
    with open(input_path) as input_file:
        data = pkl.load(input_file)

    print ' '.join(data)
except: print