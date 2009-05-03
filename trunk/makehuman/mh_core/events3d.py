class Event:
  def __init__(self, x = None, y = None, dx = None, dy = None, b = None, key = None, character = None, wheelDelta = None):
    self.x = x
    self.y = y
    self.dx = dx
    self.dy = dy
    self.b = b
    self.key = key
    self.character = character
    self.wheelDelta = wheelDelta
    
  def __repr__(self):
    return "event: %s, %s, %s, %s, %s, " %(self.x, self.y, self.b, self.key, self.character)
    
class EventHandler:
  def __init__(self):
    pass
    
  def callEvent(self, eventType, event):
    if hasattr(self, eventType):
      getattr(self, eventType)(event)
      
  def attachEvent(self, eventName, eventMethod):
    setattr(self, eventName, eventMethod)
    
  def detachEvent(self, eventName):
    delattr(self, eventName)
      
  def event(self, eventMethod):
    self.attachEvent(eventMethod.__name__, eventMethod)
    
SDLK_BACKSPACE		= 8
SDLK_TAB		      = 9
SDLK_CLEAR		    = 12
SDLK_RETURN		    = 13
SDLK_PAUSE		    = 19
SDLK_ESCAPE		    = 27
SDLK_SPACE		    = 32
SDLK_EXCLAIM		  = 33
SDLK_QUOTEDBL		  = 34
SDLK_HASH		      = 35
SDLK_DOLLAR		    = 36
SDLK_AMPERSAND		= 38
SDLK_QUOTE		    = 39
SDLK_LEFTPAREN		= 40
SDLK_RIGHTPAREN		= 41
SDLK_ASTERISK		  = 42
SDLK_PLUS		      = 43
SDLK_COMMA		    = 44
SDLK_MINUS		    = 45
SDLK_PERIOD		    = 46
SDLK_SLASH		    = 47
SDLK_0			      = 48
SDLK_1			      = 49
SDLK_2			      = 50
SDLK_3			      = 51
SDLK_4			      = 52
SDLK_5			      = 53
SDLK_6			      = 54
SDLK_7			      = 55
SDLK_8			      = 56
SDLK_9			      = 57
SDLK_COLON		    = 58
SDLK_SEMICOLON		= 59
SDLK_LESS		      = 60
SDLK_EQUALS		    = 61
SDLK_GREATER		  = 62
SDLK_QUESTION		  = 63
SDLK_AT			      = 64

SDLK_LEFTBRACKET	= 91
SDLK_BACKSLASH		= 92
SDLK_RIGHTBRACKET	= 93
SDLK_CARET		    = 94
SDLK_UNDERSCORE		= 95
SDLK_BACKQUOTE		= 96
SDLK_a			      = 97
SDLK_b			      = 98
SDLK_c			      = 99
SDLK_d			      = 100
SDLK_e			      = 101
SDLK_f			      = 102
SDLK_g			      = 103
SDLK_h			      = 104
SDLK_i			      = 105
SDLK_j			      = 106
SDLK_k			      = 107
SDLK_l			      = 108
SDLK_m			      = 109
SDLK_n			      = 110
SDLK_o			      = 111
SDLK_p			      = 112
SDLK_q			      = 113
SDLK_r			      = 114
SDLK_s			      = 115
SDLK_t			      = 116
SDLK_u			      = 117
SDLK_v			      = 118
SDLK_w			      = 119
SDLK_x			      = 120
SDLK_y			      = 121
SDLK_z			      = 122
SDLK_DELETE		    = 127

SDLK_KP0		      = 256
SDLK_KP1		      = 257
SDLK_KP2		      = 258
SDLK_KP3		      = 259
SDLK_KP4		      = 260
SDLK_KP5		      = 261
SDLK_KP6		      = 262
SDLK_KP7		      = 263
SDLK_KP8		      = 264
SDLK_KP9		      = 265
SDLK_KP_PERIOD		= 266
SDLK_KP_DIVIDE		= 267
SDLK_KP_MULTIPLY	= 268
SDLK_KP_MINUS		  = 269
SDLK_KP_PLUS		  = 270
SDLK_KP_ENTER		  = 271
SDLK_KP_EQUALS		= 272

SDLK_UP			      = 273
SDLK_DOWN		      = 274
SDLK_RIGHT		    = 275
SDLK_LEFT		      = 276
SDLK_INSERT		    = 277
SDLK_HOME		      = 278
SDLK_END		      = 279
SDLK_PAGEUP		    = 280
SDLK_PAGEDOWN		  = 281

SDLK_F1			      = 282
SDLK_F2			      = 283
SDLK_F3			      = 284
SDLK_F4			      = 285
SDLK_F5			      = 286
SDLK_F6			      = 287
SDLK_F7			      = 288
SDLK_F8			      = 289
SDLK_F9			      = 290
SDLK_F10		      = 291
SDLK_F11		      = 292
SDLK_F12		      = 293
SDLK_F13		      = 294
SDLK_F14		      = 295
SDLK_F15		      = 296

SDLK_NUMLOCK		  = 300
SDLK_CAPSLOCK		  = 301
SDLK_SCROLLOCK		= 302
SDLK_RSHIFT		    = 303
SDLK_LSHIFT		    = 304
SDLK_RCTRL		    = 305
SDLK_LCTRL		    = 306
SDLK_RALT		      = 307
SDLK_LALT		      = 308
SDLK_RMETA		    = 309
SDLK_LMETA		    = 310
SDLK_LSUPER		    = 311
SDLK_RSUPER		    = 312
SDLK_MODE		      = 313
SDLK_COMPOSE		  = 314

SDLK_HELP		      = 315
SDLK_PRINT		    = 316
SDLK_SYSREQ		    = 317
SDLK_BREAK		    = 318
SDLK_MENU		      = 319
SDLK_POWER		    = 320
SDLK_EURO		      = 321
SDLK_UNDO		      = 322
