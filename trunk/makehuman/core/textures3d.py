#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Functions for processing bitmaps. 

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

This module contains a series of functions to perform standard processes on bitmaps. 
These functions provide simple higher level functionality for use by other functions, 
such as the 3D algorithms.

"""

__docformat__ = 'restructuredtext'

import log

def byteToBit(val, numdigits=8, base=2):
    """
    This function returns a list of binary digits representing the number specified.
    
    Parameters
    ----------

    val:
        *integer*. The value to be converted to binary.
    numdigits:
        *integer*. The number of digits to process.  
    base:
        *integer*. The factor to repeatedly divide by.
    
    """

    digits = [0 for i in xrange(numdigits)]
    for i in xrange(numdigits):
        (val, digits[i]) = divmod(val, base)
    return digits


def readTGA(filename):
    """
    This function reads a TGA file and constructs a list of lists 
    with RGB values plus an alpha channel.
    By way of an example, the following output could be the result 
    of processing a 9x9 pixels 32 bit TGA (ie 4 bytes per color):

    [0, 0, 0, 255, 255, 255, 255, 255, 0, 255, 0, 255,
    255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 255, 255,
    0, 0, 255, 255, 255, 255, 255, 255, 0, 0, 0, 255]

    Where, because 32 bit = 4 byte for each color, we get:
      - 0, 0, 0, 255 = B G R A first pixel
      - 255, 255, 255, 255 = B G R A second pixel
      - 0, 255, 0, 255 B G R A third pixel
      - etc.
    
    Parameters
    ----------

    filename:
        *string*. The full file system path to the TGA file to be processed.
    """

    origin = ''
    lengthOfID = 0
    byteList = []

    try:
        f = open(filename, 'rb')
    except IOError, (errno, strerror):
        log.error('I/O error(%s): %s', errno, strerror)
        return None
    fileReaded = f.read()
    for i in xrange(len(fileReaded)):
        byteList.append(ord(fileReaded[i]))
    f.close()

    # byteList[0] is the Identification Field.

    lengthOfID = byteList[0]
    log.message('Identification Field lentgh = %i', lengthOfID)

    # byteList[1] is the Color Map Type.

    if byteList[1] != 0:
        log.warning('this module work only with true color image, no mapped type')
        return None

    # byteList[2] is the image type field.

    if byteList[2] != 2:
        log.message('Image type = %s', byteList[2])
        log.warning('This module work only with uncompressed true color image')
        return None

    # byteList[12] and istByte[13] are 2 byte of image X resolution.
    # TGA files are stored using the Intel byte ordering convention
    # (least significant byte first, most significant
    # byte last). For this reason, applications running on
    # Motorola-based systems will need to invert the ordering
    # of bytes for short and long values after a file has been read.

    TGAXres = byteList[12] + byteList[13] * 256
    log.message('X resolution: %i', TGAXres)

    # byteList[14] and istByte[15] are 2 byte of image Y resolution.

    TGAYres = byteList[14] + byteList[15] * 256
    log.message('Y resolution: %i', TGAYres)

    # byteList[16] is the pixel depth: 8,16,24,32, etc.

    pixelDepth = byteList[16]
    if pixelDepth == 24:
        byteUsedForPixel = 3
    elif pixelDepth == 32:
        byteUsedForPixel = 4
    else:
        log.warning('This module work only with uncompressed true color image')
        return None

    log.message('Pixel Depth: %i', pixelDepth)

    # byteList[17] is Image Descriptor

    imageDescriptor = byteList[17]

    # In this case we need to examine the single bits

    imageDescrBit = byteToBit(imageDescriptor)

    # We need just bit 4 and 5 for TGA coordinate system origin

    a = imageDescrBit[5]
    b = imageDescrBit[4]
    if a == 0 and b == 0:
        log.message('The image origin is Bottom Left')
        origin = 'BL'
    if a == 0 and b == 1:
        log.message('The image origin is Bottom Right')
        origin = 'BR'
    if a == 1 and b == 0:
        log.message('The image origin is Top Left')
        origin = 'TL'
    if a == 1 and b == 1:
        log.message('The image origin is Top Right')
        origin = 'TR'

    # Calculation of TGA header length

    standardLength = 18
    headerLength = standardLength + lengthOfID
    numOfPixel = TGAXres * TGAYres
    numeOfBytesUsedForPixels = numOfPixel * byteUsedForPixel
    byteList = byteList[headerLength:headerLength + numeOfBytesUsedForPixels]
    return [byteList, TGAXres, TGAYres, numOfPixel, byteUsedForPixel]


def uvCooToBitmapIndex(TGAXres, TGAYres, U, V):
    """ 
    
    This function takes UV coordinates and a bitmap resolution as input and 
    returns an index to the position of a pixel in the bitmap.
     
    UV coordinates are used to map 2D images to 3D surfaces. 
    In the case of the MakeHuman mesh, each face has 3 vertices each of which has 
    a pair of uv-coordinates that provide a horizontal and vertical value between 0 and 1 
    to point to the location on an image map from which to read a value.
    
    For an image with a resolution of Xn x Ym, any UV coordinate will lie within 
    a square whose bottom left corner has a pixel coordinate between <0,0> and 
    <Xn-1,Ym-1>. 
    This in turn can be transformed into a pixel index in the bitmap image by multiplying 
    the Y value by Xn and adding the X value. In the example on the right the UV coordinates
    <0.38,0.32> lie in the pixel whose bottom left coordinates are <3,2>, giving a pixel index 
    of 2x8+3 = 19. 
    (This will be the 20th pixel in the bitmap because the first is numbered '0'). 
    
    Parameters
    ----------

    TGAXres:
        *integer*. The X component of the resolution of the bitmap.
    TGAYres:
        *integer*. The Y component of the resolution of the bitmap.
    U:
        *float*. The horizontal component of the UV coordinates. A value between 0 and 1.
    V:
        *float*. The vertical component of the UV coordinate. A value between 0 and 1
    """

    # We use 'resolution - 1' in both dimensions as multiplication
    # factors to work out which pixel the UV coordinate sits in.
    # The calculated coordinates are integer values counting from '0'.

    UVimageCoordX = int(abs((TGAXres - 1) * U))
    UVimageCoordY = int(abs((TGAYres - 1) * V))
    pixelIndex = UVimageCoordX + UVimageCoordY * TGAXres
    return pixelIndex


