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

This module contains classes and methods to work with bitmap fonts and text.
"""

import module3d
import log

class Font:
    """
    A font object used to display text on the screen.
    """
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
        try:
            charRecord = self.charMap[ord(char)]
        except:
            log.notice('Character with ordinal %04x is missing.', ord(char))
            charRecord = self.charMap[ord('?')]
        x1 = charRecord['xoffset']
        y1 = charRecord['yoffset']
        x2 = charRecord['xoffset'] + charRecord['width']
        y2 = charRecord['yoffset'] + charRecord['height']
        advance = charRecord['xadvance']
        return (x1, y1, x2, y2, advance)

    def getRelativeSizesForChar(self, char):
        try:
            charRecord = self.charMap[ord(char)]
        except:
            log.notice('Character with ordinal %04x is missing.', ord(char))
            charRecord = self.charMap[ord('?')]
        x1 = float(charRecord['xoffset']) / float(self.width)
        y1 = float(charRecord['yoffset']) / float(self.height)
        x2 = float(charRecord['xoffset'] + charRecord['width']) / float(self.width)
        y2 = float(charRecord['yoffset'] + charRecord['height']) / float(self.height)
        advance = float(charRecord['xadvance']) / float(self.width)
        return (x1, y1, x2, y2, advance)

    def getTextureCoordinatesForChar(self, char):
        try:
            charRecord = self.charMap[ord(char)]
        except:
            log.notice('Character with ordinal %04x is missing.', ord(char))
            charRecord = self.charMap[ord('?')]
        u1 = float(charRecord['x']) / float(self.width)
        v1 = 1.0 - float(charRecord['y']) / float(self.height)
        u2 = float(charRecord['x'] + charRecord['width']) / float(self.width)
        v2 = 1.0 - float(charRecord['y'] + charRecord['height']) / float(self.height)
        return (u1, v1, u2, v2)

    # Returns the width of the string
    def stringWidth(self, text):
        """
        Measures the width of the text if displayed using this font.
        
        :param text: The text to measure.
        :type text: str
        :return: The width of the text if displayed using this font.
        :rtype: int
        """
        width = 0
        previous = -1

        for char in text:
            co = self.getAbsoluteCoordsForChar(char)
            kerning = self.kerning.get((previous, char), 0)
            previous = ord(char)
            width += co[4] + kerning
            
        return width
        
def wrapText(font, text, width):
    """
    Wraps text according to the given width by inserting extra enters. The wrapped text is returned.
    
    :param font: The font which is going to be used to display the text.
    :type font: font3d.Font
    :param text: The text to wrap.
    :type text: str
    :param width: The width.
    :type width: int or float
    :return: The wrapped text.
    :rtype: str
    """
    wrappedText = ''
    line = ''
    space = 0
    
    for char in text:
        # A space, just note the position
        if char == ' ':
            line += char
            space = len(line)
        # A linebreak, add and reset line
        elif char == '\n':
            wrappedText += line + '\n'
            line = ''
            space = 0
        # Line will get too long, break at last space
        elif space and font.stringWidth(line + char) > width:
            wrappedText += line[:space] + '\n'
            line = line[space:] + char
        # Just add the caharacter to the line
        else:
            line += char
            
    wrappedText += line
            
    return wrappedText
    
AlignLeft = 0
AlignCenter = 1
AlignRight = 2

def isRtl(ch):
    index = ord(ch)
    return True if index >= 0x600 and index <= 0x77F else False
            
#returns font as object3d with 1 visibility
def createMesh(font, text, object = None, width=0, alignment=AlignLeft, wrap=False, rtl=False):

    if wrap:
        text = wrapText(font, text, width)
        
    if rtl and alignment==AlignLeft:
        alignment = AlignRight
        
    object = object or module3d.Object3D(text)
    
    # create group
    fg = object.createFaceGroup('text')

    index = 0
    xoffset = 0
    yoffset = 0
    zoffset = 0
    previous = -1

    v = []
    uvs = []
    f = []
    base = 0

    for line in text.splitlines():
    
        if rtl and line:
            rtlLine = u''
            section = u''
            ltr = isRtl(line[0])
            for char in line:
                if ltr:
                    if isRtl(char):
                        rtlLine += section
                        section = char
                        ltr = False
                    else:
                        section += char
                else:
                    if isRtl(char):
                        section += char
                    else:
                        for ch in reversed(section):
                            rtlLine += ch
                        section = char
                        ltr = True
            if ltr:
                rtlLine += section
            else:
                for ch in reversed(section):
                    rtlLine += ch
            line = rtlLine
        
        if alignment == AlignLeft:
            xoffset = 0
        elif alignment == AlignCenter:
            xoffset = int(width - font.stringWidth(line)) / 2
        elif alignment == AlignRight:
            xoffset = (width - font.stringWidth(line))
        
        zoffset = 0

        for char in line:

            co = font.getAbsoluteCoordsForChar(char)
            uv = font.getTextureCoordinatesForChar(char)
            kerning = font.kerning.get((previous, char), 0)
            previous = ord(char)
            
            xoffset += kerning

            # create vertices

            v.extend([(xoffset + co[i], yoffset + co[j], zoffset) for j in [1,3] for i in [0,2]])

            xoffset += co[4]
            zoffset += 0.0001

            uvs.extend([(uv[i], uv[j]) for j in [1,3] for i in [0,2]])

            # create faces
            f.append(tuple(base + i for i in [0,2,3,1]))

            base += 4
            
        yoffset += font.lineHeight

    object.setCoords(v)
    object.setUVs(uvs)
    object.setFaces(f, f, fg.idx)

    object.texture = font.file
    object.updateIndexBuffer()

    return object
