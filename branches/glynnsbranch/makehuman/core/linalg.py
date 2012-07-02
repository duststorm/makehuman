#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module that uses the wrapped lapack and blas for pthon.

B{Project Name:}      MakeHuman

B{Product Home Page:} U{http://www.makehuman.org/}

B{Code Home Page:}    U{http://code.google.com/p/makehuman/}

B{Authors:}           Jose Capco

B{Copyright(c):}      MakeHuman Team 2001-2011

B{Licensing:}         GPL3 (see also U{http://sites.google.com/site/makehumandocs/licensing})

B{Coding Standards:}  See U{http://sites.google.com/site/makehumandocs/developers-guide}

Abstract
========

This module uses LAPACK and BLAS methods imported to linalg_module
"""

import linalg_module

def linsolve(A,b):
    """
    Given a system of linear equations defined by the formula Ax = b for some square matrix A, we solve x
    """
    return linalg_module.svx(A,b, len(b))