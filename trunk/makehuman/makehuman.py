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

from __future__ import absolute_import  # Fix 'from . import x' statements on python 2.6
import sys
import os
import string
import re
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

def get_revision_svn_info():
    # Try getting svn revision by calling svn info (will only work in linux
    #  and windows where sliksvn is installed)
    output = subprocess.Popen(["svn","info","."], stdout=subprocess.PIPE, stderr=sys.stderr).communicate()[0]
    for line in output.splitlines():
        key, value = line.split(':', 1)
        if key.strip().lower() == 'revision':
            return value.strip()
    raise RuntimeError("revision not found in 'svn info .' output")

def get_revision_entries():
    # First fallback: try to parse the entries file manually
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    svndir = os.path.join(scriptdir,'.svn')
    entriesfile = os.path.join(svndir,'entries')
    entries = open(entriesfile, 'r').read()
    result = re.search(r'dir\n(\d+)\n',entries)
    output = result.group(1)
    if not output:
        raise RuntimeError("revision not found in 'entries' file")
    return output

def get_revision_pysvn():
    # The following only works if pysvn is installed. We'd prefer not to use this since it's very slow.
    # It was taken from this stackoverflow post:
    # http://stackoverflow.com/questions/242295/how-does-one-add-a-svn-repository-build-number-to-python-code
    import pysvn
    repo = "."
    rev = pysvn.Revision( pysvn.opt_revision_kind.working )
    client = pysvn.Client()
    info = client.info2(repo,revision=rev,recurse=False)
    output = format(str(info[0][1].rev.number))
    return output

def get_revision_file():
    # Default fallback to use if we can't figure out SVN revision in any other
    # way: Use this file's svn revision.
    pattern = re.compile(r'[^0-9]')
    return pattern.sub("", "$Revision$")

def get_svn_revision_1():
    svnrev = None

    try:
        svnrev = get_revision_svn_info()
        os.environ['SVNREVISION_SOURCE'] = "svn info command"
        return svnrev
    except Exception as e:
        print "NOTICE: Failed to get svn version number from command line: " + format(str(e)) + " (This is just a head's up, not a critical error)"

    try:
        svnrev = get_revision_entries()
        os.environ['SVNREVISION_SOURCE'] = "entries file"
        return svnrev
    except Exception as e:
        print "NOTICE: Failed to get svn version from file: " + format(str(e)) + " (This is just a head's up, not a critical error)"

    try:
        svnrev = get_revision_pysvn()
        os.environ['SVNREVISION_SOURCE'] = "pysvn"
        return svnrev
    except Exception as e:
        print "NOTICE: Failed to get svn version number using pysvn: " + format(str(e)) + " (This is just a head's up, not a critical error)"

    print "NOTICE: Using SVN rev from file stamp. This is likely outdated, so the number in the title bar might be off by a few commits."
    svnrev = get_revision_file()
    os.environ['SVNREVISION_SOURCE'] = "approximated from file stamp"
    return svnrev

def get_svn_revision():
    # Set SVN rev in environment so it can be used elsewhere
    svnrev = get_svn_revision_1()
    print "Detected SVN revision: " + svnrev
    os.environ['SVNREVISION'] = svnrev

def recursiveDirNames(root):
    pathlist=[]
    #root=os.path.dirname(root)
    for filename in os.listdir(root):
        path=os.path.join(root,filename)
        if not (os.path.isfile(path) or filename=="." or filename==".." or filename==".svn"):
            pathlist.append(path)
            pathlist = pathlist + recursiveDirNames(path) 
    return(pathlist)

def set_sys_path():
    syspath = ["./", "./lib", "./apps", "./shared", "./shared/mhx/templates", "./shared/mhx"]
    syspath = syspath + recursiveDirNames("./apps")
    syspath.append("./core")
    syspath = syspath + recursiveDirNames("./core")
    syspath.extend(sys.path)
    sys.path = syspath

stdout_filename = None
stderr_filename = None

def get_platform_paths():
    global stdout_filename, stderr_filename

    if sys.platform == 'win32':
        find_mydocuments()
        home = os.environ['MYDOCUMENTS']
        home = os.path.join(home,'makehuman')
        if not os.path.exists(home):
            os.makedirs(home)
        stdout_filename = os.path.join(home, "python_out.txt")
        stderr_filename = os.path.join(home, "python_err.txt")

    elif sys.platform.startswith("darwin"):
        home = os.path.join(os.path.expanduser('~'),"Documents")
        home = os.path.join(home,"MakeHuman")
        if not os.path.exists(home):
            os.makedirs(home)            

        stdout_filename = os.path.join(home, "makehuman-output.txt")
        stderr_filename = os.path.join(home, "makehuman-error.txt")

def redirect_standard_streams():
    if stdout_filename:
        sys.stdout = open(stdout_filename, "w")
    if stderr_filename:
        sys.stderr = open(stderr_filename, "w")

def close_standard_streams():
    sys.stdout.close()
    sys.stderr.close()

def make_user_dir():
    import getpath
    userDir = getpath.getPath('')
    if not os.path.isdir(userDir):
        os.makedirs(userDir)

def init_logging():
    import log
    log.init()
    log.message('Initialized logging')
    
def debug_dump():
    try:
        import log
        from debugdump import DebugDump
        debugdump = DebugDump()
        debugdump.reset()
    except Exception as e:
        log.error("Could not create debug dump", exc_info=True)

def main():
    get_platform_paths()
    redirect_standard_streams()
    get_svn_revision()
    set_sys_path()
    make_user_dir()
    init_logging()
    debug_dump()

    from mhmain import MHApplication
    application = MHApplication()
    application.run()

    #import cProfile
    #cProfile.run('application.run()')

    close_standard_streams()

if __name__ == '__main__':
    main()
