#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

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
        
        # create group
        fg = self.createFaceGroup('9slice')
        
        xc = [0, border[0], width  - border[2], width]
        yc = [0, border[1], height - border[3], height]

        xuv = [0.0, border[0] / textureWidth, (textureWidth - border[2]) / textureWidth, 1.0]
        yuv = [1.0, 1.0 - border[1] / textureHeight, 1.0 - (textureHeight - border[3]) / textureHeight, 0.0]
        
        # The 16 vertices
        v = [(x, y, 0.0) for y in yc for x in xc]

        # The 16 uv values
        uv = [(x, y) for y in yuv for x in xuv]

        # The 18 faces (9 quads)
        f = [[o+4, o+5, o+1, o] for y in xrange(3) for x in xrange(3) for o in [x + y * 4]]

        self.setCoords(v)
        self.setUVs(uv)
        self.setFaces(f, f, fg.idx)

        self.border = border
        self.texture = texture
        self.setCameraProjection(1)
        self.setShadeless(1)
        self.updateIndexBuffer()
    
    def resize(self, width, height):
        xc = [0, self.border[0], width  - self.border[2], width]
        yc = [0, self.border[1], height - self.border[3], height]
        v = [(x, y, 0.0) for y in yc for x in xc]
        self.changeCoords(v)
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
        
        # create group
        fg = self.createFaceGroup('rectangle')
        
        # The 4 vertices
        v = [
            (0.0, 0.0, 0.0),
            (width, 0.0, 0.0),
            (width, height, 0.0),
            (0.0, height, 0.0)
            ]
        
        # The 4 uv values
        uv = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))
        
        # The face
        fv = [(0,1,2,3)]
        fuv = [(0,1,2,3)]

        self.setCoords(v)
        self.setUVs(uv)
        self.setFaces(fv, fuv, fg.idx)

        self.texture = texture
        self.setCameraProjection(1)
        self.setShadeless(1)
        self.updateIndexBuffer()

    def move(self, dx, dy):
        self.coord += (dx, dy, 0)
        self.markCoords(coor=True)
        self.update()     
        
    def resize(self, width, height):
        v = [
            (0.0, 0.0, 0.0),
            (width, 0.0, 0.0),
            (width, height, 0.0),
            (0.0, height, 0.0)
            ]
        self.changeCoords(v)
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
        
        # create group
        fg = self.createFaceGroup('frame')

        # The 4 vertices
        v = [
            (0.0, 0.0, 0.0),
            (width, 0.0, 0.0),
            (width, height, 0.0),
            (0.0, height, 0.0)
            ]
        
        # The 4 uv values
        uv = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))
        
        # The faces
        f = [(0,3),(1,0),(2,1),(3,2)]

        self.setCoords(v)
        self.setUVs(uv)
        self.setFaces(f, f, fg.idx)
        
        self.setCameraProjection(1)
        self.setShadeless(1)
        self.updateIndexBuffer()

    def move(self, dx, dy):
        self.coord += (dx, dy, 0)
        self.markCoords(coor=True)
        self.update()

    def resize(self, width, height):
        v = [
            (0.0, 0.0, 0.0),
            (width, 0.0, 0.0),
            (width, height, 0.0),
            (0.0, height, 0.0)
            ]
        self.changeCoords(v)
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
        
        # create group
        fg = self.createFaceGroup('cube')
        
        # The 8 vertices
        v = [(x,y,z) for z in [0,depth] for y in [0,height] for x in [0,width]]

        #         /0-----1\
        #        / |     | \
        #       |4---------5|
        #       |  |     |  |
        #       |  3-----2  |  
        #       | /       \ |
        #       |/         \|
        #       |7---------6|
        
        # The 4 uv values
        #uv = ([0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0])
        
        # The 6 faces
        f = [
            (4, 5, 6, 7), # front
            (1, 0, 3, 2), # back
            (0, 4, 7, 3), # left
            (5, 1, 2, 6), # right
            (0, 1, 5, 4), # top
            (7, 6, 2, 3), # bottom
            ]

        self.setCoords(v)
        # self.setUVs(uv)
        self.setFaces(f, fg.idx)

        self.texture = texture
        self.setCameraProjection(0)
        self.setShadeless(0)
        self.updateIndexBuffer()
        
    def resize(self, width, height, depth):
        v = [(x,y,z) for z in [0,depth] for y in [0,height] for x in [0,width]]
        self.changeCoords(v)
        self.update()
