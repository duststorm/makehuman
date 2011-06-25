print 'importing Pose2 plugin'

import os.path
#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import math
from aljabr import * #todo: import the necessities only
from skeleton import Skeleton
from mh2obj import exportObj
print 'importing linalg'
from linalg import *
print 'imported linalg'
from copy import deepcopy
import module3d

#torso comes after clavicle because of getJointZones :P
jointZones = ('l-eye','r-eye', 'jaw', 'nose', 'mouth', 'head', 'neck',  
'r-torso-clavicle', 'l-torso-clavicle', 'torso', 'hip', 'pelvis', 
'r-upperarm', 'l-upperarm', 'r-lowerarm', 'l-lowerarm', 'l-hand', 'r-hand', 'r-upperleg', 'l-upperleg', 'r-lowerleg', 'l-lowerleg', 'l-foot', 'r-foot')

zonesToJointsMapping = {
    'pelvis':'joint-pelvis',
    'hip':'joint-spine2',
    'torso':'joint-spine1',
    'neck':'joint-neck',
    'head':'joint-head',
    'r-eye':'joint-r-eye',
    'l-eye':'joint-l-eye',
    'l-torso-clavicle':'joint-l-clavicle',
    'l-upperarm':'joint-l-shoulder',
    'l-lowerarm':'joint-l-elbow',
    'l-hand':'joint-l-hand',
    'r-torso-clavicle':'joint-r-clavicle',
    'r-upperarm':'joint-r-shoulder',
    'r-lowerarm':'joint-r-elbow',
    'r-hand':'joint-r-hand',
    'l-upperleg':'joint-l-upper-leg',
    'l-lowerleg':'joint-l-knee',
    'l-foot':'joint-l-ankle',
    'r-upperleg':'joint-r-upper-leg',
    'r-lowerleg':'joint-r-knee',
    'r-foot':'joint-r-ankle'
}

class PoseTaskView(gui3d.TaskView):

  def __init__(self, category):
    gui3d.TaskView.__init__(self, category, 'Pose')      

    self.zone = ""
    self.skeleton = Skeleton()
    self.selectedGroups = []
    self.joint = None
            
    self.box = gui3d.GroupBox(self, [10, 80, 9.0], 'Rotation', gui3d.GroupBoxStyle._replace(height=25+36*3+4+24*3+6))

    self.Xslider = gui3d.Slider(self.box, value = 0.0, min = -180.0, max = 180.0, label = "RotX: %d")
    self.Yslider = gui3d.Slider(self.box, value = 0.0, min = -180.0, max = 180.0, label = "RotY: %d")
    self.Zslider = gui3d.Slider(self.box, value = 0.0, min = -180.0, max = 180.0, label = "RotZ: %d")
    
    self.skin = gui3d.CheckBox(self.box, "Skin", False)
    
    self.resetPoseButton = gui3d.Button(self.box, "Reset")
    self.savePoseButton = gui3d.Button(self.box, "Save")
    #self.testButton = gui3d.Button(self.box, "Test")
    
    #get bindings for r-shoulder-joint
    f = open("utils/makepose/r-shoulder-joint.txt")
    self.jointVerts = []
    while (1): 
      line = f.readline()
      if not line: break 
      self.jointVerts.append(int(line));
    f.close()           
    
    self.tets = None

    #get prejoint points to create cage from
    f = open("utils/makepose/r-clavicle.txt")
    self.preJointVerts = []
    while (1): 
      line = f.readline()
      if not line: break 
      self.preJointVerts.append(int(line));
    f.close()
    f = open("utils/makepose/r-scapula.txt") 
    while (1): 
      line = f.readline()
      if not line: break 
      self.preJointVerts.append(int(line));
    f.close()
    
    self.preTets = None

    
    @self.savePoseButton.event
    def onClicked(event):
        exportObj(self.app.selectedHuman.meshData, os.path.join(getPath('exports'), "posed.obj"))

    @self.resetPoseButton.event
    def onClicked(event):
        self.reset()

    @self.Xslider.event
    def onChange(value):
        if self.joint:
            rotation = [value - self.joint.rotation[0], 0.0, 0.0]
            self.joint.rotation[0] = value
            self.rotateJoint(self.joint, self.joint.position, rotation)
            self.app.selectedHuman.meshData.calcNormals()
            self.app.selectedHuman.meshData.update()
                
    @self.Yslider.event
    def onChange(value):
        if self.joint:
            rotation = [0.0, value - self.joint.rotation[1], 0.0]
            self.joint.rotation[1] = value
            self.rotateJoint(self.joint, self.joint.position, rotation)
            self.app.selectedHuman.meshData.calcNormals()
            self.app.selectedHuman.meshData.update()
        
    @self.Zslider.event
    def onChange(value):
        if self.joint:
            rotation = [0.0, 0.0, value - self.joint.rotation[2]]
            self.joint.rotation[2] = value
            self.rotateJoint(self.joint, self.joint.position,rotation)
            self.app.selectedHuman.meshData.calcNormals()
            self.app.selectedHuman.meshData.update()
                  
  def onMouseMoved(self, event):
    if not self.joint:
      human = self.app.selectedHuman
      groups = []
      self.zone = self.getJointZones(event.group.name)

      if self.zone:
        for g in human.mesh.faceGroups:
          if self.zone != "torso":
            if self.zone in g.name:
              groups.append(g)
          elif (self.zone in g.name) and not g.name.endswith("clavicle"):
            groups.append(g)

        for g in self.selectedGroups:
          if g not in groups:
            g.setColor([255, 255, 255, 255])

        for g in groups:
          if g not in self.selectedGroups:
            g.setColor([0, 169, 184, 255])
            
        self.selectedGroups = groups
        self.app.redraw()
  
  def onMouseUp(self, event):
      if self.joint: 
          self.joint = None
      else:
          self.joint = self.skeleton.getJoint(zonesToJointsMapping.get(self.zone))
          if self.joint:
              self.Xslider.setValue(self.joint.rotation[0])
              self.Yslider.setValue(self.joint.rotation[1])
              self.Zslider.setValue(self.joint.rotation[2])
  
  def onShow(self, event):
      self.app.selectedHuman.storeMesh()
      self.skeleton.update(self.app.selectedHuman.meshData)         
      
      #compute bounding box
      #must do this! because mh human changes after the init -_-
      bboxj = calcBBox(self.app.selectedHuman.meshData.verts, self.jointVerts)
      
      #compute right shoulder joint position because we cannot rely on the diamond
      self.skeleton.getJoint('joint-r-shoulder').position = vmul(vadd(bboxj[0],bboxj[1]),0.5)
      
      #adding offset
      bboxj[0][0]= bboxj[0][0] - 0.01
      bboxj[1][0]= bboxj[1][0] + 0.01
      bboxj[0][1]= bboxj[0][1] - 0.01
      bboxj[1][1]= bboxj[1][1] + 0.01
      bboxj[0][2]= bboxj[0][2] - 0.01
      bboxj[1][2]= bboxj[1][2] + 0.01  
      self.tets =  box2Tetrahedrons(bboxj)
      
      #computing prejoint bounding box
      bboxpre = calcBBox(self.app.selectedHuman.meshData.verts, self.preJointVerts)
      self.preTets =  box2Tetrahedrons(bboxpre)
      
      gui3d.TaskView.onShow(self, event)

  def onHide(self, event):
      self.app.selectedHuman.restoreMesh()
      self.app.selectedHuman.meshData.update()
      gui3d.TaskView.onHide(self, event)
      
  def getJointZones(self, groupName):
      for k in jointZones:
          if k in groupName:
              return k
      return None
   
  def rotateJoint(self, joint, center, rotation, transform=None):                
    src = self.app.selectedHuman.meshStored
    dst = self.app.selectedHuman.meshData.verts
    if not transform:
      transform = euler2matrix(vmul(rotation,degree2rad), "sxyz")
      #transform2 = euler2matrix(vmul(self.joint.rotation,degree2rad), "sxyz")
    elif rotation:
      joint.position = vadd(mtransform(transform, vsub(joint.position, center)),center)
      
    if (joint == self.joint) and self.skin.selected and (joint.name == 'joint-r-shoulder'):
      transform2 = euler2matrix(vmul(self.joint.rotation,degree2rad), "sxyz")
      tets2 = deformTets(self.tets, center, transform2)
      preJointRot = [0.0,0.0,0.0]
      
      tets = self.tets + self.preTets
      for i in self.jointVerts:
        #using all 10 tetrahedrons as controls
        weights = computeAllWeights(src[i],tets)
        v = [0.0,0.0,0.0]
        for tet_i in xrange(0,5):
          for j in xrange(0,4):
            v= vadd(vmul(tets2[tet_i][j],weights[tet_i][j]),v)
        for tet_i in xrange(0,5):
          for j in xrange(0,4):
            v= vadd(vmul(self.preTets[tet_i][j],weights[tet_i][j]),v)
        #average of 10 tetrahedrons
        dst[i].co = vmul(v, 0.1)
        
        """
        #using all 5 tetrahedrons as controls
        weights = computeAllWeights(src[i],self.tets)
        v = [0.0,0.0,0.0]
        for tet_i in xrange(0,5):
          for j in xrange(0,4):
            v= vadd(vmul(tets2[tet_i][j],weights[tet_i][j]),v)
        #average of 5 tetrahedrons
        dst[i].co = vmul(v, 0.2)
        #end of using 5
        """
        
        """
        #using only one tetrahedron as control
        j,w = computeWeights(src[i], self.tets)
        if not j: print src[i]
        v = [0.0,0.0,0.0]
        for k in xrange(0,4):
          v= vadd(vmul(tets2[j][k],w[k]),v)
        dst[i].co = v[:]
        #end of using 1
        """

    for i in joint.bindedVects:
      if (i not in self.jointVerts):
        dst[i].co = vadd(mtransform(transform, vsub(dst[i].co, center)),center)
    
    for child in joint.children:
      self.rotateJoint(child, center, rotation, transform)
  
  def reset(self):
      self.Xslider.setValue(0.0)
      self.Yslider.setValue(0.0)
      self.Zslider.setValue(0.0)
      if self.joint:
        rotation = [-self.joint.rotation[2],-self.joint.rotation[1],-self.joint.rotation[0]]
        self.joint.rotation = [0.0,0.0,0.0]
        transform = euler2matrix(vmul(rotation,degree2rad), "szyx")
        #self.joint.rotation = [0.0,0.0,0.0]
        self.rotateJoint(self.joint, self.joint.position,None, transform)
        self.app.selectedHuman.meshData.calcNormals()
        self.app.selectedHuman.meshData.update()
        
      self.app.redraw()
        

category = None
taskview = None


# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements
def load(app):
    category = app.getCategory('Posing')
    taskview = PoseTaskView(category)
    print 'pose loaded'
            
    @taskview.event
    def onMouseDown(event):
        part = app.scene3d.getSelectedFacesGroup()
        print part.name

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements

def unload(app):  
    print 'pose unloaded'
    
#rotate one side of tets along z-axis
def deformTets(tets, center, transform):
    tets2 = deepcopy(tets)
    for tet in tets2:
        for v in tet:
            if v[0] > center[0]:
                v[:] = vadd(mtransform(transform, vsub(v, center)),center)
                #v[:] = vadd(mtransform(makeRotation([0.0,0.0,1.0],angle), vsub(v, center)),center)
    return tets2

#needed for making mvc or harmonic coord. cage
def box2Tetrahedrons(box):
    """
    Subdivides a cuboid into 4 tetrahedrons as shown here:
    U{http://download.tuxfamily.org/makehuman/tutorials/tetrahedron-cube.png}
    subdivision is done with front view of cube having a slice from upper left to lower right corner. Views are with respect to right-hand
    coordinate system
    
    @rtype: list of list of 4 vertices
    @return: a list containing four tetrahedrons whose union is the cuboid. The order of this list is as follows: front left, front right, back 
    right, back left.
    @type  box: list of two vertices
    @param box: two vertices representing minimum and maximum corners of the cuboid
    """
    tetrahedrons = [[],[],[],[],[]]
    #for the first 4 tetrahedrons we traverse 2 diagonals and then the last corner of the tetrahedron whose all angles are 90 degrees
    #traversal is counterclockwise and always starts from the upper corners of the box
    
    #front left
    tet = tetrahedrons[0]
    for i in xrange(0,4):
      tet.append(box[0][:])
    #front upper left corner
    tet[0][2] = box[1][2]
    #back lower left corner
    tet[1][1] = box[1][1]
    #front lower right corner
    tet[2][0] = box[1][0]
    #front lower left corner is ok
    
    #front right
    tet1 = tetrahedrons[1]
    #front upper left corner
    tet1.append(tetrahedrons[0][0][:])
    #front lower right corner    
    tet1.append(tetrahedrons[0][2][:])
    #back upper right corner
    tet1.append(box[1][:])
    #front upper right corner    
    tet1.append(box[1][:])
    tet1[3][1] = box[0][1]
    
    #back right
    tet2 = tetrahedrons[2]
    tet2.append(box[1][:])
    tet2.append(tetrahedrons[0][1][:])
    tet2.append(tetrahedrons[0][2][:])
    tet2.append(box[1][:])
    tet2[3][2] = box[0][2]
    
    #back left
    tet3 = tetrahedrons[3]
    tet3.append(tetrahedrons[2][0][:])
    tet3.append(tetrahedrons[0][0][:])
    tet3.append(tetrahedrons[0][1][:])
    tet3.append(box[1][:])
    tet3[3][0] = box[0][0]
    
    #one last tetrahedron lies in the middle of the box
    tet4 = tetrahedrons[4]
    tet4.append(box[1][:])
    tet4.append(tetrahedrons[0][1][:])
    tet4.append(tetrahedrons[0][0][:])
    tet4.append(tetrahedrons[0][2][:])
    return tetrahedrons

def findTetrahedron(tets, v):
    """
    Given 4 tetrahedrons generated from a box (see box2Tetrahedrons) and given a point v that resides in the box. Find
    the (unique) tetrahedron in which v resides.
    
    @rtype: integer
    @return: the index of tets representing the tetrahedron that contains v
    @type  tets: list of list of 4 vertices
    @param tets:  a list containing four tetrahedrons whose union is a cuboid. The order of this list is as follows: front left, front right, 
    back right, back left.
    @type  v: list of floats
    @param v: a vertex inside a one of the tetrahedrons in tets
    """
    indices = [0,1,2,3]
    
    #front pass (x-z plane)
    diffv = vsub(v, tets[1][1])
    diffBox = vsub(tets[1][0],tets[1][1])
    #check tangents
    if fabs(diffv[2]*diffBox[0]) > fabs(diffv[0]*diffBox[2]):
        #point lies about the front face diagonal (see tetrahedron image in box2Tetrahedrons link)
        indices.remove(0) #remove the below tetrahedron
    else: indices.remove(1)
    
    #back pass (x-z plane)
    diffv = vsub(v, tets[2][1])
    diffBox = vsub(tets[2][0],tets[2][1])
    if fabs(diffv[2]*diffBox[0]) > fabs(diffv[0]*diffBox[2]): #x,z tangent
        indices.remove(2)
    else: indices.remove(3)
    
    #check if we need a top/below pass or a side pass
    if (indices[1] - indices[0])== 2: # so we have inidices {0,2} or {1,3} or 
        #we need top/below pass, x-y plane
        i,j,k = 1-indices[0],2,indices[0]
        diffv = vsub(v,tets[k][i])
        diffBox = vsub(tets[k][j],tets[k][i])
        if fabs(diffv[1]*diffBox[0]) > fabs(diffv[0]*diffBox[1]): #x,y tangent
          indices.remove(indices[0])
        else: indices.remove(indices[1])
    else: # so we have indices {0,3} or {1,2}
        #we need a side pass, y-z plane
        #todo: side pass is faslse... review i,j,k
        i,j,k = 0,1+indices[0],2*indices[0]
        diffv = vsub(v,tets[k][j])
        diffBox = vsub(tets[k][i],tets[k][j])
        if fabs(diffv[2]*diffBox[1]) > fabs(diffv[1]*diffBox[2]): #y,z tangent
          indices.remove(k)
        else: indices.remove(3-k)
    return indices[0]
    
def computeWeights(v,tets):
  y = [v[0], v[1], v[2]]
  A = [0]*9
  j = 0
  
  #solutions = []
  for i in xrange(0,5):
    tet = tets[i]
    z = vsub(y, tet[0])
    for cols in xrange(0,3):
        v2 = vsub(tet[cols+1], tet[0])
        for rows in xrange(0,3):
          A[rows*3 + cols] = v2[rows]
    w = linsolve(A,z)
    
    if validWeight(w): 
      w =[1-w[0]-w[1]-w[2],w[0], w[1],w[2]]
      return i,w

  return None,None

def computeAllWeights(v,tets):
  y = [v[0], v[1], v[2]]
  A = [0]*9
  
  allWeights = []
  #solutions = []
  for i in xrange(0,5):
    tet = tets[i]
    z = vsub(y, tet[0])
    for cols in xrange(0,3):
        v2 = vsub(tet[cols+1], tet[0])
        for rows in xrange(0,3):
          A[rows*3 + cols] = v2[rows]
    w = linsolve(A,z) 
    allWeights.append([1-w[0]-w[1]-w[2],w[0], w[1],w[2]])
  
  return allWeights
   
# checks if one of the solutions have valid weights (>0 and sum <= 1)
def validWeight(weight):
  temp = 0.0
  for w in weight:
    if (w < 0.0):
      return False
    temp = temp + w
  if (temp < 0.0) or (1 - temp < 0): return False
  else: return True
    
"""
EVERYTHING BELOW ARE OLD TEST STUFFS!!
"""

def mvcTest(self):
            
  angle = -90*degree2rad
  joint = self.skeleton.getJoint('joint-r-shoulder')
  center = joint.position
  verts = self.app.selectedHuman.meshData.verts
  
  
  #print bboxj
  #return 
  
  rotation = [0.0,angle, 0.0]
  transform = euler2matrix(rotation, "sxyz")
  
  tets2 = deformTets(self.tets, center, transform)
  
  #todo take a norm on the diff between old vertex and skinned vertex if the norm is less than some epsilon dont do changes
  # this avoid excessive wrinkles when the rotations are not extreme
  for i in joint.bindedVects:
    if verts[i].co[0] < self.tets[0][2][0]:
      #tet_i,w = computeWeights(verts[i].co,tets)
      weights = computeAllWeights(verts[i].co,self.tets)
      v = [0.0,0.0,0.0]
      #print w
      for tet_i in xrange(0,5):
        for j in xrange(0,4):
          v= vadd(vmul(tets2[tet_i][j],weights[tet_i][j]),v)
      verts[i].co = vmul(v, 0.2)
      """
      for j in xrange(0,4):
        v = vadd(vmul(tets2[tet_i][j],w[j]), v)
      verts[i].co = v[:]
      """
    else :
      v= verts[i].co
      verts[i].co = vadd(mtransform(transform, vsub(v, center)),center)
  
  for child in joint.children:
    self.rotateJoint(child, joint.position, rotation, transform)
    
  self.app.selectedHuman.meshData.calcNormals()
  self.app.selectedHuman.meshData.update()
  
print 'Pose2 plugin imported'