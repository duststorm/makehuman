#!/usr/bin/python
# -*- coding: utf-8 -*-

import module3d


class Font:

    def __init__(self, filename):
        f = open(filename, 'r')

        self.charMap = {}
        self.kerning = {}

        for data in f.readlines():
            lineData = data.split()

            if lineData[0] == 'common':
                for paramValue in lineData[1:]:
                    paramData = paramValue.split('=')

                    if paramData[0] == 'lineHeight':
                        self.lineHeight = int(paramData[1])
                    elif paramData[0] == 'scaleW':
                        self.width = int(paramData[1])
                    elif paramData[0] == 'scaleH':
                        self.height = int(paramData[1])
            elif lineData[0] == 'page':

                for paramValue in lineData[1:]:
                    paramData = paramValue.split('=')

                    if paramData[0] == 'file':
                        self.file = 'data/fonts/' + (paramData[1])[1:-1]  # Removes the ""
            elif lineData[0] == 'char':

                charRecord = {}
                for paramValue in lineData[1:]:
                    paramData = paramValue.split('=')

                    if paramData[0] == 'id':
                        charRecord['id'] = int(paramData[1])
                    elif paramData[0] == 'x':
                        charRecord['x'] = int(paramData[1])
                    elif paramData[0] == 'y':
                        charRecord['y'] = int(paramData[1])
                    elif paramData[0] == 'width':
                        charRecord['width'] = int(paramData[1])
                    elif paramData[0] == 'height':
                        charRecord['height'] = int(paramData[1])
                    elif paramData[0] == 'xoffset':
                        charRecord['xoffset'] = int(paramData[1])
                    elif paramData[0] == 'yoffset':
                        charRecord['yoffset'] = int(paramData[1])
                    elif paramData[0] == 'xadvance':
                        charRecord['xadvance'] = int(paramData[1])

        # print(charRecord)

                self.charMap[charRecord['id']] = charRecord
                
            elif lineData[0] == 'kerning':
                
                for paramValue in lineData[1:]:
                    paramData = paramValue.split('=')

                    if paramData[0] == 'first':
                        first = int(paramData[1])
                    elif paramData[0] == 'second':
                        second = int(paramData[1])
                    elif paramData[0] == 'amount':
                        amount = int(paramData[1])
                        
                self.kerning[(first, second)] = amount

        # print(self.charMap)

    def getAbsoluteCoordsForChar(self, char):
        charRecord = self.charMap[ord(char)]
        x1 = float(charRecord['xoffset'])
        y1 = float(charRecord['yoffset'])
        x2 = float(charRecord['xoffset'] + charRecord['width'])
        y2 = float(charRecord['yoffset'] + charRecord['height'])
        advance = float(charRecord['xadvance'])
        return [x1, y1, x2, y2, advance]

    def getRelativeSizesForChar(self, char):
        charRecord = self.charMap[ord(char)]
        x1 = float(charRecord['xoffset']) / float(self.width)
        y1 = float(charRecord['yoffset']) / float(self.height)
        x2 = float(charRecord['xoffset'] + charRecord['width']) / float(self.width)
        y2 = float(charRecord['yoffset'] + charRecord['height']) / float(self.height)
        advance = float(charRecord['xadvance']) / float(self.width)
        return [x1, y1, x2, y2, advance]

    def getTextureCoordinatesForChar(self, char):
        charRecord = self.charMap[ord(char)]
        u1 = float(charRecord['x']) / float(self.width)
        v1 = 1.0 - float(charRecord['y']) / float(self.height)
        u2 = float(charRecord['x'] + charRecord['width']) / float(self.width)
        v2 = 1.0 - float(charRecord['y'] + charRecord['height']) / float(self.height)
        return [u1, v1, u2, v2]

    # Returns the width of the string
    def stringWidth(self, text):
        width = 0.0
        previous = -1

        for char in text:
            co = self.getAbsoluteCoordsForChar(char)
            kerning = self.kerning.get((previous, char), 0.0)
            previous = ord(char)
            width += co[4] + kerning
            
        return width

#returns font as object3d with 1 visibility
def createMesh(font, text, object = None):

    object = object or module3d.Object3D(text)
    object.uvValues = object.uvValues or []
    object.indexBuffer = object.indexBuffer or []
    
    # create group
    fg = object.createFaceGroup('text')

    index = 0
    xoffset = 0.0
    yoffset = 0.0
    zoffset = 0.0
    previous = -1

    for char in text:
        if char == '\n':
            xoffset = 0.0
            yoffset += font.lineHeight
        else:
            co = font.getAbsoluteCoordsForChar(char)
            uv = font.getTextureCoordinatesForChar(char)
            kerning = font.kerning.get((previous, char), 0.0)
            previous = ord(char)
            
            xoffset += kerning

            # create vertices

            v1 = object.createVertex([xoffset + co[0], yoffset + co[1], zoffset])
            v2 = object.createVertex([xoffset + co[2], yoffset + co[1], zoffset])
            v3 = object.createVertex([xoffset + co[2], yoffset + co[3], zoffset])
            v4 = object.createVertex([xoffset + co[0], yoffset + co[3], zoffset])

            xoffset += co[4]
            zoffset += 0.001

            uv1 = [uv[0], uv[1]]
            uv2 = [uv[2], uv[1]]
            uv3 = [uv[2], uv[3]]
            uv4 = [uv[0], uv[3]]

            # create faces
            fg.createFace(v1, v4, v3, v2, uv=(uv1, uv4, uv3, uv2))

    object.texture = font.file
    object.updateIndexBuffer()

    return object
    #scene.update()


# font = Font("../data/fonts/arial.fnt")
# print(font.getAbsoluteCoordsForChar('a'))
# print(font.getRelativeSizesForChar('a'))
# print(font.getTextureCoordinatesForChar('a'))
