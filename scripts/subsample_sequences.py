#!/usr/bin/env python
import sys
import random

n = int(sys.argv[1])

try:
    input_path = sys.argv[2]
    with open(input_path) as input_file:
        data = input_file.read()
except: data = sys.stdin.read()

sequences = data.split('>')[1:]

sys.stdout.write('>' + '>'.join(random.sample(sequences, n)))