#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

from cProfile import Profile

_sort = 'cumulative'
_accum = {}

def run(cmd, globals, locals):
    prof = Profile()
    try:
        prof.runctx(cmd, globals, locals)
    finally:
        show(prof)

def accum(cmd, globals, locals):
    if cmd not in _accum:
        prof = Profile()
        _accum[cmd] = prof
    else:
        prof = _accum[cmd]
    prof.runctx(cmd, globals, locals)

def flush():
    for cmd in sorted(_accum.keys()):
        show(_accum[cmd])
    _accum.clear()

def show(prof):
    prof.print_stats(_sort)

def set_sort(sort):
    global _sort
    _sort = sort
