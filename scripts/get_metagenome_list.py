#!/usr/bin/env python
import sys
try:
    output_path = sys.argv[1]
except:
    raise Exception('Usage: python get_metagenome_list.py pickle_file')
    
import urllib2
import json
import cPickle as pkl

search_term = 'marine'
search_url = ('http://api.metagenomics.anl.gov/1/metagenome?verbosity=mixs&metadata=%s&order=sequence_type&direction=asc&match=any&limit=1000&offset=0'
              % search_term)

def subsearch(url):
    print '=>', url
    doc = urllib2.urlopen(url)
    data = json.loads(doc.read())
    doc.close()
    return data

result = subsearch(search_url)
metagenomes = []
while result:
    if 'data' in result:
        amplicon_results = [d for d in result['data'] if d['sequence_type'] == 'Amplicon']
        metagenomes += amplicon_results
        if len(amplicon_results) < len(result['data']): break
    
    if 'next' in result and result['next']:
        result = subsearch(result['next'])
    else: result = None

with open(output_path, 'wb') as output_file:
    pkl.dump({g['id']: g for g in metagenomes}, output_file, -1)