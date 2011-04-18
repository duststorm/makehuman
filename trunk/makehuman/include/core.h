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
     <td>Marc Flerackers                                 </td></tr>
 <tr><td>Copyright(c):                                   </td>
     <td>MakeHuman Team 2001-2010                        </td></tr>
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

#ifdef _DEBUG
#undef _DEBUG
#include <Python.h>
#define _DEBUG
#else
#include <Python.h>
#endif

#ifdef __cplusplus
extern "C"
{
#endif

    void RegisterObject3D(PyObject *module);
    void RegisterCamera(PyObject *module);
    void RegisterTexture(PyObject *module);

    extern PyTypeObject Object3DType;

    /*! \brief 3D object basic structure. */
    /*!        3D object basic structure. */
    typedef struct
    {
        PyObject_HEAD
        int shadeless;              /**< \brief Whether this object is affected by scene lights or not.                     */
        unsigned int texture;       /**< \brief A texture id or 0 if this object doesn't have a texture.                    */
        unsigned int shader;        /**< \brief A shader id or 0 if this object doesn't have a shader.                      */
        PyObject *shaderParameters; /**< \brief A dictionary containing the shader parameters, read only.                   */
        int isVisible;              /**< \brief Whether this object is currently visible or not.                            */
        /**<        An int defining whether this object is currently visible or not.            */
        int inMovableCamera;        /**< \brief Whether this object uses the Movable or Fixed camera mode.                  */
        /**<        An int defining whether this object uses the Movable or Fixed camera mode.  */
        int isPickable;             /**< \brief Whether this object can be picked.                                          */
        /**<        An int defining whether this object can be picked.                          */
        int isSolid;                /**< \brief Whether this object is solid or wireframe.                                  */
        /**<        An int defining whether this object is solid or wireframe.                          */
        float x, y, z;              /**< \brief Tthe object location.                                                       */
        /**<        Array of 3 floats defining the object location (x,y,z).                     */
        float rx, ry, rz;           /**< \brief The object orientation.                                                     */
        /**<        Array of 3 floats defining the object orientation (x, y and z rotations).   */
        float sx, sy, sz;           /**< \brief The object scale.                                                           */
        /**<        Array of 3 floats defining the object size (x, y and z scale).              */
        int nVerts;                 /**< \brief The number of vertices in this object.                                      */
        /**<        An int holding the number of vertices in this object.                       */
        int nQuads;                 /**< \brief The number of faces in this object.                                         */
        /**<        An int holding the number of faces in this object.
                    MakeHuman only supports quadrilateral faces.                                */
        int nTransparentQuads;      /**< \brief The number of transparent faces in this object.                             */
        /**<        An int holding the number of transparent faces in this object.
                    MakeHuman only supports quadrilateral faces.                                */
        int nNorms;                 /**< \brief The number of surface normals in this object.                               */
        /**<        An int holding the number of surface normals defined for this object.       */
        int nColors;                /**< \brief The number of colors used in this object.                                   */
        /**<        An int holding the number of colors used in this object.                    */
        int nColors2;               /**< \brief The number of colors used in this object.                                   */
        /**<        An int holding the number of colors used in this object.
                <b>EDITORIAL NOTE: One of these may be for 'false' colors. Find out which.</b>  */
        int *quads;                 /**< \brief The indices of faces in this object.                                        */
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

    } Object3D;

// Object3D Methods
    PyObject *Object3D_setVertCoo(Object3D *self, PyObject *args);
    PyObject *Object3D_setNormCoo(Object3D *self, PyObject *args);
    PyObject *Object3D_setUVCoo(Object3D *self, PyObject *args);
    PyObject *Object3D_setColorIDComponent(Object3D *self, PyObject *args);
    PyObject *Object3D_setColorComponent(Object3D *self, PyObject *args);
    PyObject *Object3D_getTranslation(Object3D *self, void *closure);
    int Object3D_setTranslation(Object3D *self, PyObject *value);
    PyObject *Object3D_getRotation(Object3D *self, void *closure);
    int Object3D_setRotation(Object3D *self, PyObject *value);
    PyObject *Object3D_getScale(Object3D *self, void *closure);
    int Object3D_setScale(Object3D *self, PyObject *value);
    PyObject *Object3D_getTransparentQuads(Object3D *self, void *closure);
    int Object3D_setTransparentQuads(Object3D *self, PyObject *value);

// Object3D attributes indirectly accessed by Python
    PyObject *Object3D_getShaderParameters(Object3D *self, void *closure);
    PyObject *Object3D_getText(Object3D *self, void *closure);
    int Object3D_setText(Object3D *self, PyObject *value, void *closure);

// Object3D object methods
    void Object3D_dealloc(Object3D *self);
    PyObject *Object3D_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
    int Object3D_init(Object3D *self, PyObject *args, PyObject *kwds);

    typedef struct
    {
      PyObject_HEAD

        float fovAngle;
      float nearPlane;
      float farPlane;

      int projection;

      int stereoMode;
      float eyeSeparation;

      float eyeX;
      float eyeY;
      float eyeZ;
      float focusX;
      float focusY;
      float focusZ;
      float upX;
      float upY;
      float upZ;
    } Camera;

    typedef struct
    {
        int indices[4];
        float distance;
    } SortStruct;

    /** \brief A struct consolidating all global variables.
               A global struct - all globals must be here.
     */
    typedef struct
    {
        PyObject *world;
        PyObject *cameras;

        int windowHeight;              /**< \brief The current window height in pixels.                                        */
        /**<        An int holding the current window height in pixels.                         */
        int windowWidth;               /**< \brief The current window width in pixels.                                         */
        /**<        An int holding the current window width in pixels.                          */
        unsigned char color_picked[3]; /**< \brief The 'color' of the currently selected object.                               */
        /**<        An array of three characters holding the Red, Green and Blue color
                    components (each with a value from 0 to 255) of the color of the currently
                    selected object.
                    This is a 'false' color used as part of the technique for identifying
                    objects selected with the mouse.                                            */
        /**<        An array of ints holding the list of textures.                              */
        unsigned int millisecTimer; /*millisecond delay for SDL_AddTimer*/

        int pendingUpdate; /*1 if an update is already pending*/
        int pendingTimer; /*1 if a timer is already pending*/
        int loop; /*1 if we haven't quit yet*/
        int fullscreen; /*1 for fullscreen, 0 for windowed*/
        float clearColor[4]; /*color for background clear*/

        PyObject *timerCallback;
        PyObject *resizeCallback;
        PyObject *mouseDownCallback;
        PyObject *mouseUpCallback;
        PyObject *mouseMovedCallback;
        PyObject *keyDownCallback;
        PyObject *keyUpCallback;

        SortStruct *sortData;
        int nSortData;
    } Global;
    extern Global G;

// Python callbacks
    void callMouseButtonDown(int b, int x, int y);
    void callMouseButtonUp(int b, int x, int y);
    void callMouseMotion(int s, int x, int y, int xrel, int yrel);
    void callTimerFunct(void);
    void callStartFunct(void);
    void callKeyDown(int key, unsigned short character, int modifiers);
    void callKeyUp(int key, unsigned short character, int modifiers);
    void callResize(int w, int h, int fullscreen);

// Scene methods
    void setClearColor(float r, float g, float b, float a);

// Helper functions
    void Object3D_sortFaces(Object3D *self);
    float *makeFloatArray(int n);
    unsigned char *makeUCharArray(int n);
    int *makeIntArray(int n);

#ifdef __cplusplus
}
#endif

#endif // CORE_H
