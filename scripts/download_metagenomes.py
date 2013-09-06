#!/usr/bin/env python
import sys
import os
import urllib2
import cPickle as pkl
import json

try:
    input_path = sys.argv[1]
    output_dir = sys.argv[2]
    genome_ids = sys.argv[3:]
except:
    raise Exception('Usage: python download_metagenomes.py input_pickle output_dir [genome_id ...]')

with open(input_path) as input_file:
    data = pkl.load(input_file)

download_url = 'http://api.metagenomics.anl.gov/sequenceset/%s'

for id in genome_ids:
    genome = data[id]
    
    filename = os.path.join(output_dir, '%s.fna.gz' % id)
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        os.utime(filename, None)
        continue

    print '=>', id
    doc = urllib2.urlopen(download_url % id)
    data = json.loads(doc.read())
    doc.close()
    for file in data:
        if file['stage_name'] == 'search':
            # download this file
            doc = urllib2.urlopen(file['url'])
            with open(filename, 'wb') as output_file:
                r = True
                while r:
                    r = doc.read(1024)
                    if r: output_file.write(r)