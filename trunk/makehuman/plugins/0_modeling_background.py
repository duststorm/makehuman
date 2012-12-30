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
from aljabr import vnorm, vsub, vadd, vdot, mtransform
from math import floor, ceil, pi, sqrt, exp
import gui
import filechooser as fc
import log

def pointInRect(point, rect):

    if point[0] < rect[0] or point[0] > rect[2] or point[1] < rect[1] or point[1] > rect[3]:
        return False
    else:
        return True

class Shader(object):

    def __init__(self):

        pass

    def shade(self, x, y, u, v, w):

        return (255, 255, 255, 0)

class ColorShader(Shader):

    def __init__(self, colors):

        self.colors = colors

    def shade(self, x, y, u, v, w):

        col = [self.colors[0][i] * u + self.colors[1][i] * v + self.colors[2][i] * w for i in xrange(3)]
        return tuple(map(int, col))

class UvShader(Shader):

    def __init__(self, texture, uv):

        self.texture = texture
        self.width = texture.width
        self.height = texture.height
        self.uv = uv

    def shade(self, x, y, u, v, w):

        x, y = [self.uv[0][i] * u + self.uv[1][i] * v + self.uv[2][i] * w for i in xrange(2)]
        try:
            return self.texture[int(x*self.width), int(y*self.height)]
        except:
            return (255, 255, 255, 255)

class UvAlphaShader(Shader):

    def __init__(self, dst, texture, uva):

        self.dst = dst
        self.texture = texture
        self.width = texture.width
        self.height = texture.height
        self.uva = uva

    def shade(self, x, y, u, v, w):

        dst = self.dst[x, y]
        x, y, a = [self.uva[0][i] * u + self.uva[1][i] * v + self.uva[2][i] * w for i in xrange(3)]
        try:
            src = self.texture[int(x*self.width), int(y*self.height)]
            return tuple([int(a * (src[i] - dst[i]) + dst[i]) for i in xrange(4)])
        except:
            return dst

# Not really fast since it checks every pixel in the bounding rectangle
# http://www.devmaster.net/codespotlight/show.php?id=17
def RasterizeTriangle(dst, p0, p1, p2, shader):

    y1 = round(p0[1])
    y2 = round(p1[1])
    y3 = round(p2[1])

    x1 = round(p0[0])
    x2 = round(p1[0])
    x3 = round(p2[0])

    dx12 = x1 - x2
    dx23 = x2 - x3
    dx31 = x3 - x1

    dy12 = y1 - y2
    dy23 = y2 - y3
    dy31 = y3 - y1

    minx = min([x1, x2, x3])
    maxx = max([x1, x2, x3])
    miny = min([y1, y2, y3])
    maxy = max([y1, y2, y3])

    c1 = dy12 * x1 - dx12 * y1
    c2 = dy23 * x2 - dx23 * y2
    c3 = dy31 * x3 - dx31 * y3

    if (dy12 < 0 or (dy12 == 0 and dx12 > 0)): c1+=1
    if (dy23 < 0 or (dy23 == 0 and dx23 > 0)): c2+=1
    if (dy31 < 0 or (dy31 == 0 and dx31 > 0)): c3+=1

    cy1 = c1 + dx12 * miny - dy12 * minx
    cy2 = c2 + dx23 * miny - dy23 * minx
    cy3 = c3 + dx31 * miny - dy31 * minx

    for y in xrange(int(miny), int(maxy)):

        cx1 = cy1
        cx2 = cy2
        cx3 = cy3

        for x in xrange(int(minx), int(maxx)):

            if cx1 > 0 and cx2 > 0 and cx3 > 0:

                d = - dy23 * dx31 + dx23 * dy31
                u = (dy23 * (x - x3) - dx23 * (y - y3)) / d
                v = (dy31 * (x - x3) - dx31 * (y - y3)) / d
                w = 1.0 - u - v
                dst[x, y] = shader.shade(x, y, u, v, w)

            cx1 -= dy12
            cx2 -= dy23
            cx3 -= dy31

        cy1 += dx12
        cy2 += dx23
        cy3 += dx31

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
            gui3d.app.modelCamera.switchToOrtho()

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

    def projectBackground(self):

        if not hasattr(self, "leftTop"):
            gui3d.app.prompt("Warning", "You need to load a background before you can project it.", "OK")
            return

        mesh = gui3d.app.selectedHuman.getSeedMesh()

        # for all quads, project vertex to screen
        # if one vertex falls in bg rect, project screen quad into uv quad
        # warp image region into texture
        leftTop = gui3d.app.modelCamera.convertToScreen(*self.leftTop)
        rightBottom = gui3d.app.modelCamera.convertToScreen(*self.rightBottom)

        r = [leftTop[0], leftTop[1], rightBottom[0], rightBottom[1]]

        srcImg = mh.Image(self.backgroundImage.getTexture())
        dstImg = mh.Image(gui3d.app.selectedHuman.getTexture())

        srcW = srcImg.width
        srcH = srcImg.height
        dstW = dstImg.width
        dstH = dstImg.height

        eye = gui3d.app.modelCamera.eye
        focus = gui3d.app.modelCamera.focus
        transform = mesh.object3d.transform
        eye = mtransform(transform, eye)
        focus = mtransform(transform, focus)
        camera = vnorm(vsub(eye, focus))

        for g in mesh.faceGroups:

            if g.name.startswith("joint") or g.name.startswith("helper"):
                continue

            for f in g.faces:
                # From hdusel in regard of issue 183: As agreed with marc I'll change the
                # call from packed to discrete because packed structs
                # are not available on Python 2.6.1 which is mandatory for MakeHuman to run
                # on OS X 10.5.x
                #
                # src = [gui3d.app.modelCamera.convertToScreen(*v.co, obj=mesh.object3d) for v in f.verts]
                #
                src = [gui3d.app.modelCamera.convertToScreen(v.co[0], v.co[1], v.co[2], obj=mesh.object3d) for v in f.verts]

                if any([pointInRect(p, r) for p in src]):

                    for i, v in enumerate(f.verts):
                        src[i][2] = max(0.0, vdot(v.no, camera))

                    if any([v[2] >= 0.0 for v in src]):

                        for i, v in enumerate(f.verts):
                            src[i][2] = max(0.0, vdot(v.no, camera))

                        co = [(mesh.texco[i][0]*dstW, dstH-(mesh.texco[i][1]*dstH)) for i in f.uv]
                        uva = [((v[0]-leftTop[0])/(rightBottom[0] - leftTop[0]), (v[1]-leftTop[1])/(rightBottom[1] - leftTop[1]), v[2]) for v in src]
                        RasterizeTriangle(dstImg, co[0], co[1], co[2], UvAlphaShader(dstImg, srcImg, (uva[:3])))
                        RasterizeTriangle(dstImg, co[2], co[3], co[0], UvAlphaShader(dstImg, srcImg, ((uva[2], uva[3], uva[0]))))

        dstImg.save(os.path.join(mh.getPath(''), 'data', 'skins', 'projection.tga'))
        gui3d.app.selectedHuman.setTexture(os.path.join(mh.getPath(''), 'data', 'skins', 'projection.tga'))

    @staticmethod
    def RasterizeTriangles(dst, coords, colors, progress = None):
        cmin = np.floor(np.amin(coords, axis=1)).astype(int)
        cmax = np.ceil( np.amax(coords, axis=1)).astype(int)

        x1 = coords[:,0,0]
        x2 = coords[:,1,0]
        x3 = coords[:,2,0]

        y1 = coords[:,0,1]
        y2 = coords[:,1,1]
        y3 = coords[:,2,1]

        dx12 = x1 - x2
        dx23 = x2 - x3
        dx31 = x3 - x1

        dy12 = y1 - y2
        dy23 = y2 - y3
        dy31 = y3 - y1

        d = - dy23 * dx31 + dx23 * dy31

        minx = cmin[:,0]
        maxx = cmax[:,0]
        miny = cmin[:,1]
        maxy = cmax[:,1]

        c1 = dy12 * x1 - dx12 * y1
        c2 = dy23 * x2 - dx23 * y2
        c3 = dy31 * x3 - dx31 * y3

        for i in xrange(len(coords)):
            if progress is not None and i % 100 == 0:
                progress(i, len(coords))
            row, col = np.mgrid[miny[i]:maxy[i],minx[i]:maxx[i]]
            x = col + 0.5
            y = row + 0.5

            cx1 = c1[i] + dx12[i] * y - dy12[i] * x
            cx2 = c2[i] + dx23[i] * y - dy23[i] * x
            cx3 = c3[i] + dx31[i] * y - dy31[i] * x

            mask = (cx1 > 0) * (cx2 > 0) * (cx3 > 0)

            u = (dy23[i] * (x - x3[i]) - dx23[i] * (y - y3[i])) / d[i]
            v = (dy31[i] * (x - x3[i]) - dx31[i] * (y - y3[i])) / d[i]
            w = 1.0 - u - v

            col = np.sum(colors[i][:,None,None,:] * np.array([u,v,w])[:,:,:,None], axis=0)

            # log.debug('dst: %s', dst._data[miny[i]:maxy[i],minx[i]:maxx[i]].shape)
            # log.debug('src: %s', col.shape)
            dst._data[miny[i]:maxy[i],minx[i]:maxx[i]][mask] = col[mask]

    def projectLighting(self):

        mesh = gui3d.app.selectedHuman.mesh
        mesh.setShadeless(1)

        dstImg = mh.Image(width=1024, height=1024, bitsPerPixel=24)
        dstImg._data[...] = 0

        dstW = dstImg.width
        dstH = dstImg.height

        delta = (-10.99, 20.0, 20.0) - mesh.coord
        ld = delta / np.sqrt(np.sum(delta ** 2, axis=-1))[...,None]
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

        # log.debug("projectLighting: begin render")

        def progress(base, i, n):
            gui3d.app.progress(base + 0.5 * i / n)

        self.RasterizeTriangles(dstImg, coords[:,[0,1,2],:], colors[:,[0,1,2],:][...,:3], progress = lambda i,n: progress(0.0,i,n))
        self.RasterizeTriangles(dstImg, coords[:,[2,3,0],:], colors[:,[2,3,0],:][...,:3], progress = lambda i,n: progress(0.5,i,n))
        gui3d.app.progress(1.0)

        # log.debug("projectLighting: end render")

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
