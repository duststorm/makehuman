from OpenGL.GL import *
from OpenGL.GL.ARB.texture_non_power_of_two import *
from core import G
import image_base as img
from image import Image

class Texture(object):
    def __new__(cls, *args, **kwargs):
        self = super(Texture, cls).__new__(cls)

        self.textureId = glGenTextures(1)
        self.width = 0
        self.height = 0

        return self

    def __init__(self, image = None):
        if image is not None:
            self.loadTexture(image, self.textureId, self)

    def __del__(self):
        try:
            glDeleteTextures(self.textureId)
        except StandardError:
            pass

    def loadImage(self, image):
        self.loadTexture(image, self.textureId, self)

    def loadSubImage(self, image, x, y):
        self.loadSubTexture(image, self.textureId, x, y)

    @staticmethod
    def loadTexture(image, texture, texobj):
        mipmaps = not glInitTextureNonPowerOfTwoARB()

        if isinstance(image, (str, unicode)):
            image = Image(image)

        surface = image.surface
        if surface is None:
            return

        if surface.mode == "L":
            internalFormat = GL_ALPHA8
            format = GL_ALPHA
        elif surface.mode == "RGB":
            internalFormat = 3
            format = GL_RGB
        elif surface.mode == "RGBA":
            internalFormat = 4
            format = GL_RGBA
        else:
            raise RuntimeError("Could not load image, unsupported pixel format")

        surface = surface.flip_vertical()
        pixels = surface.data()

        if surface.size[1] == 1:
            glBindTexture(GL_TEXTURE_1D, texture)
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            if mipmaps:
                glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            else:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            if mipmaps:
                gluBuild1DMipmaps(GL_TEXTURE_1D, internalFormat, surface.size[0], format, GL_UNSIGNED_BYTE, pixels)
            else:
                glTexImage1D(GL_TEXTURE_1D, 0, internalFormat, surface.size[0], 0, format, GL_UNSIGNED_BYTE, pixels)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        else:
            glBindTexture(GL_TEXTURE_2D, texture)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            if mipmaps:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            else:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            if mipmaps:
                gluBuild2DMipmaps(GL_TEXTURE_2D, internalFormat, surface.size[0], surface.size[1], format, GL_UNSIGNED_BYTE, pixels)
            else:
                glTexImage2D(GL_TEXTURE_2D, 0, internalFormat, surface.size[0], surface.size[1], 0, format, GL_UNSIGNED_BYTE, pixels)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

        texobj.width, texobj.height = surface.size

    @staticmethod
    def loadSubTexture(image, texture, x, y):
        if not texture:
            raise RuntimeError("Texture is empty, cannot load a sub texture into it")

        if isinstance(image, (str, unicode)):
            image = Image(image)

        surface = image.surface
        if surface is None:
            return

        if surface.mode == "L":
            internalFormat = GL_ALPHA8
            format = GL_ALPHA
        elif surface.mode == "RGB":
            internalFormat = 3
            format = GL_RGB
        elif surface.mode == "RGBA":
            internalFormat = 4
            format = GL_RGBA
        else:
            raise RuntimeError("Could not load image, unsupported pixel format")

        surface = surface.flip_vertical()
        pixels = surface.data()

        if surface.size[1] == 1:
            glBindTexture(GL_TEXTURE_1D, texture)
            glTexSubImage1D(GL_TEXTURE_1D, 0, x, surface.size[0], format, GL_UNSIGNED_BYTE, pixels)
        else:
            glBindTexture(GL_TEXTURE_2D, texture)
            glTexSubImage2D(GL_TEXTURE_2D, 0, x, y, surface.size[0], surface.size[1], format, GL_UNSIGNED_BYTE, pixels)
