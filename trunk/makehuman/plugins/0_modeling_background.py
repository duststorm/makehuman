#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

TO DO

"""

__docformat__ = 'restructuredtext'

import numpy as np

import gui3d
import events3d
import mh
import os
from aljabr import vsub, vadd, vdot, mtransform
from math import floor, ceil, pi, sqrt, exp
import gui
import filechooser as fc
import log

def v4to3(v):
    v = np.asarray(v)
    return v[:3,0] / v[3:,0]

def vnorm(v):
    return v / np.sqrt(np.sum(v ** 2, axis=-1))[...,None]

def pointInRect(point, rect):

    if point[0] < rect[0] or point[0] > rect[2] or point[1] < rect[1] or point[1] > rect[3]:
        return False
    else:
        return True

class BackgroundTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Background')

        self.backgroundsFolder = os.path.join(mh.getPath(''), 'backgrounds')
        if not os.path.exists(self.backgroundsFolder):
            os.makedirs(self.backgroundsFolder)

        self.texture = mh.Texture()

        self.filenames = {}

        mesh = gui3d.RectangleMesh(420, 420)
        self.backgroundImage = gui3d.app.categories['Modelling'].addObject(gui3d.Object([190, 90, 1], mesh, visible=False))
        self.opacity = 100
        mesh.setColor([255, 255, 255, self.opacity])
        mesh.setPickable(False)
        mesh.setShadeless(True)
        mesh.setDepthless(True)
        mesh.priority = -90

        self.backgroundImageToggle = gui3d.app.categories['Modelling'].viewBox.addWidget(gui.ToggleButton('Background'), 3);

        @self.backgroundImageToggle.mhEvent
        def onClicked(event):
            if self.backgroundImage.isVisible():
                self.backgroundImage.hide()
                self.backgroundImageToggle.setSelected(False)
            elif self.backgroundImage.hasTexture():
                self.backgroundImage.show()
                self.backgroundImageToggle.setSelected(True)
            else:
                mh.changeTask('Library', 'Background')

        self.filechooser = self.addTopWidget(fc.FileChooser(self.backgroundsFolder, ['bmp', 'png', 'tif', 'tiff', 'jpg', 'jpeg'], None))
        self.addLeftWidget(self.filechooser.sortBox)

        self.backgroundBox = self.addLeftWidget(gui.GroupBox('Background 2 settings'))

        self.radioButtonGroup = []
        self.bgImageFrontRadioButton  = self.backgroundBox.addWidget(gui.RadioButton(self.radioButtonGroup, label='Front', selected=True))
        self.bgImageBackRadioButton   = self.backgroundBox.addWidget(gui.RadioButton(self.radioButtonGroup, label='Back'))
        self.bgImageLeftRadioButton   = self.backgroundBox.addWidget(gui.RadioButton(self.radioButtonGroup, label='Left'))
        self.bgImageRightRadioButton  = self.backgroundBox.addWidget(gui.RadioButton(self.radioButtonGroup, label='Right'))
        self.bgImageTopRadioButton    = self.backgroundBox.addWidget(gui.RadioButton(self.radioButtonGroup, label='Top'))
        self.bgImageBottomRadioButton = self.backgroundBox.addWidget(gui.RadioButton(self.radioButtonGroup, label='Bottom'))

        @self.filechooser.mhEvent
        def onFileSelected(filename):

            self.reference = gui3d.app.selectedHuman.getPosition()

            if self.bgImageFrontRadioButton.selected:
                self.filenames['front'] = filename
            elif self.bgImageBackRadioButton.selected:
                self.filenames['back'] = filename
            elif self.bgImageLeftRadioButton.selected:
                self.filenames['left'] = filename
            elif self.bgImageRightRadioButton.selected:
                self.filenames['right'] = filename
            elif self.bgImageTopRadioButton.selected:
                self.filenames['top'] = filename
            elif self.bgImageBottomRadioButton.selected:
                self.filenames['bottom'] = filename

            self.texture.loadImage(mh.Image(os.path.join(self.backgroundsFolder, filename)))

            bg = self.backgroundImage
            bg.mesh.setTexture(os.path.join(self.backgroundsFolder, filename))

            bg.setPosition([80, 80, 8])
            bg.mesh.resize(self.texture.width, self.texture.height)
            self.backgroundWidth = self.texture.width
            self.backgroundHeight = self.texture.height
            self.originalWidth = self.texture.width
            self.originalHeight = self.texture.height

            self.fixateBackground()

            bg.show()
            self.backgroundImageToggle.setSelected(True)

            mh.changeTask('Modelling', 'Background')
            gui3d.app.redraw()

            # Switch to orthogonal view
            # gui3d.app.modelCamera.switchToOrtho()

    def fixateBackground(self):

        self.reference = gui3d.app.selectedHuman.getPosition()
        _, _, z = gui3d.app.modelCamera.convertToScreen(*self.reference)
        x, y, _ = self.backgroundImage.getPosition()
        self.leftTop = gui3d.app.modelCamera.convertToWorld3D(x, y, z)
        self.rightBottom = gui3d.app.modelCamera.convertToWorld3D(x + self.backgroundWidth, y + self.backgroundHeight, z)

    def updateBackground(self):

        if self.backgroundImage.hasTexture():

            reference = gui3d.app.selectedHuman.getPosition()
            diff = vsub(reference, self.reference)
            self.leftTop = vadd(self.leftTop, diff)
            self.rightBottom = vadd(self.rightBottom, diff)

            leftTop = gui3d.app.modelCamera.convertToScreen(*self.leftTop)
            rightBottom = gui3d.app.modelCamera.convertToScreen(*self.rightBottom)

            self.backgroundImage.setPosition([leftTop[0], leftTop[1], 8])
            self.backgroundWidth = rightBottom[0]-leftTop[0]
            self.backgroundHeight = rightBottom[1]-leftTop[1]
            self.backgroundImage.mesh.resize(self.backgroundWidth, self.backgroundHeight)

            self.reference = reference

    class Shader(object):
        pass

    class UvAlphaShader(Shader):
        def __init__(self, dst, texture, uva):
            self.dst = dst
            self.texture = texture
            self.size = np.array([texture.width, texture.height])
            self.uva = uva

        def shade(self, i, xy, uvw):
            dst = self.dst._data[xy[...,1],xy[...,0]][...,:3]
            uva = np.sum(self.uva[i][None,None,:,:] * uvw[...,[1,2,0]][:,:,:,None], axis=2)
            ix = np.floor(uva[:,:,:2] * self.size[None,None,:]).astype(int)
            src = self.texture._data[ix[...,1], ix[...,0]][...,:3]
            a = uva[:,:,2]
            return a[:,:,None] * (src.astype(float) - dst) + dst

    class ColorShader(Shader):
        def __init__(self, colors):
            self.colors = colors

        def shade(self, i, xy, uvw):
            return np.sum(self.colors[i][None,None,:,:] * uvw[...,[1,2,0]][:,:,:,None], axis=2)

    @staticmethod
    def RasterizeTriangles(dst, coords, shader, progress = None):
        delta = coords - coords[:,[1,2,0],:]
        perp = np.concatenate((delta[:,:,1,None], -delta[:,:,0,None]), axis=-1)
        dist = np.sum(perp[:,0,:] * delta[:,2,:], axis=-1)
        perp /= dist[:,None,None]
        base = np.sum(perp * coords, axis=-1)

        cmin = np.floor(np.amin(coords, axis=1)).astype(int)
        cmax = np.ceil( np.amax(coords, axis=1)).astype(int)

        minx = cmin[:,0]
        maxx = cmax[:,0]
        miny = cmin[:,1]
        maxy = cmax[:,1]

        for i in xrange(len(coords)):
            if progress is not None and i % 100 == 0:
                progress(i, len(coords))

            ixy = np.mgrid[miny[i]:maxy[i],minx[i]:maxx[i]].transpose([1,2,0])[:,:,::-1]
            xy = ixy + 0.5
            uvw = np.sum(perp[i,None,None,:,:] * xy[:,:,None,:], axis=-1) - base[i,None,None,:]
            mask = np.all(uvw > 0, axis=-1)
            col = shader.shade(i, ixy, uvw)
            # log.debug('dst: %s', dst._data[miny[i]:maxy[i],minx[i]:maxx[i]].shape)
            # log.debug('src: %s', col.shape)
            dst._data[miny[i]:maxy[i],minx[i]:maxx[i],:3][mask] = col[mask]

    def projectBackground(self):
        if not hasattr(self, "leftTop"):
            gui3d.app.prompt("Warning", "You need to load a background before you can project it.", "OK")
            return

        mesh = gui3d.app.selectedHuman.getSeedMesh()

        self.fixateBackground()

        # for all quads, project vertex to screen
        # if one vertex falls in bg rect, project screen quad into uv quad
        # warp image region into texture
        leftTop = gui3d.app.modelCamera.convertToScreen(*self.leftTop)
        rightBottom = gui3d.app.modelCamera.convertToScreen(*self.rightBottom)

        srcImg = mh.Image(self.backgroundImage.getTexture())
        dstImg = mh.Image(gui3d.app.selectedHuman.getTexture())

        dstW = dstImg.width
        dstH = dstImg.height

        ex, ey, ez = gui3d.app.modelCamera.eye
        eye = np.matrix([ex,ey,ez,1]).T
        fx, fy, fz = gui3d.app.modelCamera.focus
        focus = np.matrix([fx,fy,fz,1]).T
        transform = mesh.object3d.transform
        eye = v4to3(transform * eye)
        focus = v4to3(transform * focus)
        camera = vnorm(eye - focus)
        # log.debug('%s %s %s', eye, focus, camera)

        group_mask = np.ones(len(mesh._faceGroups), dtype=bool)
        for g in mesh._faceGroups:
            if g.name.startswith('joint') or g.name.startswith('helper'):
                group_mask[g.idx] = False
        faces = np.argwhere(group_mask[mesh.group])[...,0]
        del group_mask

        # log.debug('matrix: %s', gui3d.app.modelCamera.camera.getConvertToScreenMatrix())

        texco = np.asarray([0,dstH])[None,None,:] + mesh.texco[mesh.fuvs[faces]] * np.asarray([dstW,-dstH])[None,None,:]
        matrix = np.asarray(gui3d.app.modelCamera.camera.getConvertToScreenMatrix(mesh))
        coord = np.concatenate((mesh.coord[mesh.fvert[faces]], np.ones((len(faces),4,1))), axis=-1)
        # log.debug('texco: %s, coord: %s', texco.shape, coord.shape)
        coord = np.sum(matrix[None,None,:,:] * coord[:,:,None,:], axis = -1)
        # log.debug('coord: %s', coord.shape)
        coord = coord[:,:,:2] / coord[:,:,3:]
        # log.debug('coord: %s', coord.shape)
        # log.debug('coords: %f-%f, %f-%f',
        #           np.amin(coord[...,0]), np.amax(coord[...,0]),
        #           np.amin(coord[...,1]), np.amax(coord[...,1]))
        # log.debug('rect: %s %s', leftTop, rightBottom)
        coord -= np.asarray([leftTop[0], leftTop[1]])[None,None,:]
        coord /= np.asarray([rightBottom[0] - leftTop[0], rightBottom[1] - leftTop[1]])[None,None,:]
        alpha = np.sum(mesh.vnorm[mesh.fvert[faces]] * np.asarray(camera)[None,None,:], axis=-1)
        alpha = np.maximum(0, alpha)
        # alpha[...] = 1 # debug
        # log.debug('alpha: %s', alpha.shape)
        # log.debug('coords: %f-%f, %f-%f',
        #           np.amin(coord[...,0]), np.amax(coord[...,0]),
        #           np.amin(coord[...,1]), np.amax(coord[...,1]))
        uva = np.concatenate((coord, alpha[...,None]), axis=-1)
        # log.debug('uva: %s', uva.shape)
        valid = np.any(alpha >= 0, axis=1)
        # log.debug('valid: %s', valid.shape)
        texco = texco[valid,:,:]
        uva = uva[valid,:,:]

        # log.debug('%s %s', texco.shape, uva.shape)

        def progress(base, i, n):
            gui3d.app.progress(base + 0.5 * i / n)

        # log.debug('src: %s, dst: %s', srcImg._data.shape, dstImg._data.shape)

        log.debug("projectBackground: begin render")

        self.RasterizeTriangles(dstImg, texco[:,[0,1,2],:], self.UvAlphaShader(dstImg, srcImg, uva[:,[0,1,2],:]), progress = lambda i,n: progress(0.0,i,n))
        self.RasterizeTriangles(dstImg, texco[:,[2,3,0],:], self.UvAlphaShader(dstImg, srcImg, uva[:,[2,3,0],:]), progress = lambda i,n: progress(0.5,i,n))
        gui3d.app.progress(1.0)

        log.debug("projectBackground: end render")

        dstImg.save(os.path.join(mh.getPath(''), 'data', 'skins', 'projection.png'))
        gui3d.app.selectedHuman.setTexture(os.path.join(mh.getPath(''), 'data', 'skins', 'projection.png'))

    def projectLighting(self):

        mesh = gui3d.app.selectedHuman.mesh
        mesh.setShadeless(1)

        dstImg = mh.Image(width=1024, height=1024, bitsPerPixel=24)
        dstImg._data[...] = 0

        dstW = dstImg.width
        dstH = dstImg.height

        delta = (-10.99, 20.0, 20.0) - mesh.coord
        ld = vnorm(delta)
        del delta
        s = np.sum(ld * mesh.vnorm, axis=-1)
        del ld
        s = np.maximum(0, np.minimum(255, (s * 256))).astype(np.uint8)
        mesh.color[...,:3] = s[...,None]
        mesh.color[...,3] = 255
        del s

        group_mask = np.ones(len(mesh._faceGroups), dtype=bool)
        for g in mesh._faceGroups:
            if g.name.startswith('joint') or g.name.startswith('helper'):
                group_mask[g.idx] = False
        faces = np.argwhere(group_mask[mesh.group])[...,0]
        del group_mask

        coords = np.asarray([0,dstH])[None,None,:] + mesh.texco[mesh.fuvs[faces]] * np.asarray([dstW,-dstH])[None,None,:]
        colors = mesh.color[mesh.fvert[faces]]
        # log.debug("projectLighting: %s %s %s", faces.shape, coords.shape, colors.shape)

        log.debug("projectLighting: begin render")

        def progress(base, i, n):
            gui3d.app.progress(base + 0.5 * i / n)

        self.RasterizeTriangles(dstImg, coords[:,[0,1,2],:], self.ColorShader(colors[:,[0,1,2],:][...,:3]), progress = lambda i,n: progress(0.0,i,n))
        self.RasterizeTriangles(dstImg, coords[:,[2,3,0],:], self.ColorShader(colors[:,[2,3,0],:][...,:3]), progress = lambda i,n: progress(0.5,i,n))
        gui3d.app.progress(1.0)

        log.debug("projectLighting: end render")

        #dstImg.resize(128, 128);

        dstImg.save(os.path.join(mh.getPath(''), 'data', 'skins', 'lighting.png'))
        gui3d.app.selectedHuman.setTexture(os.path.join(mh.getPath(''), 'data', 'skins', 'lighting.png'))

        mesh.setColor([255, 255, 255, 255])

    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        gui3d.app.selectedHuman.hide()
        gui3d.app.prompt('Info', u'Images which are placed in %s will show up here.' % self.backgroundsFolder, 'OK', helpId='backgroundHelp')
        self.filechooser.setFocus()

    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        gui3d.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)

    def onHumanTranslated(self, event):

        self.updateBackground()

    def setBackgroundImage(self, side):
        filename = self.filenames.get(side)
        if filename:
            self.backgroundImage.mesh.setTexture(os.path.join(self.backgroundsFolder, filename))

    def onHumanRotated(self, event):
        rot = gui3d.app.selectedHuman.getRotation()
        if rot==[0,0,0]:
            self.setBackgroundImage('front')
        elif rot==[0,180,0]:
            self.setBackgroundImage('back')
        elif rot==[0,-90,0]:
            self.setBackgroundImage('left')
        elif rot==[0,90,0]:
            self.setBackgroundImage('right')
        elif rot==[90,0,0]:
            self.setBackgroundImage('top')
        elif rot==[-90,0,0]:
            self.setBackgroundImage('bottom')

        self.updateBackground()

    def onCameraChanged(self, event):

        self.updateBackground()

    def onResized(self, event):
        self.updateBackground()

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = category.addTask(BackgroundTaskView(category))
    category = app.getCategory('Modelling')
    taskview = category.addTask(settingsTaskView(category, taskview))

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass


class settingsTaskView(gui3d.TaskView) :

    def __init__(self, category, taskview):

        self.backgroundImage = taskview.backgroundImage
        self.texture = taskview.texture

        gui3d.TaskView.__init__(self, category, 'Background')

        y = 80

        self.lastPos = [0, 0]

        self.backgroundBox = self.addLeftWidget(gui.GroupBox('Background settings'))

        # sliders
        self.opacitySlider = self.backgroundBox.addWidget(gui.Slider(value=taskview.opacity, min=0,max=255, label = "Opacity: %d"))

        @self.opacitySlider.mhEvent
        def onChanging(value):
            self.backgroundImage.mesh.setColor([255, 255, 255, value])
        @self.opacitySlider.mhEvent
        def onChange(value):
            taskview.opacity = value
            self.backgroundImage.mesh.setColor([255, 255, 255, value])

        @self.backgroundImage.mhEvent
        def onMouseDragged(event):

            if event.button == mh.Buttons.LEFT_MASK:
                x, y, z = self.backgroundImage.getPosition()
                self.backgroundImage.setPosition([x + event.dx, y + event.dy, z])
                taskview.fixateBackground()
            elif event.button == mh.Buttons.RIGHT_MASK:
                if abs(event.dx) > abs(event.dy):
                    taskview.backgroundWidth += event.dx
                    taskview.backgroundHeight = taskview.originalHeight * taskview.backgroundWidth / taskview.originalWidth
                else:
                    taskview.backgroundHeight += event.dy
                    taskview.backgroundWidth = taskview.originalWidth * taskview.backgroundHeight / taskview.originalHeight
                self.backgroundImage.mesh.resize(taskview.backgroundWidth, taskview.backgroundHeight)
                taskview.fixateBackground()

        self.dragButton = self.backgroundBox.addWidget(gui.ToggleButton('Move && Resize'))

        @self.dragButton.mhEvent
        def onClicked(event):
            self.backgroundImage.mesh.setPickable(self.dragButton.selected)

        self.projectBackgroundButton = self.backgroundBox.addWidget(gui.Button('Project background'))

        @self.projectBackgroundButton.mhEvent
        def onClicked(event):
            taskview.projectBackground()

        self.projectLightingButton = self.backgroundBox.addWidget(gui.Button('Project lighting'))

        @self.projectLightingButton.mhEvent
        def onClicked(event):
            taskview.projectLighting()

    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        self.backgroundImage.mesh.setPickable(self.dragButton.selected)

    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        self.backgroundImage.mesh.setPickable(0)
