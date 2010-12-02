#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Renderman Export functions

B{Project Name:}      MakeHuman

B{Product Home Page:} U{http://www.makehuman.org/}

B{Code Home Page:}    U{http://code.google.com/p/makehuman/}

B{Authors:}           Manuel Bastioni, Marc Flerackers

B{Copyright(c):}      MakeHuman Team 2001-2010

B{Licensing:}         GPL3 (see also U{http://sites.google.com/site/makehumandocs/licensing})

B{Coding Standards:}  See U{http://sites.google.com/site/makehumandocs/developers-guide}

Abstract
========

This module implements functions to export a human model in Renderman format and render it
using either the Aqsis or Renderman engine.

The MakeHuman data structures are transposed into renderman objects.

"""

import mh
import os
import aljabr
import files3d
import subprocess
import random
import hair
import time
import math



class MaterialParameter:

    def __init__(self, type, name, val):
        self.type = type
        self.val = val
        self.name = name



class RMRMaterial:

    def __init__(self, name):

        self.name = name
        self.type = "Surface"
        self.parameters = []

    def writeRibCode(self, file):
        file.write('\t\t%s "%s" '%(self.type,self.name))
        print "Writing %s material"%(self.name)
        for p in self.parameters:
            print p.name, p.val
            if p.type == "float":
                file.write('"%s %s" [%f] '%(p.type, p.name, p.val))
            if p.type == "string":
                file.write('"%s %s" "%s" '%(p.type, p.name, p.val))
            if p.type == "color":
                file.write('"%s %s" [%f %f %f] '%(p.type, p.name, p.val[0],  p.val[1],  p.val[2]))
        file.write('\n')

    def setParameter(self, name, val, pType = "float"):
        newParamater = True
        for p in self.parameters:
            if p.name == name:
                newParamater = False
                p.val = val
        if newParamater == True:
            print "Setting paramater %s with value %s"%(name, str(val))
            self.parameters.append(MaterialParameter(pType, name, val))
            for p in  self.parameters:
                print p.name, p.val
            
            


class RMRLight:

    lightCounter = 0

    def __init__(self, ribsPath, position = [0,0,0], lookAt = [0,0,0], intensity = 1.0, type = "pointlight", blur = 0.025):

        RMRLight.lightCounter += 1
        self.ribsPath = ribsPath
        self.position = position
        self.lookAt = lookAt
        self.type = type
        self.intensity = intensity
        self.color = [1,1,1]
        self.counter = RMRLight.lightCounter
        self.samples = 64
        self.blur = blur        
        self.coneangle = 0.25
        self.roll = None
        self.shadowMapDataFile = os.path.join(self.ribsPath,"%sshadow%d.zfile"%(self.type, self.counter)).replace('\\', '/')
        self.ambientOcclusionDataFile = os.path.join(self.ribsPath,"occlmap.sm" ).replace('\\', '/')
    def __str__(self):
        return "Renderman %s Light, from [%f,%f,%f] to [%f %f %f]"%(self.type,self.position[0],self.position[1],self.position[2],self.lookAt[0],self.lookAt[1],self.lookAt[2])

    def writeRibCode(self, ribfile, n=0):
        # remember z in opengl -> -z in renderman
        if self.type == "pointlight":
             ribfile.write('\tLightSource "pointlight" %i  "from" [%f %f %f] "intensity" %f "color lightcolor" [%f %f %f]\n' % (n, self.position[0], self.position[1], self.position[2],
                      self.intensity, self.color[0], self.color[1], self.color[2]))
        if self.type == "ambient":
            ribfile.write('\tLightSource "ambientlight" %i "intensity" [%f] "color lightcolor" [%f %f %f]\n'%(n, self.intensity, self.color[0], self.color[1], self.color[2]))
        if self.type == "envlight":
            ribfile.write('\tLightSource "envlight" %i "string filename" "%s" "intensity" [%f] "float samples" [ %f ] "float blur" [ %f ]\n'%(n, self.ambientOcclusionDataFile, self.intensity, self.samples, self.blur))
        if self.type == "shadowspot":
            ribfile.write('\tLightSource "shadowspot" %i "intensity" [%f] "from" [%f %f %f] "to" [%f %f %f] "coneangle" [%f] "string shadowname" ["%s"] "float blur" [%f]\n'%(n, self.intensity,\
             self.position[0],self.position[1],self.position[2], self.lookAt[0], self.lookAt[1], self.lookAt[2],\
             self.coneangle, self.shadowMapDataFile, self.blur))



    def shadowRotate(self, ribfile, angle, x, y, z):
        """
        To place the cam for shadow map
        """
        if math.fabs(angle) > 0.001:
            ribfile.write("Rotate %0.2f %0.2f %0.2f %0.2f\n"% (angle, x, y, z))

    def shadowTranslate(self, ribfile, dx, dy, dz):
        """
        To place the cam for shadow map
        """
        ribfile.write("Translate %0.2f %0.2f %0.2f\n"%(dx, dy, dz))

    def shadowProjection(self, ribfile):
        if self.coneangle != 0.0:
            fov = self.coneangle * 360.0/math.pi
            ribfile.write("Projection \"perspective\" \"fov\" [%0.2f]\n"%(fov))

    def pointToAim(self, ribfile, direction):
        """
        pointToAim(): rotate the world so the direction vector points in
        positive z by rotating about the y axis, then x. The cosine
        of each rotation is given by components of the normalized
        direction vector. Before the y rotation the direction vector
        might be in negative z, but not afterward.
        """

        if (direction[0]==0) and (direction[1]==0) and (direction[2]==0):
            return

        #The initial rotation about the y axis is given by the projection of
        #the direction vector onto the x,z plane: the x and z components
        #of the direction.

        xzlen = math.sqrt(direction[0]*direction[0]+direction[2]*direction[2]);
        if xzlen == 0:
            if direction[1] < 0:
                yrot = 180
            else:
                yrot = 0
        else:
            yrot = 180*math.acos(direction[2]/xzlen)/math.pi;

        #The second rotation, about the x axis, is given by the projection on
        #the y,z plane of the y-rotated direction vector: the original y
        #component, and the rotated x,z vector from above.

        yzlen = math.sqrt(direction[1]*direction[1]+xzlen*xzlen);
        xrot = 180*math.acos(xzlen/yzlen)/math.pi; #yzlen should never be 0

        if direction[1] > 0:
            self.shadowRotate(ribfile, xrot, 1.0, 0.0, 0.0)
        else:
            self.shadowRotate(ribfile, -xrot, 1.0, 0.0, 0.0)

        #The last rotation declared gets performed first
        if direction[0] > 0:
            self.shadowRotate(ribfile, -yrot, 0.0, 1.0, 0.0)
        else:
            self.shadowRotate(ribfile, yrot, 0.0, 1.0, 0.0)

    def placeShadowCamera(self, ribfile):
        direction = aljabr.vsub(self.lookAt, self.position)
        print "VIEW",self.lookAt, self.position
        print "DIRECTION: ", direction
        self.shadowProjection(ribfile)
        if self.roll:
            self.shadowRotate(ribfile,-self.roll, 0.0, 0.0, 1.0);
        self.pointToAim(ribfile, direction);
        self.shadowTranslate(ribfile, -self.position[0], -self.position[1], -self.position[2])


class RMNObject:

    def __init__(self, name, obj = None):

        self.groupsDict = {}
        self.facesGroup = None
        self.material = None
        self.materialBump = None
        self.name = name
        self.facesIndices = []
        
        #Note: base.obj must have not redundat facegroups (This mean each face can have an unique group)
        #In case, Aqsis will crash.


        if obj:
            self.meshData = obj
            self.name = obj.name
            self.wavefrontPath = os.path.join('data','3dobjs',obj.name)
            self.facesIndices = files3d.loadFacesIndices(self.wavefrontPath, True)
            self.facesUVvalues = obj.uvValues

            #create a dictionary for all facesgroups
            currentGroup = "Empty"
            indices = []
            for faceIdx in self.facesIndices:
                if type(faceIdx) == type("abc"):
                    self.groupsDict[currentGroup]=indices
                    indices = []
                    currentGroup = faceIdx
                else:
                    indices.append(faceIdx)
                self.groupsDict[currentGroup]=indices #add latest group


    def writeRibCode(self, ribPath ):


        facesUVvalues = self.meshData.uvValues #TODO usa direttamente self.

        ribObjFile = file(ribPath, 'w')
        ribObjFile.write('Declare "st" "facevarying float[2]"\n')
        ribObjFile.write('Declare "Cs" "facevarying color"\n')
        ribObjFile.write('SubdivisionMesh "catmull-clark" [')
        for faceIdx in self.facesIndices:
            ribObjFile.write('%i ' % len(faceIdx))
        ribObjFile.write('] ')

        ribObjFile.write('[')
        for faceIdx in self.facesIndices:
            faceIdx.reverse()
            if len(faceIdx) == 3:
                ribObjFile.write('%i %i %i ' % (faceIdx[0][0], faceIdx[1][0], faceIdx[2][0]))
            if len(faceIdx) == 4:
                ribObjFile.write('%i %i %i %i ' % (faceIdx[0][0], faceIdx[1][0], faceIdx[2][0], faceIdx[3][0]))
        ribObjFile.write(']')

        ribObjFile.write('''["interpolateboundary"] [0 0] [] []"P" [''')
        for vert in self.meshData.verts:
            ribObjFile.write('%f %f %f ' % (vert.co[0], vert.co[1], -vert.co[2]))
        ribObjFile.write('] ')

        ribObjFile.write('\n"st" [')
        for faceIdx in self.facesIndices:
            for idx in faceIdx:
                uvIdx = idx[1]
                uvValue = facesUVvalues[uvIdx]
                ribObjFile.write('%s %s ' % (uvValue[0], 1 - uvValue[1]))
        ribObjFile.write(']')
        ribObjFile.close()

    def joinGroupIndices(self):
        for g in self.facesGroup:
            gIndices = self.groupsDict[g]
            self.facesIndices.extend(gIndices)


class RMRHuman(RMNObject):

    def __init__(self, human, name, obj, ribRepository):

        RMNObject.__init__(self, name, obj)
        self.subObjects = []
        self.human = human
        self.hairFileName = name + "_hairs.rib"

        #hairs
        self.hairsClass = human.hairs
        self.hairFilePath = os.path.join(ribRepository, self.hairFileName)

        #materials  TODO: remove the hardcoded texture names.
        self.skinMat = RMRMaterial("skin2")
        self.skinMat.parameters.append(MaterialParameter("string", "colortexture", "texture.texture"))
        self.skinMat.parameters.append(MaterialParameter("string", "spectexture", "texture_ref.texture"))
        self.skinMat.parameters.append(MaterialParameter("float", "Ks", 0.1))
        self.skinMat.parameters.append(MaterialParameter("string", "ssstexture", "lightmap.texture"))
        self.skinMat.parameters.append(MaterialParameter("string", "aotexture", "occlmap.texture"))

        #self.skinMat.parameters.append(MaterialParameter("float", "Value", 2.0))

        self.hairMat = RMRMaterial("hair")
        self.hairMat.parameters.append(MaterialParameter("float", "Kd", .5))
        self.hairMat.parameters.append(MaterialParameter("float", "Ks", 5))
        self.hairMat.parameters.append(MaterialParameter("float", "roughness", 0.08))
        self.hairMat.parameters.append(MaterialParameter("color", "rootcolor", self.human.hairColor))
        self.hairMat.parameters.append(MaterialParameter("color", "tipcolor", self.human.hairColor))

        self.skinBump = RMRMaterial("skinbump")
        self.skinBump.type = "Displacement"
        self.skinBump.parameters.append(MaterialParameter("string", "bumpTexture", "texture_bump.texture"))
        self.skinBump.parameters.append(MaterialParameter("float", "bumpVal", 0.001))
        
        self.corneaMat = RMRMaterial("cornea")        
        
        self.eyeBallMat = RMRMaterial("eyeball")        
        self.eyeBallMat.parameters.append(MaterialParameter("string", "colortexture", "texture.texture"))
        
    def getHumanParameters(self):       

        parameters = []
        
        #character parameters
        humanCategories = [ "_flaccid",
                            "_muscle",
                            "_heavy",
                            "_light",
                            "_flaccid_heavy",
                            "_flaccid_light",
                            "_muscle_heavy",
                            "_muscle_light"]
        humanAges = ["_young", "_old","_child"]
        humanTypes = ["female","male"]

        #Generation of values, in order to apply the corrections data
        #according the character parameters
        averageWeightVal = 1 - (self.human.underweightVal + self.human.overweightVal)
        averageToneVal = 1 - (self.human.muscleVal + self.human.flaccidVal)
        humanCategoriesVal = [self.human.flaccidVal*averageWeightVal,
                            self.human.muscleVal*averageWeightVal,
                            self.human.overweightVal*averageToneVal,
                            self.human.underweightVal*averageToneVal,
                            self.human.flaccidVal*self.human.overweightVal,
                            self.human.flaccidVal*self.human.underweightVal,
                            self.human.muscleVal*self.human.overweightVal,
                            self.human.muscleVal*self.human.underweightVal]
        humanTypesVal = [self.human.femaleVal,self.human.maleVal]
        humanAgesVal = [self.human.youngVal,self.human.oldVal,self.human.childVal]
        
        for n1,h1 in enumerate(humanTypes):
            for n2,h2 in enumerate(humanAges):
                targetLabel1 = h1+h2
                targetValue1 = humanTypesVal[n1]*humanAgesVal[n2]
                #traslExamples[targetLabel1] = targetValue1
                #print targetLabel1,targetValue1
                parameters.append([targetLabel1,targetValue1])
                for n3,h3 in enumerate(humanCategories):
                    targetLabel2 = h1+h2+h3
                    targetValue2 = humanTypesVal[n1]*humanAgesVal[n2]*humanCategoriesVal[n3]
                    #traslExamples[targetLabel2] = targetValue2
                    #print targetLabel2,targetValue2
                    parameters.append([targetLabel2,targetValue2])
        return parameters

    def subObjectsInit(self):

        #SubObjects
        self.rEyeBall = RMNObject(name = "right_eye_ball")
        self.rEyeBall.groupsDict = self.groupsDict
        self.rEyeBall.meshData = self.meshData
        self.rEyeBall.facesGroup = set(['r-eye-ball'])
        self.rEyeBall.material = self.eyeBallMat
        self.rEyeBall.joinGroupIndices()

        self.lEyeBall = RMNObject(name = "left_eye_ball")
        self.lEyeBall.groupsDict = self.groupsDict
        self.lEyeBall.meshData = self.meshData
        self.lEyeBall.facesGroup = set(['l-eye-ball'])
        self.lEyeBall.material = self.eyeBallMat
        self.lEyeBall.joinGroupIndices()

        self.rCornea = RMNObject(name = "right_cornea")
        self.rCornea.groupsDict = self.groupsDict
        self.rCornea.meshData = self.meshData
        self.rCornea.facesGroup = set(['r-eye-cornea'])
        self.rCornea.material = self.corneaMat
        self.rCornea.joinGroupIndices()

        self.lCornea = RMNObject(name = "left_cornea")
        self.lCornea.groupsDict = self.groupsDict
        self.lCornea.meshData = self.meshData
        self.lCornea.facesGroup = set(['l-eye-cornea'])
        self.lCornea.material = self.corneaMat
        self.lCornea.joinGroupIndices()

        teethGr = set()
        allGr = set()
        nailsGr = set()
        toSubtract = set()
        for f in self.meshData.facesGroups:
            if 'joint' not in f.name:
                allGr.add(f.name)
            if 'teeth' in f.name:
                teethGr.add(f.name)
            if 'nail' in f.name:
                nailsGr.add(f.name)

        self.teeth = RMNObject(name = "teeth")
        self.teeth.groupsDict = self.groupsDict
        self.teeth.meshData = self.meshData
        self.teeth.facesGroup = teethGr
        self.teeth.material = self.skinMat
        self.teeth.joinGroupIndices()

        self.nails = RMNObject(name = "nails")
        self.nails.groupsDict = self.groupsDict
        self.nails.meshData = self.meshData
        self.nails.facesGroup = nailsGr
        self.nails.material = self.skinMat
        self.nails.joinGroupIndices()

        for s in [self.rEyeBall,self.lEyeBall,self.rCornea,\
            self.lCornea,self.teeth,self.nails]:
            toSubtract = toSubtract.union(s.facesGroup)

        self.skin = RMNObject(name = "skin")
        self.skin.groupsDict = self.groupsDict
        self.skin.meshData = self.meshData
        self.skin.facesGroup = allGr.difference(toSubtract)
        self.skin.material = self.skinMat
        self.skin.materialBump = self.skinBump
        self.skin.joinGroupIndices()

        #parts to render with different material
        self.subObjects = [self.skin,self.rEyeBall,self.lEyeBall,
                        self.rCornea,self.lCornea,self.nails]

    def getSubObject(self, name):
        for subOb in self.subObjects:
            if subOb.name == name:
                return subObj

    def getHumanPosition(self):
        return (self.human.getPosition()[0], self.human.getPosition()[1],\
                self.human.getRotation()[0], self.human.getRotation()[1])

    def adjustHairStyle(self):
        hair.adjustHair(self.human, self.hairsClass)

    def writeHairsInclusion(self, ribfile):
        archivePath = self.hairFilePath.replace('\\', '/')
        ribfile.write('\t\tReadArchive "%s"\n'%(archivePath))

    def writeHairsCurve(self):


        # Write the full hairstyle

        totalNumberOfHairs = 0
        self.hairsClass.humanVerts = self.human.meshData.verts
        hairs = self.hairsClass.generateHairToRender()
        print 'Writing hairs'

        hairFile = open(self.hairFilePath, 'w')

        hairFile.write('\t\tBasis "b-spline" 1 "b-spline" 1\n')
        for strands in hairs:

            hDiameter = self.hairsClass.hairDiameterMultiStrand * random.uniform(0.5, 1)
            totalNumberOfHairs += 1
            hairFile.write('Curves "cubic" [%i] "nonperiodic" "P" ['% len(strands))

            #renderman engine understand cubic spline not connected to endpoints, whilest makehuman and blender hair particle connect endpoints
            hairFile.write('%s %s %s ' % (strands[0][0], strands[0][1], -strands[0][2]))  # z * -1 blender  to renderman coords

            for cP in strands:
                hairFile.write('%s %s %s ' % (cP[0], cP[1], -cP[2]))  # z * -1 blender  to renderman coords

            #renderman engine understand cubic spline not connected to endpoints, whilest makehuman and blender hair particle connect endpoints
            hairFile.write('%s %s %s ' % (strands[len(strands)-1][0], strands[len(strands)-1][1],\
            -strands[len(strands)-1][2]))  # z * -1 blender  to renderman coords

            #if random.randint(0, 3) >= 1:
            #    hairFile.write(']\n"N" [')
            #    for cP in strands:
            #            hairFile.write('0 1 0 ')  # arbitrary normals
            hairFile.write(']  "constantwidth" [%s]\n' % hDiameter)

        hairFile.close()
        print 'Totals hairs written: ', totalNumberOfHairs
        #print 'Number of tufts', len(hairs)


    def __str__(self):
        return "Human Character"


class RMRTexture:

    def __init__(self, picturename, appTexturePath, usrTexturePath):

        self.picturename = os.path.join(appTexturePath, picturename).replace('\\', '/')
        self.texturename = os.path.join(usrTexturePath,os.path.splitext(picturename)[0]+".texture").replace('\\', '/')
        self.swrap = "periodic"
        self.twrap = "periodic"
        self.filterfunc = "box"
        self.swidth = 1
        self.twidth = 1

    def writeRibCode(self, ribfile):
        ribfile.write('MakeTexture "%s" "%s" "%s" "%s" "%s" %d %d\n' %\
                        (self.picturename,self.texturename,self.swrap,self.twrap,\
                        self.filterfunc,self.swidth,self.twidth))
                        
                        
class RMRHeader:
    
    def __init__(self):
        
        self.screenwindow = None
        self.options = {}       
        self.statistics =  ["endofframe", '[1]']
        self.projection = "perspective"
        self.sizeFormat = [800,600]
        self.clipping = None
        self.pixelsamples = [2, 2]
        self.fov = None
        self.shadingRate = 1  
        self.displayName = None
        self.displayType = None 
        self.displayColor = None
        self.displayName2 = None
        self.displayType2 = None
        self.displayColor2 = None
        self.cameraX = None
        self.cameraY = None
        self.cameraZ = None    
        self.searchShaderPath = ""
        self.searchTexturePath = ""
        self.searchArchivePath = ""
        self.bucketSize = None
        self.eyesplits = None
        self.depthfilter = None
        self.sides = 2
        self.pixelFilter = None
        self.shadingInterpolation = None
        
    def setCameraPosition(self, camX,camY,camZ):
        self.cameraX = camX
        self.cameraY = camY
        self.cameraZ = camZ        
    
    def setSearchShaderPath(self, usrShaderPath):
        self.searchShaderPath = "%s:&"%(usrShaderPath.replace('\\', '/'))
        
    def setSearchTexturePath(self, usrTexturePath):
        self.searchTexturePath = "%s:&"%(usrTexturePath.replace('\\', '/'))
        
    def setSearchArchivePath(self, usrArchivePath):
        self.searchArchivePath = "%s:&"%(usrArchivePath.replace('\\', '/'))  
        
    def writeRibCode(self, ribfile):        
        #Write headers
        if self.bucketSize:
            ribfile.write('Option "limits" "bucketsize" [%d %d]\n'%(self.bucketSize[0], self.bucketSize[1]))
        if self.eyesplits:
            ribfile.write('Option "limits" "eyesplits" [%d]\n'%(self.eyesplits))
        if self.depthfilter:
            ribfile.write('Hider "hidden" "depthfilter" "%s"\n'%(self.depthfilter))
        if self.pixelFilter:
            ribfile.write('PixelFilter "%s" 1 1\n'%(self.pixelFilter))
        if self.projection == "perspective" and self.fov:
            ribfile.write('Projection "%s" "fov" %f\n' % (self.projection, self.fov))
        if self.projection == "orthographic":
            ribfile.write('Projection "%s"\n' % (self.projection))
        if self.shadingInterpolation:
            ribfile.write('ShadingInterpolation "%s"\n' % self.shadingInterpolation)
        if self.clipping:    
            ribfile.write('Clipping %f %f\n'%(self.clipping[0], self.clipping[1]))
        if self.screenwindow:    
            ribfile.write('ScreenWindow %f %f %d %d\n'%(self.screenwindow[0], self.screenwindow[1], self.screenwindow[2], self.screenwindow[3]))
        ribfile.write('Option "statistics" "%s" %s\n'%(self.statistics[0], self.statistics[1]))
        ribfile.write('Option "searchpath" "shader" "%s"\n' %(self.searchShaderPath))
        ribfile.write('Option "searchpath" "texture" "%s"\n' %(self.searchTexturePath))        
        ribfile.write('Format %s %s 1\n' % (self.sizeFormat[0],self.sizeFormat[1]))
        ribfile.write('Sides %d\n' % (self.sides))
        
        ribfile.write('PixelSamples %s %s\n' % (self.pixelsamples[0], self.pixelsamples[1]))
        ribfile.write('ShadingRate %s \n' % self.shadingRate)
        if self.displayName:
            ribfile.write('Display "%s" "%s" "%s"\n'%(self.displayName, self.displayType, self.displayColor))   
        if self.displayName2:
            ribfile.write('Display "+%s" "%s" "%s"\n'%(self.displayName2, self.displayType2, self.displayColor2))       
        if (self.cameraX != None) and (self.cameraY != None) and (self.cameraZ != None):     
            ribfile.write('\tTranslate %f %f %f\n' % (self.cameraX, self.cameraY, self.cameraZ))
    


class RMRScene:

    #def __init__(self, MHscene, camera):
    def __init__(self, app):
        MHscene = app.scene3d
        camera = app.modelCamera
        
        #rendering properties
        self.camera = camera
        
        
        self.app = app
        self.lastUndoItem = None
        self.lastRotation = [0,0,0]
        self.lastCameraPosition = [self.camera.eyeX, -self.camera.eyeY, self.camera.eyeZ]
        self.firstTimeRendering = True

        #resources paths
        self.renderPath = mh.getPath('render')
        self.ribsPath = os.path.join(self.renderPath, 'ribFiles')
        self.usrShaderPath = os.path.join(self.ribsPath, 'shaders')
        self.usrTexturePath = os.path.join(self.ribsPath, 'textures')
        self.applicationPath = os.getcwd()  # TODO: this may not always return the app folder
        self.appTexturePath = os.path.join(self.applicationPath, 'data', 'textures')
        self.appObjectPath = os.path.join(self.applicationPath, 'data', '3dobjs')
        self.worldFileName = os.path.join(self.ribsPath,"world.rib").replace('\\', '/')
        self.lightsFolderPath = os.path.join(self.applicationPath, 'data', 'lights', 'aqsis')
        self.texturesFileName = os.path.join(self.ribsPath, "texture.rib")

        #mainscenefile
        self.sceneFileName = os.path.join(self.ribsPath, "scene.rib")

        #Human in the scene
        self.humanCharacter = RMRHuman(MHscene.selectedHuman, "base.obj", MHscene.getObject("base.obj"), self.ribsPath)
        self.humanParameters = self.humanCharacter.getHumanParameters()
        self.humanCharacter.subObjectsInit()
        
        #Rendering options
        self.calcAmbientOcclusion = False
        self.calcShadow = False
        self.calcSSS = False

        #Ambient Occlusion paths
        self.ambientOcclusionFileName = os.path.join(self.ribsPath, "occlmap.rib").replace('\\', '/')
        self.ambientOcclusionDataFile = os.path.join(self.usrTexturePath,"occlmap.tif" ).replace('\\', '/')
        self.ambientOcclusionDataFileTex = os.path.join(self.usrTexturePath,"occlmap.texture" ).replace('\\', '/')        

        #Shadow path
        self.shadowFileName = os.path.join(self.ribsPath,"shadow.rib").replace('\\', '/')

        #SSS path
        self.bakeFilename = os.path.join(self.ribsPath,"skinbake.rib").replace('\\', '/')
        self.lightmapFileName = os.path.join(self.ribsPath,"lightmap.rib").replace('\\', '/')
        self.bakeTMPTexture = os.path.join(self.usrTexturePath,"bake.bake").replace('\\', '/')
        self.bakeTexture = os.path.join(self.usrTexturePath,"bake.texture").replace('\\', '/')
        self.lightmapTMPTexture = os.path.join(self.usrTexturePath,"lightmap.tif").replace('\\', '/')
        self.lightmapTexture = os.path.join(self.usrTexturePath,"lightmap.texture").replace('\\', '/')

        #Lights list
        self.lights = []

        #creating resources folders
        if not os.path.isdir(self.renderPath):
            os.makedirs(self.renderPath)
        if not os.path.isdir(self.ribsPath):
            os.makedirs(self.ribsPath)
        if not os.path.isdir(self.usrTexturePath):
            os.makedirs(self.usrTexturePath)
        if not os.path.isdir(self.usrShaderPath):
            os.makedirs(self.usrShaderPath)

        

        #textures used in the scene
        self.textures = []
        
        self.textures.append(RMRTexture("texture.tif", self.appTexturePath, self.usrTexturePath))
        self.textures.append(RMRTexture("texture_ref.tif", self.appTexturePath, self.usrTexturePath))
        self.textures.append(RMRTexture("texture_bump.tif", self.appTexturePath, self.usrTexturePath))
        for hPar in self.humanParameters:
            self.textures.append(RMRTexture(hPar[0]+".tif", self.appTexturePath, self.usrTexturePath))
            
        

    def __str__(self):
        return "Renderman Scene"
        
        
    def loadLighting(self, lightsFolderPath, lightFile):
        self.lights = []
        RMRLight.lightCounter = 0
        path = os.path.join(lightsFolderPath,lightFile)        
        fileDescriptor = open(path) 
        
        for data in fileDescriptor:
            print data
            dataList = data.split()
            fromX = float(dataList[0])
            fromY = float(dataList[1])
            fromZ = float(dataList[2])
            toX = float(dataList[3])
            toY = float(dataList[4])
            toZ = float(dataList[5])
            lIntensity = float(dataList[6])
            lType = dataList[7]   
                
            l = RMRLight(self.ribsPath,[fromX, fromY, fromZ], [toX, toY, toZ], intensity = lIntensity, type = lType)            
            if len(dataList) >= 9:            
                l.blur = float(dataList[8]) 
            if len(dataList) >= 10:            
                l.coneangle = float(dataList[9])                 
            print l
            self.lights.append(l)
        
    


    def writeWorldFile(self, fName, shadowMode = None, bakeMode = None):
        """

        """
        #Init and write rib code for hairs        
        self.humanCharacter.writeHairsCurve()
        
        #Get global subobjs parameteres.
        self.humanCharacter.skinMat.setParameter("sweat", self.app.settings.get('rendering_aqsis_oil', 0.3))
        self.humanCharacter.subObjectsInit()

        if len(self.humanCharacter.subObjects) < 1:
            print "Warning: AO calculation on 0 objects"

        ribfile = file(fName, 'w')
        if not bakeMode:
            print "Writing world"
            for subObj in self.humanCharacter.subObjects:
                print "rendering....", subObj.name
                ribPath = os.path.join(self.ribsPath, subObj.name + '.rib')
                ribfile.write('\tAttributeBegin\n')
                subObj.writeRibCode(ribPath)
                if shadowMode:
                    ribfile.write('\tSurface "null"\n')
                else:
                    if subObj.materialBump:
                        subObj.materialBump.writeRibCode(ribfile)
                    if subObj.material:
                        subObj.material.writeRibCode(ribfile)
                ribfile.write('\t\tReadArchive "%s"\n' % ribPath.replace('\\', '/'))
                ribfile.write('\tAttributeEnd\n')
            ribfile.write('\tAttributeBegin\n')
            if shadowMode:
                ribfile.write('\tSurface "null"\n')
            else:
                self.humanCharacter.hairMat.writeRibCode(ribfile)
            self.humanCharacter.writeHairsInclusion(ribfile)
            ribfile.write('\tAttributeEnd\n')
        else:
            print "Writing bake world"
            ribfile.write('\tAttributeBegin\n')
            ribfile.write('\tSurface "bakelightmap" "string bakefilename" "%s" "string texturename" "%s"\n'%(self.bakeTMPTexture, os.path.join(self.usrTexturePath,"texture.texture").replace('\\', '/')))
            ribPath = os.path.join(self.ribsPath, 'skin.rib')
            ribfile.write('\t\tReadArchive "%s"\n' % ribPath.replace('\\', '/'))
            ribfile.write('\tAttributeEnd\n')

        ribfile.close()


    def writeTextureFile(self):
        """        
        """ 
        
        
        ribfile = file(self.texturesFileName, 'w')

        #Write rib code for textures
        for t in self.textures:
            t.writeRibCode(ribfile)  


    def writeSceneFile(self):
        """
        This function creates the frame definition for a Renderman scene.
        """
        imgFile = str(time.time())+".tif"      
        
        
        #Getting global settings
        
        
        
        ribSceneHeader = RMRHeader()
        
        ribSceneHeader.sizeFormat = [self.app.settings.get('rendering_width', 800), self.app.settings.get('rendering_height', 600)]
        ribSceneHeader.pixelSamples = [self.app.settings.get('rendering_aqsis_samples', 2),self.app.settings.get('rendering_aqsis_samples', 2)]
        ribSceneHeader.shadingRate = self.app.settings.get('rendering_aqsis_shadingrate', 2)
        ribSceneHeader.setCameraPosition(self.camera.eyeX, -self.camera.eyeY, self.camera.eyeZ)     
        ribSceneHeader.setSearchShaderPath(self.usrShaderPath)
        ribSceneHeader.setSearchTexturePath(self.usrTexturePath)  
        ribSceneHeader.fov = self.camera.fovAngle    
        ribSceneHeader.displayName = os.path.join(self.ribsPath, imgFile).replace('\\', '/')
        ribSceneHeader.displayType = "file" 
        ribSceneHeader.displayColor = "rgba"  
        ribSceneHeader.displayName2 = "Final Render"
        ribSceneHeader.displayType2 = "framebuffer" 
        ribSceneHeader.displayColor2 = "rgb"      
        
        
        
        pos = self.humanCharacter.getHumanPosition()
        imgFile = str(time.time())+".tif"
        ribfile = file(self.sceneFileName, 'w')      

        #Write rib header
        ribSceneHeader.writeRibCode(ribfile)       
        
        #Write rib body
        ribfile.write('\tTranslate %f %f %f\n' % (pos[0], pos[1], 0.0)) # Model
        ribfile.write('\tRotate %f 1 0 0\n' % -pos[2])
        ribfile.write('\tRotate %f 0 1 0\n' % -pos[3])
        ribfile.write('WorldBegin\n')
        for l in self.lights:
            l.writeRibCode(ribfile, l.counter)        
        ribfile.write('\tReadArchive "%s"\n'%(self.worldFileName))
        ribfile.write('WorldEnd\n')
        ribfile.close()


    def writeSkinBakeFile(self):
        """
        This function creates the frame definition for a Renderman scene.
        """

        #Getting global settings
        self.xResolution, self.yResolution = self.app.settings.get('rendering_width', 800), self.app.settings.get('rendering_height', 600)
        self.pixelSamples = [2,2]
        self.shadingRate = 0.5
        
        pos = self.humanCharacter.getHumanPosition()
        
        ribfile = file(self.bakeFilename, 'w')


        ribfile.write('FrameBegin 1\n')
        
        #Getting global settings
        ribSceneHeader = RMRHeader()
        ribSceneHeader.sizeFormat = [self.app.settings.get('rendering_width', 800), self.app.settings.get('rendering_height', 600)]
        ribSceneHeader.pixelSamples = [self.app.settings.get('rendering_aqsis_samples', 2),self.app.settings.get('rendering_aqsis_samples', 2)]
        ribSceneHeader.shadingRate = self.app.settings.get('rendering_aqsis_shadingrate', 2)
        ribSceneHeader.setCameraPosition(self.camera.eyeX, -self.camera.eyeY, self.camera.eyeZ)     
        ribSceneHeader.setSearchShaderPath(self.usrShaderPath)
        ribSceneHeader.setSearchTexturePath(self.usrTexturePath)  
        ribSceneHeader.fov = self.camera.fovAngle           
        
        #Write rib header
        ribSceneHeader.writeRibCode(ribfile)       
        
        #Write rib body
        ribfile.write('\tTranslate %f %f %f\n' % (pos[0], pos[1], 0.0)) # Model
        ribfile.write('\tRotate %f 1 0 0\n' % -pos[2])
        ribfile.write('\tRotate %f 0 1 0\n' % -pos[3])
        ribfile.write('WorldBegin\n')
        for l in self.lights:
            l.writeRibCode(ribfile, l.counter)        
        ribfile.write('\tReadArchive "%s"\n'%(self.worldFileName+"bake.rib"))
        ribfile.write('WorldEnd\n')
        ribfile.write('FrameEnd\n')
        ribfile.write('MakeTexture "%s" "%s" "periodic" "periodic" "box" 1 1 "float bake" 1024\n'%(self.bakeTMPTexture, self.bakeTexture))

        ribfile.write('FrameBegin 2\n')
        
        #Getting global settings
        ribSceneHeader = RMRHeader()        
        ribSceneHeader.sizeFormat = [1024,1024]        
        ribSceneHeader.setCameraPosition(0,0,0.02)     
        ribSceneHeader.setSearchShaderPath(self.usrShaderPath)
        ribSceneHeader.setSearchTexturePath(self.usrTexturePath)         
        ribSceneHeader.shadingInterpolation = "smooth"
        ribSceneHeader.projection = "orthographic" 
        ribSceneHeader.displayType = "file" 
        ribSceneHeader.displayColor = "rgba"  
        ribSceneHeader.displayName = self.lightmapTMPTexture       
        
        #Write rib header
        ribSceneHeader.writeRibCode(ribfile)        
        

        ribfile.write('WorldBegin\n')
        ribfile.write('Color [ 1 1 1 ]\n')
        ribfile.write('\tSurface "scatteringtexture" "string texturename" "%s"\n'%(self.bakeTexture))
        #ribfile.write('Translate 0 0 0.02\n')
        ribfile.write('Polygon "P" [ -1 -1 0   1 -1 0   1 1 0  -1 1 0 ]"st" [ 0 1  1 1  1 0  0 0  ]\n')
        ribfile.write('WorldEnd\n')
        ribfile.write('FrameEnd\n')

        ribfile.write('MakeTexture "%s" "%s" "periodic" "periodic" "box" 1 1 "float bake" 1024\n'%(self.lightmapTMPTexture, self.lightmapTexture))


    def writeAOFile(self):
        """
        This function creates the frame definition for a Renderman scene.
        """

        #Getting global settings
        self.xResolution, self.yResolution = 512,512
        self.pixelSamples = [2,2]        
        
        pos = self.humanCharacter.getHumanPosition()
        
        normalizingFactor = 0
        for hPar in self.humanParameters:
            hVal = hPar[1]
            if hVal > 0:
                normalizingFactor += hVal
        
        ribfile = file(self.ambientOcclusionFileName, 'w')         
        
        #Getting global settings
        ribSceneHeader = RMRHeader()        
        ribSceneHeader.sizeFormat = [512,512]        
        ribSceneHeader.setCameraPosition(0,0,0.02)     
        ribSceneHeader.setSearchShaderPath(self.usrShaderPath)
        ribSceneHeader.setSearchTexturePath(self.usrTexturePath)         
        ribSceneHeader.shadingInterpolation = "smooth"
        ribSceneHeader.projection = "orthographic" 
        ribSceneHeader.displayType = "file" 
        ribSceneHeader.displayColor = "rgba"  
        ribSceneHeader.displayName = self.ambientOcclusionDataFile     
        
        #Write rib header
        ribSceneHeader.writeRibCode(ribfile)         

        ribfile.write('WorldBegin\n')
        ribfile.write('Color [ 1 1 1 ]\n')
        ribfile.write('Surface "mixer" "float[54] tValues" [')
        for hPar in self.humanParameters:
            ribfile.write('%.1f '%(hPar[1]/normalizingFactor))
        ribfile.write(']')
        ribfile.write('"string[54] textures" [')
        for hPar in self.humanParameters:
            ribfile.write('"%s.texture" '%(hPar[0]))
        ribfile.write(']\n')
        ribfile.write('Polygon "P" [ -1 -1 0   1 -1 0   1 1 0  -1 1 0 ]"st" [ 0 1  1 1  1 0  0 0  ]\n')
        ribfile.write('WorldEnd\n')
        ribfile.write('MakeTexture "%s" "%s" "periodic" "periodic" "box" 1 1 "float bake" 1024\n'%(self.ambientOcclusionDataFile, self.ambientOcclusionDataFileTex))

    def writeShadowFile(self):
        """
        This function creates the frame definition for a Renderman scene.
        """

        ribfile = file(self.shadowFileName, 'w')          
        ribSceneHeader = RMRHeader()
        ribSceneHeader.sizeFormat = [1024,1024]        
        ribSceneHeader.pixelSamples = [1,1]
        ribSceneHeader.shadingRate = 2           
        ribSceneHeader.setSearchShaderPath(self.usrShaderPath)
        ribSceneHeader.setSearchTexturePath(self.usrTexturePath) 
        ribSceneHeader.bucketSize = [32,32]
        ribSceneHeader.eyesplits = 10
        ribSceneHeader.depthfilter = "midpoint"      
        ribSceneHeader.pixelFilter = "box"

        #Write rib header
        ribSceneHeader.writeRibCode(ribfile)        
        for l in self.lights:
            if l.type == "shadowspot":
                ribfile.write('FrameBegin %d\n'%(l.counter))
                ribfile.write('Display "%s" "zfile" "z"\n'%(l.shadowMapDataFile))
                l.placeShadowCamera(ribfile)
                ribfile.write('WorldBegin\n')
                ribfile.write('\tSurface "null"\n')
                ribfile.write('\tReadArchive "%s"\n'%(self.worldFileName+"shad.rib"))
                ribfile.write('WorldEnd\n')
                ribfile.write('FrameEnd\n')
                shadowMapDataFileFinal = l.shadowMapDataFile.replace("zfile","shad")
                ribfile.write('MakeShadow "%s" "%s"\n'%(l.shadowMapDataFile,shadowMapDataFileFinal))
        ribfile.close()    
        
 


    def render(self):
        
        filesTorender = [self.texturesFileName]
        self.loadLighting(self.lightsFolderPath, "default.lights")    
        self.writeTextureFile() #TODO move in the init
        
        recalculateAll = 0
        recalculateSSS = 0
        
        
            
        print "DEBUG1", self.app.scene3d.selectedHuman.getRotation(), self.lastRotation
        
        if (self.app.scene3d.selectedHuman.getRotation() != self.lastRotation) or ([self.camera.eyeX, -self.camera.eyeY, self.camera.eyeZ] != self.lastCameraPosition):
            print "CONDICIO 1"
            recalculateSSS = 1            
            self.lastRotation = self.app.scene3d.selectedHuman.getRotation()  
            
        if len(self.app.undoStack) > 0:  
            
            print "DEBUG2", self.app.undoStack[-1], self.lastUndoItem
            if self.app.undoStack[-1] != self.lastUndoItem:  
                print "CONDICIO 2"
                self.lastUndoItem = self.app.undoStack[-1]
                recalculateAll = 1
        else:            
            if recalculateSSS == 0:
                recalculateAll = 1
                print "CONDICIO 3"
                
        if self.firstTimeRendering == True:
            recalculateAll = 1
            self.firstTimeRendering = False
            print "CONDICIO 4"
            
            
        if  recalculateAll == 1:
            print "RECALCULATING ALL"
            self.writeWorldFile(self.worldFileName+"shad.rib", shadowMode = 1)               
            self.writeShadowFile()
            filesTorender.append(self.shadowFileName)        
            self.writeAOFile()            
            filesTorender.append(self.ambientOcclusionFileName) 
            self.writeWorldFile(self.worldFileName+"bake.rib", bakeMode = 1)
            self.writeSkinBakeFile()
            filesTorender.append(self.bakeFilename)           
            
            
        if (recalculateSSS == 1) and (recalculateAll == 0):
            print "RECALCULATING SSS"
            self.writeWorldFile(self.worldFileName+"bake.rib", bakeMode = 1)
            self.writeSkinBakeFile()
            filesTorender.append(self.bakeFilename)
        
        
        self.writeWorldFile(self.worldFileName)
        self.writeSceneFile()
        filesTorender.append(self.sceneFileName)

        #command = '%s "%s"' % ('aqsis -progress', self.sceneFileName)
        #subprocess.Popen(command, shell=True)

        renderThread = RenderThread(self.app, filesTorender)
        renderThread.start()

from threading import Thread

class RenderThread(Thread):

    def __init__(self, app, filenames):

        Thread.__init__(self)
        self.app = app
        self.filenames = filenames

    def run(self):
        n = 0
        for filename in self.filenames:
            
            print "Rendering: %s"%(filename)
            print "Percentage: %f"%(n*(100/len(self.filenames)))

            command = '%s "%s"' % ('aqsis -progress -progressformat="progress %f %p %s %S" -v 0', filename)
            renderProc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)

            #self.app.progress(0.0)
            #self.app.scene3d.redraw()

            for line in renderProc.stdout:
              if line.startswith("progress"):
                progress = line.split()
                #self.app.progress(float(progress[2])/100.0)
                #self.app.scene3d.redraw()
                #print progress

            #self.app.progress(1.0)
            #self.app.scene3d.redraw()
            n = n+1




