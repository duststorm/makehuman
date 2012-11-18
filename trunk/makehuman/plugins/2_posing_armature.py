#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

print 'importing Pose armature plugin'

import os
import numpy as np
import gui3d
import module3d
import mh
import aljabr

import armature
from armature import transformations as tm
import warpmodifier


#
#   Dynamic buttons
#

class PoseRadioButton(gui3d.RadioButton):
    def __init__(self, group, label, selected, view):
        self.view = view
        self.name = label
        self.file = os.path.join(mh.getPath(''), "data", "poses", label+".bvh")
        gui3d.RadioButton.__init__(self, group, label, selected)
        
        @self.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self, event)
            self.view.armature.readBvhFile(self.file, gui3d.app.selectedHuman)
            self.view.updateAll()
            self.view.poseBox.hide()


class BoneRadioButton(gui3d.RadioButton):
    def __init__(self, group, label, selected, view):
        self.view = view
        self.name = label
        gui3d.RadioButton.__init__(self, group, label, selected)
        
        @self.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self, event)
            bone = self.view.armature.bones[self.name]
            if self.view.activeBone:
                self.view.armatureObject.setColor(self.view.activeBone, [255, 255, 255, 255])
            self.view.armatureObject.setColor(bone, [0, 255, 0, 255])
            self.view.activeBone = bone
            self.view.status.setText(bone.name)
            self.view.updateSliders(bone)


class LayerCheckBox(gui3d.CheckBox):
    def __init__(self, label, selected, view):
        self.view = view
        self.name = label
        gui3d.CheckBox.__init__(self, label, selected)
        
        @self.event
        def onClicked(event):
            gui3d.CheckBox.onClicked(self, event)
            self.view.updateLayers()

#
#   Pose Window
#

class PoseArmatureTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Posing')            

        self.zone = ""
        self.rigtype = None
        self.armature = None
        self.armatureObject = None
        self.objects = []
        self.activeBone = None
        self.poseModifier = None
        
        cubeLayer = CLayerObject("Cube", 'CUBE')
        cubeLayer.buildCube((-8,8,0), 1.0)
        cubeLayer.finishBuild((0,0,0))
        self.cube = cubeLayer.object
        self.cube.hide()

        self.status = self.addView(gui3d.TextView(style=gui3d.TextViewStyle._replace(left=10, top=585, zIndex=9.1)))
        print "Status", self.status

        # Main box
        self.mainBox = self.addView(gui3d.GroupBox([10, 80, 9.0], 'Rotation', gui3d.GroupBoxStyle._replace(height=25+36*3+4+24*3+6)))
        self.quatBox = self.addView(gui3d.GroupBox([10, 480, 9.0], 'Quaternion', gui3d.GroupBoxStyle._replace(height=25+36*3+4+24*3+6)))
        self.eulerBox = self.addView(gui3d.GroupBox([10, 660, 9.0], 'Euler', gui3d.GroupBoxStyle._replace(height=25+36*3+4+24*3+6)))

        self.QWslider = self.quatBox.addView(gui3d.Slider(value = 1000.0, min = -1000.0, max = 1000.0, label = "W: %d"))
        self.QXslider = self.quatBox.addView(gui3d.Slider(value = 0.0, min = -1000.0, max = 1000.0, label = "X: %d"))
        self.QYslider = self.quatBox.addView(gui3d.Slider(value = 0.0, min = -1000.0, max = 1000.0, label = "Y: %d"))
        self.QZslider = self.quatBox.addView(gui3d.Slider(value = 0.0, min = -1000.0, max = 1000.0, label = "Z: %d"))

        self.EXslider = self.eulerBox.addView(gui3d.Slider(value = 0.0, min = -180, max = 180, label = "X: %d"))
        self.EYslider = self.eulerBox.addView(gui3d.Slider(value = 0.0, min = -180, max = 180, label = "Y: %d"))
        self.EZslider = self.eulerBox.addView(gui3d.Slider(value = 0.0, min = -180, max = 180, label = "Z: %d"))

        self.rotSlider = self.mainBox.addView(gui3d.Slider(value = 0.0, min = -180, max = 180, label = "Rotation: %d"))
        self.rotWorld = self.mainBox.addView(gui3d.CheckBox("World Rotation", False))
        rots = []
        self.rotX = self.mainBox.addView(gui3d.RadioButton(rots, "X", True)) 
        self.rotY = self.mainBox.addView(gui3d.RadioButton(rots, "Y", False)) 
        self.rotZ = self.mainBox.addView(gui3d.RadioButton(rots, "Z", False)) 
        
        self.showMesh = self.mainBox.addView(gui3d.CheckBox("Show Mesh", True))
        self.showRig = self.mainBox.addView(gui3d.CheckBox("Show Rig", False))
        self.restPosition = self.mainBox.addView(gui3d.CheckBox("Rest Position", False))
        self.quatSkinning = self.mainBox.addView(gui3d.CheckBox("Quaternion skinning", False))
        
        #self.updateButton = self.mainBox.addView(gui3d.Button("Update"))
        self.reloadCharacterButton = self.mainBox.addView(gui3d.Button("Reload Character"))
        self.zeroBoneButton = self.mainBox.addView(gui3d.Button("Zero Bone"))
        self.zeroAllButton = self.mainBox.addView(gui3d.Button("Zero All"))
        self.poseButton = self.mainBox.addView(gui3d.Button("Pose"))
        self.testButton = self.mainBox.addView(gui3d.Button("Test bones"))
        self.mainBox.hide()
        self.quatBox.hide()
        self.eulerBox.hide()

        # Rig select box        
        self.rigBox = self.addView(gui3d.GroupBox([10, 80, 9.0], 'Rig', gui3d.GroupBoxStyle._replace(height=25+24*14+6)))

        prisms = []
        self.prismButtons = {}
        first = True
        for type in ['Prism', 'Box', 'Line']:
            self.prismButtons[type] = self.rigBox.addView(gui3d.RadioButton(prisms, type, first))
            first = False

        self.selectRigButton = self.rigBox.addView(gui3d.Button("SelectRig"))

        rigs = []
        self.rigButtons = {}
        self.rigButtons["mhx"] = self.rigBox.addView(gui3d.RadioButton(rigs, "Mhx", False))
        path = "data/rigs"
        if not os.path.exists(path):
            print("Did not find directory %s" % path)
        else:
            buttons = []
            for name in ["game", "simple", "rigid"]:
            #for fname in os.listdir(path):
            #    (name, ext) = os.path.splitext(fname)
            #    if ext == ".rig":
                    self.rigButtons[name] = self.rigBox.addView(gui3d.RadioButton(rigs, name.capitalize(), False)) 
        self.rigBox.show()                    
        
        # Bone select box        
        self.boneBox = self.addView(gui3d.GroupBox([600, 80, 9.0], 'Bone', gui3d.GroupBoxStyle._replace(height=25+24*14+6)))
        self.boneButtons = {}
        self.boneBox.hide()
        
        # Pose select box        
        self.poseBox = self.addView(gui3d.GroupBox([300, 80, 9.0], 'Pose', gui3d.GroupBoxStyle._replace(height=25+24*14+6)))
        self.poseButtons = {}
        self.poseBox.hide()
        
        # Layer select box
        self.layerBox = self.addView(gui3d.GroupBox([750, 80, 9.0], 'Layers', gui3d.GroupBoxStyle._replace(height=25+24*14+6)))
        self.layerButtons = {}
        self.layerBox.hide()
        
         
        @self.selectRigButton.event
        def onClicked(event):     
            for name,button in self.prismButtons.items():
                if button.selected:
                    prismType = name
            for name,button in self.rigButtons.items():
                if button.selected:
                    rigtype = name
            if rigtype:
                self.selectRig(prismType, rigtype)                   
            
        @self.testButton.event
        def onClicked(event):
            #self.loadBvhFile("data/poses/walk.bvh")
            #return
            
            listBones = doTest1(self.armature.bones)
            self.updateAll()
            doTest2(listBones)
                
        @self.poseButton.event
        def onClicked(event):
            if not self.poseButtons:
                radio = []
                self.poseButtons = {}
                path = os.path.join(mh.getPath(''), "data", "poses")
                if not os.path.exists(path):
                    os.makedirs(path)
                for file in os.listdir(path):
                    (pose, ext) = os.path.splitext(file)
                    if ext.lower() == ".bvh":
                        button = PoseRadioButton(radio, pose, False, self)
                        self.poseButtons[pose] = self.poseBox.addView(button)
            self.poseBox.show()
                       
        @self.showMesh.event
        def onClicked(event):
            gui3d.CheckBox.onClicked(self.showMesh, event)
            self.updateAll()                        

        @self.showMesh.event
        def onClicked(event):
            gui3d.CheckBox.onClicked(self.showMesh, event)
            self.armature.quatSkinning = self.quatSkinning.selected
            self.updateAll()                        

        @self.showRig.event
        def onClicked(event):
            gui3d.CheckBox.onClicked(self.showRig, event)
            self.updateAll()                        

        @self.restPosition.event
        def onClicked(event):
            gui3d.CheckBox.onClicked(self.restPosition, event)
            self.updateAll()                        

        @self.zeroBoneButton.event
        def onClicked(event):
            bone = self.getSelectedBone()
            bone.zeroTransformation()
            self.zeroSliders()
            self.updateAll()

        @self.zeroAllButton.event
        def onClicked(event):
            self.zeroSliders()
            for bone in self.armature.controls:
                bone.zeroTransformation()
            self.updateAll()

        @self.reloadCharacterButton.event
        def onClicked(event):
            self.zeroSliders()
            human = gui3d.app.selectedHuman
            print "Reload", human.meshData.verts[0]
            amt = self.getArmature()
            self.armatureObject = None
            if amt:
                #amt.hide()
                gui3d.app.removeObject(amt)
            self.armature = armature.rigdefs.createRig(human, self.armature.rigtype, self.quatSkinning.selected)
            print "  ", human.meshData.verts[0]
            self.updateAll()
            print "  ", human.meshData.verts[0]

        @self.rotSlider.event
        def onChange(value):
            bone = self.getSelectedBone()
            if self.rotX.selected:
                axis = 0
            elif self.rotY.selected:
                axis = 1
            elif self.rotZ.selected:
                axis = 2
            bone.rotate(value, axis, self.rotWorld.selected)
            self.updateSliders(bone)
                                                       
        @self.QXslider.event
        def onChange(value):
            bone = self.getSelectedBone()
            bone.setRotationIndex(1, value, True)
            self.updateSliders(bone)
                
        @self.QYslider.event
        def onChange(value):
            bone = self.getSelectedBone()
            bone.setRotationIndex(2, value, True)
            self.updateSliders(bone)
                
        @self.QZslider.event
        def onChange(value):
            bone = self.getSelectedBone()
            bone.setRotationIndex(3, value, True)
            self.updateSliders(bone)
                
        @self.EXslider.event
        def onChange(value):
            bone = self.getSelectedBone()
            bone.setRotationIndex(1, value, False)
            self.updateSliders(bone)
                
        @self.EYslider.event
        def onChange(value):
            bone = self.getSelectedBone()
            bone.setRotationIndex(2, value, False)
            self.updateSliders(bone)
        
        @self.EZslider.event
        def onChange(value):
            bone = self.getSelectedBone()
            bone.setRotationIndex(3, value, False)
            self.updateSliders(bone)

        @self.cube.event
        def onMouseEntered(event):            
            gui3d.TaskView.onMouseEntered(self, event)
            gui3d.app.redraw()

        @self.cube.event
        def onMouseDragged(event):        
            gui3d.app.selectedHuman.show()
            self.getArmature().hide()
        
            gui3d.TaskView.onMouseDragged(self, event)

            if not self.showMesh.selected:
                gui3d.app.selectedHuman.hide()
            if self.showRig.selected:
                self.getArmature().show()
        
        @self.cube.event
        def onMouseWheel(event):        
            gui3d.app.selectedHuman.show()
            self.getArmature().hide()
        
            gui3d.TaskView.onMouseWheel(self, event)
            
            if not self.showMesh.selected:
                gui3d.app.selectedHuman.hide()
            if self.showRig.selected:
                self.getArmature().show()
        
    def selectRig(self, prismType, rigtype):     
        self.prismType = prismType
        self.rigtype = rigtype
        self.armature = armature.rigdefs.createRig(gui3d.app.selectedHuman, self.rigtype, self.quatSkinning.selected)
        self.armatureObject = None
        
        self.mainBox.show()
        self.quatBox.show()
        self.eulerBox.show()
        
        first = True
        radio = []
        self.boneButtons = {}
        for bone in self.armature.controls:
            print bone.name
            button = BoneRadioButton(radio, bone.name, first, self)
            self.boneButtons[bone.name] = self.boneBox.addView(button)
            first = False    
            
        self.boneBox.show()
        
        if self.rigtype == "mhx":
            self.layerButtons = []
            for bit,lname in armature.rigdefs.LayerNames:
                check = LayerCheckBox(lname, self.armature.visible & bit, self)
                self.layerButtons.append(self.layerBox.addView(check))
            self.layerBox.show()
        else:
            self.layerBox.hide()
            
        self.rigBox.hide()
        self.cube.show()
        self.updateAll()
 
 
    def updateSliders(self, bone):
        angles = bone.getRotation()
        self.setSliders(angles)
        self.updateAll()
        gui3d.app.redraw()
    
    def zeroSliders(self):
        self.setSliders((1000,0,0,0,0,0,0))
        
    def setSliders(self, angles):
        qw,qx,qy,qz,ax,ay,az = angles
        self.rotSlider.setValue(0)
        self.QWslider.setValue(qw)
        self.QXslider.setValue(qx)
        self.QYslider.setValue(qy)
        self.QZslider.setValue(qz)
        self.EXslider.setValue(ax)
        self.EYslider.setValue(ay)
        self.EZslider.setValue(az)            
                        

    def getSelectedBone(self):
        for (name,button) in self.boneButtons.items():
            if button.selected:
                #print "Bone", name, "selected"
                return self.armature.bones[name]
        print "BUG: No bone selected"                    
        return None

   
    def updateBones(self):
        bone = self.getSelectedBone()
        self.updateSliders(bone)

   
    def updateLayers(self):
        if not self.layerButtons:
            return
        vis = 0
        for n,button in enumerate(self.layerButtons):
            if button.selected:
                bit,lname = armature.rigdefs.LayerNames[n]
                vis |= bit
        self.armature.visible = vis
        self.updateAll()                


    def onShow(self, event):
        if not self.rigtype:
            self.selectRig("Prism", "rigid")       
        if self.armature:
            self.cube.show()
        self.activeBone = None
        #self.status.setText("")
        gui3d.TaskView.onShow(self, event)
        
     
    def onHide(self, event):
        self.cube.hide()
        self.activeBone = None
        #self.status.setText("")
        gui3d.TaskView.onHide(self, event)
        
     
    def updateAll(self):    
        if not self.armature:
            return
        self.armature.restPosition = self.restPosition.selected
        self.armature.quatSkinning = self.quatSkinning.selected
        human = gui3d.app.selectedHuman
        self.armature.update(human)
        amt = self.getArmature()

        if self.showMesh.selected:
            human.show()
        else:
            human.hide()
        #human.storeMesh()
            
        if not amt:
            pass
        elif self.showRig.selected:
            amt.show()
        else:
            amt.hide()        
        
        bone = self.getSelectedBone()

        
    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)

        human = gui3d.app.selectedHuman
        human.show()
        if self.armature:
            amt = self.getArmature()
            if amt:
                amt.hide()
        #human.restoreMesh()
        human.meshData.calcNormals()
        human.meshData.update()
        
    
    def getArmature(self):
        
        human = gui3d.app.selectedHuman
        #self.armature.update(human)
        
        if not self.armatureObject:            
            self.armatureObject = CArmatureObject(self.armature, self)
            self.armatureObject.build(human)
            self.armatureObject.setRotation(human.getRotation())        
        else:            
            self.armatureObject.update()
            self.armatureObject.setPosition(aljabr.vadd(human.getPosition(), [0.0, 0.0, 0.0]))             
            self.armatureObject.setRotation(human.getRotation())        
        return self.armatureObject
        
        
    def loadBvhFile(self, filepath): 
        if not self.rigtype:
            self.selectRig("Prism", "rigid")  
        human = gui3d.app.selectedHuman
        
        self.armature.readBvhFile(filepath, human)
        #self.updateAll()        
        #return
        
        folder = os.path.dirname(filepath)
        (fname, ext) = os.path.splitext(os.path.basename(filepath))
        modpath = '%s/${ethnic}-${gender}-${age}-%s.target' % (folder, fname)
        print filepath, modpath
        modifier = warpmodifier.WarpModifier(modpath, "body", "GenderAgeEthnicModifier2")
        if self.poseModifier:
            self.poseModifier.updateValue(human, 0.0)
        modifier.updateValue(human, 1.0)
        self.poseModifier = modifier        
     
        self.updateAll()        

     
    def loadHandler(self, human, values):
        print "loadHandler", values
        filepath = values[1]
        self.loadBvhFile(filepath)
       

    def saveHandler(self, human, file):
        return

     
        
#
#   Armature Object
#

class CArmatureObject:
    def __init__(self, armature, view):
        self.armature = armature
        self.view = view
        self.layers = {}
        for n in range(self.armature.last):
            self.layers[n] = None


    def getLayers(self, mask):
        layers = []
        bit = 1
        for n in range(self.armature.last):
            if bit & mask:
                layers.append(n)
            bit <<= 1
        return layers
        
        
    def setColor(self, bone, value):
        print bone.name, value
        for layer in self.layers.values():
            if layer:
                layer.setColor(bone, value)
        
        
    def build(self, human):
        for bone in self.armature.boneList:
            for n in self.getLayers(bone.layers):
                if not self.layers[n]:
                    self.layers[n] = CLayerObject('Layer%2d' % n, self.view.prismType)
                self.layers[n].buildBoneMesh(bone)
            
        for layer in self.layers.values():
            if layer:
                location = aljabr.vadd(human.getPosition(), [0.0, 0.0, 0.0])
                ob = layer.finishBuild(location)            
                    
                    
    def update(self):
        change = False
        for bone in self.armature.boneList:
            for n in self.getLayers(bone.layers & self.armature.visible):
                layer = self.layers[n]
                change |= layer.updateBoneMesh(bone)
            
        for n in self.getLayers(self.armature.visible):
            layer = self.layers[n]
            if layer:
                layer.update(change)
                    
                    
    def setRotation(self, rot):
        for layer in self.layers.values():
            if layer:
                layer.object.setRotation(rot)
                        

    def setPosition(self, pos):
        for layer in self.layers.values():
            if layer:
                layer.object.setPosition(pos)   
                       

    def show(self): 
        bit = 1
        for n in range(self.armature.last):
            layer = self.layers[n]
            if layer:
                if bit & self.armature.visible:
                    layer.object.show()
                else:
                    layer.object.hide()
            bit <<= 1

                        
    def hide(self): 
        for layer in self.layers.values():
            if layer:
                layer.object.hide()    


#
#   Visual representation of armature
#

class CLayerObject:
    def __init__(self, name, prismType):
        self.mesh = None
        self.object = None
        self.prisms = {}
        self.prismType = prismType
        self.nVerts = 0
        self.coords = None
        self._data = []

        self.mesh = module3d.Object3D(name)

        """
        dummy = module3d.Object3D('Dummy%2d' % self.index)
         gui3d.app.addObject(gui3d.Object([0.0, 0.0, 0.0], dummy))  
        
        @self.object.event
        def onMouseEntered(self, event):
            print "Emtered", event

        @self.object.event
        def onMouseDown(self, event):
            print "Dpwm", event

        @self.object.event
        def onMouseDragged(self, event):
            print "Dragged", event

        @self.object.event
        def onMouseMoved(self, event):
            print "Moved", event

        @self.object.event
        def onMouseUp(self, event):
            print "Up", event
        """

    
    def finishBuild(self, location):
        coord = []
        faces = []
        group = []
        for name, p, f in self._data:
            fg = self.mesh.createFaceGroup(name)
            coord.append(p)
            faces.append(f)
            group.append(np.zeros(len(f), dtype=np.uint16) + fg.idx)
        del self._data

        self.coords = np.vstack(coord)
        print "fb", len(coord), len(self.coords)
        self.mesh.setCoords(self.coords)
        self.mesh.setUVs(np.zeros((1, 2), dtype=np.float32))
        self.mesh.setFaces(np.vstack(faces), None, np.hstack(group))

        self.mesh.setCameraProjection(0)
        self.mesh.setShadeless(0)
        self.mesh.setSolid(0)
        self.mesh.calcNormals()
        self.mesh.updateIndexBuffer()

        self.object = gui3d.app.addObject( gui3d.Object(location, self.mesh) )  
        
        for fg in self.mesh.faceGroups:
            if not fg.parent:
                print fg, fg.parent
                halt
        return self.object

    
    def setColor(self, bone, value):
        for fg in self.mesh.faceGroups:
            if fg.name == bone.name:
                fg.setColor(value)
                return
                
    
    def buildBoneMesh(self, bone):    
        points, faces = bone.prismPoints(self.prismType)
        p,n = self.addPrism(bone.name, points, faces)
        self.prisms[bone.name] = (p, self.nVerts)
        self.nVerts += n
        
        
    def buildCube(self, location, scale):
        offsets = armature.rigdefs.CBone.PrismVectors['Cube']
        points = []
        for dx in offsets:
            points.append( location + scale*dx[:3] )
        faces = armature.rigdefs.CBone.PrismFaces['Box']
        p,n = self.addPrism('Cube', points, faces)
        self.prisms['Cube'] = (p, 0)
        self.nVerts = n       
            
            
    def update(self, change):
        if 0 and change:
            print "Armature has changed"
            #gui3d.app.removeObject(self.armatureObject)
            self.armatureObject.hide()
            self.armatureObject = None
            self.mesh = None
            self.getArmature()
        else:
            self.mesh.setCoords(self.coords)
            self.mesh.calcNormals()
            self.mesh.update()

        
    def updateBoneMesh(self, bone):
        try:
            prism,index = self.prisms[bone.name]
        except KeyError:
            return True
        self.updatePrism(bone, index)
        return False


    def addPrism(self, name, points, faces):
        p = np.asarray(points, dtype=np.float32)
        f = np.asarray(faces, dtype=np.uint32)
        self._data.append((name, p, f + self.nVerts))
        return points[0], len(points)
            
       
    def updatePrism(self, bone, index):            
        points, faces = bone.prismPoints(self.prismType)
        for n,p in enumerate(points):
            self.coords[index+n] = p
            
            


#
#   Testing poses
#

thePoseBoneFile = os.path.expanduser("~/documents/makehuman/posebones.txt")
thePosesFile = os.path.expanduser("~/documents/makehuman/poses_mh.txt")
 
def doTest1(bones):            
    try:
        fp = open(thePoseBoneFile)
    except:
        print "Did not find", thePoseBoneFile
        return
    readBones = []
    setBones = []
    for line in fp:
        words = line.split()
        if len(words) == 0:
            continue
        elif len(words) == 1:
            bone = bones[words[0]]
            readBones.append((bone,[]))
        elif len(words) == 4:
            bone = bones[words[0]]   
            coords = (float(words[1]), float(words[2]), float(words[3]))
            setBones.append((bone, coords))
    fp.close()
    
    for bone, coords in setBones:        
        bone.setRotationIndex(1, coords[0], False)
        bone.setRotationIndex(2, coords[1], False)
        bone.setRotationIndex(3, coords[2], False)
        #bone.setRotation(coords)
        angles = bone.getRotation()
    return setBones+readBones
    

def doTest2(listBones):            
    fp = open(thePosesFile, "w")
    for bone,coords in listBones:
        fp.write("\n%s %.4f\n" % (bone.name, bone.roll)) 
        writeMat(fp, "Rest", bone.matrixRest)
        writeMat(fp, "Global", bone.matrixGlobal)
        pose = bone.getPoseFromGlobal()
        writeMat(fp, "Pose", pose)
        xyz = tm.euler_from_matrix(pose, axes='sxyz')
        fp.write("XYZ %.4g %.4g %.4g\n" % tuple(xyz))
        zyx = tm.euler_from_matrix(pose, axes='szyx')
        fp.write("ZYX %.4g %.4g %.4g\n" % tuple(zyx))
        #writeMat(fp, "Pose0", bone.matrixPose)
    fp.close()
    

def writeMat(fp, string, mat):
    fp.write("%s\n[" % string)
    for n in range(4):
        row = mat[n]
        fp.write( "( %.4f, %.4f, %.4f, %.4f)\n" % (row[0], row[1], row[2], row[3]) )
        

def printArray(array):
    print "["
    for row in array:
        print " ", row
    print "]"

#
#   Pose library
#

class Action:

    def __init__(self, human, filename, poseArmatureTaskView, postAction=None):
        self.name = 'Load pose'
        self.human = human
        self.filename = filename
        self.poseArmatureTaskView = poseArmatureTaskView
        self.postAction = postAction
        self.before = {}

        #for name, modifier in self.poseArmatureTaskView.modifiers.iteritems():
        #    self.before[name] = modifier.getValue(self.human)

    def do(self):
        self.poseArmatureTaskView.loadBvhFile(self.filename)
        return True

    def undo(self):
        if self.postAction:
            self.postAction()
        return True

class PoseLoadTaskView(gui3d.TaskView):

    def __init__(self, category, poseArmatureTaskView):

        gui3d.TaskView.__init__(self, category, 'poses', label='Poses')

        self.poseArmatureTaskView = poseArmatureTaskView

        self.globalPoseArmaturePath = os.path.join('data', 'poses')
        self.poseArmaturePath = os.path.join(mh.getPath(''), 'data', 'poses')

        if not os.path.exists(self.poseArmaturePath):
            os.makedirs(self.poseArmaturePath)

        self.filechooser = self.addView(gui3d.FileChooser([self.globalPoseArmaturePath, self.poseArmaturePath], 'bvh', 'png', 'data/poses/notfound.png'))

        @self.filechooser.event
        def onFileSelected(filename):

            gui3d.app.do(Action(gui3d.app.selectedHuman, filename, self.poseArmatureTaskView))
            
            gui3d.app.switchCategory('Modelling')

    def onShow(self, event):

        # When the task gets shown, set the focus to the file chooser
        gui3d.TaskView.onShow(self, event)
        gui3d.app.selectedHuman.hide()
        self.filechooser.setFocus()

    def onHide(self, event):
        gui3d.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
        
    def onResized(self, event):
        self.filechooser.onResized(event)

#
#   Loading
#

category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements
def load(app):
    category = app.getCategory('Posing')
    taskview = category.addView(PoseArmatureTaskView(category))

    app.addLoadHandler('poses', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

    category = app.getCategory('Library')
    category.addView(PoseLoadTaskView(category, taskview))
    print 'pose loaded'
            
    @taskview.event
    def onMouseDown(event):
        part = app.getSelectedFaceGroup()
        print part.name

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements

def unload(app):  
    print 'pose unloaded'
    
