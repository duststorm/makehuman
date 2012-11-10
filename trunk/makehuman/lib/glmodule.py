
import sys
import math
import atexit
import numpy as np

import OpenGL
OpenGL.ERROR_CHECKING = False
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *

from core import *
import image_base as img
import matrix

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

    p = glCreateProgram()

    glAttachShader(p, vertexShader)
    glAttachShader(p, fragmentShader)

    glLinkProgram(p)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise RuntimeError("Error linking shader: %s" % glGetProgramInfoLog(program))

    return p

def grabScreen(x, y, width, height, filename):
    if width <= 0 or height <= 0:
        raise RuntimeError("width or height is 0")

    # Draw before grabbing, to make sure we grab a rendering and not a picking buffer
    draw()

    rwidth = (width + 3) / 4 * 4

    surface = np.empty((height, rwidth, 3), dtype = np.uint8)

    glReadPixels(x, G.windowHeight - y - height, rwidth, height, GL_RGB, GL_UNSIGNED_BYTE, surface)
    surface = img.fromdata(surface[:,:width,:])
    surface = surface.flip_vertical()

    surface.save(filename)

pickingBuffer = None

def updatePickingBuffer():
    width = G.windowWidth
    height = G.windowHeight

    # Resize the buffer in case the window size has changed
    global pickingBuffer
    if pickingBuffer is None or pickingBuffer.shape != (height, width, 3):
        pickingBuffer = np.empty((height, width, 3), dtype = np.uint8)

    # Turn off lighting
    glDisable(GL_LIGHTING)

    # Turn off antialiasing
    glDisable(GL_BLEND)
    glDisable(GL_MULTISAMPLE)

    # Clear screen
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for i, camera in enumerate(G.cameras):
        cameraPosition(camera, 0)
        drawMeshes(1, i)

    # Make sure the data is 1 byte aligned
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    #glFlush()
    #glFinish()
    glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE, pickingBuffer)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Turn on antialiasing
    glEnable(GL_BLEND)
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
    G.windowHeight = h
    G.windowWidth = w

    updatePickingBuffer()

    callResize(w, h, False)

def drawBegin():
    # clear the screen & depth buffer
    glClearColor(G.clearColor[0], G.clearColor[1], G.clearColor[2], G.clearColor[3])
    glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)

def drawEnd():
    G.swapBuffers()

def OnInit():
    def A(*args):
        return np.array(list(args), dtype=np.float32)

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
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # Activate and specify pointers to vertex and normal array
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glEnableClientState(GL_VERTEX_ARRAY)

def OnExit():
    # Deactivate the pointers to vertex and normal array
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    # glDisableClientState(GL_TEXTURE_COORD_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)
    print "Exit from event loop\n"

def cameraPosition(camera, eye):
    proj, mv = camera.getMatrices(eye)
    glMatrixMode(GL_PROJECTION)
    glLoadMatrixd(np.ascontiguousarray(proj.T))
    glMatrixMode(GL_MODELVIEW)
    glLoadMatrixd(np.ascontiguousarray(mv.T))

def transformObject(obj):
    glMultMatrixd(np.ascontiguousarray(objectTransform(obj).T))

def objectTransform(obj):
    m = matrix.translate((obj.x, obj.y, obj.z))
    if any(x != 0 for x in obj.parent.rot):
        m = m * matrix.rotx(obj.rx)
        m = m * matrix.roty(obj.ry)
        m = m * matrix.rotz(obj.rz)
    if any(x != 1 for x in obj.parent.scale):
        m = m * matrix.scale((obj.sx, obj.sy, obj.sz))
    return m

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

def drawMesh(obj, cameraType):
    if obj.cameraMode != cameraType:
        return
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

    # Enable lighting if the object was shadeless
    if obj.shadeless:
        glEnable(GL_LIGHTING)

    if obj.texture and obj.solid:
        glDisable(GL_TEXTURE_2D)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

    glPopMatrix()

def pickMesh(obj, cameraType):
    if obj.cameraMode != cameraType:
        return
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

    # draw the meshes
    for i, (start, count) in enumerate(obj.groups):
        glColor3ub(*obj.clrid(i))
        indices = obj.primitives[start:start+count,:]
        glDrawElements(g_primitiveMap[obj.vertsPerPrimitive-1], indices.size, GL_UNSIGNED_INT, indices)

    glEnable(GL_LIGHTING)
    glEnableClientState(GL_COLOR_ARRAY)

    glPopMatrix()

def drawMeshes(pickMode, cameraType):
    if G.world is None:
        return

    # Draw all objects contained by G.world
    for obj in G.world:
        if pickMode:
            if hasattr(obj, 'pick'):
                obj.pick(cameraType)
        else:
            if hasattr(obj, 'draw'):
                obj.draw(cameraType)

def _draw():
    drawBegin()

    for i, camera in enumerate(G.cameras):
        # draw the objects in dynamic camera
        if camera.stereoMode:
            glColorMask(GL_TRUE, GL_FALSE, GL_FALSE, GL_TRUE) # Red
            cameraPosition(camera, 1)
            drawMeshes(0, i)
            glClear(GL_DEPTH_BUFFER_BIT)
            glColorMask(GL_FALSE, GL_TRUE, GL_TRUE, GL_TRUE) # Cyan
            cameraPosition(camera, 2)
            drawMeshes(0, i)
            # To prevent the GUI from overwritting the red model, we need to render it again in the z-buffer
            glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE) # None, only z-buffer
            cameraPosition(camera, 1)
            drawMeshes(0, i)
            glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE) # All
        else:
            cameraPosition(camera, 0)
            drawMeshes(0, i)

    drawEnd()

def draw():
    if G.profile:
        profiler.accum('_draw()', globals(), locals())
    else:
        _draw()

def drawOneMesh(obj):
    glDrawBuffer(GL_FRONT)
    glClear(GL_DEPTH_BUFFER_BIT)
    cameraPosition(G.cameras[obj.cameraMode], 0)
    obj.draw(obj.cameraMode)
    glDrawBuffer(GL_BACK)
    glFlush()
