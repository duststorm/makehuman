# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; eithe.r version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the.
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
# Script copyright (C) MakeHuman Team 2001-2011
# Coding Standards:    See http://sites.google.com/site/makehumandocs/developers-guide

import bpy
from bpy.props import EnumProperty

from . import globvar as the
from . import utils

#
#   Select or delete action
#   Delete button really deletes action. Handle with care.
#
#   listAllActions(context):
#   findAction(name):
#   class VIEW3D_OT_McpUpdateActionListButton(bpy.types.Operator):
#

def listAllActions(context):
    scn = context.scene
    try:
        doFilter = scn['McpFilterActions']
        filter = context.object.name
        if len(filter) > 4:
            filter = filter[0:4]
            flen = 4
        else:
            flen = len(filter)
    except:
        doFilter = False
        
    the.actions = []     
    for act in bpy.data.actions:
        name = act.name
        if (not doFilter) or (name[0:flen] == filter):
            the.actions.append((name, name, name))
    bpy.types.Scene.McpActions = EnumProperty(
        items = the.actions,
        name = "Actions")  
    return

def findAction(name):
    for n,action in enumerate(the.actions):
        (name1, name2, name3) = action        
        if name == name1:
            return n
    raise NameError("Unrecognized action %s" % name)


class VIEW3D_OT_McpUpdateActionListButton(bpy.types.Operator):
    bl_idname = "mcp.update_action_list"
    bl_label = "Update action list"

    @classmethod
    def poll(cls, context):
        return context.object

    def execute(self, context):
        listAllActions(context)
        return{'FINISHED'}    

#
#   deleteAction(context):
#   class VIEW3D_OT_McpDeleteButton(bpy.types.Operator):
#

def selectedAction(scn):
    n = scn['McpActions']
    (name1, name2, name3) = the.actions[n]
    return name1

def deleteAction(context):
    listAllActions(context)
    scn = context.scene
    name = selectedAction(scn)
    print('Delete action', name)    
    try:
        act = bpy.data.actions[name]
    except:
        act = None
    if act:
        act.use_fake_user = False
        if act.users == 0:
            print("Deleting", act)
            n = findAction(name)
            the.actions.pop(n)
            bpy.data.actions.remove(act)
            print('Action', act, 'deleted')
            listAllActions(context)
            #del act
        else:
            print("Cannot delete. %s has %d users." % (act, act.users))

class VIEW3D_OT_McpDeleteButton(bpy.types.Operator):
    bl_idname = "mcp.delete"
    bl_label = "Delete action"

    @classmethod
    def poll(cls, context):
        return context.scene.McpReallyDelete

    def execute(self, context):
        deleteAction(context)
        return{'FINISHED'}    

#
#   deleteHash():
#   class VIEW3D_OT_McpDeleteHashButton(bpy.types.Operator):
#

def deleteHash():
    for act in bpy.data.actions:
        if act.name[0] == '#':
            utils.deleteAction(act)
    return 
    
class VIEW3D_OT_McpDeleteHashButton(bpy.types.Operator):
    bl_idname = "mcp.delete_hash"
    bl_label = "Delete hash actions"

    def execute(self, context):
        deleteHash()
        return{'FINISHED'}    

#
#   setCurrentAction(context):
#   class VIEW3D_OT_McpSetCurrentActionButton(bpy.types.Operator):
#

def setCurrentAction(context):
    listAllActions(context)
    name = selectedAction(context.scene)
    try:
        act = bpy.data.actions[name]
    except:
        print("Did not find action %s" % name)
        return
    context.object.animation_data.action = act
    print("Action set to %s" % act)
    return
    
class VIEW3D_OT_McpSetCurrentActionButton(bpy.types.Operator):
    bl_idname = "mcp.set_current_action"
    bl_label = "Set current action"

    def execute(self, context):
        setCurrentAction(context)
        return{'FINISHED'}    

########################################################################
#
#   class ActionPanel(bpy.types.Panel):
#

class ActionPanel(bpy.types.Panel):
    bl_label = "Mocap: Manage action"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        if context.object and context.object.type == 'ARMATURE':
            return True

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        layout.prop_menu_enum(context.scene, "McpActions")
        layout.prop(scn, 'McpFilterActions')
        layout.operator("mcp.update_action_list")
        layout.operator("mcp.set_current_action")
        layout.prop(scn, "McpReallyDelete")
        layout.operator("mcp.delete")
        layout.operator("mcp.delete_hash")

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

