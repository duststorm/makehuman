#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
:Authors:
    Marc Flerackers

:Version: 1.0
:Copyright: MakeHuman Team 2001-2011
:License: GPL3 

This module contains classes for commonly used geometry
"""

import module3d

class NineSliceMesh(module3d.Object3D):
    
    """
    A 9 slice mesh. It is a mesh with fixed size borders and a resizeable center.
    This makes sure the borders of a group box are not stretched.
    
    :param width: The width.
    :type width: int or float
    :param height: The height.
    :type height: int or float
    :param texture: The texture.
    :type texture: str
    :param border: The border, a list of 4 int or float elements.
    :type border: list
    """
    
    def __init__(self, width, height, texture, border):
        
        module3d.Object3D.__init__(self, '9slice_' + texture + '_' + str(border))
        
        t = module3d.getTexture(texture)
        
        # Make sure fractions are calculated correctly
        textureWidth = float(t.width)
        textureHeight = float(t.height)
        
        # Make up some dimesnions when the texture is missing
        if not textureWidth or not textureHeight:
            textureWidth = border[0] + border[2] + 1
            textureHeight = border[1] + border[3] + 1
            
        outer=[[0, 0], [width, height]]
        inner=[[border[0], border[1]], [width - border[2], height - border[3]]]
            
        self.uvValues = []
        self.indexBuffer = []
        
        # create group
        fg = self.createFaceGroup('9slice')
        
        xc = [outer[0][0], inner[0][0], inner[1][0], outer[1][0]]
        yc = [outer[0][1], inner[0][1], inner[1][1], outer[1][1]]
        xuv = [0.0, border[0] / textureWidth, (textureWidth - border[2]) / textureWidth, 1.0]
        yuv = [1.0, 1.0 - border[1] / textureHeight, 1.0 - (textureHeight - border[3]) / textureHeight, 0.0]
        
        # The 16 vertices
        v = []
        for y in yc:
            for x in xc:  
                v.append(self.createVertex([x, y, 0.0]))
        
        # The 16 uv values
        uv = []
        for y in yuv:
            for x in xuv:  
                uv.append([x, y])
        
        # The 18 faces (9 quads)
        for y in xrange(3):
            for x in xrange(3):
                o = x + y * 4
                fg.createFace((v[o+4], v[o+5], v[o+1], v[o]), (uv[o+4], uv[o+5], uv[o+1], uv[o]))
                
        self.border = border
        self.texture = texture
        self.setCameraProjection(1)
        self.setShadeless(1)
        self.updateIndexBuffer()
    
    def resize(self, width, height):
        
        outer=[[0, 0], [width, height]]
        inner=[[self.border[0], self.border[1]], [width - self.border[2], height - self.border[3]]]
        
        xc = [outer[0][0], inner[0][0], inner[1][0], outer[1][0]]
        yc = [outer[0][1], inner[0][1], inner[1][1], outer[1][1]]
        
        i = 0
        for y in yc:
            for x in xc:  
                self.verts[i].co = [x, y, 0.0]
                i += 1
        
        self.update()
    
class RectangleMesh(module3d.Object3D):

    """
    A filled rectangle.
    
    :param width: The width.
    :type width: int or float
    :param height: The height.
    :type height: int or float
    :param texture: The texture.
    :type texture: str
    """
            
    def __init__(self, width, height, texture=None):

        module3d.Object3D.__init__(self, 'rectangle_%s' % texture)
        
        self.uvValues = []
        self.indexBuffer = []
        
        # create group
        fg = self.createFaceGroup('rectangle')
        
        # The 4 vertices
        v = []
        v.append(self.createVertex([0.0, 0.0, 0.0]))
        v.append(self.createVertex([width, 0.0, 0.0]))
        v.append(self.createVertex([width, height, 0.0]))
        v.append(self.createVertex([0.0, height, 0.0]))
        
        # The 4 uv values
        uv = ([0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0])
        
        # The face
        fg.createFace((v[3], v[2], v[1], v[0]), uv)
                
        self.texture = texture
        self.setCameraProjection(1)
        self.setShadeless(1)
        self.updateIndexBuffer()
        
    def resize(self, width, height):
        
        self.verts[1].co[0] = width
        self.verts[2].co[0] = width
        self.verts[2].co[1] = height
        self.verts[3].co[1] = height
        self.update()     
       
class FrameMesh(module3d.Object3D):

    """
    A wire rectangle.

    :param width: The width.
    :type width: int or float
    :param height: The height.
    :type height: int or float
    """
            
    def __init__(self, width, height):

        module3d.Object3D.__init__(self, 'frame', 2)
        
        self.uvValues = []
        self.indexBuffer = []
        
        # create group
        fg = self.createFaceGroup('frame')
        
        # The 4 vertices
        v = []
        v.append(self.createVertex([0.0, 0.0, 0.0]))
        v.append(self.createVertex([width, 0.0, 0.0]))
        v.append(self.createVertex([width, height, 0.0]))
        v.append(self.createVertex([0.0, height, 0.0]))
        
        # The face
        fg.createFace((v[3], v[2]))
        fg.createFace((v[2], v[1]))
        fg.createFace((v[1], v[0]))
        fg.createFace((v[0], v[3]))
        
        self.setCameraProjection(1)
        self.setShadeless(1)
        self.updateIndexBuffer()
        
    def resize(self, width, height):
        
        self.verts[1].co[0] = width
        self.verts[2].co[0] = width
        self.verts[2].co[1] = height
        self.verts[3].co[1] = height
        self.update()     

class Cube(module3d.Object3D):

    """
    A cube.
    
    :param width: The width.
    :type width: int or float
    :param height: The height, if 0 it will be equal to width.
    :type height: int or float
    :param depth: The depth, if 0 it will be equal to width.
    :type depth: int or float
    :param texture: The texture.
    :type texture: str
    """
            
    def __init__(self, width, height=0, depth=0, texture=None):

        module3d.Object3D.__init__(self, 'cube_%s' % texture)
        
        width = width
        height = height or width
        depth = depth or width
        
        self.uvValues = []
        self.indexBuffer = []
        
        # create group
        fg = self.createFaceGroup('cube')
        
        # The 8 vertices
        v = []
        v.append(mesh.createVertex(aljabr.vadd(position, [0,     0,      0])))     # 0         /0-----1\
        v.append(mesh.createVertex(aljabr.vadd(position, [width, 0,      0])))     # 1        / |     | \
        v.append(mesh.createVertex(aljabr.vadd(position, [width, height, 0])))     # 2       |4---------5|
        v.append(mesh.createVertex(aljabr.vadd(position, [0,     height, 0])))     # 3       |  |     |  |
        v.append(mesh.createVertex(aljabr.vadd(position, [0,     0,      depth]))) # 4       |  3-----2  |  
        v.append(mesh.createVertex(aljabr.vadd(position, [width, 0,      depth]))) # 5       | /       \ |
        v.append(mesh.createVertex(aljabr.vadd(position, [width, height, depth]))) # 6       |/         \|
        v.append(mesh.createVertex(aljabr.vadd(position, [0,     height, depth]))) # 7       |7---------6|
        
        # The 4 uv values
        #uv = ([0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0])
        
        # The 6 faces
        fg.createFace((v[4], v[5], v[6], v[7])) # front
        fg.createFace((v[1], v[0], v[3], v[2])) # back
        fg.createFace((v[0], v[4], v[7], v[3])) # left
        fg.createFace((v[5], v[1], v[2], v[6])) # right
        fg.createFace((v[0], v[1], v[5], v[4])) # top
        fg.createFace((v[7], v[6], v[2], v[3])) # bottom
                
        self.texture = texture
        self.setCameraProjection(0)
        self.setShadeless(0)
        self.updateIndexBuffer()
        
    def resize(self, width, height, depth):
        
        self.verts[1].co[0] = width
        self.verts[2].co[0] = width
        self.verts[5].co[0] = width
        self.verts[6].co[0] = width
        self.verts[2].co[1] = height
        self.verts[3].co[1] = height
        self.verts[6].co[1] = height
        self.verts[7].co[1] = height
        self.verts[4].co[1] = depth
        self.verts[5].co[1] = depth
        self.verts[6].co[1] = depth
        self.verts[7].co[1] = depth
        self.update()     