#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
:Authors:
    Marc Flerackers

:Version: 1.0
:Copyright: MakeHuman Team 2001-2011
:License: GPL3 

This module contains classes and methods to work with bitmap fonts and text.
"""

import module3d

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
            print('Character with ordinal %04x is missing.' % ord(char))
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
            print('Character with ordinal %04x is missing.' % ord(char))
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
            print('Character with ordinal %04x is missing.' % ord(char))
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
def createMesh(font, text, object = None, wrapWidth=0, alignment=AlignLeft, rtl=False):

    if wrapWidth:
        text = wrapText(font, text, wrapWidth)
        
    object = object or module3d.Object3D(text)
    object.uvValues = object.uvValues or []
    
    # create group
    fg = object.createFaceGroup('text')

    index = 0
    xoffset = 0
    yoffset = 0
    zoffset = 0
    previous = -1

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
            xoffset = int(wrapWidth - font.stringWidth(line)) / 2
        elif alignment == AlignRight:
            xoffset = (wrapWidth - font.stringWidth(line))
        
        zoffset = 0
        
        for char in line:

            co = font.getAbsoluteCoordsForChar(char)
            uv = font.getTextureCoordinatesForChar(char)
            kerning = font.kerning.get((previous, char), 0)
            previous = ord(char)
            
            xoffset += kerning

            # create vertices

            v1 = object.createVertex([xoffset + co[0], yoffset + co[1], zoffset])
            v2 = object.createVertex([xoffset + co[2], yoffset + co[1], zoffset])
            v3 = object.createVertex([xoffset + co[2], yoffset + co[3], zoffset])
            v4 = object.createVertex([xoffset + co[0], yoffset + co[3], zoffset])

            xoffset += co[4]
            zoffset += 0.0001

            uv1 = [uv[0], uv[1]]
            uv2 = [uv[2], uv[1]]
            uv3 = [uv[2], uv[3]]
            uv4 = [uv[0], uv[3]]

            # create faces
            fg.createFace((v1, v4, v3, v2), (uv1, uv4, uv3, uv2))
            
        yoffset += font.lineHeight

    object.texture = font.file
    object.updateIndexBuffer()

    return object

