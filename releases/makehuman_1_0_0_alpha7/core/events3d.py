#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
:Authors:
    Marc Flerackers

:Version: 1.0
:Copyright: MakeHuman Team 2001-2011
:License: GPL3 

This module contains classes to allow an object to handle events.
"""

class Event:
    """
    Base class for all events, does not contain information.
    """
    def __init__(self):
        pass

    def __repr__(self):
        return 'event:'


class MouseEvent(Event):
    """
    Contains information about a mouse event.
    
    :param button: the button that is pressed in case of a mousedown or mouseup event, or button flags in case of a mousemove event.
    :type button: int
    :param x: the x position of the mouse in window coordinates.
    :type x: int
    :param y: the y position of the mouse in window coordinates.
    :type y: int
    :param dx: the difference in x position in case of a mousemove event.
    :type dx: int
    :param dy: the difference in y position in case of a mousemove event.
    :type dy: int
    """
    def __init__(self, button, x, y, dx=0, dy=0):
        self.button = button
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def __repr__(self):
        return 'MouseEvent(%d, %d, %d, %d, %d)' % (self.button, self.x, self.y, self.dx, self.dy)


class MouseWheelEvent(Event):
    """
    Contains information about a mouse wheel event.
    
    :param wheelDelta: the amount and direction that the wheel was scrolled.
    :type wheelDelta: int
    """
    def __init__(self, wheelDelta):
        self.wheelDelta = wheelDelta

    def __repr__(self):
        return 'MouseWheelEvent(%d)' % self.wheelDelta


class KeyEvent(Event):
    """
    Contains information about a keyboard event.
    
    :param key: the key code of the key that was pressed or released.
    :type key: int
    :param character: the unicode character if the key represents a character.
    :type character: unicode
    :param modifiers: the modifier keys that were down at the time of pressing the key.
    :type modifiers: int
    """
    def __init__(self, key, character, modifiers):
        self.key = key
        self.character = character
        self.modifiers = modifiers

    def __repr__(self):
        return 'KeyEvent(%d, %04x %s, %d)' % (self.key, ord(self.character), self.character, self.modifiers)


class FocusEvent(Event):
    """
    Contains information about a view focus/blur event
    
    :param blurred: the view that lost the focus.
    :type blurred: guid3d.View
    :param focused: the view that gained the focus.
    :type focused: guid3d.View
    """
    def __init__(self, blurred, focused):
        self.blurred = blurred
        self.focused = focused

    def __repr__(self):
        return 'FocusEvent(%s, %s)' % (self.blurred, self.focused)


class ResizeEvent(Event):
    """
    Contains information about a resize event
    
    :param width: the new width of the window in pixels.
    :type width: int
    :param height: the new height of the window in pixels.
    :type height: int
    :param fullscreen: the new fullscreen state of the window.
    :type fullscreen: Boolean
    :param dx: the change in width of the window in pixels.
    :type dx: int
    :param dy: the change in height of the window in pixels.
    :type dy: int
    """
    def __init__(self, width, height, fullscreen, dx, dy):
        self.width = width
        self.height = height
        self.fullscreen = fullscreen
        self.dx = dx
        self.dy = dy

    def __repr__(self):
        return 'ResizeEvent(%d, %d, %s, %d, %d)' % (self.width, self.height, self.fullscreen, self.dx, self.dy)
        

class EventHandler(object):
    """
    Base event handler class. Derive from this class if an object needs to be able to have events attached to it.
    Currently only one event per event name can be attached. This is because we either allow a class method or
    a custom method to be attached as event handling method. Since the custom method replaces the class method,
    it is needed in some case to call the base class's method from the event handling method.
    
    There are 2 ways to attach handlers:
    
    1. Override the method. This is the most appropriate way when you want to add distinctive behaviour to many EventHandlers.
    
    ::
        
        class Widget(View):
        
            def onMouseDown(self, event):
                #Handle event
                
    2. Use the event decorator. This is the most appropriate way when you want to attach distinctive behaviour to one EventHandler.
    
    ::
        
        widget = Widget()
        
        @widget.event:
        def onMouseDown(event):
            #Handle event
            
    Note that self is not passed to the handler in this case, which should not be a problem as you can just use the variable since you are creating a closure. 
    """
    def __init__(self):
        pass

    def callEvent(self, eventType, event):

        #print("Sending %s to %s" % (eventType, self))

        if hasattr(self, eventType):
            getattr(self, eventType)(event)

    def attachEvent(self, eventName, eventMethod):
        setattr(self, eventName, eventMethod)

    def detachEvent(self, eventName):
        delattr(self, eventName)

    def event(self, eventMethod):
        self.attachEvent(eventMethod.__name__, eventMethod)

SDL_BUTTON_LEFT = 1
SDL_BUTTON_MIDDLE = 2
SDL_BUTTON_RIGHT = 3

SDL_BUTTON_LEFT_MASK = 1
SDL_BUTTON_MIDDLE_MASK = 2
SDL_BUTTON_RIGHT_MASK = 4

SDLK_BACKSPACE = 8
SDLK_TAB = 9
SDLK_CLEAR = 12
SDLK_RETURN = 13
SDLK_PAUSE = 19
SDLK_ESCAPE = 27
SDLK_SPACE = 32
SDLK_EXCLAIM = 33
SDLK_QUOTEDBL = 34
SDLK_HASH = 35
SDLK_DOLLAR = 36
SDLK_AMPERSAND = 38
SDLK_QUOTE = 39
SDLK_LEFTPAREN = 40
SDLK_RIGHTPAREN = 41
SDLK_ASTERISK = 42
SDLK_PLUS = 43
SDLK_COMMA = 44
SDLK_MINUS = 45
SDLK_PERIOD = 46
SDLK_SLASH = 47
SDLK_0 = 48
SDLK_1 = 49
SDLK_2 = 50
SDLK_3 = 51
SDLK_4 = 52
SDLK_5 = 53
SDLK_6 = 54
SDLK_7 = 55
SDLK_8 = 56
SDLK_9 = 57
SDLK_COLON = 58
SDLK_SEMICOLON = 59
SDLK_LESS = 60
SDLK_EQUALS = 61
SDLK_GREATER = 62
SDLK_QUESTION = 63
SDLK_AT = 0x0040

SDLK_LEFTBRACKET = 91
SDLK_BACKSLASH = 92
SDLK_RIGHTBRACKET = 93
SDLK_CARET = 94
SDLK_UNDERSCORE = 95
SDLK_BACKQUOTE = 96
SDLK_a = 97
SDLK_b = 98
SDLK_c = 99
SDLK_d = 100
SDLK_e = 101
SDLK_f = 102
SDLK_g = 103
SDLK_h = 104
SDLK_i = 105
SDLK_j = 106
SDLK_k = 107
SDLK_l = 108
SDLK_m = 109
SDLK_n = 110
SDLK_o = 111
SDLK_p = 112
SDLK_q = 113
SDLK_r = 114
SDLK_s = 115
SDLK_t = 116
SDLK_u = 117
SDLK_v = 118
SDLK_w = 119
SDLK_x = 120
SDLK_y = 121
SDLK_z = 122
SDLK_DELETE = 127

SDLK_KP0 = 0x0100
SDLK_KP1 = 257
SDLK_KP2 = 258
SDLK_KP3 = 259
SDLK_KP4 = 260
SDLK_KP5 = 261
SDLK_KP6 = 262
SDLK_KP7 = 263
SDLK_KP8 = 264
SDLK_KP9 = 265
SDLK_KP_PERIOD = 266
SDLK_KP_DIVIDE = 267
SDLK_KP_MULTIPLY = 268
SDLK_KP_MINUS = 269
SDLK_KP_PLUS = 270
SDLK_KP_ENTER = 271
SDLK_KP_EQUALS = 272

SDLK_UP = 273
SDLK_DOWN = 274
SDLK_RIGHT = 275
SDLK_LEFT = 276
SDLK_INSERT = 277
SDLK_HOME = 278
SDLK_END = 279
SDLK_PAGEUP = 280
SDLK_PAGEDOWN = 281

SDLK_F1 = 282
SDLK_F2 = 283
SDLK_F3 = 284
SDLK_F4 = 285
SDLK_F5 = 286
SDLK_F6 = 287
SDLK_F7 = 288
SDLK_F8 = 289
SDLK_F9 = 290
SDLK_F10 = 291
SDLK_F11 = 292
SDLK_F12 = 293
SDLK_F13 = 294
SDLK_F14 = 295
SDLK_F15 = 296

SDLK_NUMLOCK = 300
SDLK_CAPSLOCK = 301
SDLK_SCROLLOCK = 302
SDLK_RSHIFT = 303
SDLK_LSHIFT = 304
SDLK_RCTRL = 305
SDLK_LCTRL = 306
SDLK_RALT = 307
SDLK_LALT = 308
SDLK_RMETA = 309
SDLK_LMETA = 310
SDLK_LSUPER = 311
SDLK_RSUPER = 312
SDLK_MODE = 313
SDLK_COMPOSE = 314

SDLK_HELP = 315
SDLK_PRINT = 316
SDLK_SYSREQ = 317
SDLK_BREAK = 318
SDLK_MENU = 319
SDLK_POWER = 320
SDLK_EURO = 321
SDLK_UNDO = 322

KMOD_LSHIFT = 0x0001
KMOD_RSHIFT = 0x0002
KMOD_LCTRL = 0x0040
KMOD_RCTRL = 0x0080
KMOD_LALT = 0x0100
KMOD_RALT = 0x0200
KMOD_LMETA = 0x0400
KMOD_RMETA = 0x0800
KMOD_NUM = 0x1000
KMOD_CAPS = 0x2000
KMOD_MODE = 0x4000
KMOD_RESERVED = 0x8000

KMOD_CTRL = KMOD_LCTRL | KMOD_RCTRL
KMOD_SHIFT = KMOD_LSHIFT | KMOD_RSHIFT
KMOD_ALT = KMOD_LALT | KMOD_RALT
KMOD_META = KMOD_LMETA | KMOD_RMETA
