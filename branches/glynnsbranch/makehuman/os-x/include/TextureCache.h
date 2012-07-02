#ifndef _TextureCache_H_
#define _TextureCache_H_ "61430C8B-26F0-4659-A87F-56B5F09524E3"

/** \file TextureCache.h
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

#include <glew/glew.h>
#include <OpenGL/OpenGL.h>

/* Gain access to this class methods by some C-Calls. We need this because the core modules
 * of MakeHuman are written in C.
 */
#ifdef __cplusplus
extern "C" {
#endif // __cplusplus
    /** \brief Load a texture from a file and bind it into the textures array.
     *
     *  \param inFileName a character string pointer to a string containing a file system path to a
     *         texture file.
     *  \param textureId an int specifying the existing texture id to use or 0 to create a new
     *         texture handle.
     *  \param width A pointer to an int which will be used to store the width of the texture.
     *               This param may be NULL. In this case it will not be used.
     *  \param height A pointer to an int which will be used to store the height of the texture.
     *               This param may be NULL. In this case it will not be used.
     *
     *  This function loads a texture from a texture file and binds it into the OpenGL textures
     *  array.
     *
     *  The loaded texture will be cached and may be recalled by #textureCacheRestoreTextures()
     *
     * \see #textureCacheRestoreTextures()
     * \see #textureCacheLoadSubTexture(const char*, GLuint, int, int)
     */
    GLuint textureCacheLoadTexture(const char* inFileName,
                                   GLuint textureId,
                                   int *width,
                                   int *height);

    /** \brief Load a positioned texture as MipMap from a file and bind it into the textures array.
     *
     *  \param inFileName a character string pointer to a string containing a file system path to a
     *         texture file.
     *  \param textureId an int specifying the existing texture id to use or 0 to create a new
     *         texture handle.
     *  \param x The X-Coordinate to be used to position the texture to.
     *  \param y The Y-Coordinate to be used to position the texture to.
     *
     *  This function loads a texture from a texture file and binds it into the OpenGL textures
     *  array.
     *
     *  The loaded texture will be cached and may be recalled by #textureCacheRestoreTextures()
     *
     * \see #textureCacheRestoreTextures()
     * \see #textureCacheLoadTexture(const char*, GLuint, int*, int*)
     */
    GLuint textureCacheLoadSubTexture(const char * inFileName,
                                      GLuint textureId,
                                      int x,
                                      int y);

    /** Restore all Textures which has been previously loaded by either textureCacheLoadTexture()
     * or textureCacheLoadSubTexture().
     *
     * \see #textureCacheLoadTexture(const char*, GLuint, int*, int*)
     * \see #textureCacheLoadSubTexture(const char*, GLuint, int, int)
     */
    void textureCacheRestoreTextures();
#ifdef __cplusplus
}
#endif // __cplusplus

#ifdef __cplusplus

struct SDL_Surface;

#include <string>
#include <list>
#include <map>

/** This class implements a texture cache which is supposed to tracks the loading of all
 *  textures and stores their corresponding SDL_Surface and the OpenGL Texture Handle for each
 *  particular texture.
 *
 * Beside of tracking the load of textures this cache offers an addition feature that
 * is to restore all OpenGL texture Handles on demand.
 * This comes in business to restore all textures if a SDL_SetVideoMode() call happens because
 * on some systems SDL_SetVideoMode() destroys the OpenGL context which causes that the
 * loaded textures will be lost.
 * (see http://forums.libsdl.org/viewtopic.php?t=5503&sid=bb2bd59aff7710bbb3dc3ecd5e9b79cf)
 *
 * @author Hans-Peter Dusel <hdusel@tangerine-soft.de>
 */
class CTextureCache
{
private:
    struct texture_t
    {
        bool m_IsSubTexture;
        GLuint       m_OpenGLTextureRef;
        SDL_Surface *m_Surface;
        int m_X, m_Y;

        texture_t(GLuint inTextureRef, SDL_Surface* inSurface);
        texture_t(GLuint inTextureRef, SDL_Surface* inSurface, int inX, int inY);
        ~texture_t();
        
        int x() const {return m_X;}
        int y() const {return m_Y;}

        bool bindAndBuildTexture();
        bool isSubTexture() const {return m_IsSubTexture;}

    private: // intentionally not implemented yet
        texture_t            (const texture_t&);
        texture_t& operator= (const texture_t&);
    }; // struct texture_t

    typedef std::map<std::string, texture_t*> TextureMap;
    TextureMap m_Textures;

    CTextureCache();
    ~CTextureCache(){flushAll();}

    bool textureExists(const std::string& inFileName, TextureMap::const_iterator &outMap) const;
    bool textureExists(const std::string& inFileName) const;

    /** Clean the Texture cache by erasing all textures and freeing their allocated 
     *  resources.
     */
    void flushAll();

public:
    static CTextureCache* instance();

    /** \brief Load a texture from a file and bind it into the textures array.
     *  \param fname a character string pointer to a string containing a file system path to a texture file.
     *  \param texture an int specifying the existing texture id to use or 0 to create a new texture.
     *
     *  This function loads a texture from a texture file and binds it into the OpenGL textures array.
     */
    GLuint loadTexture(const std::string& inFileName, GLuint texture, int *width, int *height);
    GLuint loadSubTexture(const std::string& inFileName, GLuint texture, int x, int y);

    void restore();

private:
    texture_t* pushTexture(const std::string& inFileName, GLuint inTextureRef, SDL_Surface* inSurface);
    texture_t* pushTexture(const std::string& inFileName, GLuint inTextureRef, SDL_Surface* inSurface, int inX, int inY);
}; // class CTextureCache
#endif // __cplusplus

#endif /* _TextureCache_H_ */
