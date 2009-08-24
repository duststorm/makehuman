/** \file glmodule.c
 *  \brief This module provides integration with OpenGL and SDL functionality.

 <table>
 <tr><td>Project Name:                                   </td>
     <td><b>MakeHuman</b>                                </td></tr>
 <tr><td>Product Home Page:                              </td>
     <td>http://www.makehuman.org/                       </td></tr>
 <tr><td>SourceForge Home Page:                          </td>
     <td>http://sourceforge.net/projects/makehuman/      </td></tr>
 <tr><td>Authors:                                        </td>
     <td>Manuel Bastioni, Paolo Colombo, Simone Re, Marc Flerackers, Hans-Peter Dusel</td></tr>
 <tr><td>Copyright(c):                                   </td>
     <td>MakeHuman Team 2001-2009                        </td></tr>
 <tr><td>Licensing:                                      </td>
     <td>GPL3 (see also
         http://makehuman.wiki.sourceforge.net/Licensing)</td></tr>
 <tr><td>Coding Standards:                               </td>
     <td>See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards
                                                         </td></tr>
 </table>

 This module implements the OpenGL and SDL functions used to control the
 application window and to process user interaction with the GUI. It provides
 control functions to enable other application components to interact with the
 OpenGL and SDL functionality and invokes event handling functions to
 respond to keyboard and mouse events and idle time captured by the SDL
 (Simple DirectMedia Layer) libraries.

 */

#include "glmodule.h"
#include "core.h"

#ifdef _DEBUG
  #undef _DEBUG
  #include <Python.h>
  #define _DEBUG
#else
  #include <Python.h>
#endif

#ifdef __WIN32__
    #include <windows.h>
    #include <SDL_syswm.h>
#elif __APPLE__
    void buildFont(GLint inBase, int inCount, char inStartCode, const char* inFontName, int inFontSize);
    #include "SDL_image.h"
#else
    #include <X11/Xlib.h>
    #include <X11/Xutil.h>
    #include <GL/glx.h>
#endif
#ifdef __APPLE__
    #include <Python/structmember.h>
#else
    #include <structmember.h>
#endif

static int g_savedx=0; /*saved x mouse position*/
static int g_savedy=0; /*saved y mouse position*/
static int g_desktopWidth = 0;
static int g_desktopHeight = 0;
static int g_windowWidth = 800;
static int g_windowHeight = 600;
static SDL_Surface *g_screen = NULL;

#ifndef __APPLE__
typedef SDL_Surface *(*PFN_IMG_LOAD)(const char *);
static void *g_sdlImageHandle = NULL;
static PFN_IMG_LOAD IMG_Load = NULL;
#endif

#ifndef __APPLE__ /* Mac OS X already supports this! */
static PFNGLCREATESHADERPROC glCreateShader = NULL;
static PFNGLSHADERSOURCEPROC glShaderSource = NULL;
static PFNGLCOMPILESHADERPROC glCompileShader = NULL;
static PFNGLCREATEPROGRAMPROC glCreateProgram = NULL;
static PFNGLATTACHSHADERPROC glAttachShader = NULL;
static PFNGLLINKPROGRAMPROC glLinkProgram = NULL;
static PFNGLUSEPROGRAMPROC glUseProgram = NULL;
static PFNGLGETSHADERIVPROC glGetShaderiv = NULL;
static PFNGLGETSHADERINFOLOGPROC glGetShaderInfoLog = NULL;
static PFNGLGETPROGRAMIVPROC glGetProgramiv = NULL;
static PFNGLGETPROGRAMINFOLOGPROC glGetProgramInfoLog = NULL;
static PFNGLGETACTIVEUNIFORMPROC glGetActiveUniform = NULL;
#ifdef __WIN32__
static PFNGLACTIVETEXTUREPROC glActiveTexture = NULL;
#endif
static PFNGLUNIFORM1FPROC glUniform1f = NULL;
static PFNGLUNIFORM2FPROC glUniform2f = NULL;
static PFNGLUNIFORM3FPROC glUniform3f = NULL;
static PFNGLUNIFORM4FPROC glUniform4f = NULL;
static PFNGLUNIFORM1IPROC glUniform1i = NULL;

static int g_ShadersSupported = 0;
#else
static int g_ShadersSupported = 1;
#endif /* ifndef __APPLE__*/

typedef struct
{
    PyObject_HEAD
    int textureId;
    int width;
    int height;
} Texture;

// Texture attributes directly accessed by Python
static PyMemberDef Texture_members[] = {
    {"textureId", T_UINT, offsetof(Texture, textureId), READONLY, "The id of the OpenGL texture."},
    {"width",     T_UINT, offsetof(Texture, width),     READONLY, "The width of the texture in pixels."},
    {"height",    T_UINT, offsetof(Texture, height),    READONLY, "The height of the texture in pixels."},
    {NULL}  /* Sentinel */
};

static PyObject *Texture_loadImage(Texture *texture, PyObject *path);

// Texture Methods
static PyMethodDef Texture_methods[] = {
  {"loadImage", (PyCFunction)Texture_loadImage, METH_O,
   "Loads the specified image from file"
  },
  {NULL}  /* Sentinel */
};

static void Texture_dealloc(Texture *self);
static PyObject *Texture_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int Texture_init(Texture *self, PyObject *args, PyObject *kwds);

// Texture type definition
PyTypeObject TextureType = {
    PyObject_HEAD_INIT(NULL)
    0,                                        // ob_size
    "mh.Texture",                             // tp_name
    sizeof(Texture),                          // tp_basicsize
    0,                                        // tp_itemsize
    (destructor)Texture_dealloc,              // tp_dealloc
    0,                                        // tp_print
    0,                                        // tp_getattr
    0,                                        // tp_setattr
    0,                                        // tp_compare
    0,                                        // tp_repr
    0,                                        // tp_as_number
    0,                                        // tp_as_sequence
    0,                                        // tp_as_mapping
    0,                                        // tp_hash
    0,                                        // tp_call
    0,                                        // tp_str
    0,                                        // tp_getattro
    0,                                        // tp_setattro
    0,                                        // tp_as_buffer
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, // tp_flags
    "Texture object",                         // tp_doc
    0,		                                    // tp_traverse
    0,		                                    // tp_clear
    0,		                                    // tp_richcompare
    0,		                                    // tp_weaklistoffset
    0,		                                    // tp_iter
    0,		                                    // tp_iternext
    Texture_methods,                          // tp_methods
    Texture_members,                          // tp_members
    0,                                        // tp_getset
    0,                                        // tp_base
    0,                                        // tp_dict
    0,                                        // tp_descr_get
    0,                                        // tp_descr_set
    0,                                        // tp_dictoffset
    (initproc)Texture_init,                   // tp_init
    0,                                        // tp_alloc
    Texture_new,                              // tp_new
};

/** \brief Registers the Object3D object in the Python environment.
 *  \param module The module to register the Object3D object in.
 *
 *  This function registers the Object3D object in the Python environment.
 */
void RegisterTexture(PyObject *module)
{
  if (PyType_Ready(&TextureType) < 0)
      return;

  Py_INCREF(&TextureType);
  PyModule_AddObject(module, "Texture", (PyObject*)&TextureType);
}

/** \brief Takes care of the deallocation of the OpenGL texture.
 *  \param self The Texture object which is being deallocated.
 *
 *  This function takes care of the deallocation of the OpenGL texture.
 */
static void Texture_dealloc(Texture *self)
{
  // Free our data
  glDeleteTextures(1, &self->textureId);

  // Free Python data
  self->ob_type->tp_free((PyObject*)self);
}

/** \brief Takes care of the initialization of the Texture object members.
 *  \param self The Texture object which is being initialized.
 *
 *  This function takes care of the initialization of the Texture object members.
 */
static PyObject *Texture_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
  // Alloc Python data
  Texture *self = (Texture*)type->tp_alloc(type, 0);

  // Init our data
  if (self)
  {
    glGenTextures(1, &self->textureId);
    self->width = 0;
    self->height = 0;
  }

  return (PyObject*)self;
}

/** \brief The constructor of the Texture object.
 *  \param self The Texture object which is being constructed.
 *  \param args The arguments.
 *
 *  The constructor of the Texture object.
 */
static int Texture_init(Texture *self, PyObject *args, PyObject *kwds)
{
  char *path = NULL;

  if (!PyArg_ParseTuple(args, "|s", &path))
    return -1;

  if (path && !mhLoadTexture(path, self->textureId, &self->width, &self->height))
    return -1;

  return 0;
}

static PyObject *Texture_loadImage(Texture *texture, PyObject *path)
{
  if (!PyString_Check(path))
  {
      PyErr_SetString(PyExc_TypeError, "String expected");
      return NULL;
  }

  if (!mhLoadTexture(PyString_AsString(path), texture->textureId, &texture->width, &texture->height))
    return NULL;

  return Py_BuildValue(""); 
}

/** \brief Draw text at a specified location on the screen.
 *  \param x a float specifying the horizontal position in the GUI window.
 *  \param y a float specifying the vertical position in the GUI window.
 *  \param message a character string pointer to the text to display.
 *
 *  This function displays a piece of text at the specified position on the screen.
 */
void mhDrawText(float x, float y, const char *message)
{
    /* raster pos sets the current raster position
     * mapped via the modelview and projection matrices
     */

    /*Turn off lighting*/
    glDisable(GL_LIGHTING);

    /*Set text color and position*/
    glColor3f(1.0, 1.0, 1.0);
    glRasterPos3f(x, y, 2);

    /*Draw the text*/
    glListBase(G.fontOffset);
    glCallLists((GLsizei)strlen(message), GL_UNSIGNED_BYTE, message);
    
    /* restore lighting */
    glEnable(GL_LIGHTING);
}

/** \brief Flip an SDL surface from top to bottom.
 *  \param surface a pointer to an SDL_Surface.
 *
 *  This function takes an SDL surface, working line by line it takes the top line and 
 *  swaps it with the bottom line, then the second line and swaps it with the second 
 *  line from the bottom etc. until the surface has been mirrored from top to bottom.
 */
static void mhFlipSurface(const SDL_Surface *surface)
{
    unsigned char *line = malloc(surface->w * surface->format->BytesPerPixel);
    unsigned char *pixels = surface->pixels;
    int lineIndex;

    for (lineIndex = 0; lineIndex < surface->h / 2; lineIndex++)
    {
        memcpy(line, pixels + lineIndex * surface->pitch, surface->w * surface->format->BytesPerPixel);
        memcpy(pixels + lineIndex * surface->pitch,
               pixels + (surface->h - lineIndex - 1) * surface->pitch,
               surface->w * surface->format->BytesPerPixel);
        memcpy(pixels + (surface->h - lineIndex - 1) * surface->pitch, line, surface->w * surface->format->BytesPerPixel);
    }

    free(line);
}

/** \brief Load a texture from a file and bind it into the textures array.
 *  \param fname a character string pointer to a string containing a file system path to a texture file.
 *  \param texture an int specifying the existing texture id to use or 0 to create a new texture.
 *
 *  This function loads a texture from a texture file and binds it into the OpenGL textures array.
 */
GLuint mhLoadTexture(const char *fname, GLuint texture, int *width, int *height)
{
    int mode, components;
    SDL_Surface *surface;

    if (!texture)
        glGenTextures(1, &texture);

#ifndef __APPLE__ // OS X utilizes the SDL_image framework for image loading!
    if (!g_sdlImageHandle)
    {
#ifdef __WIN32__
        g_sdlImageHandle = SDL_LoadObject("SDL_image");
#else
        g_sdlImageHandle = SDL_LoadObject("libSDL_image-1.2.so.0");
#endif

        if (!g_sdlImageHandle)
        {
            PyErr_Format(PyExc_RuntimeError, "Could not load %s, SDL_image not found", fname);
            return 0;
        }

        IMG_Load = (PFN_IMG_LOAD)SDL_LoadFunction(g_sdlImageHandle, "IMG_Load");
    }

    if (!IMG_Load)
    {
        PyErr_Format(PyExc_RuntimeError, "Could not load %s, IMG_Load not found", fname);
        return 0;
    }
#endif // ifndef __APPLE__
    surface = (SDL_Surface*)IMG_Load(fname);

    if (!surface)
    {
        PyErr_Format(PyExc_RuntimeError, "Could not load %s, %s", fname, SDL_GetError());
        return 0;
    }

    switch (surface->format->BytesPerPixel)
    {
    case 3:
        components = 3;
        if (surface->format->Rshift) // If there is a shift on the red value, we need to tell that red and blue are switched
            mode = GL_BGR;
        else
            mode = GL_RGB;
        break;
    case 4:
        components = 4;
        if (surface->format->Rshift) // If there is a shift on the red value, we need to tell that red and blue are switched
            mode = GL_BGRA;
        else
            mode = GL_RGBA;
        break;
    default:
        SDL_FreeSurface(surface);
        PyErr_Format(PyExc_RuntimeError, "Could not load %s, unsupported pixel format", fname);
        return 0;

    }

    // For some reason we need to flip the surface vertically
    mhFlipSurface(surface);

    if (surface->h == 1)
    {
      glBindTexture(GL_TEXTURE_1D, texture);
      glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_CLAMP);
      glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_T, GL_CLAMP);
      glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
      glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
      gluBuild1DMipmaps(GL_TEXTURE_1D, components, surface->w, mode, GL_UNSIGNED_BYTE, surface->pixels);
      glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
    }
    else
    {
      glBindTexture(GL_TEXTURE_2D, texture);
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
      //glTexImage2D(GL_TEXTURE_2D, 0, components, surface->w, surface->h, 0, mode, GL_UNSIGNED_BYTE, surface->pixels);
      gluBuild2DMipmaps(GL_TEXTURE_2D, components, surface->w, surface->h, mode, GL_UNSIGNED_BYTE, surface->pixels);
      glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
    }

    if (width)
      *width = surface->w;
    if (height)
      *height = surface->h;

    SDL_FreeSurface(surface);

    return texture;
}

GLuint mhCreateVertexShader(const char *source)
{
  GLuint v;
  GLint status;

  if (!g_ShadersSupported)
    return 0;

  v = glCreateShader(GL_VERTEX_SHADER);

  glShaderSource(v, 1, &source, NULL);

  glCompileShader(v);
  glGetShaderiv(v, GL_COMPILE_STATUS, &status);
  if (status != GL_TRUE)
  {
    GLsizei logLength;
    
    glGetShaderiv(v, GL_INFO_LOG_LENGTH, &logLength);

    if (logLength > 0)
    {
      char *log;
      GLsizei charsWritten;

      log = (char*)malloc(logLength);
      glGetShaderInfoLog(v, logLength, &charsWritten, log);
      PyErr_Format(PyExc_RuntimeError, "Error compiling vertex shader: %s", log);
      free(log);
    }
    else
      PyErr_SetString(PyExc_RuntimeError, "Error compiling vertex shader");

    return 0;
  }

  return v;
}

GLuint mhCreateFragmentShader(const char *source)
{
  GLuint f;
  GLint status;

  f = glCreateShader(GL_FRAGMENT_SHADER);

  glShaderSource(f, 1, &source, NULL);

  glCompileShader(f);
  glGetShaderiv(f, GL_COMPILE_STATUS, &status);
  if (status != GL_TRUE)
  {
    GLsizei logLength;
    
    glGetShaderiv(f, GL_INFO_LOG_LENGTH, &logLength);

    if (logLength > 0)
    {
      char *log;
      GLsizei charsWritten;

      log = (char*)malloc(logLength);
      glGetShaderInfoLog(f, logLength, &charsWritten, log);
      PyErr_Format(PyExc_RuntimeError, "Error compiling fragment shader: %s", log);
      free(log);
    }
    else
      PyErr_SetString(PyExc_RuntimeError, "Error compiling fragment shader");

    return 0;
  }

  return f;
}

GLuint mhCreateShader(GLuint vertexShader, GLuint fragmentShader)
{
  GLuint p;
  GLint status;

	p = glCreateProgram();
	
	glAttachShader(p, vertexShader);
	glAttachShader(p, fragmentShader);

	glLinkProgram(p);
  glGetProgramiv(p, GL_LINK_STATUS, &status);
  if (status != GL_TRUE)
  {
    GLsizei logLength;
    
    glGetProgramiv(p, GL_INFO_LOG_LENGTH, &logLength);

    if (logLength > 0)
    {
      char *log;
      GLsizei charsWritten;

      log = (char*)malloc(logLength);
      glGetProgramInfoLog(p, logLength, &charsWritten, log);
      PyErr_Format(PyExc_RuntimeError, "Error linking shader: %s", log);
      free(log);
    }
    else
      PyErr_SetString(PyExc_RuntimeError, "Error linking shader");

    return 0;
  }
	
  return p;
}

/** \brief Capture a rectangular area from the screen into an image file.
 *  \param x an int containing the x coordinate of the corner of the area (in pixels)
 *  \param y an int containing the y coordinate of the corner of the area (in pixels)
 *  \param width an int containing the width of the area in pixels
 *  \param height an int containing the height of the area in pixels
 *  \param filename a pointer to a char string containing the full path of the file on disk 
 *
 *  This function takes a rectangular section from the screen and writes an image to 
 *  a bitmap image file on disk containing the pixels currently displayed in that 
 *  section of screen.
 */
int mhGrabScreen(int x, int y, int width, int height, const char *filename)
{
  GLint viewport[4];
  SDL_Surface *surface;
  GLenum format;

  if (width <= 0 || height <= 0)
  {
    PyErr_Format(PyExc_RuntimeError, "width or height is 0");
    return 0;
  }

  surface = SDL_CreateRGBSurface(SDL_SWSURFACE, width, height, 24, 0xFF, 0xFF00, 0xFF0000, 0);
  glGetIntegerv(GL_VIEWPORT, viewport);

  if (SDL_LockSurface(surface))
  {
    SDL_FreeSurface(surface);
    PyErr_Format(PyExc_RuntimeError, "Could not lock surface to grab region to file %s, %s", filename, SDL_GetError());
    return 0;
  }

  // Draw before grabbing, to make sure we grab a rendering and not a picking buffer
  mhDraw();
  glPixelStorei(GL_PACK_ALIGNMENT, 4);

/* SDL interprets each pixel as a 32-bit number, so our masks must depend
   on the endianness (byte order) of the machine (PowerPC is big endian 
   in contrast to i386 which is little endian!) */
#if SDL_BYTEORDER == SDL_BIG_ENDIAN
  format = GL_BGR; /* For big endian Machines as based on PowerPC */
#else
  format = GL_RGB; /* For little endian Machines as based on Intel x86 */
#endif
  glReadPixels(x, viewport[3] - y - height, width, height, format, GL_UNSIGNED_BYTE, surface->pixels);
  mhFlipSurface(surface);

  SDL_UnlockSurface(surface);

  if (SDL_SaveBMP(surface, filename))
  {
    SDL_FreeSurface(surface);
    PyErr_Format(PyExc_RuntimeError, "Could not access file to grab region to file %s, %s", filename, SDL_GetError());
    return 0;
  }

  SDL_FreeSurface(surface);
  return 1;
}

/** \brief Pass a keydown event up to Python.
 *  \param key an int containing the key code of the key pressed.
 *  \param character an unsigned short character containing the Unicode character corresponding to the key pressed.
 *
 *  This function calls a keydown keyboard event handling function that will be bubbled up 
 *  to the keyDown Python function and on to an appropriate handler function if registered 
 *  against the Scene3D object. That function processes the event and control is returned
 *  to the event loop to await the next event.
 *
 */
void mhKeyDown(int key, unsigned short character, int modifiers)
{
    callKeyDown(key, character, modifiers);
}

void mhKeyUp(int key, unsigned short character, int modifiers)
{
    callKeyUp(key, character, modifiers);

    UpdatePickingBuffer();
}

/** \brief Pass a timer callback event up to Python.
 *  \param interval an unsigned int, not used here.
 *  \param param a pointer, not used here.
 *
 *  If the useTimer parameter is set when mhCreateWindow is called during the MakeHuman
 *  initiation sequence then this function is registered as the SDL timer event handler.
 *
 *  This function processes timer events. It creates a new event that it pushes into the 
 *  event queue, it resets the timer and returns. This timer function is called in a 
 *  separate thread, but the newly registered event is handled by the standard thread 
 *  in mhEventLoop, where it calls callTimerFunct, which calls mainScene.timerFunc in 
 *  the Python module. 
 * 
 *  Any Python functions registered to use this event perform their tasks before 
 *  returning control to the event loop.
 *  
 */
unsigned int mhTimerFunc(unsigned int interval, void* param)
{
    SDL_Event event;

    if (G.pendingTimer)
    {
        return G.millisecTimer;
    }

    G.pendingTimer = 1;

    event.type = SDL_USEREVENT;
    event.user.code = 0;
    event.user.data1 = NULL;
    event.user.data2 = NULL;

    SDL_PushEvent(&event);

    /*reset the timer to recall the function again, after G.millisecTimer msec*/
    return G.millisecTimer;
}

/** \brief Pass a mouse button down event up to Python.
 *  \param b an int indicating which button this event relates to.
 *  \param x an int specifying the horizontal mouse pointer position in the GUI window (in pixels).
 *  \param y an int specifying the vertical mouse pointer position in the GUI window (in pixels).
 *
 *  This function processes mouse clicks (mouse button down events).
 *  This function writes the current mouse position and keyboard modifier
 *  states (Shift, Ctl etc.) into globals.
 *  Then it calls one of a set of mouse click event handling functions that
 *  will be bubbled up to the corresponding Python event handler.
 *
 *  The Python Scene3D object holds separate attributes
 *  (sceneLMousePressedCallBack and
 *  sceneRMousePressedCallBack) to point to the
 *  different mouse button event handling functions.
 *
 */
void mhMouseButtonDown(int b, int x, int y)
{
    /* Since the mouse cursor doesn't move when a button is down, we
       save the mouse position and restore it later to avoid jumping.
       We also grab the input so we can move the (invisible) mouse outside the screen.
    */
    g_savedx=x;
    g_savedy=y;
#ifdef __WIN32__
    SDL_WM_GrabInput(SDL_GRAB_ON);
#endif

    // Calculate 3d positions
    mhGetPickedCoords(x,y);

    // Check which object/group was hit
    if (b != 4 && b != 5)
      mhGetPickedColor(x, y);

    // Notify python
    callMouseButtonDown(b, x, y);

    // Update screen
    mhQueueUpdate();

    if (b != 4 && b != 5)
      UpdatePickingBuffer();
}

/** \brief Pass a mouse button up event up to Python.
 *  \param b an int indicating which button this event relates to.
 *  \param x an int specifying the horizontal mouse pointer position in the GUI window (in pixels).
 *  \param y an int specifying the vertical mouse pointer position in the GUI window (in pixels).
 *
 *  This function processes mouse clicks (mouse button up events).
 *  This function writes the current mouse position and keyboard modifier
 *  states (Shift, Ctl etc.) into globals.
 *  Then it calls one of a set of mouse click event handling functions that
 *  will be bubbled up to the corresponding Python event handler.
 *
 *  The Python Scene3D object holds separate attributes
 *  (sceneLMouseReleasedCallBack and
 *  sceneRMouseReleasedCallBack) to point to the
 *  different mouse button event handling functions.
 *
 */
void mhMouseButtonUp(int b, int x, int y)
{
    /* Since the mouse cursor doesn't move when a button is down, we
       save the mouse position and restore it later to avoid jumping.
       We also ungrab the previously grabbed input
    */
#ifdef __WIN32__
    SDL_WM_GrabInput(SDL_GRAB_OFF);
#endif
    //SDL_WarpMouse(g_savedx, g_savedy);

    // Calculate 3d positions
    mhGetPickedCoords(x,y);

    // Check which object/group was hit
    if (b != 4 && b != 5)
    {
        mhGetPickedColor(x, y);
    }

    // Notify python
    callMouseButtonUp(b, x, y);

    // Update screen
    mhQueueUpdate();

    UpdatePickingBuffer();
}

/** \brief Pass a mouse motion event up to Python and adjust current camera view.
 *  \param s an int indicating the mouse.motion.state of the event (1=Mouse moved, 0=Mouse click).
 *  \param x an int specifying the horizontal mouse pointer position in the GUI window (in pixels).
 *  \param y an int specifying the vertical mouse pointer position in the GUI window (in pixels).
 *  \param xrel an int specifying the difference between the previously recorded horizontal mouse 
 *         pointer position in the GUI window and the current position (in pixels).
 *  \param yrel an int specifying the difference between the previously recorded vertical mouse 
 *         pointer position in the GUI window and the current position (in pixels).
 *
 *  This function processes mouse movement events, calling a corresponding Python event handler.
 *
 *  This function writes the difference between the last recorded mouse position and the current
 *  mouse position, along with the current mouse position and keyboard modifier states
 *  (Shift, Ctl etc.) into globals.
 *  Then it calls a mouse click motion handling function that will be bubbled up to
 *  the Python function assigned to the sceneMouseMotionCallback attribute
 *  on the Scene3D object. That function processes the event and control is
 *  returned to the event loop to await the next event.
 */
void mhMouseMotion(int s, int x, int y, int xrel, int yrel)
{
    // Calculate 3d positions
    mhGetPickedCoords(x,y);

    // Check which object/group was hit
    if (!s)
      mhGetPickedColor(x, y);

    // Notify python
    callMouseMotion(s, x, y, xrel, yrel);

    // Update screen
    if (s)
        mhQueueUpdate();
}

/** \brief Retrieve the object coordinates for the specified window coordinates.
 *  \param x an int specifying the horizontal position in the image plane (in pixels).
 *  \param y an int specifying the vertical position in the image plane (in pixels).
 *
 *  This function retrieves the object coordinates corresponding to the
 *  window coordinates passed in as parameters.
 *
 */
void mhGetPickedCoords(int x, int y)
{
    double modelview[16], projection[16];
    GLint viewport[4];
    glGetIntegerv(GL_VIEWPORT, viewport);

    /*Getting mouse 3D coords on the GUI plane, using a fixed z value.
    Assuming we use a 3D cursor in scene, with coords (x,y,9.5).
    Using glPerspective clip planes near = 0.1 and far = 100,
    the z coord = 9.5 is normalized to 0.800801. So we use this fixed
    precalculated value.
    */
    mhGUICameraPosition();/*Applying GUI matrix*/
    glGetDoublev(GL_PROJECTION_MATRIX, projection);
    glGetDoublev(GL_MODELVIEW_MATRIX, modelview);
    gluUnProject(x, viewport[3]-y, 0.800801f, modelview,
      projection, viewport, &G.mouseGUIX, &G.mouseGUIY, &G.mouseGUIZ);
}

static unsigned char *pickingBuffer = NULL;
static int pickingBufferSize = 0;

void UpdatePickingBuffer(void)
{
  // Get the viewport
  GLint viewport[4];
  GLint width;
  GLint height;
  glGetIntegerv(GL_VIEWPORT, viewport);

  width = viewport[2];
  height = viewport[3];

  if (pickingBuffer)
  {
    // Resize the buffer in case the window size has changed
    if  (pickingBufferSize != width * height * 3)
    {
      pickingBufferSize = width * height * 3;
      pickingBuffer = realloc(pickingBuffer, pickingBufferSize);
    }
  }
  else
  {
    pickingBufferSize = width * height * 3;
    pickingBuffer = malloc(pickingBufferSize);
  }

  // Turn off lighting
  glDisable(GL_LIGHTING);

  // Turn off antialiasing
  glDisable (GL_BLEND);
  glDisable(GL_MULTISAMPLE);

  // Clear screen
  glClearColor(0.0, 0.0, 0.0, 0.0);
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

  // draw the objects in static camera
  mhGUICameraPosition();
  mhDrawMeshes(1, 0);

  // draw the objects in dynamic camera
  mhSceneCameraPosition();
  mhDrawMeshes(1, 1);

  // Make sure the data is 1 byte aligned
  glPixelStorei(GL_PACK_ALIGNMENT, 1);
  glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE, pickingBuffer);

  // Turn on antialiasing
  glEnable (GL_BLEND);
  glEnable(GL_MULTISAMPLE);

  /* restore lighting */
  glEnable(GL_LIGHTING);
}

/** \brief Retrieve the 'selected' color index for the specified coordinates.
 *  \param x an int specifying the horizontal position in the image plane (in pixels).
 *  \param y an int specifying the vertical position in the image plane (in pixels).
 *
 *  This function draws a 'false' color image, assigning a unique sequencial color to each
 *  separate component using the current camera and scene settings. By retrieving the color
 *  index at the location in that image that corresponds to the mouse position during a
 *  mouse click the application can easily tell which object was selected.
 *  The resulting color index is assigned into the global variable 'G.color_picked'.
 *  This function always returns a '0'.
 *
 *  This function turns off lights and textures to draw only 'pure' colors, without
 *  shadows, reflections etc.
 *
 *  This technique is called *Selection Using Unique Color IDs*
 *  and uses glReadPixels() to read the single pixel under the current mouse location mapped
 *  to this invisible copy of the object.
 *
 *  For further information on this technique, see:
 *
 *    - http://www.opengl.org/resources/faq/technical/selection.htm and
 *    - http://wiki.gamedev.net/index.php/OpenGL_Selection_Using_Unique_Color_IDs
 */
void mhGetPickedColor(int x, int y)
{
    // Viewport declaration (required before other expressions)
    GLint viewport[4];

    glGetIntegerv(GL_VIEWPORT, viewport);

    y = viewport[3] - y;

    if (y < 0 || y >= viewport[3] || x < 0 || x >= viewport[2])
    {
      memset(G.color_picked, 0, 3);
      return;
    }

    if (!pickingBuffer)
      UpdatePickingBuffer();

    memcpy(G.color_picked, pickingBuffer + (y * viewport[2] + x) * 3, 3);
}

/** \brief Convert 3D OpenGL world coordinates to screen coordinates.
 *  \param world a list of doubles containing the 3D OpenGL world coordinates.
 *  \param screen a list of doubles that will contain the screen coordinates.
 *  \param camera an int indicating the camera mode (1=Scene or 0=GUI).
 *
 *  This function converts 3D OpenGL world coordinates to screen coordinates based upon 
 *  the specified camera setting.
 *
 */
void mhConvertToScreen(const double world[3], double screen[3], int camera)
{
  GLint viewport[4];
  double modelview[16], projection[16];

  if (camera)
      mhSceneCameraPosition();
  else
      mhGUICameraPosition();

  glGetIntegerv(GL_VIEWPORT, viewport);
  glGetDoublev(GL_PROJECTION_MATRIX, projection);
  glGetDoublev(GL_MODELVIEW_MATRIX, modelview);

  gluProject(world[0], world[1], world[2], modelview, projection, viewport, screen, screen + 1, screen + 2);
  screen[1] = viewport[3] - screen[1];
}

/** \brief Convert 2D (x, y) screen coordinates to OpenGL world coordinates.
 *  \param screen a list of doubles that will contain the screen coordinates.
 *  \param world a list of doubles containing the 3D OpenGL world coordinates.
 *  \param camera an int indicating the camera mode (1=Scene or 0=GUI).
 *
 *  This function converts screen coordinates to 2D OpenGL world coordinates based upon 
 *  the specified camera setting.
 *
 */
void mhConvertToWorld2D(const double screen[2], double world[3], int camera)
{
  GLint viewport[4];
  GLdouble modelview[16], projection[16];
  GLdouble z;

  if (camera)
      mhSceneCameraPosition();
  else
      mhGUICameraPosition();

  glGetIntegerv(GL_VIEWPORT, viewport);
  glGetDoublev(GL_PROJECTION_MATRIX, projection);
  glGetDoublev(GL_MODELVIEW_MATRIX, modelview);

  glReadPixels((GLint)screen[0], (GLint)(viewport[3] - screen[1]), 1, 1, GL_DEPTH_COMPONENT, GL_DOUBLE, &z);
  gluUnProject(screen[0], viewport[3] - screen[1], z, modelview, projection, viewport, world, world + 1, world + 2);
}

/** \brief Convert 3D (x, y, depth) screen coordinates to 3D OpenGL world coordinates.
 *  \param screen a list of doubles that will contain the screen coordinates.
 *  \param world a list of doubles containing the 3D OpenGL world coordinates.
 *  \param camera an int indicating the camera mode (1=Scene or 0=GUI).
 *
 *  This function converts screen coordinates to 3D OpenGL world coordinates based upon 
 *  the specified camera setting.
 *
 */
void mhConvertToWorld3D(const double screen[3], double world[3], int camera)
{
  GLint viewport[4];
  double modelview[16], projection[16];

  if (camera)
      mhSceneCameraPosition();
  else
      mhGUICameraPosition();

  glGetIntegerv(GL_VIEWPORT, viewport);
  glGetDoublev(GL_PROJECTION_MATRIX, projection);
  glGetDoublev(GL_MODELVIEW_MATRIX, modelview);

  gluUnProject(screen[0], viewport[3] - screen[1], screen[2], modelview, projection, viewport, world, world + 1, world + 2);
}

/** \brief Redraw the contents of the window when the user resizes the window.
 *  \param w an int specifying the current width of the available canvas (in pixels).
 *  \param h an int specifying the current height of the available canvas (in pixels).
 *
 *  This function redraws the contents of the window when the user resizes it.
 */
void mhReshape(int w, int h)
{
    /*Prevent a division by zero when minimising the window*/
    if (h == 0)
        h = 1;
    /*Set the drawable region of the window*/
    glViewport(0, 0, w, h);
    // set up the projection matrix
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    // just use a perspective projection
    gluPerspective(G.fovAngle, (float)w/h, 0.1, 100);
    // go back to modelview matrix so we can move the objects about
    glMatrixMode(GL_MODELVIEW);
    G.windowHeight = h;
    G.windowWidth = w;

    UpdatePickingBuffer();
}

/** \brief Initialise the drawing space.
 *
 *  This function clears the screen and depth buffer and any previous transformations
 *  to initialize the drawing space.
 */
void mhDrawBegin(void)
{
    // clear the screen & depth buffer
    glClearColor(G.clearColor[0], G.clearColor[1], G.clearColor[2], G.clearColor[3]);
    glClear(GL_DEPTH_BUFFER_BIT|GL_COLOR_BUFFER_BIT);
}

/** \brief Swap buffers following a redraw.
 *
 *  This function swaps the drawing buffers following a redraw.
 */
void mhDrawEnd(void)
{
    SDL_GL_SwapBuffers();
}

/** \brief Initialize lights and materials/textures.
 *
 *  This function initializes lights and materials/textures available to a scene.
 */
void OnInit(void)
{
    /*Lights and materials*/
    const float lightPos[] = { -10.99f, 20.0f, 20.0f, 1.0f};  /* Light Position */
    const float ambientLight[] = { 0.0f, 0.0f, 0.0f, 1.0f};   /* Ambient Light Values */
    const float diffuseLight[] = { .5f, .5f, .5f, 1.0f};      /* Diffuse Light Values */
    const float specular[] = {0.5f, .5f, .5f, .5f};           /* Specular Light Values */
    const float MatAmb[] = {0.11f, 0.06f, 0.11f, 1.0f};       /* Material - Ambient Values */
    const float MatDif[] = {0.7f, 0.6f, 0.6f, 1.0f};          /* Material - Diffuse Values */
    const float MatSpc[] = {0.33f, 0.33f, 0.52f, 1.0f};       /* Material - Specular Values */
    const float MatShn[] = {50.0f};                           /* Material - Shininess */
    //const float MatEms[] = {0.1f, 0.05f, 0.0f, 1.0f};         /* Material - emission Values */

    glEnable(GL_DEPTH_TEST);                                  /* Hidden surface removal */
    glEnable(GL_CULL_FACE);                                   /* Inside face removal */
    glEnable(GL_LIGHTING);                                    /* Enable lighting */
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight);
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular);
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos);
    glLightModeli(GL_LIGHT_MODEL_COLOR_CONTROL, GL_SEPARATE_SPECULAR_COLOR); // If we enable this, we have stronger specular highlights
    glMaterialfv(GL_FRONT, GL_SHININESS, MatShn);             /* Set Material Shininess */
    glMaterialfv(GL_FRONT, GL_AMBIENT, MatAmb);               /* Set Material Ambience */
    glMaterialfv(GL_FRONT, GL_DIFFUSE, MatDif);               /* Set Material Diffuse */
    glMaterialfv(GL_FRONT, GL_SPECULAR, MatSpc);              /* Set Material Specular */
    glMaterialfv(GL_FRONT, GL_SHININESS, MatShn);             /* Set Material Shininess */
    //glMaterialfv(GL_FRONT, GL_EMISSION, MatEms);              /* Set Material Emission */
    glEnable(GL_LIGHT0);
    glEnable(GL_COLOR_MATERIAL);
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE);
    //glEnable(GL_TEXTURE_2D);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    /*Activate and specify pointers to vertex and normal array*/
    glEnableClientState(GL_NORMAL_ARRAY);
    glEnableClientState(GL_COLOR_ARRAY);
    glEnableClientState(GL_VERTEX_ARRAY);

#ifndef __APPLE__ /* Omit initialization 'cos Mac OS X already supports this! */
    // Init shader functions
    glCreateShader = (PFNGLCREATESHADERPROC)SDL_GL_GetProcAddress("glCreateShader");
    glShaderSource = (PFNGLSHADERSOURCEPROC)SDL_GL_GetProcAddress("glShaderSource");
    glCompileShader = (PFNGLCOMPILESHADERPROC)SDL_GL_GetProcAddress("glCompileShader");
    glCreateProgram = (PFNGLCREATEPROGRAMPROC)SDL_GL_GetProcAddress("glCreateProgram");
    glAttachShader = (PFNGLATTACHSHADERPROC)SDL_GL_GetProcAddress("glAttachShader");
    glLinkProgram = (PFNGLLINKPROGRAMPROC)SDL_GL_GetProcAddress("glLinkProgram");
    glUseProgram = (PFNGLUSEPROGRAMPROC)SDL_GL_GetProcAddress("glUseProgram");
    glGetShaderiv = (PFNGLGETSHADERIVPROC)SDL_GL_GetProcAddress("glGetShaderiv");
    glGetShaderInfoLog = (PFNGLGETSHADERINFOLOGPROC)SDL_GL_GetProcAddress("glGetShaderInfoLog");
    glGetProgramiv = (PFNGLGETPROGRAMIVPROC)SDL_GL_GetProcAddress("glGetProgramiv");
    glGetProgramInfoLog = (PFNGLGETPROGRAMINFOLOGPROC)SDL_GL_GetProcAddress("glGetProgramInfoLog");
    glGetActiveUniform = (PFNGLGETACTIVEUNIFORMPROC)SDL_GL_GetProcAddress("glGetActiveUniform");
#ifdef __WIN32__
    glActiveTexture = (PFNGLACTIVETEXTUREPROC)SDL_GL_GetProcAddress("glActiveTexture");
#endif
    glUniform1f = (PFNGLUNIFORM1FPROC)SDL_GL_GetProcAddress("glUniform1f");
    glUniform2f = (PFNGLUNIFORM2FPROC)SDL_GL_GetProcAddress("glUniform2f");
    glUniform3f = (PFNGLUNIFORM3FPROC)SDL_GL_GetProcAddress("glUniform3f");
    glUniform4f = (PFNGLUNIFORM4FPROC)SDL_GL_GetProcAddress("glUniform4f");
    glUniform1i = (PFNGLUNIFORM1IPROC)SDL_GL_GetProcAddress("glUniform1i");

    g_ShadersSupported = glCreateShader && glShaderSource && glCompileShader &&
      glCreateProgram && glAttachShader && glLinkProgram && glUseProgram &&
      glGetShaderiv && glGetShaderInfoLog && glGetProgramiv && glGetProgramInfoLog &&
      glGetActiveUniform &&
#ifdef __WIN32__
      glActiveTexture &&
#endif
      glUniform1f && glUniform2f && glUniform3f && glUniform4f &&
      glUniform1i && glGetString(GL_SHADING_LANGUAGE_VERSION);
#endif // #ifndef __APPLE__

    // Init font
    G.fontOffset = glGenLists(256);

#ifdef __WIN32__
    {
        HDC   hDC;
        HFONT font;
        SDL_SysWMinfo wmi;
        SDL_VERSION(&wmi.version);
        SDL_GetWMInfo(&wmi);

        hDC = GetDC(wmi.window);
        font = CreateFont(12, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE, ANSI_CHARSET, OUT_TT_PRECIS, CLIP_DEFAULT_PRECIS, 0	, FF_DONTCARE | DEFAULT_PITCH, TEXT("Helvetica"));
        SelectObject(hDC, font);
        wglUseFontBitmaps(hDC, 0, 256, G.fontOffset);
        ReleaseDC(wmi.window, hDC);
    }
#elif defined(__APPLE__)
    buildFont(G.fontOffset, 256, 0, "Lucida Grande", 10);
#else
    {
        Display *dpy = XOpenDisplay(NULL);

        assert(dpy);  // Display valid?
        if (NULL != dpy)
        {
            // 1st attempt: Try to load an helvetica font of the adobe foundry.
            // (see Encoding of the font desription in https://www.msu.edu/~huntharo/xwin/docs/xwindows/XLFD.pdf)
            XFontStruct *XFont = XLoadQueryFont(dpy, "-adobe-helvetica-medium-r-normal--12-120-75-75-p-67-iso8859-1");

            // If this fails then start an 2nd attempt: Try to load *any* font which has a point size of 120.
            if (NULL == XFont)
            {
                XFont = XLoadQueryFont(dpy, "-*-*-*-*-*--*-120-*");            
            }
            assert(XFont); // Failed anyway? :-(

            if (NULL != XFont)
            {
                glXUseXFont(XFont->fid, 0, 256, G.fontOffset);
                XFreeFont(dpy, XFont);
            }
            XCloseDisplay(dpy);
        }
    }
#endif
}

/** \brief Delete materials/textures when the event loop exits.
 *
 *  This function deletes materials/textures when the event loop is exited.
 */
void OnExit(void)
{
    /*Deactivate the pointers to vertex and normal array*/
    glDisableClientState(GL_VERTEX_ARRAY);
    glDisableClientState(GL_NORMAL_ARRAY);
    //glDisableClientState(GL_TEXTURE_COORD_ARRAY);
    glDisableClientState(GL_COLOR_ARRAY);
    printf("Exit from event loop\n");
}

/** \brief Set the camera zoom, position and orientation.
 *
 *  This function sets the camera zoom, position and orientation based upon the
 *  current settings found in global variables.
 *  This function is called before drawing the dynamic camera.
 */
void mhSceneCameraPosition(void)
{
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(G.fovAngle, (float)G.windowWidth/G.windowHeight, 0.1, 100);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glTranslatef(0, 0, -G.zoom);
    glTranslatef(G.translX, G.translY, 0);
    glRotatef(G.rotX, 1 ,0 , 0);
    glRotatef(G.rotY, 0 ,1 , 0);
}

/** \brief Zoom the camera by -10 units.
 *
 *  This function defines a fixed camera zoom for the static camera,
 *  moving it by -10 in the Z dimension.
 */
void mhGUICameraPosition(void)
{
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45, (float)G.windowWidth/G.windowHeight, 0.1, 100);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glTranslatef(0, 0, -10);
}

/** \brief Draw all of the 3D objects held in the G.world array matching the 'pickMode' setting.
 *  \param pickMode an int indicating whether to use selection colors or draw colors.
 *  \param cameraType an int specifying the camera type (movable or fixed).
 *
 *  This function draws all of the 3D objects held in the G.world array, but it does it in two groups.
 *  It can be called to draw all of the fixed elements in the scene, such as the GUI controls or
 *  it can be called to draw all of the movable elements in the scenes (elements that can be moved, rotated etc.).
 *  Movable elements include the elements being modelled, such as the humanoid figure.
 *
 *  This function uses the glDrawElements function to add elements to the scene.
 *  It is used to provide an optimized interface
 *  for drawing the mesh.
 *  <b>Note: </b> Each vertex can only have a single UV value, which
 *  reduces the amount of data that needs to be transferred between Python and
 *  the C engine, but results in some artifacts along the UV seams.
 *
 *  Each model can be drawn in its natural color or in an adapted color to indicate
 *  that the model is currently selected. The pickMode parameter indicates which
 *  mode to use for this call.
 *
 *  Each object can be viewed using one or other of two different cameras:
 *    -  a <i>dynamic</i> camera for items that can be moved using the mouse (typically objects being modelled)
 *    -  a <i>static</i> camera for fixed GUI elements (e.g. GUI controls)
 */
void mhDrawMeshes(int pickMode, int cameraType)
{
    PyObject *iterator;
    Object3D *obj;
    
    if (!G.world)
    {
        return;
    }

    /*Draw all objects contained by G.world*/
    iterator = PyObject_GetIter(G.world);

    for (obj = (Object3D*)PyIter_Next(iterator); obj; obj = (Object3D*)PyIter_Next(iterator))
    {
        if (!PyObject_TypeCheck(obj, &Object3DType))
          continue;

        if (obj->inMovableCamera == cameraType)
        {
            if (obj->isVisible && (!pickMode || obj->isPickable))
            {
                //printf("draw obj n %i\n",G.world[i].nVerts/3);
                /*Transform the current object*/
                glPushMatrix();
                glTranslatef(obj->location[0], obj->location[1], obj->location[2]);
                glRotatef(obj->rotation[0], 1, 0, 0);
                glRotatef(obj->rotation[1], 0, 1, 0);
                glRotatef(obj->rotation[2], 0, 0, 1);
                glScalef(obj->scale[0], obj->scale[1], obj->scale[2]);

                if (obj->texture && !pickMode)
                {
                    glEnable(GL_TEXTURE_2D);
                    /*Bind the texture, that has the same index of object*/

                    glEnableClientState(GL_TEXTURE_COORD_ARRAY);
                    glBindTexture(GL_TEXTURE_2D, obj->texture);

                    glTexCoordPointer(2, GL_FLOAT, 0, obj->UVs);
                }

                /*Fill the array pointers with object mesh data*/
                glVertexPointer(3, GL_FLOAT, 0, obj->verts);
                glNormalPointer(GL_FLOAT, 0, obj->norms);

                /*Because the selection is based on color, the color array can have 2 values*/
                if (pickMode)
                {
                    /*Use color to pick i */
                    glColorPointer(3, GL_UNSIGNED_BYTE, 0, obj->colors);
                }
                else
                {
                    /*Use color to draw i */
                    glColorPointer(4, GL_UNSIGNED_BYTE, 0, obj->colors2);
                    /*draw text attribute if there is one; because this function
                    restores lighting, it can be used only in non picking mode*/
                    if (obj->textString && obj->textString[0] != '\0')
                        mhDrawText(obj->location[0], obj->location[1], obj->textString);
                }

                /*Disable lighting if the object is shadeless*/
                if (obj->shadeless || pickMode)
                {
                    glDisable(GL_LIGHTING);
                }

                // Enable the shader if the driver supports it and there is a shader assigned
                if (!pickMode && g_ShadersSupported && obj->shader)
                {
                  //int isValid;
                  //glValidateProgram(ProgramObject);
                  //glGetProgramiv(ProgramObject, GL_VALIDATE_STATUS, &isValid);
                  //glGetProgramInfoLog

                  glUseProgram(obj->shader);

                  // This should be optimized, since we only need to do it when it's changed
                  // Validation should also only be done when it is set
                  if (obj->shaderParameters)
                  {
                    GLint parameterCount = 0;
                    int index;
                    int currentTextureSampler = 1;
                    
                    glGetProgramiv(obj->shader, GL_ACTIVE_UNIFORMS, &parameterCount);

                    for (index = 0; index < parameterCount; index++)
                    {
                      GLsizei length;
 	                    GLint size;
 	                    GLenum type;
 	                    GLchar name[32];
                      PyObject *value;

                      glGetActiveUniform(obj->shader, index, 32, &length, &size, &type, name);

                      value = PyDict_GetItemString(obj->shaderParameters, name);

                      if (value)
                      {
                        switch (type)
                        {
                          case GL_FLOAT:
                          {
                            glUniform1f(index, PyFloat_AsDouble(value));
                            break;
                          }
                          case GL_FLOAT_VEC2:
                          {
                            if (!PyList_Check(value) || PyList_Size(value) != 2)
                              break;
                            glUniform2f(index, PyFloat_AsDouble(PyList_GetItem(value, 0)), PyFloat_AsDouble(PyList_GetItem(value, 1)));
                            break;
                          }
                          case GL_FLOAT_VEC3:
                          {
                            if (!PyList_Check(value) || PyList_Size(value) != 3)
                              break;
                            glUniform3f(index, PyFloat_AsDouble(PyList_GetItem(value, 0)), PyFloat_AsDouble(PyList_GetItem(value, 1)),
                              PyFloat_AsDouble(PyList_GetItem(value, 2)));
                            break;
                          }
                          case GL_FLOAT_VEC4:
                          {
                            if (!PyList_Check(value) || PyList_Size(value) != 4)
                              break;
                            glUniform4f(index, PyFloat_AsDouble(PyList_GetItem(value, 0)), PyFloat_AsDouble(PyList_GetItem(value, 1)),
                              PyFloat_AsDouble(PyList_GetItem(value, 2)), PyFloat_AsDouble(PyList_GetItem(value, 3)));
                            break;
                          }
                          case GL_SAMPLER_1D:
                          {
                            glActiveTexture(GL_TEXTURE0 + currentTextureSampler);
                            glBindTexture(GL_TEXTURE_1D, PyInt_AsLong(value));
                            glUniform1i(index, currentTextureSampler++);
                            break;
                          }
                          case GL_SAMPLER_2D:
                          {
                            glActiveTexture(GL_TEXTURE0 + currentTextureSampler);
                            glBindTexture(GL_TEXTURE_2D, PyInt_AsLong(value));
                            glUniform1i(index, currentTextureSampler++);
                            break;
                          }
                        }
                      }
                    }
                  }
                }

                /*draw the mesh*/
                glDrawElements(GL_TRIANGLES, obj->nTrigs * 3, GL_UNSIGNED_INT, obj->trigs);

                // Disable the shader if the driver supports it and there is a shader assigned
                if (!pickMode && g_ShadersSupported && obj->shader)
                {
                  glUseProgram(0);
                  glActiveTexture(GL_TEXTURE0);
                }

                /*Enable lighting if the object was shadeless*/
                if (obj->shadeless || pickMode)
                {
                    glEnable(GL_LIGHTING);
                }

                if (obj->texture && !pickMode)
                {
                    glDisable(GL_TEXTURE_2D);
                    glDisableClientState(GL_TEXTURE_COORD_ARRAY);
                }

                glPopMatrix();
            }
        }

        Py_DECREF((PyObject*)obj);
    }

    Py_DECREF(iterator);
}

/** \brief Draw all visible 3D objects.
 *
 *  This function re-initializes the canvas and draws all of the 3D objects by making two
 *  calls to the mhDrawMeshes function. The first call draws all static objects
 *  (typically GUI controls). The second call draws all dynamic objects (e.g. the humanoid model)
 */
void mhDraw(void)
{
    mhDrawBegin();

    // draw the objects in dynamic camera
    mhSceneCameraPosition();
    mhDrawMeshes(0, 1);

    // draw the objects in static camera
    mhGUICameraPosition();
    mhDrawMeshes(0, 0);

    mhDrawEnd();
}

/** \brief Shutdown the MakeHuman Application.
 *
 *  This function is part of the MakeHuman termination sequence prompted
 *  by a user electing to end the application.
 *
 *  This function sets loop to 0 which makes the event loop exit.
 */
void mhShutDown(void)
{
    G.loop = 0;
}

/** \brief Queue an update.
 *
 *  This function places an update event into the event queue if there
 *  isn't one pending already. This makes sure we don't create a "traffic
 *  jam" in the event queue when the system is slow in redrawing
 */
void mhQueueUpdate(void)
{
    SDL_Event ev;

    if (G.pendingUpdate)
    {
        return;
    }

    G.pendingUpdate = 1;

    ev.type = SDL_VIDEOEXPOSE;
    SDL_PushEvent(&ev);
}

/** \brief Set fullscreen mode.
 *  \param fullscreen an int indicating whether to use a window or full screen mode.
 *
 *  This function controls whether the MakeHuman GUI is displayed in a window
 *  or in full screen mode:
 *    0 for windowed
 *    1 for fullscreen
 */
void mhSetFullscreen(int fullscreen)
{
    if (G.fullscreen == fullscreen)
    {
        return;
    }
    
    G.fullscreen = fullscreen;
    
    if (fullscreen)
    {
        G.windowWidth  = g_desktopWidth;
        G.windowHeight = g_desktopHeight;
    }
    else
    {
        G.windowWidth  = g_windowWidth;
        G.windowHeight = g_windowHeight;
    }

    if (!g_screen)

    if (!g_screen)
    {
        return;
    }
    
    g_screen = SDL_SetVideoMode(G.windowWidth, G.windowHeight, 24, SDL_OPENGL | (G.fullscreen ? SDL_FULLSCREEN : 0) | SDL_RESIZABLE);
    OnInit();
    mhReshape(G.windowWidth, G.windowHeight);
    callReloadTextures();
    mhDraw();
}

/** \brief Create SDL window.
 *  \param useTimer an int controlling whether timer based processing is to be used (1=yes, 0=no).
 *
 *  This function implements one of the first parts of the MakeHuman initiation sequence.
 *  It sets up the environment that the SDL module will use to manage the GUI window.
 *
 */
void mhCreateWindow(int useTimer)
{
    unsigned int colorkey;
    SDL_Surface *image;
    const SDL_VideoInfo *info;

    atexit(SDL_Quit);

    if (SDL_Init(SDL_INIT_VIDEO) < 0)
    {
        printf("Unable to init SDL: %s\n", SDL_GetError());
        exit(1);
    }

    SDL_GL_SetAttribute(SDL_GL_RED_SIZE, 8);
    SDL_GL_SetAttribute(SDL_GL_GREEN_SIZE, 8);
    SDL_GL_SetAttribute(SDL_GL_BLUE_SIZE, 8);
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24);
    SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1);
    SDL_GL_SetAttribute(SDL_GL_SWAP_CONTROL, 1); // This fixes flickering in compiz
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 1);
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 4);

    info = SDL_GetVideoInfo();
    g_desktopWidth = info->current_w;
    g_desktopHeight = info->current_h;

    // Load and set window icon
    image = SDL_LoadBMP("mh_icon.bmp");
    if (image)
    {
        colorkey = SDL_MapRGB(image->format, 255, 255, 255);
        SDL_SetColorKey(image, SDL_SRCCOLORKEY, colorkey);
        SDL_WM_SetIcon(image, NULL);
    }

    if (G.fullscreen)
    {
        G.windowWidth = g_desktopWidth;
        G.windowHeight = g_desktopHeight;
    }
    else
    {
        G.windowWidth = g_windowWidth;
        G.windowHeight = g_windowHeight;
    }

    g_screen = SDL_SetVideoMode(G.windowWidth, G.windowHeight, 24, SDL_OPENGL | (G.fullscreen ? SDL_FULLSCREEN : 0) | SDL_RESIZABLE);
    if (g_screen == NULL)
    {
        printf("No antialiasing available, turning off antialiasing.\n");
        SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 0);
        SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 0);
        g_screen = SDL_SetVideoMode(G.windowWidth, G.windowHeight, 24, SDL_OPENGL | (G.fullscreen ? SDL_FULLSCREEN : 0) | SDL_RESIZABLE);
        if (g_screen == NULL)
        {
            printf("No 24 bit z buffer available, switching to 16 bit.\n");
            SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 16);
            g_screen = SDL_SetVideoMode(G.windowWidth, G.windowHeight, 24, SDL_OPENGL | (G.fullscreen ? SDL_FULLSCREEN : 0) | SDL_RESIZABLE);
            if (g_screen == NULL)
            {
                printf("No 16 bit z buffer available, exiting.\n");
                exit(1);
            }
        }
    }

    SDL_WM_SetCaption("MakeHuman", "");
    SDL_EnableKeyRepeat(SDL_DEFAULT_REPEAT_DELAY, SDL_DEFAULT_REPEAT_INTERVAL);

#ifdef __WIN32__
    SDL_EnableUNICODE(1);

#endif

    if (useTimer == 1)
    {
        SDL_InitSubSystem(SDL_INIT_TIMER);
        SDL_AddTimer(G.millisecTimer, mhTimerFunc, NULL);
    }

    OnInit();
    mhReshape(G.windowWidth, G.windowHeight);
    mhDraw();
}


/** \brief Start the event loop to manage the MakeHuman GUI.
 *
 *  This function implements the event loop which manages all user interaction, 
 *  determining which functions to call to handle events etc.
 */
void mhEventLoop(void)
{
    //SDL_ShowCursor(SDL_DISABLE);

    while (G.loop)
    {
        SDL_Event event;
        SDL_WaitEvent(&event);

        switch (event.type)
        {
        case SDL_ACTIVEEVENT:
            if (event.active.state & SDL_APPINPUTFOCUS)
            {
              if (event.active.gain)
              {
                //SDL_ShowCursor(SDL_DISABLE);
              }
              else
              {
                //SDL_ShowCursor(SDL_ENABLE);
#ifdef __WIN32__
                SDL_WM_GrabInput(SDL_GRAB_OFF);
#endif
              }
            }
            break;
        case SDL_KEYDOWN:
            G.modifiersKeyState = event.key.keysym.mod;
            mhKeyDown(event.key.keysym.sym, event.key.keysym.unicode, event.key.keysym.mod);
            break;
        case SDL_KEYUP:
            G.modifiersKeyState = event.key.keysym.mod;
            if (event.key.keysym.sym == SDLK_F11 || (event.key.keysym.sym == SDLK_RETURN && event.key.keysym.mod & KMOD_ALT))
                mhSetFullscreen(!G.fullscreen); // Switch fullscreen
            else
                mhKeyUp(event.key.keysym.sym, event.key.keysym.unicode, event.key.keysym.mod);
            break;
        case SDL_MOUSEMOTION:
            mhMouseMotion(event.motion.state, event.motion.x, event.motion.y, event.motion.xrel, event.motion.yrel);
            break;
        case SDL_MOUSEBUTTONDOWN:
            mhMouseButtonDown(event.button.button, event.button.x, event.button.y);
            break;
        case SDL_MOUSEBUTTONUP:
            mhMouseButtonUp(event.button.button, event.button.x, event.button.y);
            break;
        case SDL_USEREVENT:
            callTimerFunct();
            G.pendingTimer = 0;
            break;
        case SDL_VIDEORESIZE:
            G.windowWidth = g_windowWidth = event.resize.w;
            G.windowHeight = g_windowHeight = event.resize.h;
            g_screen = SDL_SetVideoMode(G.windowWidth, G.windowHeight, 24, SDL_OPENGL | (G.fullscreen ? SDL_FULLSCREEN : 0) | SDL_RESIZABLE);
            OnInit();
            mhReshape(event.resize.w, event.resize.h);
            callReloadTextures();
            mhDraw();
            break;
        case SDL_VIDEOEXPOSE:
            mhDraw();
            G.pendingUpdate = 0;
            break;
        case SDL_QUIT:
            mhShutDown();
            break;
        }
    }

    OnExit();
}
