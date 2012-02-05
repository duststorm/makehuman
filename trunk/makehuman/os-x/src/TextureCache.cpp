/** \file TextureCache.cpp
 \brief This module provides methods to cache and recall textures which may be
 handy to restore OpenGL Textures on a Context loss.
 
 <table>
 <tr><td>Project Name:                                   </td>
 <td><b>MakeHuman</b>                                </td></tr>
 <tr><td>Product Home Page:                              </td>
 <td>http://www.makehuman.org/                       </td></tr>
 <tr><td>SourceForge Home Page:                          </td>
 <td>http://sourceforge.net/projects/makehuman/      </td></tr>
 <tr><td>Authors:                                        </td>
 <td>Hans-Peter Dusel</td></tr>
 <tr><td>Copyright(c):                                   </td>
 <td>MakeHuman Team 2001-2011                        </td></tr>
 <tr><td>Licensing:                                      </td>
 <td>GPL3 (see also
 http://makehuman.wiki.sourceforge.net/Licensing)</td></tr>
 <tr><td>Coding Standards:                               </td>
 <td>See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards
 </td></tr>
 </table>
 
 This module implements a texture cache in C++ which is supposed to tracks the loading of all
 textures and stores their corresponding SDL_Surface and the OpenGL Texture handle for each
 particular texture.
 
 The C++ class is implemented as a singleton pattern because every process has a sole
 texture cache.
 
 Beside of tracking the load of textures this cache offers an addition feature that
 is to restore all OpenGL texture Handles on demand.
 This comes in business to restore all textures if a SDL_SetVideoMode() call happens because
 on some systems SDL_SetVideoMode() destroys the OpenGL context which causes that the
 loaded textures will be lost.
 
 (see http://forums.libsdl.org/viewtopic.php?t=5503&sid=bb2bd59aff7710bbb3dc3ecd5e9b79cf)
 
 */

#include "TextureCache.h"

#include <string>
#include <list>
#include <map>
#include <SDL/SDL.h>
#include <SDL_image/SDL_image.h>
#include <Python/Python.h>

void textureCacheRestoreTextures()
{
    CTextureCache::instance()->restore();
}

GLuint textureCacheLoadTexture(const char* inFileName, GLuint textureId, int *width, int *height)
{
    assert(inFileName);
    return CTextureCache::instance()->loadTexture(inFileName, textureId, width, height);
}

GLuint textureCacheLoadSubTexture(const char * inFileName, GLuint textureId, int x, int y)
{
    assert(inFileName);
    return CTextureCache::instance()->loadSubTexture(inFileName, textureId, x, y);
}

static bool getTextureFormatOfSurface(const SDL_Surface* inSurface, int& outInternalFormat, int& outFormat)
{
    switch (inSurface->format->BytesPerPixel)
    {
        case 1:
            outInternalFormat = GL_ALPHA8;
            outFormat = GL_ALPHA;
            break;
        case 3:
            outInternalFormat = 3;
            if (inSurface->format->Rshift) // If there is a shift on the red value, we need to tell that red and blue are switched
                outFormat = GL_BGR;
            else
                outFormat = GL_RGB;
            break;
        case 4:
            outInternalFormat = 4;
            if (inSurface->format->Rshift) // If there is a shift on the red value, we need to tell that red and blue are switched
                outFormat = GL_BGRA;
            else
                outFormat = GL_RGBA;
            break;
        default:
            return false; // failure
    }
    return true; // success!
}

static bool isTextureFormatOfSurfaceValid(const SDL_Surface* inSurface)
{
    int internalFormat, format;
    return getTextureFormatOfSurface(inSurface, internalFormat, format);
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
    size_t i;
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
static void flipSurface(SDL_Surface *surface)
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

static SDL_Surface *loadImage(const char *fname)
{
    assert(fname);
    SDL_Surface *surface;

    surface = (SDL_Surface*)IMG_Load(fname);

    if (!surface)
    {
        PyErr_Format(PyExc_RuntimeError, "Could not load %s, %s", fname, SDL_GetError());
        return 0;
    }

    return surface;
}

// =====================================================================================
#pragma mark -
#pragma mark CTextureCache::texture_t - public
// =====================================================================================

CTextureCache::texture_t::texture_t(GLuint inTextureRef, SDL_Surface* inSurface)
: m_IsSubTexture(false)
, m_OpenGLTextureRef(inTextureRef)
, m_Surface(inSurface)
, m_X(0), m_Y(0)
{}

CTextureCache::texture_t::texture_t(GLuint inTextureRef, SDL_Surface* inSurface, int inX, int inY)
: m_IsSubTexture(true)
, m_OpenGLTextureRef(inTextureRef)
, m_Surface(inSurface)
, m_X(inX), m_Y(inY)
{}

CTextureCache::texture_t::~texture_t()
{
    SDL_FreeSurface(m_Surface);
    glDeleteTextures(1, &m_OpenGLTextureRef);
}

bool CTextureCache::texture_t::bindAndBuildTexture()
{
    int internalFormat, format;
    bool rc = getTextureFormatOfSurface(m_Surface, internalFormat, format);
    assert(true == rc);

    if (isSubTexture())
    {
        if (m_Surface->h == 1)
        {
            glBindTexture(GL_TEXTURE_1D, m_OpenGLTextureRef);
            glTexSubImage1D(GL_TEXTURE_1D, 0, x(), m_Surface->w, format, GL_UNSIGNED_BYTE, m_Surface->pixels);
        }
        else
        {
            glBindTexture(GL_TEXTURE_2D, m_OpenGLTextureRef);
            glTexSubImage2D(GL_TEXTURE_2D, 0, x(), y(), m_Surface->w, m_Surface->h, format, GL_UNSIGNED_BYTE, m_Surface->pixels);
        }
    }
    else
    {
        if (m_Surface->h == 1)
        {
            glBindTexture(GL_TEXTURE_1D, m_OpenGLTextureRef);
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE_EXT);
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE_EXT);
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
            gluBuild1DMipmaps(GL_TEXTURE_1D, internalFormat, m_Surface->w, format, GL_UNSIGNED_BYTE, m_Surface->pixels);
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
        }
        else
        {
            glBindTexture(GL_TEXTURE_2D, m_OpenGLTextureRef);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE_EXT);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE_EXT);

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

            gluBuild2DMipmaps(GL_TEXTURE_2D, internalFormat, m_Surface->w, m_Surface->h, format, GL_UNSIGNED_BYTE, m_Surface->pixels);
                //glTexImage2D(GL_TEXTURE_2D, 0, internalFormat, surface->w, surface->h, 0, format, GL_UNSIGNED_BYTE, surface->pixels);
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
        }
    }
    return true; // success!
}


// =====================================================================================
#pragma mark -
#pragma mark CTextureCache - public
// =====================================================================================
CTextureCache::CTextureCache()
: m_Textures()
{}

// static
CTextureCache* CTextureCache::instance()
{
    static CTextureCache* s_Singleton = NULL;

    if (NULL == s_Singleton)
    {
        s_Singleton = new CTextureCache();
    }
    return s_Singleton;
}

void CTextureCache::flushAll()
{
    TextureMap::iterator mapIt;
    for (mapIt = m_Textures.begin(); mapIt != m_Textures.end(); ++mapIt)
    {
        texture_t* texture(mapIt->second);
        delete texture;
    }
    m_Textures.clear(); // Clear the list finally.
}

bool CTextureCache::textureExists(const std::string& inFileName, TextureMap::const_iterator &outMap) const
{
    outMap = m_Textures.find(inFileName);
    return outMap != m_Textures.end();
}

bool CTextureCache::textureExists(const std::string& inFileName) const
{
    const TextureMap::const_iterator textMapIt = m_Textures.find(inFileName);
    return textMapIt != m_Textures.end();
}

void CTextureCache::restore()
{
    TextureMap::iterator mapIt;
    for (mapIt = m_Textures.begin(); mapIt != m_Textures.end(); ++mapIt)
    {
        texture_t* texture(mapIt->second);
        texture->bindAndBuildTexture();
    }
}

/** \brief Load a texture from a file and bind it into the textures array.
 *  \param fname a character string pointer to a string containing a file system path to a texture file.
 *  \param texture an int specifying the existing texture id to use or 0 to create a new texture.
 *
 *  This function loads a texture from a texture file and binds it into the OpenGL textures array.
 */
GLuint CTextureCache::loadTexture(const std::string& inFileName, GLuint texture, int *width, int *height)
{
    SDL_Surface * surface = loadImage(inFileName.c_str());

    if (!surface)
    {
        return 0;
    }

    if ( !isTextureFormatOfSurfaceValid(surface) )
    {
        SDL_FreeSurface(surface);
        return 0;
    }

    if ( 0 == texture )
    {
        glGenTextures(1, &texture);
    }

    // Flip the surface 'cos OpenGL has its origin in the left bottom corner while images
    // are starting with 0,0 at the top left corner.
    flipSurface(surface);
    texture_t* newTexture = pushTexture(inFileName, texture, surface);

    if (newTexture->bindAndBuildTexture() == false)
    {
        ::SDL_FreeSurface(surface);
        return 0;
    }

    if (width)
        *width = surface->w;
    if (height)
        *height = surface->h;

//    SDL_FreeSurface(surface);

    return texture;
}

GLuint CTextureCache::loadSubTexture(const std::string& inFileName, GLuint texture, int x, int y)
{
    SDL_Surface *surface;

    if (!texture)
    {
        PyErr_Format(PyExc_RuntimeError, "Texture is empty, cannot load a sub texture into it");
        return 0;
    }

    surface = loadImage(inFileName.c_str());

    if (!surface)
        return 0;

    // Flip the surface 'cos OpenGL has its origin in the left bottom corner while images
    // are starting with 0,0 at the top left corner.
    flipSurface(surface);
    texture_t* newTexture = pushTexture(inFileName, texture, surface, x, y);

    newTexture->bindAndBuildTexture();

    return texture;
}

// =====================================================================================
#pragma mark -
#pragma mark CTextureCache - private
// =====================================================================================
CTextureCache::texture_t* CTextureCache::pushTexture(const std::string& inFileName, GLuint inTextureRef, SDL_Surface* inSurface)
{
    if (textureExists(inFileName))
    {
        printf("CTextureCache: Warning : Texture '%s' already loaded!\n", inFileName.c_str());
    }

    texture_t *newTexture = new texture_t(inTextureRef, inSurface);
    m_Textures[inFileName] = newTexture;
    return newTexture;
}

CTextureCache::texture_t* CTextureCache::pushTexture(const std::string& inFileName, GLuint inTextureRef, SDL_Surface* inSurface, int inX, int inY)
{
    if (textureExists(inFileName))
    {
        printf("CTextureCache: Warning : Texture '%s' already loaded!\n", inFileName.c_str());
    }

    texture_t *newTexture = new texture_t(inTextureRef, inSurface, inX, inY);
    m_Textures[inFileName] = newTexture;
    return newTexture;
}
