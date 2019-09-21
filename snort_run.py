#!/usr/bin/env python

from __future__ import print_function
from subprocess import Popen, PIPE, STDOUT


snort_process = Popen(['snort', '-dev', '-i', 'enp0s8',
                       '-c', '/etc/snort/snort.conf', '-A', 'console'],
                      stdout=PIPE, stderr=STDOUT, bufsize=1,
                      universal_newlines=True, close_fds=True)
with snort_process.stdout:
    for line in iter(snort_process.stdout.readline, ''):
        if 'Possible TCP DoS' in line:
            print(line, end='')
rc = snort_process.wait()
