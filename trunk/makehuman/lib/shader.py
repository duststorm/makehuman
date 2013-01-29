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

import os.path
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.ARB.texture_multisample import *
import texture
import log

class Uniform(object):
    def __init__(self, index, name, pytype, dims):
        self.index = index
        self.name = name
        self.pytype = pytype
        self.dims = dims

    def __call__(self, index, values):
        raise NotImplementedError

class VectorUniform(object):
    def __init__(self, index, name, pytype, dims, type, func):
        super(VectorUniform, self).__init__(index, name, pytype, dims)
        self.type = type
        self.func = func

    def __call__(self, data):
        self.call(self.values(data))

    def values(self, data):
        return np.asarray(data, dtype=self.type).reshape(self.dims)

    def call(self, values):
        self.func(self.index, len(values), values)

class MatrixUniform(VectorUniform):
    def call(self, values):
        self.func(self.index, 1, GL_TRUE, values)

class SamplerUniform(Uniform):
    def __init__(self, index, name, target):
        super(SamplerUniform, self).__init__(index, name, str, (1,))
        self.target = target

    def __call__(self, data):
        cls = type(self)
        glActiveTexture(GL_TEXTURE0 + cls.currentSampler)
        glBindTexture(self.target, texture.getTexture(data).textureId)
        glUniform1i(self.index, cls.currentSampler)
        cls.currentSampler += 1

    @classmethod
    def reset(cls):
        cls.currentSampler = 1

class Shader(object):
    _supported = None

    @classmethod
    def supported(cls):
        if cls._supported is None:
            cls._supported = bool(glCreateProgram)
        return cls._supported

    def __init__(self, path):
        if not self.supported():
            raise RuntimeError("No shader support detected")

        super(Shader, self).__init__()

        self.path = path

        self.vertexId = None
        self.fragmentId = None
        self.shaderId = None
        self.modified = None
        self.uniforms = None

        self.initShader()

    def __del__(self):
        try:
            self.delete()
        except StandardError:
            pass

    @staticmethod
    def createShader(file, type):
        with open(file, 'rU') as f:
            source = f.read()
        shader = glCreateShader(type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            logmsg = glGetShaderInfoLog(shader)
            log.error("Error compiling shader: %s", logmsg)
            return None
        return shader

    def delete(self):
        if self.vertexId:
            glDeleteShader(self.vertexId)
            self.vertexId = None
        if self.fragmentId:
            glDeleteShader(self.fragmentId)
            self.fragmentId = None
        if self.shaderId:
            glDeleteProgram(self.shaderId)
            self.shaderId = None

    def initShader(self):
        vertexSource = self.path + '_vertex_shader.txt'
        geometrySource = self.path + '_geometry_shader.txt'
        fragmentSource = self.path + '_fragment_shader.txt'

        self.shaderId = glCreateProgram()

        if os.path.isfile(vertexSource):
            self.vertexId = self.createShader(vertexSource, GL_VERTEX_SHADER)
            glAttachShader(self.shaderId, self.vertexId)

        if os.path.isfile(geometrySource) and 'GL_GEOMETRY_SHADER' in globals():
            self.geometryId = self.createShader(geometrySource, GL_GEOMETRY_SHADER)
            glAttachShader(self.shaderId, self.geometryId)

        if os.path.isfile(fragmentSource):
            self.fragmentId = self.createShader(fragmentSource, GL_FRAGMENT_SHADER)
            glAttachShader(self.shaderId, self.fragmentId)

        glLinkProgram(self.shaderId)
        if not glGetProgramiv(self.shaderId, GL_LINK_STATUS):
            log.error("Error linking shader: %s", glGetProgramInfoLog(self.shaderId))
            self.delete()
            return

        self.uniforms = None

    uniformTypes = {
        GL_FLOAT:               ((1,),  np.float32,     float,  glUniform1fv),
        GL_FLOAT_VEC2:          ((2,),  np.float32,     float,  glUniform2fv),
        GL_FLOAT_VEC3:          ((3,),  np.float32,     float,  glUniform3fv),
        GL_FLOAT_VEC4:          ((4,),  np.float32,     float,  glUniform4fv),
        GL_INT:                 ((1,),  np.int32,       int,    glUniform1iv),
        GL_INT_VEC2:            ((2,),  np.int32,       int,    glUniform2iv),
        GL_INT_VEC3:            ((3,),  np.int32,       int,    glUniform3iv),
        GL_INT_VEC4:            ((4,),  np.int32,       int,    glUniform4iv),
        GL_UNSIGNED_INT:        ((1,),  np.uint32,      int,    glUniform1uiv),
        GL_UNSIGNED_INT_VEC2:   ((2,),  np.uint32,      int,    glUniform2uiv),
        GL_UNSIGNED_INT_VEC3:   ((3,),  np.uint32,      int,    glUniform3uiv),
        GL_UNSIGNED_INT_VEC4:   ((4,),  np.uint32,      int,    glUniform4uiv),
        GL_BOOL:                ((1,),  np.int32,       bool,   glUniform1iv),
        GL_BOOL_VEC2:           ((2,),  np.int32,       bool,   glUniform2iv),
        GL_BOOL_VEC3:           ((3,),  np.int32,       bool,   glUniform3iv),
        GL_BOOL_VEC4:           ((4,),  np.int32,       bool,   glUniform4iv),
        GL_FLOAT_MAT2:          ((2,2), np.float32,     float,  glUniformMatrix2fv),
        GL_FLOAT_MAT2x3:        ((2,3), np.float32,     float,  glUniformMatrix2x3fv),
        GL_FLOAT_MAT2x4:        ((2,4), np.float32,     float,  glUniformMatrix2x4fv),
        GL_FLOAT_MAT3x2:        ((3,2), np.float32,     float,  glUniformMatrix3x2fv),
        GL_FLOAT_MAT3:          ((3,3), np.float32,     float,  glUniformMatrix3fv),
        GL_FLOAT_MAT3x4:        ((3,4), np.float32,     float,  glUniformMatrix3x4fv),
        GL_FLOAT_MAT4x2:        ((4,2), np.float32,     float,  glUniformMatrix4x2fv),
        GL_FLOAT_MAT4x3:        ((4,3), np.float32,     float,  glUniformMatrix4x3fv),
        GL_FLOAT_MAT4:          ((4,4), np.float32,     float,  glUniformMatrix4fv),
        }

    if 'glUniform1dv' in globals():
        uniformTypes2 = {
            GL_DOUBLE:              ((1,),  np.float64,     float,  glUniform1dv),
            GL_DOUBLE_VEC2:         ((2,),  np.float64,     float,  glUniform2dv),
            GL_DOUBLE_VEC3:         ((3,),  np.float64,     float,  glUniform3dv),
            GL_DOUBLE_VEC4:         ((4,),  np.float64,     float,  glUniform4dv),
            GL_DOUBLE_MAT2:         ((2,2), np.float64,     float,  glUniformMatrix2dv),
            GL_DOUBLE_MAT2x3:       ((2,3), np.float64,     float,  glUniformMatrix2x3dv),
            GL_DOUBLE_MAT2x4:       ((2,4), np.float64,     float,  glUniformMatrix2x4dv),
            GL_DOUBLE_MAT3x2:       ((3,2), np.float64,     float,  glUniformMatrix3x2dv),
            GL_DOUBLE_MAT3:         ((3,3), np.float64,     float,  glUniformMatrix3dv),
            GL_DOUBLE_MAT3x4:       ((3,4), np.float64,     float,  glUniformMatrix3x4dv),
            GL_DOUBLE_MAT4x2:       ((4,2), np.float64,     float,  glUniformMatrix4x2dv),
            GL_DOUBLE_MAT4x3:       ((4,3), np.float64,     float,  glUniformMatrix4x3dv),
            GL_DOUBLE_MAT4:         ((4,4), np.float64,     float,  glUniformMatrix4dv),
            }

    textureTargets = {
        GL_SAMPLER_1D:                                  GL_TEXTURE_1D,
        GL_SAMPLER_2D:                                  GL_TEXTURE_2D,
        GL_SAMPLER_3D:                                  GL_TEXTURE_3D,
        GL_SAMPLER_CUBE:                                GL_TEXTURE_CUBE_MAP,
        GL_SAMPLER_1D_SHADOW:                           GL_TEXTURE_1D,
        GL_SAMPLER_2D_SHADOW:                           GL_TEXTURE_2D,
        GL_SAMPLER_1D_ARRAY:                            GL_TEXTURE_1D_ARRAY,
        GL_SAMPLER_2D_ARRAY:                            GL_TEXTURE_2D_ARRAY,
        GL_SAMPLER_1D_ARRAY_SHADOW:                     GL_TEXTURE_1D_ARRAY,
        GL_SAMPLER_2D_ARRAY_SHADOW:                     GL_TEXTURE_2D_ARRAY,
        GL_SAMPLER_2D_MULTISAMPLE:                      GL_TEXTURE_2D_MULTISAMPLE,
        GL_SAMPLER_2D_MULTISAMPLE_ARRAY:                GL_TEXTURE_2D_MULTISAMPLE_ARRAY,
        GL_SAMPLER_CUBE_SHADOW:                         GL_TEXTURE_CUBE_MAP,
        GL_SAMPLER_BUFFER:                              GL_TEXTURE_BUFFER,
        GL_SAMPLER_2D_RECT:                             GL_TEXTURE_RECTANGLE,
        GL_SAMPLER_2D_RECT_SHADOW:                      GL_TEXTURE_RECTANGLE,
        GL_INT_SAMPLER_1D:                              GL_TEXTURE_1D,
        GL_INT_SAMPLER_2D:                              GL_TEXTURE_2D,
        GL_INT_SAMPLER_3D:                              GL_TEXTURE_3D,
        GL_INT_SAMPLER_CUBE:                            GL_TEXTURE_CUBE_MAP,
        GL_INT_SAMPLER_1D_ARRAY:                        GL_TEXTURE_1D_ARRAY,
        GL_INT_SAMPLER_2D_ARRAY:                        GL_TEXTURE_2D_ARRAY,
        GL_INT_SAMPLER_2D_MULTISAMPLE:                  GL_TEXTURE_2D_MULTISAMPLE,
        GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY:            GL_TEXTURE_2D_MULTISAMPLE_ARRAY,
        GL_INT_SAMPLER_BUFFER:                          GL_TEXTURE_BUFFER,
        GL_INT_SAMPLER_2D_RECT:                         GL_TEXTURE_RECTANGLE,
        GL_UNSIGNED_INT_SAMPLER_1D:                     GL_TEXTURE_1D,
        GL_UNSIGNED_INT_SAMPLER_2D:                     GL_TEXTURE_2D,
        GL_UNSIGNED_INT_SAMPLER_3D:                     GL_TEXTURE_3D,
        GL_UNSIGNED_INT_SAMPLER_CUBE:                   GL_TEXTURE_CUBE_MAP,
        GL_UNSIGNED_INT_SAMPLER_1D_ARRAY:               GL_TEXTURE_1D_ARRAY,
        GL_UNSIGNED_INT_SAMPLER_2D_ARRAY:               GL_TEXTURE_2D_ARRAY,
        GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE:         GL_TEXTURE_2D_MULTISAMPLE,
        GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY:   GL_TEXTURE_2D_MULTISAMPLE_ARRAY,
        GL_UNSIGNED_INT_SAMPLER_BUFFER:                 GL_TEXTURE_BUFFER,
        GL_UNSIGNED_INT_SAMPLER_2D_RECT:                GL_TEXTURE_RECTANGLE,
        }

    if 'GL_IMAGE_1D' in globals():    
        try:
            textureTargets2 = {
                GL_IMAGE_1D:                                    GL_TEXTURE_1D,
                GL_IMAGE_2D:                                    GL_TEXTURE_2D,
                GL_IMAGE_3D:                                    GL_TEXTURE_3D,
                GL_IMAGE_2D_RECT:                               GL_TEXTURE_2D_RECTANGLE,
                GL_IMAGE_CUBE:                                  GL_TEXTURE_CUBE_MAP,
                GL_IMAGE_BUFFER:                                GL_TEXTURE_BUFFER,
                GL_IMAGE_1D_ARRAY:                              GL_TEXTURE_1D_ARRAY,
                GL_IMAGE_2D_ARRAY:                              GL_TEXTURE_2D_ARRAY,
                GL_IMAGE_2D_MULTISAMPLE:                        GL_TEXTURE_2D_MULTISAMPLE,
                GL_IMAGE_2D_MULTISAMPLE_ARRAY:                  GL_TEXTURE_2D_MULTISAMPLE_ARRAY,
                GL_INT_IMAGE_1D:                                GL_TEXTURE_1D,
                GL_INT_IMAGE_2D:                                GL_TEXTURE_2D,
                GL_INT_IMAGE_3D:                                GL_TEXTURE_3D,
                GL_INT_IMAGE_2D_RECT:                           GL_TEXTURE_2D_RECTANGLE,
                GL_INT_IMAGE_CUBE:                              GL_TEXTURE_CUBE_MAP,
                GL_INT_IMAGE_BUFFER:                            GL_TEXTURE_BUFFER,
                GL_INT_IMAGE_1D_ARRAY:                          GL_TEXTURE_1D_ARRAY,
                GL_INT_IMAGE_2D_ARRAY:                          GL_TEXTURE_2D_ARRAY,
                GL_INT_IMAGE_2D_MULTISAMPLE:                    GL_TEXTURE_2D_MULTISAMPLE,
                GL_INT_IMAGE_2D_MULTISAMPLE_ARRAY:              GL_TEXTURE_2D_MULTISAMPLE_ARRAY,
                GL_UNSIGNED_INT_IMAGE_1D:                       GL_TEXTURE_1D,
                GL_UNSIGNED_INT_IMAGE_2D:                       GL_TEXTURE_2D,
                GL_UNSIGNED_INT_IMAGE_3D:                       GL_TEXTURE_3D,
                GL_UNSIGNED_INT_IMAGE_2D_RECT:                  GL_TEXTURE_2D_RECTANGLE,
                GL_UNSIGNED_INT_IMAGE_CUBE:                     GL_TEXTURE_CUBE_MAP,
                GL_UNSIGNED_INT_IMAGE_BUFFER:                   GL_TEXTURE_BUFFER,
                GL_UNSIGNED_INT_IMAGE_1D_ARRAY:                 GL_TEXTURE_1D_ARRAY,
                GL_UNSIGNED_INT_IMAGE_2D_ARRAY:                 GL_TEXTURE_2D_ARRAY,
                GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE:           GL_TEXTURE_2D_MULTISAMPLE,
                GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE_ARRAY:     GL_TEXTURE_2D_MULTISAMPLE_ARRAY,
                }
        except:
            pass


    def getUniforms(self):
        if self.uniforms is None:
            if hasattr(self, 'uniformTypes2') and self.uniformTypes2:
                self.uniformTypes.update(self.uniformTypes2)
                self.uniformTypes2.clear()

            if hasattr(self, 'textureTargets2') and self.textureTargets2:
                self.textureTargets.update(self.textureTargets2)
                self.textureTargets2.clear()

            parameterCount = glGetProgramiv(self.shaderId, GL_ACTIVE_UNIFORMS)
            self.uniforms = []
            for index in xrange(parameterCount):
                name, size, type = glGetActiveUniform(self.shaderId, index)
                if type in self.uniformTypes:
                    dims, nptype, pytype, glfunc = self.uniformTypes[type]
                    if len(values.shape) > 1:
                        func = MatrixUniform(index, name, pytype, dims, nptype, glfunc)
                    else:
                        func = VectorUniform(index, name, pytype, dims, nptype, glfunc)
                elif type in self.textureTargets:
                    target = self.textureTargets[type]
                    func = SamplerUniform(index, name, target)
                self.uniforms.append(func)

        return self.uniforms

    def setUniforms(self, params):
        SamplerUniform.reset()

        for uniform in self.getUniforms():
            value = params.get(name)
            if value is not None:
                uniform(value)

_shaderCache = {}

def getShader(path, cache=None):
    shader = None
    cache = cache or _shaderCache

    path1 = path + '_vertex_shader.txt'
    path2 = path + '_fragment_shader.txt'
    path3 = path + '_geometry_shader.txt'
    paths = [p for p in [path1, path2, path3] if os.path.isfile(p)]
    if not paths:
        cache[path] = False
        return False

    mtime = max(os.path.getmtime(p) for p in paths)

    if path in cache:
        shader = cache[path]
        if shader is False:
            return shader

        if mtime >= shader.modified:
            log.message('reloading %s', path)
            try:
                shader.initShader()
                shader.modified = mtime
            except RuntimeError, text:
                log.error("Error loading shader %s", path, exc_info=True)
                shader = False
    else:
        try:
            shader = Shader(path)
            shader.modified = mtime
        except RuntimeError, text:
            log.error("Error loading shader %s", path, exc_info=True)
            shader = False

    cache[path] = shader
    return shader
    
def reloadShaders():
    log.message('Reloading shaders')
    for path in _shaderCache:
        try:
            _shaderCache[path].initShader()
        except RuntimeError, text:
            log.error("Error loading shader %s", path, exc_info=True)
            _shaderCache[path] = False
