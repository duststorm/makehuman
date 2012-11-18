#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import os
import sys

def which(program):
    """
    Checks whether a program exists, similar to http://en.wikipedia.org/wiki/Which_(Unix)
    """

    import os
    import sys
    
    if sys.platform == "win32" and not program.endswith(".exe"):
        program += ".exe"
        
    print "looking for", program
        
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            print exe_file
            if is_exe(exe_file):
                return exe_file

    return None
