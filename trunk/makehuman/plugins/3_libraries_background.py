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

import gui3d
import events3d
import mh
import os
from aljabr import vnorm, vsub, vadd, vdot, mtransform
from math import floor, ceil, pi, sqrt, exp

def pointInRect(point, rect):

    if point[0] < rect[0] or point[0] > rect[2] or point[1] < rect[1] or point[1] > rect[3]:
        return False
    else:
        return True
        
class Warp(object):
    
    def __init__(self, src, dst):
    
        m1 = self.quadToSquare(src[0][0], src[0][1], src[1][0], src[1][1], src[2][0], src[2][1], src[3][0], src[3][1])
        m2 = self.squareToQuad(dst[0][0], dst[0][1], dst[1][0], dst[1][1], dst[2][0], dst[2][1], dst[3][0], dst[3][1])
        self.m = self.mult(m1, m2)
        
    def squareToQuad(self, x0, y0, x1, y1, x2, y2, x3, y3):

        m = [0] * 9
        
        ax  = x0 - x1 + x2 - x3
        ay  = y0 - y1 + y2 - y3

        if ax == 0 or ay == 0:
        
            m[0] = x1 - x0; m[1] = y1 - y0; m[2] = 0.0
            m[3] = x2 - x1; m[4] = y2 - y1; m[5] = 0.0
            m[6] = x0;      m[7] = y0;      m[8] = 1.0
        
        else:
        
            ax1 = x1 - x2
            ax2 = x3 - x2
            ay1 = y1 - y2
            ay2 = y3 - y2

            gtop    = ax  * ay2 - ax2 * ay
            htop    = ax1 * ay  - ax  * ay1
            bottom  = ax1 * ay2 - ax2 * ay1

            g = gtop/bottom
            h = htop/bottom

            a = x1 - x0 + g * x1
            b = x3 - x0 + h * x3
            c = x0
            d = y1 - y0 + g * y1
            e = y3 - y0 + h * y3
            f = y0

            m[0] = a; m[1] = d; m[2] = g
            m[3] = b; m[4] = e; m[5] = h
            m[6] = c; m[7] = f; m[8] = 1.0
        
        return m
        
    def quadToSquare(self, x0, y0, x1, y1, x2, y2, x3, y3):
    
        m = self.squareToQuad(x0, y0, x1, y1, x2, y2, x3, y3)

        return self.inverted(m)
        
    def inverted(self, m):
    
        det = self.determinant(m)
        a = self.adjoint(m)
        
        return [i/det for i in a]
        
    def determinant(self, m):
    
        return m[0] * (m[8] * m[4] - m[7] * m[5]) -\
               m[3] * (m[8] * m[1] - m[7] * m[2]) +\
               m[6] * (m[5] * m[1] - m[4] * m[2])
               
    def adjoint(self, m):
        
        a = [0] * 9
        
        a[0] = m[4]*m[8] - m[5]*m[7]
        a[3] = m[5]*m[6] - m[3]*m[8]
        a[6] = m[3]*m[7] - m[4]*m[6]
        a[1] = m[2]*m[7] - m[1]*m[8]
        a[4] = m[0]*m[8] - m[2]*m[6]
        a[7] = m[1]*m[6] - m[0]*m[7]
        a[2] = m[1]*m[5] - m[2]*m[4]
        a[5] = m[2]*m[3] - m[0]*m[5]
        a[8] = m[0]*m[4] - m[1]*m[3]
    
        return a
        
    def mult(self, m1, m2):
        
        m = [0] * 9
        
        m[0] = m1[0]*m2[0] + m1[1]*m2[3] + m1[2]*m2[6]
        m[1] = m1[0]*m2[1] + m1[1]*m2[4] + m1[2]*m2[7]
        m[2] = m1[0]*m2[2] + m1[1]*m2[5] + m1[2]*m2[8]

        m[3] = m1[3]*m2[0] + m1[4]*m2[3] + m1[5]*m2[6]
        m[4] = m1[3]*m2[1] + m1[4]*m2[4] + m1[5]*m2[7]
        m[5] = m1[3]*m2[2] + m1[4]*m2[5] + m1[5]*m2[8]

        m[6] = m1[6]*m2[0] + m1[7]*m2[3] + m1[8]*m2[6]
        m[7] = m1[6]*m2[1] + m1[7]*m2[4] + m1[8]*m2[7]
        m[8] = m1[6]*m2[2] + m1[7]*m2[5] + m1[8]*m2[8]
                             
        return m
                             
    def warp(self, x, y):
    
        wx = self.m[0] * x + self.m[3] * y + self.m[6]
        wy = self.m[1] * x + self.m[4] * y + self.m[7]
        w  = self.m[2] * x + self.m[5] * y + self.m[8]
        
        return (wx/w,wy/w)
     
# Not really fast since it checks every pixel in the bounding rectangle
# http://www.devmaster.net/codespotlight/show.php?id=17

def RasterizeTriangle(warp, src, dst, p0, p1, p2):
    
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

                dx, dy = warp.warp(x, y)
                try:
                    dst[x, y] = src[int(dx), int(dy)]
                except:
                    pass #dst[int(x), int(y)] = (255, 0, 0)

            cx1 -= dy12
            cx2 -= dy23
            cx3 -= dy31

        cy1 += dx12
        cy2 += dx23
        cy3 += dx31
        
def RasterizeColorTriangle(dst, p0, p1, p2, col0, col1, col2):
    
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
                a = (dy23 * (x - x3) - dx23 * (y - y3)) / d
                b = (dy31 * (x - x3) - dx31 * (y - y3)) / d
                c = 1.0 - a - b
                col = [col0[i] * a + col1[i] * b + col2[i] * c for i in xrange(3)]
                col = map(int, col)
                dst[x, y] = tuple(col)

            cx1 -= dy12
            cx2 -= dy23
            cx3 -= dy31

        cy1 += dx12
        cy2 += dx23
        cy3 += dx31
       
"""
def convolveAndTranspose(kernel, src, dst):

        cols = len(kernel);
        cols2 = cols/2;
        
        dstW = dst.width
        dstH = dst.height

        for y in xrange(dstH):

            for x in xrange(dstW):

                pixel = [0] * 4
                
                for index, col in enumerate(xrange(x-cols2, x+cols2+1)):
                
                    f = kernel[index];

                    if (f != 0):
                        
                        if col < 0:
                            col = 0
                        elif col >= dstW:
                            col = dstW-1

                        color = src[col, y];
                        
                        pixel = map(lambda p, c: p + f * c, pixel, color)

                pixel = map(lambda c: max(0, min(255, int(c))), pixel)
                dst[y, x] = tuple(pixel)
 
def gaussianBlur(img, radius):

    tmp = mh.Image(width=img.width, height=img.height)
    
    radius = float(radius)

    r = int(ceil(radius))
    rows = r * 2 + 1;
    kernel = [0.0] * rows
    sigma = radius / 3
    sigma22 = 2 * sigma * sigma
    sigmaPi2 = 2 * pi * sigma
    sqrtSigmaPi2 = sqrt(sigmaPi2)
    radius2 = radius * radius
    total = 0.0;
    for index, row in  enumerate(xrange(-r, r+1)):
        distance = row * row;
        if distance > radius2:
            kernel[index] = 0
        else:
            kernel[index] = exp(-(distance) / sigma22) / sqrtSigmaPi2
        total += kernel[index]

    map(lambda x: x / total, kernel)

    print kernel
    convolveAndTranspose(kernel, img, tmp)
    convolveAndTranspose(kernel, tmp, img)

def verticalSample(img, x, y, radius):
       
    sum = [0, 0, 0, 0]
    count = 0
    height = img.height

    for yy in xrange(y-radius, y+radius+1):
       
        if yy > 0 and yy < height:
            color = img[x, yy]
            sum[0] += color[0]
            sum[1] += color[1]
            sum[2] += color[2]
            sum[3] += color[3]
            count = count+1

    return (sum[0]/count, sum[1]/count, sum[2]/count, sum[3]/count)
    
def horizontalSample(img, x, y, radius):
   
    sum = [0, 0, 0, 0]
    count = 0
    width = img.width

    for xx in xrange(x-radius, x+radius+1):
       
        if xx > 0 and xx < width:
            color = img[xx, y]
            sum[0] += color[0]
            sum[1] += color[1]
            sum[2] += color[2]
            sum[3] += color[3]
            count = count+1

    return (sum[0]/count, sum[1]/count, sum[2]/count, sum[3]/count)
        
def blur(img, radius):

    tmp = mh.Image(width=img.width, height=img.height)
    width = img.width
    height = img.height
    
    # Vertical blur
    for y in xrange(height):
        for x in xrange(width):
        
           tmp[x, y] = verticalSample(img, x, y, radius)
           
    for y in xrange(height):
        for x in xrange(width):
        
           img[x, y] = horizontalSample(tmp, x, y, radius)
"""

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
        mesh.setPickable(0)
        
        self.backgroundImageToggle = gui3d.app.categories['Modelling'].viewBox.addView(gui3d.ToggleButton('Background'));
        
        @self.backgroundImageToggle.event
        def onClicked(event):
            if self.backgroundImage.isVisible():
                self.backgroundImage.hide()
                self.backgroundImageToggle.setSelected(False)
            elif self.backgroundImage.hasTexture():
                self.backgroundImage.show()
                self.backgroundImageToggle.setSelected(True)
            else:
                gui3d.app.switchCategory('Library')
                gui3d.app.switchTask('Background')
        
        y = 280
        self.backgroundBox = self.addView(gui3d.GroupBox([10, y, 9], 'Background 2 settings', gui3d.GroupBoxStyle._replace(height=25+36*3+24*1+6)));y+=25

        self.radioButtonGroup = []
        self.bgImageFrontRadioButton = self.backgroundBox.addView(gui3d.RadioButton(self.radioButtonGroup, selected=True, label='Front'))
        self.bgImageBackRadioButton = self.backgroundBox.addView(gui3d.RadioButton(self.radioButtonGroup, selected=False, label='Back'))
        self.bgImageLeftRadioButton = self.backgroundBox.addView(gui3d.RadioButton(self.radioButtonGroup, selected=False, label='Left'))
        self.bgImageRightRadioButton = self.backgroundBox.addView(gui3d.RadioButton(self.radioButtonGroup, selected=False, label='Right'))
        self.bgImageTopRadioButton = self.backgroundBox.addView(gui3d.RadioButton(self.radioButtonGroup, selected=False, label='Top'))
        self.bgImageBottomRadioButton = self.backgroundBox.addView(gui3d.RadioButton(self.radioButtonGroup, selected=False, label='Bottom'))
                        
        self.filechooser = self.addView(gui3d.FileChooser(self.backgroundsFolder, ['bmp', 'png', 'tif', 'tiff', 'jpg', 'jpeg'], None))

        @self.filechooser.event
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

            self.texture.loadImage(os.path.join(self.backgroundsFolder, filename))

            bg = self.backgroundImage
            bg.mesh.setTexture(os.path.join(self.backgroundsFolder, filename))
            
            bg.setPosition([80, 80, 8])
            bg.mesh.resize(self.texture.width, self.texture.height)
            self.backgroundWidth = self.texture.width
            self.backgroundHeight = self.texture.height

            self.fixateBackground()

            bg.show()
            self.backgroundImageToggle.setSelected(True)
            gui3d.app.switchCategory('Modelling')
            gui3d.app.switchTask('Background')
            gui3d.app.redraw()
            
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
        
            if g.name.startswith("joint"):
                continue
                
            for f in g.faces:
                
                src = [gui3d.app.modelCamera.convertToScreen(*v.co, obj=mesh.object3d) for v in f.verts]
                
                if any([pointInRect(p, r) for p in src]):
                
                    if vdot(f.no, camera) >= 0:
                
                        xscale = srcW / (rightBottom[0] - leftTop[0])
                        yscale = srcH / (rightBottom[1] - leftTop[1])
                        src = [((v[0]-leftTop[0])*xscale, (v[1]-leftTop[1])*yscale) for v in src]
                        dst = [(mesh.uvValues[i][0]*dstW, dstH-(mesh.uvValues[i][1]*dstH)) for i in f.uv]
                        w = Warp(dst, src)
                        RasterizeTriangle(w, srcImg, dstImg, *dst[:3])
                        RasterizeTriangle(w, srcImg, dstImg, dst[2], dst[3], dst[0])
                    
        dstImg.save(os.path.join(mh.getPath(''), 'data', 'skins', 'projection.tga'))
        gui3d.app.selectedHuman.setTexture(os.path.join(mh.getPath(''), 'data', 'skins', 'projection.tga'))
        
    def projectLighting(self):
    
        mesh = gui3d.app.selectedHuman.mesh
        mesh.setShadeless(1)
        
        dstImg = mh.Image(width=1024, height=1024, bitsPerPixel=24)
        
        dstW = dstImg.width
        dstH = dstImg.height
        
        for v in mesh.verts:
        
            ld = vnorm(vsub((-10.99, 20.0, 20.0,), v.co))
            s = vdot(v.no, ld)
            s = max(0, min(255, int(s*255)))
            v.setColor([s, s, s, 255])
            
        for g in mesh.faceGroups:
        
            if g.name.startswith("joint"):
                continue
                
            for f in g.faces:

                co = [(mesh.uvValues[i][0]*dstW, dstH-(mesh.uvValues[i][1]*dstH)) for i in f.uv]
                c = [v.color for v in f.verts]
                RasterizeColorTriangle(dstImg, co[0], co[1], co[2], c[0], c[1], c[2])
                RasterizeColorTriangle(dstImg, co[2], co[3], co[0], c[2], c[3], c[0])
        
        dstImg.resize(128, 128);
        
        dstImg.save(os.path.join(mh.getPath(''), 'data', 'skins', 'lighting.tga'))
        gui3d.app.selectedHuman.setTexture(os.path.join(mh.getPath(''), 'data', 'skins', 'lighting.tga'))
        
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
        
        self.filechooser.onResized(event)
        self.updateBackground()

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = category.addView(BackgroundTaskView(category))
    category = app.getCategory('Modelling')
    taskview = category.addView(settingsTaskView(category, taskview))

    print 'Background chooser loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'Background chooser unloaded'
    
    
class settingsTaskView(gui3d.TaskView) :
    
    def __init__(self, category, taskview):
        
        self.backgroundImage = taskview.backgroundImage
        self.texture = taskview.texture
                                
        gui3d.TaskView.__init__(self, category, 'Background')
        
        y = 80
        
        self.lastPos = [0, 0]
        
        self.backgroundBox = self.addView(gui3d.GroupBox([10, y, 9], 'Background settings', gui3d.GroupBoxStyle._replace(height=25+36*3+24*1+6)));y+=25
        
        # sliders
        self.opacitySlider = self.backgroundBox.addView(gui3d.Slider(value=taskview.opacity, min=0,max=255, label = "Opacity"))
            
        @self.opacitySlider.event
        def onChanging(value):
            self.backgroundImage.mesh.setColor([255, 255, 255, value])
        @self.opacitySlider.event
        def onChange(value):
            taskview.opacity = value
            self.backgroundImage.mesh.setColor([255, 255, 255, value])
            
        @self.backgroundImage.event
        def onMouseDragged(event):
        
            if event.button == events3d.SDL_BUTTON_LEFT_MASK:
                x, y, z = self.backgroundImage.getPosition()
                self.backgroundImage.setPosition([x + event.dx, y + event.dy, z])
                taskview.fixateBackground()
            elif event.button == events3d.SDL_BUTTON_RIGHT_MASK:
                if abs(event.dx) > abs(event.dy):
                    taskview.backgroundHeight = taskview.backgroundHeight * (taskview.backgroundWidth + event.dx) / taskview.backgroundWidth
                    taskview.backgroundWidth += event.dx
                else:
                    taskview.backgroundWidth = taskview.backgroundWidth * (taskview.backgroundHeight + event.dy) / taskview.backgroundHeight
                    taskview.backgroundHeight += event.dy
                self.backgroundImage.mesh.resize(taskview.backgroundWidth, taskview.backgroundHeight)
                taskview.fixateBackground()
                
        self.dragButton = self.backgroundBox.addView(gui3d.ToggleButton('Move & Resize'))
        
        @self.dragButton.event
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.dragButton, event)
            self.backgroundImage.mesh.setPickable(self.dragButton.selected)
            
        self.projectBackgroundButton = self.backgroundBox.addView(gui3d.Button('Project background'))
                
        @self.projectBackgroundButton.event
        def onClicked(event):
            taskview.projectBackground()
            
        self.projectLightingButton = self.backgroundBox.addView(gui3d.Button('Project lighting'))
                
        @self.projectLightingButton.event
        def onClicked(event):
            taskview.projectLighting()

    def onShow(self, event):
        
        gui3d.TaskView.onShow(self, event)
        self.backgroundImage.mesh.setPickable(self.dragButton.selected)

    def onHide(self, event):
        
        gui3d.TaskView.onHide(self, event)
        self.backgroundImage.mesh.setPickable(0)
