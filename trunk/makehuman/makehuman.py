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
    output = output.split(":")[0]
    svnrev = pattern.sub("", output)
except Exception as e:
    print "Failed to get svn version number from command line: " + format(str(e))

if output == "":
    # First fallback: try to parse the entries file manually
    try:
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        svndir = os.path.join(scriptdir,'.svn')
        entriesfile = os.path.join(svndir,'entries')
        entries = open(entriesfile, 'r').read()
        result = re.search(r'dir\n(\d+)\n',entries)
        output = result.group(1)
        svnrev = output
    except Exception as e:
        print "Failed to get svn version from file: " + format(str(e))

if output == "":
    # The following only works if pysvn is installed. We'd prefer not to use this since it's very slow.
    # It was taken from this stackoverflow post: http://stackoverflow.com/questions/242295/how-does-one-add-a-svn-repository-build-number-to-python-code
    try:
        import pysvn
        repo = "."
        rev = pysvn.Revision( pysvn.opt_revision_kind.working )
        client = pysvn.Client()
        info = client.info2(repo,revision=rev,recurse=False)
        output = format(str(info[0][1].rev.number))
        svnrev = output
    except Exception as e:
        print "Failed to get svn version number using pysvn: " + format(str(e))

if output == "":
    print "Using SVN rev from file stamp. This is likely outdated."

# Set SVN rev in environment so it can be used elsewhere
print "Detected SVN revision: " + svnrev    
os.environ['SVNREVISION'] = svnrev

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        mfile = sys.argv[1]
    else:
        mfile = './main.py'

    try:
        debugdump = DebugDump()
        debugdump.reset()
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
