#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MakeHuman python entry-point.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements, Joel Palmius

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

This file starts the MakeHuman python application.
"""

import sys
import os
import string
import re

sys.path.append('core')

from debugdump import DebugDump
import subprocess 

# print os.getcwd()

def find_mydocuments():
    os.environ['MYDOCUMENTS'] = os.path.expanduser('~')
    if sys.platform == 'win32':
        import _winreg
        try:
            k = _winreg.HKEY_CURRENT_USER
            for x in ['Software', 'Microsoft', 'Windows', 'CurrentVersion', 'Explorer', 'Shell Folders']:
                k = _winreg.OpenKey(k, x)

            name, type = _winreg.QueryValueEx(k, 'Personal')

            if type == 1:
                os.environ['MYDOCUMENTS'] = name
        except Exception as e:
            print "error: " + format(str(e))


def get_svn_revision():
    # Default fallback to use if we can't figure out SVN revision in any other
    # way: Use this file's svn revision.
    pattern = re.compile(r'[^0-9]')
    svnrev = pattern.sub("", "$Revision$")

    os.environ['SVNREVISION_SOURCE'] = "approximated from file stamp"

    # Try getting svn revision by calling svnversion (will only work in linux) 
    # and windows where sliksvn is installed
    output = ""
    try:
        output = subprocess.Popen(["svnversion","."], stdout=subprocess.PIPE, stderr=sys.stderr).communicate()[0]
        output = output.split(":")[0]
        svnrev = pattern.sub("", output)
        os.environ['SVNREVISION_SOURCE'] = "shell command"
    except Exception as e:
        print "NOTICE: Failed to get svn version number from command line: " + format(str(e)) + " (This is just a head's up, not a critical error)"

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
            os.environ['SVNREVISION_SOURCE'] = "entries file"
        except Exception as e:
            print "NOTICE: Failed to get svn version from file: " + format(str(e)) + " (This is just a head's up, not a critical error)"

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
            os.environ['SVNREVISION_SOURCE'] = "pysvn"
        except Exception as e:
            print "NOTICE: Failed to get svn version number using pysvn: " + format(str(e)) + " (This is just a head's up, not a critical error)"

    if output == "":
        print "NOTICE: Using SVN rev from file stamp. This is likely outdated, so the number in the title bar might be off by a few commits."

    # Set SVN rev in environment so it can be used elsewhere
    print "Detected SVN revision: " + svnrev    
    os.environ['SVNREVISION'] = svnrev

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        mfile = sys.argv[1]
    else:
        mfile = './main.py'

    if sys.platform == 'win32':
        find_mydocuments()
        home = os.environ['MYDOCUMENTS']
        home = os.path.join(home,'makehuman')

        if not os.path.exists(home):
            os.makedirs(home)

        fo = open(os.path.join(home, "python_out.txt"), "w")
        sys.stdout = fo
        fe = open(os.path.join(home, "python_err.txt"), "w")
        sys.stderr = fe

    if sys.platform.startswith("darwin"):
        home = os.path.join(os.path.expanduser('~'),"Documents")
        home = os.path.join(home,"MakeHuman")
        if not os.path.exists(home):
            os.makedirs(home)            
        fo = open(os.path.join(home, "makehuman-output.txt"), "w")
        sys.stdout = fo
        fe = open(os.path.join(home, "makehuman-error.txt"), "w")
        sys.stderr = fe

    get_svn_revision()

    try:
        debugdump = DebugDump()
        debugdump.reset()
    except Exception as e:
        print "Could not create debug dump -- " + format(str(e))

    os.environ["STARTEDCORRECTLY"] = "1"
    execfile(mfile)

    if sys.platform == 'win32':
        fo.close()
        fe.close()

    if sys.platform.startswith("darwin"):
        fo.close()
        fe.close()

