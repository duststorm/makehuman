#!/usr/bin/env python


import sys
import os
import string
import re

sys.path.append('core')

from debugdump import DebugDump

# print os.getcwd()

pattern = re.compile(r'[^0-9]')
os.environ['SVNREVISION'] = pattern.sub("", "$Revision$")
print os.environ['SVNREVISION']

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        mfile = sys.argv[1]
    else:
        mfile = './main.py'

    DebugDump()

    if sys.platform == 'win32':
        home = os.path.expanduser('~')
        fo = open(os.path.join(home, "python_out.txt"), "w")
        sys.stdout = fo
        fe = open(os.path.join(home, "python_err.txt"), "w")
        sys.stderr = fe


    execfile(mfile)

    if sys.platform == 'win32':
        fo.close()
        fe.close()
