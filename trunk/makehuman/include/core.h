/** \file core.h
 *  \brief Header file for core.c.

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

 Header file for core.c.

 */


#ifndef CORE_H
#define CORE_H 1
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*! \brief 3D object basic structure. */
/*!        3D object basic structure. */
struct object3D
{
    int shadeless;              /**< \brief Whether this object is affected by scene lights or not.                                     */
    unsigned int texture;       /**< \brief a texture id or 0 if this object doesn't have a texture.                                    */
    int isVisible;              /**< \brief Whether this object is currently visible or not.                            */
    /**<        An int defining whether this object is currently visible or not.            */
    int inMovableCamera;        /**< \brief Whether this object uses the Movable or Fixed camera mode.                  */
    /**<        An int defining whether this object uses the Movable or Fixed camera mode.  */
    float location[3];          /**< \brief Tthe object location.                                                       */
    /**<        Array of 3 floats defining the object location (x,y,z).                     */
    float rotation[3];          /**< \brief The object orientation.                                                     */
    /**<        Array of 3 floats defining the object orientation (x, y and z rotations).   */
    float scale[3];             /**< \brief The object scale.                                                           */
    /**<        Array of 3 floats defining the object size (x, y and z scale).              */
    int nVerts;                 /**< \brief The number of vertices in this object.                                      */
    /**<        An int holding the number of vertices in this object.                       */
    int nTrigs;                 /**< \brief The number of faces in this object.                                         */
    /**<        An int holding the number of triangular faces in this object.
                MakeHuman only supports triangular faces.                                   */
    int nNorms;                 /**< \brief The number of surface normals in this object.                               */
    /**<        An int holding the number of surface normals defined for this object.       */
    int nColors;                /**< \brief The number of colors used in this object.                                   */
    /**<        An int holding the number of colors used in this object.                    */
    int nColors2;               /**< \brief The number of colors used in this object.                                   */
    /**<        An int holding the number of colors used in this object.
                <b>EDITORIAL NOTE: One of these may be for 'false' colors. Find out which.</b>  */
    int *trigs;                 /**< \brief The indices of faces in this object.                                        */
    /**<        Three ints for each triangular face in this object.                         */
    float *verts;               /**< \brief Pointer to the start of the list of vertex coordinates.                     */
    /**<        A pointer to an array of floats containing the list of vertex coordinates
                for each of the vertices defined for this object.
                The x, y and z coordinates for a single vertex are stored sequentially in
                this list.                                                                  */
    float *norms;               /**< \brief Pointer to the start of the list of surface normals.                        */
    /**<        A pointer to an array of floats containing the list of surface normals
                defined for this object.
                The x, y and z components for a single normal are stored sequentially in
                this list.                                                                  */
    float *UVs;                 /**< \brief Pointer to the start of the list of UV vectors.                             */
    /**<        A pointer to an array of floats containing the list of UV vectors used for
                texture mapping onto this object.
                The U and V components for a single vector are stored sequentially in
                this list.                                                                  */
    unsigned char *colors;      /**< \brief Pointer to the start of the list of color components.                       */
    /**<        A pointer to an array of chars containing the list of color components
                defined for this object. Each color component takes a single byte and can
                have a value of 0-255.
                The Red, Green and Blue components of a single color are
                stored sequentially in this list.                                           */
    unsigned char *colors2;     /**< \brief Pointer to the start of the list of color components.                       */
    /**<        A pointer to an array of chars containing the list of color components
                defined for this object. Each color component takes a single byte and can
                have a value of 0-255.
                The Red, Green, Blue and Alpha Channel components of a single color are
                stored sequentially in this list.                                           */
    char *textString;           /**< \brief Pointer to the start of a text string.                                      */
    /**<        A pointer to a string of chars.                                             */
};

typedef struct object3D OBJ3D;
typedef struct object3D * OBJARRAY;

/** \brief A struct consolidating all global variables.
           A global struct - all globals must be here.
 */
typedef struct
{
    OBJARRAY world;                /**< \brief A pointer to the list of objects.                                           */
    /**<        A pointer to an array of object3D objects that contains the list of
                currently defined objects.                                                  */
    int nObjs;                     /**< \brief The total number of objects.                                                */
    /**<        An int holding the number of objects currently defined.                     */
    float fovAngle;                /**< \brief The current Field Of View angle.                                            */
    /**<        A float holding the current Field of View of the camera.                    */
    float zoom;                    /**< \brief The current camera Zoom setting.                                            */
    /**<        A float holding the current camera Zoom setting.                            */
    float rotX;                    /**< \brief The current camera rotation around the x-axis (the tilt).                   */
    /**<        A float holding the current camera x-rotation setting.                      */
    float rotY;                    /**< \brief The current camera rotation around the y-axis (left/right).                 */
    /**<        A float holding the current camera y-rotation setting.                      */
    float translX;                 /**< \brief The current camera x-translation (pan left/right).                          */
    /**<        A float holding the current camera x-translation setting.                   */
    float translY;                 /**< \brief The current camera y-translation (pan up/down).                             */
    /**<        A float holding the current camera y-translation setting.                   */
    int windowHeight;              /**< \brief The current window height in pixels.                                        */
    /**<        An int holding the current window height in pixels.                         */
    int windowWidth;               /**< \brief The current window width in pixels.                                         */
    /**<        An int holding the current window width in pixels.                          */
    int modifiersKeyState;         /**< \brief The current modifier key state (e.g. shift, ctrl, alt etc.).                */
    /**<        An int holding the current modifier key state (e.g. shift, ctrl, alt etc.). */
    unsigned char color_picked[3]; /**< \brief The 'color' of the currently selected object.                               */
    /**<        An array of three characters holding the Red, Green and Blue color
                components (each with a value from 0 to 255) of the color of the currently
                selected object.
                This is a 'false' color used as part of the technique for identifying
                objects selected with the mouse.                                            */
    /**<        An array of ints holding the list of textures.                              */
    double mouse3DX;/*mouse 3D scene coords*/
    double mouse3DY;/*mouse 3D scene coords*/
    double mouse3DZ;/*mouse 3D scene coords*/
    double mouseGUIX;/*mouse 3D GUI coords*/
    double mouseGUIY;/*mouse 3D GUI coords*/
    double mouseGUIZ;/*mouse 3D GUI coords*/
    unsigned int millisecTimer; /*millisecond delay for SDL_AddTimer*/

    int fontOffset; /*first index of the font display list*/
    int pendingUpdate; /*1 if an update is already pending*/
    int pendingTimer; /*1 if a timer is already pending*/
    int loop; /*1 if we haven't quit yet*/
    int fullscreen; /*1 for fullscreen, 0 for windowed*/
} Global;
extern Global G;

// Python callbacks
void callMouseButtonDown(int b, int x, int y);
void callMouseButtonUp(int b, int x, int y);
void callMouseMotion(int s, int x, int y, int xrel, int yrel);
void callTimerFunct();
void callKeyDown(int key, unsigned short character);

// Scene methods
void initscene(int n);
void addObject(int objIndex, float locX, float locY,float locZ,
               int numVerts, int numTrigs);

// Object methods
int setVertCoo(int objIndex, int vIdx, float x, float y, float z);
int setNormCoo(int objIndex, int nIdx, float x, float y, float z);
int setUVCoo(int objIndex, int nIdx, float u, float v);
int setObjTexture(int objIndex, unsigned int texture);
int setShadeless(int objIndex, int value);
int setColorIDComponent(int objIndex, int nIdx, unsigned char r, unsigned char g, unsigned char b);
int setColorComponent(int objIndex, int nIdx, unsigned char r, unsigned char g, unsigned char b, unsigned char a);
int setVisibility (int objIndex, int visibility);
int setText(int objIndex, const char *objText);
int setCamMode(int objIndex, int camMode);
int setObjLoc(int objIndex, float locX, float locY, float locZ);
int setObjRot(int objIndex, float rotX, float rotY, float rotZ);
int setObjScale(int objIndex, float sizeX, float sizeY, float sizeZ);

// Helper functions
float *makeFloatArray(int n);
unsigned char *makeUCharArray(int n);
int *makeIntArray(int n);
OBJARRAY objVector(int n);

#endif // CORE_H
