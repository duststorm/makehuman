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

import bpy
import os
import shlex
import sys

from . import fbx
from . import fbx_data
from . import fbx_mesh
from . import fbx_armature
from . import fbx_material
from . import fbx_object
from . import fbx_scene


#------------------------------------------------------------------
#   ParseNode
#------------------------------------------------------------------

class ParseNode:

    def __init__(self, key, parent):
        self.key = key.rstrip(':')
        self.values = []        
        self.parent = parent
        if parent:
            parent.values.append(self)
            self.level = self.parent.level+1
        else:
            self.level = 0
            
    def __repr__(self):
        return ("<ParseNode %s %d>" % (self.key, self.level))

    def write(self, fp=sys.stdout):
        fp.write('\n%s("%s" ' % (("  "*self.level), self.key))
        for val in self.values:
            if isinstance(val, ParseNode):
                val.write(fp)
            else:
                fp.write("%s " % val)
        fp.write('\n%s)' % (("  "*self.level)))
        
        
        
#------------------------------------------------------------------
#   Tokenizing
#------------------------------------------------------------------

class FbxLex(shlex.shlex):

    def __init__(self, stream):
        shlex.shlex.__init__(self, stream)
        self.commenters = ''
        self.wordchars += ':;-.'
        self.quotes = '"'
        

def tokenizeFbxFile(filepath):
    proot = pnode = ParseNode("RootNode:", None)
    fp = open(filepath, "rU")
    
    for line in fp:
        if len(line) > 0 and line[0] != ';':
            tokens = list(FbxLex(line))
            if len(tokens) > 0:
                key = tokens[0]
                if key == '}':
                    pnode = pnode.parent
                elif key[-1] == ':':
                    node1 = ParseNode(key, pnode)
                    for token in tokens[1:]:
                        if token == '{':
                            pnode = node1
                            break
                        elif token in ['Y','N']:
                            node1.values.append(token)
                        elif token not in [',','*']:
                            node1.values.append(eval(token))
            
    fp.close()    
    print("%s tokenized" % filepath)
    return proot
        
           
#------------------------------------------------------------------
#   Import
#------------------------------------------------------------------

def importFbxFile(context, filepath):
    fbx.activeFolder = os.path.dirname(filepath)
    print("Import", filepath)
    proot = tokenizeFbxFile(filepath)
    fbx_data.parseNodes(proot)    
    print("Tree parsed")
    fbx_data.buildObjects(context)          
    print("Objects built")
    

class VIEW3D_OT_TestImportButton(bpy.types.Operator):
    bl_idname = "fbx.test_import"
    bl_label = "Test Import"
    bl_options = {'UNDO'}

    def execute(self, context):
        importFbxFile(context, "/home/myblends/test.fbx")
        return {'FINISHED'}


print("fbx_import loaded")
