#!/usr/bin/env python3


"""
1) Assume role for TO-Domain
2) Create hosted zone for domain example.com
2) assume role for FROM-Domain
3) Run: aws route53 list-resource-record-sets --hosted-zone-id hosted-FROM-zone-id > out.json
4) Run: python convert.py out.json > out.importable.json
5) Run: aws route53 change-resource-record-sets --hosted-zone-id hosted-TO-zone-id --change-batch file://./out.importable.json

"""

import sys
import json
import argparse

from os.path import split, splitext

infile = sys.argv[1]
outfile = 'converted/' + split(infile)[-1] + '.json'

_infile = json.load(open(infile, 'rb'))
_changes = []

for rs, x in _infile.items():
    for j in x:
        if j['Type'] in ('NS', 'SOA'):
            continue

        _changes.append({
            'Action': 'CREATE',
            'ResourceRecordSet': j
        })

out = open(outfile, 'w')
out.write(json.dumps({'Changes':_changes}))
out.close()
