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
# Script copyright (C) MakeHuman Team 2001-2013
# Coding Standards:    See http://www.makehuman.org/node/165
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
    makeclothes.printClothesHeader(fp, scn)
    fp.write("# name %s\n" % ob.name.replace(" ","_"))
    
    for mat in ob.data.materials:
        fp.write("# material %s\n" % mat.name)
        makeclothes.writeColor(fp, '  diffuse_color', '  diffuse_intensity', mat.diffuse_color, mat.diffuse_intensity)
        makeclothes.writeColor(fp, '  specular_color', '  specular_intensity', mat.specular_color, mat.specular_intensity)
        fp.write("  alpha %.3g\n" % mat.alpha)
        for mtex in mat.texture_slots:
            if mtex:
                print(mat.name, mtex.name)
                tex = mtex.texture
                fp.write("  texture %s" % tex.image.name)
                if mtex.use_map_color_diffuse:
                    fp.write(" diffuse %.3g" % mtex.diffuse_color_factor)
                if mtex.use_map_specular:
                    fp.write(" specular %.3g" % mtex.specular_factor)
                if mtex.use_map_alpha:
                    fp.write(" alpha %.3g" % mtex.alpha_factor)
                if mtex.use_map_translucency:
                    fp.write(" translucency %.3g" % mtex.translucency_factor)
                if mtex.use_map_normal:
                    fp.write(" bump %.3g" % mtex.normal_factor)
                if mtex.use_map_displacement:
                    fp.write(" displacement %.3g" % mtex.displacement_factor)
                fp.write("\n")        
    
    makeclothes.printFaceNumbers(fp, ob)    
    makeclothes.printMhcloUvLayers(fp, ob, scn, False)
    fp.close()
    print("File %s written" % outfile)
    return

    
    
    
def writeTexVert(fp, uv):
    fp.write("%.4f %.4f\n" % (uv[0], uv[1]))
    
