#!/usr/bin/env python


import sys
import os
import string
import re

sys.path.append('core')

from debugdump import DebugDump
import subprocess 

# print os.getcwd()

# Default fallback to use if we can't figure out SVN revision in any other
# way: Use this file's svn revision.
pattern = re.compile(r'[^0-9]')
svnrev = pattern.sub("", "$Revision$")

# Try getting svn revision by calling svnversion (will only work in linux) 
# and windows where sliksvn is installed
output = ""
try:
    output = subprocess.Popen(["svnversion","."], stdout=subprocess.PIPE).communicate()[0]
    output = pattern.sub("", output)
    svnrev = output
except Exception as e:
    print "Failed to get svn version number from command line: " + format(str(e))

# If output is still empty at this point, the above approaches failed and
# we need to do something else about it
if output == "":
    print "have to use some other approach"
    # Some other smart way to detect svn revision

# Set SVN rev in environment so it can be used elsewhere
print "Detected SVN revision: " + svnrev    
os.environ['SVNREVISION'] = svnrev

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        mfile = sys.argv[1]
    else:
        mfile = './main.py'

    try:
        DebugDump()
    except Exception as e:
        print "Could not create debug dump -- " + format(str(e))

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
