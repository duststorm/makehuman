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
     <td>MakeHuman Team 2001-2010                        </td></tr>
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
#ifdef _DEBUG
    #undef _DEBUG
    #include <Python.h>
    #define _DEBUG
#else
    #include <Python.h>
#endif

#include "glmodule.h"
#include "core.h"
#include <assert.h>
#include <structmember.h>

#ifdef __WIN32__
    #include <windows.h>
    #include <SDL_syswm.h>
#elif __APPLE__
    #include "SDL_image.h"
    #include "TextureCache.h"
#else
    #include <X11/Xlib.h>
    #include <X11/Xutil.h>
    #include <GL/glx.h>
#endif

static int g_savedx=0; /*saved x mouse position*/
static int g_savedy=0; /*saved y mouse position*/
static int g_desktopWidth = 0;
static int g_desktopHeight = 0;
static int g_windowWidth = 800;
static int g_windowHeight = 600;
static SDL_Surface *g_screen = NULL;

unsigned int g_primitiveMap[] = { GL_POINTS, GL_LINES, GL_TRIANGLES, GL_QUADS };

#ifndef __APPLE__
typedef SDL_Surface *(*PFN_IMG_LOAD)(const char *);
static void *g_sdlImageHandle = NULL;
static PFN_IMG_LOAD IMG_Load = NULL;
#endif

void mhCameraPosition(Camera *camera, int eye);

// Camera attributes directly accessed by Python
static PyMemberDef Camera_members[] =
{
    {"fovAngle", T_FLOAT, offsetof(Camera, fovAngle), 0, "The Field Of View angle."},
    {"nearPlane", T_FLOAT, offsetof(Camera, nearPlane), 0, "The Near Clipping Plane."},
    {"farPlane", T_FLOAT, offsetof(Camera, farPlane), 0, "The Far Clipping Plane."},
    {"projection", T_UINT, offsetof(Camera, projection), 0, "The projection type, 0 for orthogonal, 1 for perspective."},
    {"stereoMode", T_UINT, offsetof(Camera, stereoMode), 0, "The Stereo Mode, 0 for no stereo, 1 for toe-in, 2 for off-axis."},
    {"eyeSeparation", T_FLOAT, offsetof(Camera, eyeSeparation), 0, "The Eye Separation."},
    {"eyeX", T_FLOAT, offsetof(Camera, eyeX), 0, "The x position of the eye."},
    {"eyeY", T_FLOAT, offsetof(Camera, eyeY), 0, "The y position of the eye."},
    {"eyeZ", T_FLOAT, offsetof(Camera, eyeZ), 0, "The z position of the eye."},
    {"focusX", T_FLOAT, offsetof(Camera, focusX), 0, "The x position of the focus."},
    {"focusY", T_FLOAT, offsetof(Camera, focusY), 0, "The y position of the focus."},
    {"focusZ", T_FLOAT, offsetof(Camera, focusZ), 0, "The z position of the focus."},
    {"upX", T_FLOAT, offsetof(Camera, upX), 0, "The x of the up vector."},
    {"upY", T_FLOAT, offsetof(Camera, upY), 0, "The y of the up vector."},
    {"upZ", T_FLOAT, offsetof(Camera, upZ), 0, "The z of the up vector."},
    {NULL}  /* Sentinel */
};

PyObject *Camera_convertToScreen(Camera *camera, PyObject *args);
PyObject *Camera_convertToWorld2D(Camera *camera, PyObject *args);
PyObject *Camera_convertToWorld3D(Camera *camera, PyObject *args);

// Camera Methods
static PyMethodDef Camera_methods[] =
{
    {
        "convertToScreen", (PyCFunction)Camera_convertToScreen, METH_VARARGS,
        "Converts world coordinates to screen coordinates."
    },
    {
        "convertToWorld2D", (PyCFunction)Camera_convertToWorld2D, METH_VARARGS,
        "Converts 2D screen coordinates to world coordinates."
    },
    {
        "convertToWorld3D", (PyCFunction)Camera_convertToWorld3D, METH_VARARGS,
        "Converts 3D screen coordinates to world coordinates."
    },
    {NULL}  /* Sentinel */
};

static PyObject *Camera_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int Camera_init(Camera *self, PyObject *args, PyObject *kwds);

// Camera type definition
PyTypeObject CameraType =
{
    PyObject_HEAD_INIT(NULL)
    0,                                        // ob_size
    "mh.Camera",                              // tp_name
    sizeof(Camera),                           // tp_basicsize
    0,                                        // tp_itemsize
    0,                                        // tp_dealloc
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
    "Camera object",                          // tp_doc
    0,                                        // tp_traverse
    0,                                        // tp_clear
    0,                                        // tp_richcompare
    0,                                        // tp_weaklistoffset
    0,                                        // tp_iter
    0,                                        // tp_iternext
    Camera_methods,                           // tp_methods
    Camera_members,                           // tp_members
    0,                                        // tp_getset
    0,                                        // tp_base
    0,                                        // tp_dict
    0,                                        // tp_descr_get
    0,                                        // tp_descr_set
    0,                                        // tp_dictoffset
    (initproc)Camera_init,                    // tp_init
    0,                                        // tp_alloc
    Camera_new,                               // tp_new
};

/** \brief Registers the Camera object in the Python environment.
 *  \param module The module to register the Camera object in.
 *
 *  This function registers the Camera object in the Python environment.
 */
void RegisterCamera(PyObject *module)
{
    if (PyType_Ready(&CameraType) < 0)
        return;

    Py_INCREF(&CameraType);
    PyModule_AddObject(module, "Camera", (PyObject*)&CameraType);
}

/** \brief Takes care of the initialization of the Camera object members.
 *  \param self The Camera object which is being initialized.
 *
 *  This function takes care of the initialization of the Camera object members.
 */
static PyObject *Camera_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    // Alloc Python data
    Camera *self = (Camera*)type->tp_alloc(type, 0);

    // Init our data
    if (self)
    {
        self->fovAngle = 25.0f;
        self->nearPlane = 0.1f;
        self->farPlane = 100.0f;

        self->projection = 1;

        self->stereoMode = 0;
        self->eyeSeparation = 1.0f;

        self->eyeX = 0.0f;
        self->eyeY = 0.0f;
        self->eyeZ = 60.0f;
        self->focusX = 0.0f;
        self->focusY = 0.0f;
        self->focusZ = 0.0f;
        self->upX = 0.0f;
        self->upY = 1.0f;
        self->upZ = 0.0f;
    }

    return (PyObject*)self;
}

/** \brief The constructor of the Texture object.
 *  \param self The Texture object which is being constructed.
 *  \param args The arguments.
 *
 *  The constructor of the Texture object.
 */
static int Camera_init(Camera *self, PyObject *args, PyObject *kwds)
{
    char *path = NULL;

    if (!PyArg_ParseTuple(args, "|s", &path))
        return -1;

    return 0;
}

typedef struct
{
    PyObject_HEAD
    GLuint textureId;
    int width;
    int height;
} Texture;

// Texture attributes directly accessed by Python
static PyMemberDef Texture_members[] =
{
    {"textureId", T_UINT, offsetof(Texture, textureId), READONLY, "The id of the OpenGL texture."},
    {"width",     T_UINT, offsetof(Texture, width),     READONLY, "The width of the texture in pixels."},
    {"height",    T_UINT, offsetof(Texture, height),    READONLY, "The height of the texture in pixels."},
    {NULL}  /* Sentinel */
};

static PyObject *Texture_loadImage(Texture *texture, PyObject *path);
static PyObject *Texture_loadSubImage(Texture *texture, PyObject *args);

// Texture Methods
static PyMethodDef Texture_methods[] =
{
    {
        "loadImage", (PyCFunction)Texture_loadImage, METH_O,
        "Loads the specified image from file"
    },
    {
        "loadSubImage", (PyCFunction)Texture_loadSubImage, METH_VARARGS,
        "Loads the specified image from file at the specified coordinates"
    },
    {NULL}  /* Sentinel */
};

static void Texture_dealloc(Texture *self);
static PyObject *Texture_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int Texture_init(Texture *self, PyObject *args, PyObject *kwds);

// Texture type definition
PyTypeObject TextureType =
{
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
    0,                                        // tp_traverse
    0,                                        // tp_clear
    0,                                        // tp_richcompare
    0,                                        // tp_weaklistoffset
    0,                                        // tp_iter
    0,                                        // tp_iternext
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

/** \brief Registers the Texture object in the Python environment.
 *  \param module The module to register the Texture object in.
 *
 *  This function registers the Texture object in the Python environment.
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
    if (PyString_Check(path))
    {
        if (!mhLoadTexture(PyString_AsString(path), texture->textureId, &texture->width, &texture->height))
            return NULL;
    }
    else if (PyUnicode_Check(path))
    {
        path = PyUnicode_AsUTF8String(path);
        if (!mhLoadTexture(PyString_AsString(path), texture->textureId, &texture->width, &texture->height))
        {
            Py_DECREF(path);
            return NULL;
        }
        Py_DECREF(path);
    }
    else
    {
        PyErr_SetString(PyExc_TypeError, "String or Unicode object expected");
        return NULL;
    }

    return Py_BuildValue("");
}

static PyObject *Texture_loadSubImage(Texture *texture, PyObject *args)
{
  PyObject *path;
  int x, y;

  if (!PyArg_ParseTuple(args, "Oii", &path, &x, &y))
    return NULL;

  if (PyString_Check(path))
  {
    if (!mhLoadSubTexture(PyString_AsString(path), texture->textureId, x, y))
      return NULL;
  }
  else if (PyUnicode_Check(path))
  {
    path = PyUnicode_AsUTF8String(path);
    if (!mhLoadSubTexture(PyString_AsString(path), texture->textureId, x, y))
    {
      Py_DECREF(path);
      return NULL;
    }
    Py_DECREF(path);
  }
  else
  {
    PyErr_SetString(PyExc_TypeError, "String or Unicode object expected");
    return NULL;
  }

  return Py_BuildValue("");
}

#if SDL_BYTEORDER == SDL_BIG_ENDIAN
/** \brief Perform a byte swapping of a long value by reversing all bytes
 *         (e.g. 0x12345678 becomes 0x78563412).
 *  \param inValue The long to swap to.
 *  \return The long value swapped.
 */

static uint32_t swapLong(uint32_t inValue)
{
#ifdef __GNUC__
    return __builtin_bswap32(inValue);
#endif
    return (((inValue      ) & 0xff) << 24) |
           (((inValue >>  8) & 0xff) << 16) |
           (((inValue >> 16) & 0xff) <<  8) |
           (((inValue >> 24) & 0xff));
}
#endif // #if SDL_BYTEORDER == SDL_BIG_ENDIAN

/** \brief Copy one Array of long values (32 bits) to another location in
 *         memory by considering the endian correctness.
 *         The rule here is that if the machine this method is a big endian
 *         architecture (e.g. PowerPC) then every long is swapped accordingly.
 *         On big endian architectures (as x86) no byte swapping will be done.
 *
 *  \param destPtr the destination pointer (the target of the copy process).
 *  \param srcPtr the source pointer which points to the data to copy from.
 *  \param inLongs The count of long values to copy to. Note that this is not
 *         in bytes but in long values (1 long consumes 4 bytes)
 *  \return The numer of longs copied.
 */
static int longCopyEndianSafe(uint32_t *destPtr, const uint32_t *srcPtr, size_t inLongs)
{
#if SDL_BYTEORDER == SDL_LIL_ENDIAN
    memcpy(destPtr, srcPtr, inLongs << 2);
#else /* For Big Endian we'll need to swap all bytes within the long */
    int i;
    for (i=0; i<inLongs; ++i)
    {
        *(destPtr++) = swapLong(*(srcPtr++));
    }
#endif
    return (int)inLongs;
}

/** \brief Flip an SDL surface from top to bottom.
 *  \param surface a pointer to an SDL_Surface.
 *
 *  This function takes an SDL surface, working line by line it takes the top line and
 *  swaps it with the bottom line, then the second line and swaps it with the second
 *  line from the bottom etc. until the surface has been mirrored from top to bottom.
 */
static void mhFlipSurface(SDL_Surface *surface)
{
    unsigned char *line = (unsigned char*)malloc(surface->pitch);
    const size_t lineBytes = surface->pitch;
    const size_t lineLongs = lineBytes >> 2;

    unsigned char *pixelsA;
    unsigned char *pixelsB;

    int lineIndex;

    if (line)
    {
        if (SDL_MUSTLOCK(surface)) SDL_LockSurface(surface);

        pixelsA = (unsigned char*)surface->pixels;
        pixelsB = (unsigned char*)surface->pixels + (surface->h - 1) * lineBytes;

        for (lineIndex = 0; lineIndex < surface->h >> 1; lineIndex++)
        {
            memcpy((uint32_t*)line,    (const uint32_t*)pixelsA, lineBytes);
            longCopyEndianSafe((uint32_t*)pixelsA, (const uint32_t*)pixelsB, lineLongs);
            longCopyEndianSafe((uint32_t*)pixelsB, (const uint32_t*)line,    lineLongs);

            pixelsA += lineBytes;
            pixelsB -= lineBytes;
        }
        if (SDL_MUSTLOCK(surface)) SDL_UnlockSurface(surface);
        free(line);
    }
}

static SDL_Surface *mhLoadImage(const char *fname)
{
    SDL_Surface *surface;

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

    return surface;
}

/** \brief Load a texture from a file and bind it into the textures array.
 *  \param fname a character string pointer to a string containing a file system path to a texture file.
 *  \param texture an int specifying the existing texture id to use or 0 to create a new texture.
 *
 *  This function loads a texture from a texture file and binds it into the OpenGL textures array.
 */
GLuint mhLoadTexture(const char *fname, GLuint texture, int *width, int *height)
{
#ifdef __APPLE__
    return textureCacheLoadTexture(fname, texture, width, height);
#else /* !__APPLE__ */
    SDL_Surface *surface;
    int internalFormat, format;

    if (!texture)
        glGenTextures(1, &texture);

    surface = mhLoadImage(fname);

    if (!surface)
        return 0;

    switch (surface->format->BytesPerPixel)
    {
    case 1:
        internalFormat = GL_ALPHA8;
        format = GL_ALPHA;
        break;
    case 3:
        internalFormat = 3;
        if (surface->format->Rshift) // If there is a shift on the red value, we need to tell that red and blue are switched
            format = GL_BGR;
        else
            format = GL_RGB;
        break;
    case 4:
        internalFormat = 4;
        if (surface->format->Rshift) // If there is a shift on the red value, we need to tell that red and blue are switched
            format = GL_BGRA;
        else
            format = GL_RGBA;
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
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE_EXT);
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE_EXT);
        //glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        //gluBuild1DMipmaps(GL_TEXTURE_1D, internalFormat, surface->w, format, GL_UNSIGNED_BYTE, surface->pixels);
		glTexImage1D(GL_TEXTURE_1D, 0, internalFormat, surface->w, 0, format, GL_UNSIGNED_BYTE, surface->pixels);
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
    }
    else
    {
        glBindTexture(GL_TEXTURE_2D, texture);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE_EXT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE_EXT);

        //glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

        //gluBuild2DMipmaps(GL_TEXTURE_2D, internalFormat, surface->w, surface->h, format, GL_UNSIGNED_BYTE, surface->pixels);
        glTexImage2D(GL_TEXTURE_2D, 0, internalFormat, surface->w, surface->h, 0, format, GL_UNSIGNED_BYTE, surface->pixels);
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
    }

    if (width)
        *width = surface->w;
    if (height)
        *height = surface->h;

    SDL_FreeSurface(surface);

    return texture;
#endif // ! __APPLE__
}

GLuint mhLoadSubTexture(const char *fname, GLuint texture, int x, int y)
{
#ifdef __APPLE__
    return textureCacheLoadSubTexture(fname, texture, x, y);
#else
    SDL_Surface *surface;
    int internalFormat, format;

    if (!texture)
    {
        PyErr_Format(PyExc_RuntimeError, "Texture is empty, cannot load a sub texture into it");
        return 0;
    }

    surface = mhLoadImage(fname);

    if (!surface)
        return 0;

    switch (surface->format->BytesPerPixel)
    {
    case 1:
        internalFormat = GL_ALPHA8;
        format = GL_ALPHA;
        break;
    case 3:
        internalFormat = 3;
        if (surface->format->Rshift) // If there is a shift on the red value, we need to tell that red and blue are switched
            format = GL_BGR;
        else
            format = GL_RGB;
        break;
    case 4:
        internalFormat = 4;
        if (surface->format->Rshift) // If there is a shift on the red value, we need to tell that red and blue are switched
            format = GL_BGRA;
        else
            format = GL_RGBA;
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
        glTexSubImage1D(GL_TEXTURE_1D, 0, x, surface->w, format, GL_UNSIGNED_BYTE, surface->pixels);
    }
    else
    {
        glBindTexture(GL_TEXTURE_2D, texture);
        glTexSubImage2D(GL_TEXTURE_2D, 0, x, y, surface->w, surface->h, format, GL_UNSIGNED_BYTE, surface->pixels);
    }

    SDL_FreeSurface(surface);

    return texture;
#endif // ! __APPLE__
}

GLuint mhCreateVertexShader(const char *source)
{
    GLuint v;
    GLint status;

    if (GLEW_VERSION_2_0)
    {
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
    else if (GLEW_ARB_shader_objects)
    {
        v = glCreateShaderObjectARB(GL_VERTEX_SHADER_ARB);

        glShaderSourceARB(v, 1, &source, NULL);

        glCompileShaderARB(v);
        glGetObjectParameterivARB(v, GL_OBJECT_COMPILE_STATUS_ARB, &status);
        if (status != GL_TRUE)
        {
            GLsizei logLength;

            glGetObjectParameterivARB(v, GL_OBJECT_INFO_LOG_LENGTH_ARB, &logLength);

            if (logLength > 0)
            {
                char *log;
                GLsizei charsWritten;

                log = (char*)malloc(logLength);
                glGetInfoLogARB(v, logLength, &charsWritten, log);
                PyErr_Format(PyExc_RuntimeError, "Error compiling vertex shader: %s", log);
                free(log);
            }
            else
                PyErr_SetString(PyExc_RuntimeError, "Error compiling vertex shader");

            return 0;
        }

        return v;
    }
    else
    {
        PyErr_SetString(PyExc_RuntimeError, "No shader support detected");
        return 0;
    }
}

GLuint mhCreateFragmentShader(const char *source)
{
    GLuint f;
    GLint status;

    if (GLEW_VERSION_2_0)
    {
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
    else if (GLEW_ARB_shader_objects)
    {
        f = glCreateShaderObjectARB(GL_FRAGMENT_SHADER_ARB);

        glShaderSourceARB(f, 1, &source, NULL);

        glCompileShaderARB(f);
        glGetObjectParameterivARB(f, GL_OBJECT_COMPILE_STATUS_ARB, &status);
        if (status != GL_TRUE)
        {
            GLsizei logLength;

            glGetObjectParameterivARB(f, GL_OBJECT_INFO_LOG_LENGTH_ARB, &logLength);

            if (logLength > 0)
            {
                char *log;
                GLsizei charsWritten;

                log = (char*)malloc(logLength);
                glGetInfoLogARB(f, logLength, &charsWritten, log);
                PyErr_Format(PyExc_RuntimeError, "Error compiling fragment shader: %s", log);
                free(log);
            }
            else
                PyErr_SetString(PyExc_RuntimeError, "Error compiling fragment shader");

            return 0;
        }

        return f;
    }
    else
    {
        PyErr_SetString(PyExc_RuntimeError, "No shader support detected");
        return 0;
    }
}

GLuint mhCreateShader(GLuint vertexShader, GLuint fragmentShader)
{
    GLuint p;
    GLint status;

    if (GLEW_VERSION_2_0)
    {
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
    else if (GLEW_ARB_shader_objects)
    {
        p = glCreateProgramObjectARB();

        glAttachObjectARB(p, vertexShader);
        glAttachObjectARB(p, fragmentShader);

        glLinkProgramARB(p);
        glGetObjectParameterivARB(p, GL_OBJECT_LINK_STATUS_ARB , &status);
        if (status != GL_TRUE)
        {
            GLsizei logLength;

            glGetObjectParameterivARB(p, GL_OBJECT_INFO_LOG_LENGTH_ARB, &logLength);

            if (logLength > 0)
            {
                char *log;
                GLsizei charsWritten;

                log = (char*)malloc(logLength);
                glGetInfoLogARB(p, logLength, &charsWritten, log);
                PyErr_Format(PyExc_RuntimeError, "Error linking shader: %s", log);
                free(log);
            }
            else
                PyErr_SetString(PyExc_RuntimeError, "Error linking shader");

            return 0;
        }

        return p;
    }
    else
    {
        PyErr_SetString(PyExc_RuntimeError, "No shader support detected");
        return 0;
    }
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
unsigned int mhTimerFunc(unsigned int interval, void *param)
{
    SDL_Event event;

    event.type = SDL_USEREVENT;
    event.user.code = 0;
    event.user.data1 = param;
    event.user.data2 = NULL;

    SDL_PushEvent(&event);

    /*reset the timer to recall the function again, after interval milliseconds*/
    return interval;
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
    // Check which object/group was hit
    if (!s)
        mhGetPickedColor(x, y);

    // Notify python
    callMouseMotion(s, x, y, xrel, yrel);

    // Update screen
    if (s)
        mhQueueUpdate();
}

static void mhQuit()
{
  callQuit();
}

static unsigned char *pickingBuffer = NULL;
static int pickingBufferSize = 0;

void UpdatePickingBuffer(void)
{
    int i;
    // Get the viewport
    GLint viewport[4];
    GLint width;
    GLint height;
    glGetIntegerv(GL_VIEWPORT, viewport);

    width = viewport[2];
    height = viewport[3];

    // Resize the buffer in case the window size has changed
    if (pickingBufferSize != width * height * 3)
    {
        pickingBufferSize = width * height * 3;
        pickingBuffer = (unsigned char*)realloc(pickingBuffer, pickingBufferSize);
        assert(pickingBuffer != NULL);
    }

    // Turn off lighting
    glDisable(GL_LIGHTING);

    // Turn off antialiasing
    glDisable (GL_BLEND);
    glDisable(GL_MULTISAMPLE);

    // Clear screen
    glClearColor(0.0, 0.0, 0.0, 0.0);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    for (i = 0; i < PyList_Size(G.cameras); i++)
    {
        mhCameraPosition((Camera*)PyList_GetItem(G.cameras, i), 0);
        mhDrawMeshes(1, i);
    }

    // Make sure the data is 1 byte aligned
    glPixelStorei(GL_PACK_ALIGNMENT, 1);
    //glFlush();
    //glFinish();
    glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE, pickingBuffer);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    // Turn on antialiasing
    glEnable (GL_BLEND);
    glEnable(GL_MULTISAMPLE);

    /* restore lighting */
    glEnable(GL_LIGHTING);

    /* hdusel: Bugfix for http://code.google.com/p/makehuman/issues/detail?id=16
     * "Red and black window - 'selection rendering'"
     *
     * This error happened for the OS X port only
     *
     * So I enforce a redraw whenever the picking buffer will be updated.
     * But I'm not certain weather we need this for OS X only? */
#ifdef __APPLE__
    mhDraw();
#endif
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
PyObject *Camera_convertToScreen(Camera *camera, PyObject *args)
{
	Object3D *obj = NULL;
    GLint viewport[4];
    GLdouble modelview[16], projection[16];
    double world[3], screen[3];

    if (!PyArg_ParseTuple(args, "ddd|O", world, world + 1, world + 2, &obj))
        return NULL;

    mhCameraPosition(camera, 0);

	if (obj && PyObject_TypeCheck(obj, &Object3DType))
	{    
		glPushMatrix();
		glTranslatef(obj->x, obj->y, obj->z);
		glRotatef(obj->rx, 1, 0, 0);
		glRotatef(obj->ry, 0, 1, 0);
		glRotatef(obj->rz, 0, 0, 1);
		glScalef(obj->sx, obj->sy, obj->sz);
	}

    glGetIntegerv(GL_VIEWPORT, viewport);
    glGetDoublev(GL_PROJECTION_MATRIX, projection);
    glGetDoublev(GL_MODELVIEW_MATRIX, modelview);

    gluProject(world[0], world[1], world[2], modelview, projection, viewport, screen, screen + 1, screen + 2);
    screen[1] = viewport[3] - screen[1];

    return Py_BuildValue("[d,d,d]", screen[0], screen[1], screen[2]);
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
PyObject *Camera_convertToWorld2D(Camera *camera, PyObject *args)
{
    GLint viewport[4];
    GLdouble modelview[16], projection[16];
    GLdouble z;
    double screen[2], world[3];

    if (!PyArg_ParseTuple(args, "dd", screen, screen + 1))
        return NULL;

    mhCameraPosition(camera, 0);

    glGetIntegerv(GL_VIEWPORT, viewport);
    glGetDoublev(GL_PROJECTION_MATRIX, projection);
    glGetDoublev(GL_MODELVIEW_MATRIX, modelview);

    glReadPixels((GLint)screen[0], (GLint)(viewport[3] - screen[1]), 1, 1, GL_DEPTH_COMPONENT, GL_DOUBLE, &z);
    gluUnProject(screen[0], viewport[3] - screen[1], z, modelview, projection, viewport, world, world + 1, world + 2);

    return Py_BuildValue("[d,d,d]", world[0], world[1], world[2]);
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
PyObject *Camera_convertToWorld3D(Camera *camera, PyObject *args)
{
    GLint viewport[4];
    GLdouble modelview[16], projection[16];
    double screen[3], world[3];

    if (!PyArg_ParseTuple(args, "ddd", screen, screen + 1, screen + 2))
        return NULL;

    mhCameraPosition(camera, 0);

    glGetIntegerv(GL_VIEWPORT, viewport);
    glGetDoublev(GL_PROJECTION_MATRIX, projection);
    glGetDoublev(GL_MODELVIEW_MATRIX, modelview);

    gluUnProject(screen[0], viewport[3] - screen[1], screen[2], modelview, projection, viewport, world, world + 1, world + 2);

    return Py_BuildValue("[d,d,d]", world[0], world[1], world[2]);
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
    const float diffuseLight[] = { 1.0f, 1.0f, 1.0f, 1.0f};   /* Diffuse Light Values */
    const float specularLight[] = {1.0f, 1.0f, 1.0f, 1.0f};   /* Specular Light Values */
    const float MatAmb[] = {0.11f, 0.11f, 0.11f, 1.0f};       /* Material - Ambient Values */
    const float MatDif[] = {1.0f, 1.0f, 1.0f, 1.0f};          /* Material - Diffuse Values */
    const float MatSpc[] = {0.2f, 0.2f, 0.2f, 1.0f};          /* Material - Specular Values */
    const float MatShn[] = {10.0f};                           /* Material - Shininess */
    //const float MatEms[] = {0.1f, 0.05f, 0.0f, 1.0f};       /* Material - emission Values */

    glewInit();

    glEnable(GL_DEPTH_TEST);                                  /* Hidden surface removal */
    //glEnable(GL_CULL_FACE);                                   /* Inside face removal */
    //glEnable(GL_ALPHA_TEST);
    //glAlphaFunc(GL_GREATER, 0.0f);
    glDisable(GL_DITHER);
    glEnable(GL_LIGHTING);                                    /* Enable lighting */
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight);
    glLightfv(GL_LIGHT0, GL_SPECULAR, specularLight);
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos);
    glLightModeli(GL_LIGHT_MODEL_COLOR_CONTROL, GL_SEPARATE_SPECULAR_COLOR); // If we enable this, we have stronger specular highlights
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
 *  If stereoMode is one of the two stereo modes, eye will determine which eye is drawn.
 */
void mhCameraPosition(Camera *camera, int eye)
{
    int stereoMode = 0;
    if (eye)
        stereoMode = camera->stereoMode;

    switch (stereoMode)
    {
    case 0: // No stereo
    {
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();

        if (camera->projection)
            gluPerspective(camera->fovAngle, (float)G.windowWidth/G.windowHeight, camera->nearPlane, camera->farPlane);
        else
            glOrtho(0.0, G.windowWidth, G.windowHeight, 0.0, camera->nearPlane, camera->farPlane);

        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        gluLookAt(camera->eyeX, camera->eyeY, camera->eyeZ,       // Eye
                  camera->focusX, camera->focusY, camera->focusZ, // Focus
                  camera->upX, camera->upY, camera->upZ);         // Up
        break;
    }
    case 1: // Toe-in method, uses different eye positions, same focus point and projection
    {
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        gluPerspective(camera->fovAngle, (float)G.windowWidth/G.windowHeight, camera->nearPlane, camera->farPlane);

        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();

        if (eye == 1)
            gluLookAt(camera->eyeX - 0.5 * camera->eyeSeparation, camera->eyeY, camera->eyeZ, // Eye
                      camera->focusX, camera->focusY, camera->focusZ,                             // Focus
                      camera->upX, camera->upY, camera->upZ);                                     // Up
        else if (eye == 2)
            gluLookAt(camera->eyeX + 0.5 * camera->eyeSeparation, camera->eyeY, camera->eyeZ, // Eye
                      camera->focusX, camera->focusY, camera->focusZ,                             // Focus
                      camera->upX, camera->upY, camera->upZ);                                     // Up

        break;
    }
    case 2: // Off-axis method, uses different eye positions, focus points and projections
    {
        double aspectratio = G.windowWidth / (double)G.windowHeight;
        double widthdiv2 = tan(camera->fovAngle * 3.14159/360.0) * camera->nearPlane;
        double left  = - aspectratio * widthdiv2;
        double right = aspectratio * widthdiv2;
        double top = widthdiv2;
        double bottom = -widthdiv2;
        double eyePosition;

        if (eye == 1) // Left
            eyePosition = -0.5 * camera->eyeSeparation;
        else if (eye == 2) // Right
            eyePosition = 0.5 * camera->eyeSeparation;
        else
            eyePosition = 0.0;

        left -= eyePosition * camera->nearPlane / camera->eyeZ;
        right -= eyePosition * camera->nearPlane / camera->eyeZ;

        // Left frustum is moved right, right frustum moved left
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        glFrustum(left, right, bottom, top, camera->nearPlane, camera->farPlane);

        // Left camera is moved left, right camera moved right
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        gluLookAt(camera->eyeX + eyePosition, camera->eyeY, camera->eyeZ,       // Eye
                  camera->focusX + eyePosition, camera->focusY, camera->focusZ, // Focus
                  camera->upX, camera->upY, camera->upZ);                       // Up

        break;
    }
    }
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
                /*Transform the current object*/
                glPushMatrix();
                glTranslatef(obj->x, obj->y, obj->z);
                glRotatef(obj->rx, 1, 0, 0);
                glRotatef(obj->ry, 0, 1, 0);
                glRotatef(obj->rz, 0, 0, 1);
                glScalef(obj->sx, obj->sy, obj->sz);

                if (obj->texture && !pickMode && obj->isSolid)
                {
                    glEnable(GL_TEXTURE_2D);
                    glEnableClientState(GL_TEXTURE_COORD_ARRAY);
                    glBindTexture(GL_TEXTURE_2D, obj->texture);
                    glTexCoordPointer(2, GL_FLOAT, 0, obj->UVs);

                    if (obj->nTransparentPrimitives)
                        Object3D_sortFaces(obj);
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
                }

                /*Disable lighting if the object is shadeless*/
                if (obj->shadeless || pickMode)
                {
                    glDisable(GL_LIGHTING);
                }

                // Enable the shader if the driver supports it and there is a shader assigned
                if (!pickMode && obj->shader && obj->isSolid)
                {
                    if (GLEW_VERSION_2_0)
                    {

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

                                glGetActiveUniform(obj->shader, index, sizeof(name), &length, &size, &type, name);

                                value = PyDict_GetItemString(obj->shaderParameters, name);

                                if (value)
                                {
                                    switch (type)
                                    {
                                    case GL_FLOAT:
                                    {
                                        glUniform1f(index, (float)PyFloat_AsDouble(value));
                                        break;
                                    }
                                    case GL_FLOAT_VEC2:
                                    {
                                        if (!PyList_Check(value) || PyList_Size(value) != 2)
                                            break;
                                        glUniform2f(index, (float)PyFloat_AsDouble(PyList_GetItem(value, 0)), (float)PyFloat_AsDouble(PyList_GetItem(value, 1)));
                                        break;
                                    }
                                    case GL_FLOAT_VEC3:
                                    {
                                        if (!PyList_Check(value) || PyList_Size(value) != 3)
                                            break;
                                        glUniform3f(index, (float)PyFloat_AsDouble(PyList_GetItem(value, 0)), (float)PyFloat_AsDouble(PyList_GetItem(value, 1)),
                                                    (float)PyFloat_AsDouble(PyList_GetItem(value, 2)));
                                        break;
                                    }
                                    case GL_FLOAT_VEC4:
                                    {
                                        if (!PyList_Check(value) || PyList_Size(value) != 4)
                                            break;
                                        glUniform4f(index, (float)PyFloat_AsDouble(PyList_GetItem(value, 0)), (float)PyFloat_AsDouble(PyList_GetItem(value, 1)),
                                                    (float)PyFloat_AsDouble(PyList_GetItem(value, 2)), (float)PyFloat_AsDouble(PyList_GetItem(value, 3)));
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
                    else if (GLEW_ARB_shader_objects)
                    {
                        glUseProgramObjectARB(obj->shader);

                        // This should be optimized, since we only need to do it when it's changed
                        // Validation should also only be done when it is set
                        if (obj->shaderParameters)
                        {
                            GLint parameterCount = 0;
                            int index;
                            int currentTextureSampler = 1;

                            glGetObjectParameterivARB(obj->shader, GL_OBJECT_ACTIVE_UNIFORMS_ARB, &parameterCount);

                            for (index = 0; index < parameterCount; index++)
                            {
                                GLsizei length;
                                GLint size;
                                GLenum type;
                                GLchar name[32];
                                PyObject *value;

                                glGetActiveUniformARB(obj->shader, index, sizeof(name), &length, &size, &type, name);

                                value = PyDict_GetItemString(obj->shaderParameters, name);

                                if (value)
                                {
                                    switch (type)
                                    {
                                    case GL_FLOAT:
                                    {
                                        glUniform1fARB(index, (float)PyFloat_AsDouble(value));
                                        break;
                                    }
                                    case GL_FLOAT_VEC2:
                                    {
                                        if (!PyList_Check(value) || PyList_Size(value) != 2)
                                            break;
                                        glUniform2fARB(index, (float)PyFloat_AsDouble(PyList_GetItem(value, 0)), (float)PyFloat_AsDouble(PyList_GetItem(value, 1)));
                                        break;
                                    }
                                    case GL_FLOAT_VEC3:
                                    {
                                        if (!PyList_Check(value) || PyList_Size(value) != 3)
                                            break;
                                        glUniform3fARB(index, (float)PyFloat_AsDouble(PyList_GetItem(value, 0)), (float)PyFloat_AsDouble(PyList_GetItem(value, 1)),
                                                       (float)PyFloat_AsDouble(PyList_GetItem(value, 2)));
                                        break;
                                    }
                                    case GL_FLOAT_VEC4:
                                    {
                                        if (!PyList_Check(value) || PyList_Size(value) != 4)
                                            break;
                                        glUniform4fARB(index, (float)PyFloat_AsDouble(PyList_GetItem(value, 0)), (float)PyFloat_AsDouble(PyList_GetItem(value, 1)),
                                                       (float)PyFloat_AsDouble(PyList_GetItem(value, 2)), (float)PyFloat_AsDouble(PyList_GetItem(value, 3)));
                                        break;
                                    }
                                    case GL_SAMPLER_1D:
                                    {
                                        glActiveTexture(GL_TEXTURE0 + currentTextureSampler);
                                        glBindTexture(GL_TEXTURE_1D, PyInt_AsLong(value));
                                        glUniform1iARB(index, currentTextureSampler++);
                                        break;
                                    }
                                    case GL_SAMPLER_2D:
                                    {
                                        glActiveTexture(GL_TEXTURE0 + currentTextureSampler);
                                        glBindTexture(GL_TEXTURE_2D, PyInt_AsLong(value));
                                        glUniform1iARB(index, currentTextureSampler++);
                                        break;
                                    }
                                    }
                                }
                            }
                        }
                    }
                }

                /*draw the mesh*/
                if (!obj->isSolid && !pickMode)
                {
                    glDisableClientState(GL_COLOR_ARRAY);
                    glColor3f(0.0f, 0.0f, 0.0f);
                    glPolygonMode(GL_FRONT_AND_BACK , GL_LINE);
                    glDrawElements(g_primitiveMap[obj->vertsPerPrimitive-1], obj->nPrimitives * obj->vertsPerPrimitive, GL_UNSIGNED_INT, obj->primitives);
                    glEnableClientState(GL_COLOR_ARRAY);
                    glPolygonMode(GL_FRONT_AND_BACK , GL_FILL);
                    glEnable(GL_POLYGON_OFFSET_FILL);
                    glPolygonOffset(1.0, 1.0);
                    glDrawElements(g_primitiveMap[obj->vertsPerPrimitive-1], obj->nPrimitives * obj->vertsPerPrimitive, GL_UNSIGNED_INT, obj->primitives);
                    glDisable(GL_POLYGON_OFFSET_FILL);
                }
                else if (obj->nTransparentPrimitives)
                {
                    glDepthMask(GL_FALSE);
                    glEnable(GL_ALPHA_TEST);
                    glAlphaFunc(GL_GREATER, 0.0f);
                    glDrawElements(g_primitiveMap[obj->vertsPerPrimitive-1], obj->nPrimitives * obj->vertsPerPrimitive, GL_UNSIGNED_INT, obj->primitives);
                    glDisable(GL_ALPHA_TEST);
                    glDepthMask(GL_TRUE);
                }
                else
                    glDrawElements(g_primitiveMap[obj->vertsPerPrimitive-1], obj->nPrimitives * obj->vertsPerPrimitive, GL_UNSIGNED_INT, obj->primitives);

                // Disable the shader if the driver supports it and there is a shader assigned
                if (!pickMode && obj->shader && obj->isSolid)
                {
                    if (GLEW_VERSION_2_0)
                        glUseProgram(0);
                    else if (GLEW_ARB_shader_objects)
                        glUseProgramObjectARB(0);
                    glActiveTexture(GL_TEXTURE0);
                }

                /*Enable lighting if the object was shadeless*/
                if (obj->shadeless || pickMode)
                {
                    glEnable(GL_LIGHTING);
                }

                if (obj->texture && !pickMode && obj->isSolid)
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
    int i;
    mhDrawBegin();

    for (i = 0; i < PyList_Size(G.cameras); i++)
    {
        Camera *camera = (Camera*)PyList_GetItem(G.cameras, i);

        // draw the objects in dynamic camera
        if (camera->stereoMode)
        {
            glColorMask(GL_TRUE, GL_FALSE, GL_FALSE, GL_TRUE); // Red
            mhCameraPosition(camera, 1);
            mhDrawMeshes(0, i);
            glClear(GL_DEPTH_BUFFER_BIT);
            glColorMask(GL_FALSE, GL_TRUE, GL_TRUE, GL_TRUE); // Cyan
            mhCameraPosition(camera, 2);
            mhDrawMeshes(0, i);
            // To prevent the GUI from overwritting the red model, we need to render it again in the z-buffer
            glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE); // None, only z-buffer
            mhCameraPosition(camera, 1);
            mhDrawMeshes(0, i);
            glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE); // All
        }
        else
        {
            mhCameraPosition(camera, 0);
            mhDrawMeshes(0, i);
        }
    }

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
    {
        return;
    }

    g_screen = SDL_SetVideoMode(G.windowWidth, G.windowHeight, 24, SDL_OPENGL | (G.fullscreen ? SDL_FULLSCREEN : 0) | SDL_RESIZABLE);
    OnInit();
    mhReshape(G.windowWidth, G.windowHeight);
    callResize(G.windowWidth, G.windowHeight, G.fullscreen);
    mhDraw();
}

void mhSetCaption(const char *caption)
{
    SDL_WM_SetCaption(caption, caption);
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

#if defined(SDL_GL_SWAP_CONTROL) /* SDL_GL_SWAP_CONTROL is deprecated in SDL 1.3! */
    SDL_GL_SetAttribute(SDL_GL_SWAP_CONTROL, 1); // This fixes flickering in compiz
#endif

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

        Py_BEGIN_ALLOW_THREADS
        SDL_WaitEvent(&event);
        Py_END_ALLOW_THREADS

        /* On OS-X SDL continuously posts events even when a native dialog or
         * Window is opened. So if the ActiveWindow (focused Window) is not
         * the main window then cancel the SDL Event.
         */

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
            mhKeyDown(event.key.keysym.sym, event.key.keysym.unicode, event.key.keysym.mod);
            break;
        case SDL_KEYUP:
            if (event.key.keysym.sym == SDLK_F11 || (event.key.keysym.sym == SDLK_RETURN && event.key.keysym.mod & KMOD_ALT))
                mhSetFullscreen(!G.fullscreen); // Switch fullscreen
            else
                mhKeyUp(event.key.keysym.sym, event.key.keysym.unicode, event.key.keysym.mod);
            break;
        case SDL_MOUSEMOTION:
        {
#if defined(WIN32) || defined(__APPLE__)
            mhMouseMotion(event.motion.state, event.motion.x, event.motion.y, event.motion.xrel, event.motion.yrel);
#else
            int x, y;
            SDL_GetMouseState(&x, &y);
            if (x == event.motion.x && y == event.motion.y)
                mhMouseMotion(event.motion.state, event.motion.x, event.motion.y, event.motion.xrel, event.motion.yrel);
#endif
            break;
        }
        case SDL_MOUSEBUTTONDOWN:
            mhMouseButtonDown(event.button.button, event.button.x, event.button.y);
            break;
        case SDL_MOUSEBUTTONUP:
            mhMouseButtonUp(event.button.button, event.button.x, event.button.y);
            break;
        case SDL_USEREVENT:
            switch (event.user.code)
            {
            case 0:
                if (!PyObject_CallFunction((PyObject*)event.user.data1, ""))
                    PyErr_Print();
                break;
            case 1:
                if (!PyObject_CallFunction((PyObject*)event.user.data1, ""))
                    PyErr_Print();
                Py_DECREF((PyObject*)event.user.data1);
                break;
            }
            break;
        case SDL_VIDEORESIZE:
            G.windowWidth = g_windowWidth = event.resize.w;
            G.windowHeight = g_windowHeight = event.resize.h;
            g_screen = SDL_SetVideoMode(G.windowWidth, G.windowHeight, 24, SDL_OPENGL | (G.fullscreen ? SDL_FULLSCREEN : 0) | SDL_RESIZABLE);
            OnInit();

/** hdusel: On some systems a SDL_SetVideoMode causes that the OpenGL context will be reinitialzed.
 * (see http://forums.libsdl.org/viewtopic.php?t=5503&sid=bb2bd59aff7710bbb3dc3ecd5e9b79cf)
 * This leads not only to loose the OpenGL Context which will be resumed by OnInit() but in
 * a lost of all loaded textures also.
 *
 * OS X is concerned of this phenomen :-/ So we'll need to restore all loaded textures after
 * SDL_SetVideoMode() has been called. The Restore of the textures needs some additional effort
 * which is actually done in a texture cache which is relized as a C++ class within the os-x code
 * folder. If any other platform has problems to restore its textures because of an OpenGL context
 * loss caused of SDL_SetVideoMode() we should consider to move this Cache to the common code
 * area.
 *
 * This issue fixes the ticket "Issue 118: Interface is not redrawn when the window is maximized on OSX"
 * (http://code.google.com/p/makehuman/issues/detail?id=118).

 */
#ifdef __APPLE__
            textureCacheRestoreTextures();
#endif

            mhReshape(event.resize.w, event.resize.h);
            callResize(event.resize.w, event.resize.h, G.fullscreen);
            mhDraw();
            break;
        case SDL_VIDEOEXPOSE:
            mhDraw();
            G.pendingUpdate = 0;
            break;
        case SDL_QUIT:
            mhQuit();
            break;
        }
    }

    OnExit();
}
