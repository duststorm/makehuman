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
     <td>MakeHuman Team 2001-2009                        </td></tr>
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

#include <SDL.h>
#include <SDL_opengl.h>

// Text, shader and texture services
void mhDrawText(float x, float y, const char *message);
GLuint mhLoadTexture(const char *fname, GLuint texture);
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
void mhConvertToScreen(const double world[3], double screen[3], int camera);
void mhConvertToWorld2D(const double screen[2], double world[3], int camera);
void mhConvertToWorld3D(const double screen[3], double world[3], int camera);

// Window events
void mhReshape(int w, int h);
void mhDrawBegin();
void mhDrawEnd();

// Callbacks to init/cleanup gl state
void OnInit();
void OnExit();

// Drawing
void mhSceneCameraPosition();
void mhGUICameraPosition();
void mhDrawMeshes(int pickMode, int cameraType);
void mhDraw();

void UpdatePickingBuffer();

// Event loop
void mhShutDown();
void mhQueueUpdate();
void mhSetFullscreen(int fullscreen);
void mhCreateWindow(int useTimer);
void mhEventLoop();
unsigned int mhTimerFunc(unsigned int interval, void* param);

#endif // GLMODULE_H
