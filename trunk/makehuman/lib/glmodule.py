#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import sys
import math
import atexit
import numpy as np

import OpenGL
OpenGL.ERROR_CHECKING = False
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.framebufferobjects import *
from OpenGL.GL.ARB.transpose_matrix import *
from OpenGL.GL.ARB.multisample import *

from core import G
from image import Image
import matrix
from debugdump import DebugDump
import log
from texture import Texture
import profiler

g_primitiveMap = [GL_POINTS, GL_LINES, GL_TRIANGLES, GL_QUADS]

def createShaderType(source, type):
    if not bool(glCreateShader):
        raise RuntimeError("No shader support detected")

    v = glCreateShader(type)
    glShaderSource(v, source)
    glCompileShader(v)
    if not glGetShaderiv(v, GL_COMPILE_STATUS):
        log = glGetShaderInfoLog(v)
        raise RuntimeError("Error compiling vertex shader: %s" % log)

    return v

def createVertexShader(source):
    return createShaderType(source, GL_VERTEX_SHADER)

def createFragmentShader(source):
    return createShaderType(source, GL_FRAGMENT_SHADER)

def createShader(vertexShader, fragmentShader):
    if not bool(glCreateProgram):
        raise RuntimeError("No shader support detected")

    program = glCreateProgram()

    glAttachShader(program, vertexShader)
    glAttachShader(program, fragmentShader)

    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise RuntimeError("Error linking shader: %s" % glGetProgramInfoLog(program))

    return program

def queryDepth(sx, sy):
    sz = np.zeros((1,), dtype=np.float32)
    glReadPixels(sx, G.windowHeight - sy, 1, 1, GL_DEPTH_COMPONENT, GL_DOUBLE, sz)
    return sz[0]

def grabScreen(x, y, width, height, filename = None):
    if width <= 0 or height <= 0:
        raise RuntimeError("width or height is 0")

    log.debug('grabScreen: %d %d %d %d', x, y, width, height)

    # Draw before grabbing, to make sure we grab a rendering and not a picking buffer
    draw()

    sx0 = x
    sy0 = G.windowHeight - y - height
    sx1 = sx0 + width
    sy1 = sy0 + height

    sx0 = max(sx0, 0)
    sx1 = min(sx1, G.windowWidth)
    sy0 = max(sy0, 0)
    sy1 = min(sy1, G.windowHeight)

    rwidth = sx1 - sx0
    rwidth -= rwidth % 4
    sx1 = sx0 + rwidth
    rheight = sy1 - sy0

    surface = np.empty((rheight, rwidth, 3), dtype = np.uint8)

    log.debug('glReadPixels: %d %d %d %d', sx0, sy0, rwidth, rheight)

    glReadPixels(sx0, sy0, rwidth, rheight, GL_RGB, GL_UNSIGNED_BYTE, surface)

    if width != rwidth or height != rheight:
        surf = np.zeros((height, width, 3), dtype = np.uint8) + 127
        surf[...] = surface[:1,:1,:]
        dx0 = (width - rwidth) / 2
        dy0 = (height - rheight) / 2
        dx1 = dx0 + rwidth
        dy1 = dy0 + rheight
        surf[dy0:dy1,dx0:dx1] = surface
        surface = surf

    surface = np.ascontiguousarray(surface[::-1,:,:])
    surface = Image(data = surface)

    if filename is not None:
        surface.save(filename)

    return surface

pickingBuffer = None

def updatePickingBuffer():
    width = G.windowWidth
    height = G.windowHeight
    rwidth = (width + 3) / 4 * 4

    # Resize the buffer in case the window size has changed
    global pickingBuffer
    if pickingBuffer is None or pickingBuffer.shape != (height, rwidth, 3):
        pickingBuffer = np.empty((height, rwidth, 3), dtype = np.uint8)

    # Turn off lighting
    glDisable(GL_LIGHTING)

    # Turn off antialiasing
    glDisable(GL_BLEND)
    if have_multisample:
        glDisable(GL_MULTISAMPLE)

    # Clear screen
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    drawMeshes(True)

    # Make sure the data is 1 byte aligned
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    #glFlush()
    #glFinish()
    glReadPixels(0, 0, rwidth, height, GL_RGB, GL_UNSIGNED_BYTE, pickingBuffer)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Turn on antialiasing
    glEnable(GL_BLEND)
    if have_multisample:
        glEnable(GL_MULTISAMPLE)

    # restore lighting
    glEnable(GL_LIGHTING)

    # draw()

def getPickedColor(x, y):
    y = G.windowHeight - y

    if y < 0 or y >= G.windowHeight or x < 0 or x >= G.windowWidth:
        G.color_picked = (0, 0, 0)
        return

    if pickingBuffer is None:
        updatePickingBuffer()

    G.color_picked = tuple(pickingBuffer[y,x,:])

def reshape(w, h):
    # Prevent a division by zero when minimising the window
    if h == 0:
        h = 1
    # Set the drawable region of the window
    glViewport(0, 0, w, h)
    # set up the projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # go back to modelview matrix so we can move the objects about
    glMatrixMode(GL_MODELVIEW)

    updatePickingBuffer()

def drawBegin():
    # clear the screen & depth buffer
    glClearColor(G.clearColor[0], G.clearColor[1], G.clearColor[2], G.clearColor[3])
    glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)

def drawEnd():
    G.swapBuffers()

have_multisample = None

def OnInit():
    def A(*args):
        return np.array(list(args), dtype=np.float32)

    try:
        # Start with writing relevant info to the debug dump in case stuff goes
        # wrong at a later time
        debugdump = DebugDump()
        debugdump.appendMessage("GL.VENDOR: " + glGetString(GL_VENDOR))
        debugdump.appendMessage("GL.RENDERER: " + glGetString(GL_RENDERER))
        debugdump.appendMessage("GL.VERSION: " + glGetString(GL_VERSION))
    except Exception as e:
        log.error("Failed to GL debug info to debug dump: %s", format(str(e)))

    global have_multisample
    have_multisample = glInitMultisampleARB()

    # Lights and materials
    lightPos = A( -10.99, 20.0, 20.0, 1.0)  # Light - Position
    ambientLight =  A(0.0, 0.0, 0.0, 1.0)   # Light - Ambient Values
    diffuseLight =  A(1.0, 1.0, 1.0, 1.0)   # Light - Diffuse Values
    specularLight = A(1.0, 1.0, 1.0, 1.0)   # Light - Specular Values

    MatAmb = A(0.11, 0.11, 0.11, 1.0)       # Material - Ambient Values
    MatDif = A(1.0, 1.0, 1.0, 1.0)          # Material - Diffuse Values
    MatSpc = A(0.2, 0.2, 0.2, 1.0)          # Material - Specular Values
    MatShn = A(10.0,)                       # Material - Shininess
    MatEms = A(0.1, 0.05, 0.0, 1.0)         # Material - Emission Values

    glEnable(GL_DEPTH_TEST)                                  # Hidden surface removal
    # glEnable(GL_CULL_FACE)                                   # Inside face removal
    # glEnable(GL_ALPHA_TEST)
    # glAlphaFunc(GL_GREATER, 0.0)
    glDisable(GL_DITHER)
    glEnable(GL_LIGHTING)                                    # Enable lighting
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specularLight)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glLightModeli(GL_LIGHT_MODEL_COLOR_CONTROL, GL_SEPARATE_SPECULAR_COLOR) #  If we enable this, we have stronger specular highlights
    glMaterialfv(GL_FRONT, GL_AMBIENT, MatAmb)               # Set Material Ambience
    glMaterialfv(GL_FRONT, GL_DIFFUSE, MatDif)               # Set Material Diffuse
    glMaterialfv(GL_FRONT, GL_SPECULAR, MatSpc)              # Set Material Specular
    glMaterialfv(GL_FRONT, GL_SHININESS, MatShn)             # Set Material Shininess
    # glMaterialfv(GL_FRONT, GL_EMISSION, MatEms)            # Set Material Emission
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    # glEnable(GL_TEXTURE_2D)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # Activate and specify pointers to vertex and normal array
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glEnableClientState(GL_VERTEX_ARRAY)
    if have_multisample:
        glEnable(GL_MULTISAMPLE)

def OnExit():
    # Deactivate the pointers to vertex and normal array
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    # glDisableClientState(GL_TEXTURE_COORD_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)
    log.message("Exit from event loop\n")

def cameraPosition(camera, eye):
    proj, mv = camera.getMatrices(eye)
    glMatrixMode(GL_PROJECTION)
    glLoadMatrixd(np.ascontiguousarray(proj.T))
    glMatrixMode(GL_MODELVIEW)
    glLoadMatrixd(np.ascontiguousarray(mv.T))

def transformObject(obj):
    glMultMatrixd(np.ascontiguousarray(obj.transform.T))

def setObjectUniforms(obj):
    if obj.uniforms is None:
        obj.uniforms = []
        parameterCount = glGetProgramiv(obj.shader, GL_ACTIVE_UNIFORMS)
        for index in xrange(parameterCount):
            name, size, type = glGetActiveUniform(obj.shader, index)
            obj.uniforms.append((name, size, type))

    currentTextureSampler = 1

    for index, (name, size, type) in enumerate(obj.uniforms):
        value = obj.shaderParameters.get(name)

        if value is not None:
            if type == GL_FLOAT:
                glUniform1f(index, value)
            elif type == GL_FLOAT_VEC2:
                if hasattr(value, '__len__') and len(value) == 2:
                    glUniform2f(index, *value)
            elif type == GL_FLOAT_VEC3:
                if hasattr(value, '__len__') and len(value) == 3:
                    glUniform3f(index, *value)
            elif type == GL_FLOAT_VEC4:
                if hasattr(value, '__len__') and len(value) == 4:
                    glUniform4f(index, *value)
            elif type == GL_SAMPLER_1D:
                glActiveTexture(GL_TEXTURE0 + currentTextureSampler)
                glBindTexture(GL_TEXTURE_1D, value)
                glUniform1i(index, currentTextureSampler)
                currentTextureSampler += 1
            elif type == GL_SAMPLER_2D:
                glActiveTexture(GL_TEXTURE0 + currentTextureSampler)
                glBindTexture(GL_TEXTURE_2D, value)
                glUniform1i(index, currentTextureSampler)
                currentTextureSampler += 1

def drawMesh(obj):
    if not obj.visibility:
        return

    glDepthFunc(GL_LEQUAL)

    # Transform the current object
    glPushMatrix()
    transformObject(obj)

    if obj.texture and obj.solid:
        glEnable(GL_TEXTURE_2D)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glBindTexture(GL_TEXTURE_2D, obj.texture)
        glTexCoordPointer(2, GL_FLOAT, 0, obj.UVs)

        if obj.nTransparentPrimitives:
            obj.sortFaces()

    # Fill the array pointers with object mesh data
    glVertexPointer(3, GL_FLOAT, 0, obj.verts)
    glNormalPointer(GL_FLOAT, 0, obj.norms)
    glColorPointer(4, GL_UNSIGNED_BYTE, 0, obj.color)

    # Disable lighting if the object is shadeless
    if obj.shadeless:
        glDisable(GL_LIGHTING)

    if obj.cull:
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK if obj.cull > 0 else GL_FRONT)

    # Enable the shader if the driver supports it and there is a shader assigned
    if obj.shader and obj.solid:
        if bool(glUseProgram):
            glUseProgram(obj.shader)

            # This should be optimized, since we only need to do it when it's changed
            # Validation should also only be done when it is set
            if obj.shaderParameters:
                setObjectUniforms(obj)

    # draw the mesh
    if not obj.solid:
        glDisableClientState(GL_COLOR_ARRAY)
        glColor3f(0.0, 0.0, 0.0)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glDrawElements(g_primitiveMap[obj.vertsPerPrimitive-1], obj.primitives.size, GL_UNSIGNED_INT, obj.primitives)
        glEnableClientState(GL_COLOR_ARRAY)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glEnable(GL_POLYGON_OFFSET_FILL)
        glPolygonOffset(1.0, 1.0)
        glDrawElements(g_primitiveMap[obj.vertsPerPrimitive-1], obj.primitives.size, GL_UNSIGNED_INT, obj.primitives)
        glDisable(GL_POLYGON_OFFSET_FILL)
    elif obj.nTransparentPrimitives:
        glDepthMask(GL_FALSE)
        glEnable(GL_ALPHA_TEST)
        glAlphaFunc(GL_GREATER, 0.0)
        glDrawElements(g_primitiveMap[obj.vertsPerPrimitive-1], obj.primitives.size, GL_UNSIGNED_INT, obj.primitives)
        glDisable(GL_ALPHA_TEST)
        glDepthMask(GL_TRUE)
    elif obj.depthless:
        glDepthMask(GL_FALSE)
        glDisable(GL_DEPTH_TEST)
        glDrawElements(g_primitiveMap[obj.vertsPerPrimitive-1], obj.primitives.size, GL_UNSIGNED_INT, obj.primitives)
        glEnable(GL_DEPTH_TEST)
        glDepthMask(GL_TRUE)
    else:
        glDrawElements(g_primitiveMap[obj.vertsPerPrimitive-1], obj.primitives.size, GL_UNSIGNED_INT, obj.primitives)

    if obj.solid and not obj.nTransparentPrimitives:
        glDisableClientState(GL_COLOR_ARRAY)
        for i, (start, count) in enumerate(obj.groups):
            color = obj.gcolor(i)
            if color is None or np.all(color[:3] == 255):
                continue
            glColor4ub(*color)
            indices = obj.primitives[start:start+count,:]
            glDrawElements(g_primitiveMap[obj.vertsPerPrimitive-1], indices.size, GL_UNSIGNED_INT, indices)
        glEnableClientState(GL_COLOR_ARRAY)

    # Disable the shader if the driver supports it and there is a shader assigned
    if obj.shader and obj.solid:
        if bool(glUseProgram):
            glUseProgram(0)
        glActiveTexture(GL_TEXTURE0)

    glDisable(GL_CULL_FACE)

    # Enable lighting if the object was shadeless
    if obj.shadeless:
        glEnable(GL_LIGHTING)

    if obj.texture and obj.solid:
        glDisable(GL_TEXTURE_2D)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

    glPopMatrix()

def pickMesh(obj):
    if not obj.visibility:
        return
    if not obj.pickable:
        return

    # Transform the current object
    glPushMatrix()
    transformObject(obj)

    # Fill the array pointers with object mesh data
    glVertexPointer(3, GL_FLOAT, 0, obj.verts)
    glNormalPointer(GL_FLOAT, 0, obj.norms)

    # Use color to pick i
    glDisableClientState(GL_COLOR_ARRAY)

    # Disable lighting
    glDisable(GL_LIGHTING)

    if obj.cull:
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK if obj.cull > 0 else GL_FRONT)

    # draw the meshes
    for i, (start, count) in enumerate(obj.groups):
        glColor3ub(*obj.clrid(i))
        indices = obj.primitives[start:start+count,:]
        glDrawElements(g_primitiveMap[obj.vertsPerPrimitive-1], indices.size, GL_UNSIGNED_INT, indices)

    glDisable(GL_CULL_FACE)

    glEnable(GL_LIGHTING)
    glEnableClientState(GL_COLOR_ARRAY)

    glPopMatrix()

def drawOrPick(pickMode, obj):
    if pickMode:
        if hasattr(obj, 'pick'):
            obj.pick()
    else:
        if hasattr(obj, 'draw'):
            obj.draw()

_hasRenderSkin = None
def hasRenderSkin():
    global _hasRenderSkin
    if _hasRenderSkin is None:
        _hasRenderSkin = all([
            bool(glGenRenderbuffers), bool(glBindRenderbuffer), bool(glRenderbufferStorage),
            bool(glGenFramebuffers), bool(glBindFramebuffer), bool(glFramebufferRenderbuffer)])
    return _hasRenderSkin
               
def renderSkin(dst, vertsPerPrimitive, verts, index = None, objectMatrix = None,
               texture = None, UVs = None, textureMatrix = None,
               color = None, clearColor = None):

    if isinstance(dst, Texture):
        glBindTexture(GL_TEXTURE_2D, dst.textureId)
    elif isinstance(dst, Image):
        dst = Texture(image = dst)
    elif isinstance(dst, tuple):
        dst = Texture(size = dst)
    else:
        raise RuntimeError('Unsupported destination: %r' % dst)

    width, height = dst.width, dst.height

    framebuffer = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, framebuffer)
    glFramebufferTexture2D(GL_DRAW_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, dst.textureId, 0)
    glFramebufferTexture2D(GL_READ_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, dst.textureId, 0)

    if clearColor is not None:
        glClearColor(clearColor[0], clearColor[1], clearColor[2], clearColor[3])
        glClear(GL_COLOR_BUFFER_BIT)

    glVertexPointer(verts.shape[-1], GL_FLOAT, 0, verts)

    if texture is not None and UVs is not None:
        if isinstance(texture, Image):
            tex = Texture()
            tex.loadImage(texture)
            texture = tex
        if isinstance(texture, Texture):
            texture = texture.textureId
        glEnable(GL_TEXTURE_2D)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexCoordPointer(UVs.shape[-1], GL_FLOAT, 0, UVs)

    if color is not None:
        glColorPointer(color.shape[-1], GL_UNSIGNED_BYTE, 0, color)
        glEnableClientState(GL_COLOR_ARRAY)
    else:
        glDisableClientState(GL_COLOR_ARRAY)
        glColor4f(1, 1, 1, 1)

    glDisableClientState(GL_NORMAL_ARRAY)
    glDisable(GL_LIGHTING)

    glDepthMask(GL_FALSE)
    glDisable(GL_DEPTH_TEST)
    # glDisable(GL_CULL_FACE)
    glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)

    glPushAttrib(GL_VIEWPORT_BIT)
    glViewport(0, 0, width, height)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    if objectMatrix is not None:
        glLoadTransposeMatrixd(objectMatrix)
    else:
        glLoadIdentity()

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 1, 0, 1, -100, 100)

    if textureMatrix is not None:
        glMatrixMode(GL_TEXTURE)
        glPushMatrix()
        glLoadTransposeMatrixd(textureMatrix)

    if index is not None:
        glDrawElements(g_primitiveMap[vertsPerPrimitive-1], index.size, GL_UNSIGNED_INT, index)
    else:
        glDrawArrays(g_primitiveMap[vertsPerPrimitive-1], 0, verts[:,:,0].size)

    if textureMatrix is not None:
        glMatrixMode(GL_TEXTURE)
        glPopMatrix()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    glPopAttrib()

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)
    glDepthMask(GL_TRUE)

    glEnable(GL_LIGHTING)
    glEnableClientState(GL_NORMAL_ARRAY)

    glEnableClientState(GL_COLOR_ARRAY)

    glDisable(GL_TEXTURE_2D)
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)

    surface = np.empty((height, width, 4), dtype = np.uint8)
    glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE, surface)
    surface = Image(data = np.ascontiguousarray(surface[::-1,:,:]))

    glFramebufferTexture2D(GL_DRAW_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, 0, 0)
    glFramebufferTexture2D(GL_READ_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, 0, 0)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glDeleteFramebuffers(np.array([framebuffer]))

    return surface

def drawMeshes(pickMode):
    if G.world is None:
        return

    cameraMode = None
    # Draw all objects contained by G.world
    for obj in sorted(G.world, key = (lambda obj: obj.priority)):
        camera = G.cameras[obj.cameraMode]
        if camera.stereoMode:
            glColorMask(GL_TRUE, GL_FALSE, GL_FALSE, GL_TRUE) # Red
            cameraPosition(camera, 1)
            drawOrPick(pickMode, obj)
            glClear(GL_DEPTH_BUFFER_BIT)
            glColorMask(GL_FALSE, GL_TRUE, GL_TRUE, GL_TRUE) # Cyan
            cameraPosition(camera, 2)
            drawOrPick(pickMode, obj)
            # To prevent the GUI from overwritting the red model, we need to render it again in the z-buffer
            glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE) # None, only z-buffer
            cameraPosition(camera, 1)
            drawOrPick(pickMode, obj)
            glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE) # All
            cameraMode = None
        else:
            if cameraMode != obj.cameraMode:
                cameraPosition(camera, 0)
                cameraMode = obj.cameraMode
            drawOrPick(pickMode, obj)

def _draw():
    drawBegin()
    drawMeshes(False)
    drawEnd()

def draw():
    if profiler.active():
        profiler.accum('_draw()', globals(), locals())
    else:
        _draw()
