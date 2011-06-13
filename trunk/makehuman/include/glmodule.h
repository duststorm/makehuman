/** \file glmodule.h
 *  \brief Header file for glmodule.c.

 <table>
 <tr><td>Project Name:                                   </td>
     <td><b>MakeHuman</b>                                </td></tr>
 <tr><td>Product Home Page:                              </td>
     <td>http://www.makehuman.org/                       </td></tr>
 <tr><td>SourceForge Home Page:                          </td>
     <td>http://sourceforge.net/projects/makehuman/      </td></tr>
 <tr><td>Authors:                                        </td>
     <td>Manuel Bastioni, Paolo Colombo, Simone Re       </td></tr>
 <tr><td>Copyright(c):                                   </td>
     <td>MakeHuman Team 2001-2010                        </td></tr>
 <tr><td>Licensing:                                      </td>
     <td>GPL3 (see also
         http://makehuman.wiki.sourceforge.net/Licensing)</td></tr>
 <tr><td>Coding Standards:                               </td>
     <td>See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards
                                                         </td></tr>
 </table>

 Header file for glmodule.c.

 */


#ifndef GLMODULE_H
#define GLMODULE_H 1

#if defined(__APPLE__)
#	include <glew/glew.h> // OS X uses the glew.framework -> special include ;)
#else
#	include <GL/glew.h>
#endif

#include <SDL.h>
/*#include <SDL_opengl.h>*/


#ifdef __cplusplus
extern "C"
{
#endif

// Text, shader and texture services
    GLuint mhLoadTexture(const char *fname, GLuint texture, int *width, int *height);
    GLuint mhLoadSubTexture(const char *fname, GLuint texture, int x, int y);
    GLuint mhCreateVertexShader(const char *source);
    GLuint mhCreateFragmentShader(const char *source);
    GLuint mhCreateShader(GLuint vertexShader, GLuint fragmentShader);
    int mhGrabScreen(int x, int y, int width, int height, const char *filename);

// Input events
    void mhKeyDown(int key, unsigned short character, int modifiers);
    void mhKeyUp(int key, unsigned short character, int modifiers);
    void mhMouseButtonDown(int b, int x,int y);
    void mhMouseButtonUp(int b, int x,int y);
    void mhMouseMotion(int s, int x, int y, int xrel, int yrel);
    void mhPassiveMotion(int x,int y, int xrel, int yrel);

// Calculations for 3d coordinates and selection
    void mhGetPickedCoords(int x, int y);
    void mhGetPickedColor(int x, int y);

// Window events
    void mhReshape(int w, int h);
    void mhDrawBegin(void);
    void mhDrawEnd(void);

// Callbacks to init/cleanup gl state
    void OnInit(void);
    void OnExit(void);

// Drawing
    void mhDrawMeshes(int pickMode, int cameraType);
    void mhDraw(void);

    void UpdatePickingBuffer(void);

// Event loop
    void mhShutDown(void);
    void mhQueueUpdate(void);
    void mhSetFullscreen(int fullscreen);
    void mhSetCaption(const char *caption);
    void mhCreateWindow(int useTimer);
    void mhEventLoop(void);
    unsigned int mhTimerFunc(unsigned int interval, void* param);
#ifdef __cplusplus
}
#endif

#endif // GLMODULE_H
