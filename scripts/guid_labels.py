#!/usr/bin/env
import sys
import uuid

for line in sys.stdin:
    if line.startswith('>'):
        line = '>' + uuid.uuid4().hex + '\n'
    sys.stdout.write(line)