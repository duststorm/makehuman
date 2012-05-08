# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Project Name:        MakeHuman
# Product Home Page:   http://www.makehuman.org/
# Code Home Page:      http://code.google.com/p/makehuman/
# Authors:             Thomas Larsson
# Script copyright (C) MakeHuman Team 2001-2012
# Coding Standards:    See http://sites.google.com/site/makehumandocs/developers-guide
#
# Abstract
# Utility for making UVs to MH characters.
#

import bpy
import os
import random
from bpy.props import *
from mathutils import Vector
from . import base_uv
from . import makeclothes


def exportUVs(context):
    scn = context.scene
    ob = context.object
    (outpath, outfile) = makeclothes.getFileName(ob, context, "mhuv")
    print("Creating UV file %s" % outfile)
    fp= open(outfile, "w")
    fp.write(
"# author %s\n" % scn.MCAuthor +
"# license %s\n" % scn.MCLicense +
"# homepage %s\n" % scn.MCHomePage)

    fp.write("# name %s\n" % ob.name.replace(" ","_"))
    
    for mat in ob.data.materials:
        fp.write("# material %s\n" % mat.name)
        makeclothes.writeColor(fp, '  diffuse_color', mat.diffuse_color, mat.diffuse_intensity)
        makeclothes.writeColor(fp, '  specular_color', mat.specular_color, mat.specular_intensity)
        for mtex in mat.texture_slots:
            if mtex:
                print(mat.name, mtex.name)
                tex = mtex.texture
                fp.write("  texture %s\n" % tex.image.name)
                #fp.write("    image %s\n" % os.path.basename(tex.image.filepath))
    
    makeclothes.printFaceNumbers(fp, ob)    
    makeclothes.printMhcloUvLayers(fp, ob, scn, False)
    #printSimpleTexFaces(fp, ob)
    fp.close()
    print("File %s written" % outfile)
    return
    
    
def printSimpleTexFaces(fp, ob):
    faces = makeclothes.getFaces(ob.data)
    if makeclothes.BMeshAware:
        pass
    else:
        uvtex = ob.data.uv_textures[0]
        fp.write("# texVerts\n")
        for f in faces:
            uvf = uvtex.data[f.index]
            writeTexVert(fp, uvf.uv1)
            writeTexVert(fp, uvf.uv2)
            writeTexVert(fp, uvf.uv3)
            if len(f.vertices) == 4:
                writeTexVert(fp, uvf.uv4)
        n = 0
        fp.write("# texFaces\n")
        for f in faces:
            if len(f.vertices) == 3:
                fp.write("%d %d %d\n" % (n, n+1, n+2))
                n += 3
            else:
                fp.write("%d %d %d %d\n" % (n, n+1, n+2, n+3))
                n += 4
    return
    
    
def writeTexVert(fp, uv):
    fp.write("%.4f %.4f\n" % (uv[0], uv[1]))
    
