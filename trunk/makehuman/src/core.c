/** \file core.c
 *  \brief Integration layer between the C core and Python functions.

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

 This module contains functions that pass events up from the SDL core to
 Python and functions that process calls from Python back to C.
 There are also a small number of utility functions for allocating memory for
 lists of Integers, Strings, Floats and Objects.

 */


#include "core.h"
#include "SDL_thread.h"
#ifdef _DEBUG
  #undef _DEBUG
  #include <Python.h>
  #define _DEBUG
#else
  #include <Python.h>
#endif

/** \brief Invokes the Python timer function.
 *
 *  This function invokes the Python idleFunc function when the SDL
 *  module detects idle time between mouse and keyboard events.
 */
void callTimerFunct()
{
    PyObject *main_module = PyImport_AddModule("__main__");
    PyObject *global_dict = PyModule_GetDict(main_module);
    PyObject *mainScene = PyDict_GetItemString(global_dict, "mainScene");
    PyObject *v;
    if (!(v = PyObject_CallMethod(mainScene, "timerFunc", "")))
        PyErr_Print();
    else
        Py_DECREF(v);
}

/** \brief Invokes the Python mouseButtonDown function.
 *  \param b an int indicating which button this event relates to.
 *  \param x an int specifying the horizontal mouse pointer position in the GUI window (in pixels).
 *  \param y an int specifying the vertical mouse pointer position in the GUI window (in pixels).
 *
 *  This function invokes the Python mouseButtonDown function when the SDL
 *  module detects a mouse button down event.
 */
void callMouseButtonDown(int b, int x, int y)
{
    PyObject *main_module = PyImport_AddModule("__main__");
    PyObject *global_dict = PyModule_GetDict(main_module);
    PyObject *mainScene = PyDict_GetItemString(global_dict, "mainScene");
    PyObject *v;
    if (!(v = PyObject_CallMethod(mainScene, "mouseButtonDown", "iii", b, x, y)))
        PyErr_Print();
    else
        Py_DECREF(v);
}

/** \brief Invokes the Python mouseButtonUp function.
 *  \param b an int indicating which button this event relates to.
 *  \param x an int specifying the horizontal mouse pointer position in the GUI window (in pixels).
 *  \param y an int specifying the vertical mouse pointer position in the GUI window (in pixels).
 *
 *  This function invokes the Python mouseButtonUp function when the SDL
 *  module detects a mouse button up event.
 */
void callMouseButtonUp(int b, int x, int y)
{
    PyObject *main_module = PyImport_AddModule("__main__");
    PyObject *global_dict = PyModule_GetDict(main_module);
    PyObject *mainScene = PyDict_GetItemString(global_dict, "mainScene");
    PyObject *v;
    if (!(v = PyObject_CallMethod(mainScene, "mouseButtonUp", "iii", b, x, y)))
        PyErr_Print();
    else
        Py_DECREF(v);
}

/** \brief Invokes the Python mouseMotion function.
 *  \param s an int indicating the mouse.motion.state of the event (1=Mouse moved, 0=Mouse click)..
 *  \param x an int specifying the horizontal mouse pointer position in the GUI window (in pixels).
 *  \param y an int specifying the vertical mouse pointer position in the GUI window (in pixels).
 *  \param xrel an int specifying the difference between the previously recorded horizontal mouse 
 *         pointer position in the GUI window and the current position (in pixels).
 *  \param yrel an int specifying the difference between the previously recorded vertical mouse 
 *         pointer position in the GUI window and the current position (in pixels).
 *
 *  This function invokes the Python mouseMotion function when the SDL
 *  module detects movement of the mouse.
 */
void callMouseMotion(int s, int x, int y, int xrel, int yrel)
{
    PyObject *main_module = PyImport_AddModule("__main__");
    PyObject *global_dict = PyModule_GetDict(main_module);
    PyObject *mainScene = PyDict_GetItemString(global_dict, "mainScene");
    PyObject *v;
    if (!(v = PyObject_CallMethod(mainScene, "mouseMotion", "iiiii", s, x, y, xrel, yrel)))
        PyErr_Print();
    else
        Py_DECREF(v);
}

/** \brief Invokes the Python keyDown function.
 *  \param key an int containing the key code of the key pressed.
 *  \param character an unsigned short character containing the Unicode character corresponding to the key pressed.
 *
 *  This function invokes the Python keyDown function when the SDL
 *  module detects a standard keyboard event, ie. when a standard character key is pressed.
 */
void callKeyDown(int key, unsigned short character, int modifiers)
{
    PyObject *main_module = PyImport_AddModule("__main__");
    PyObject *global_dict = PyModule_GetDict(main_module);
    PyObject *mainScene = PyDict_GetItemString(global_dict, "mainScene");
    PyObject *v;
#ifdef __WIN32__
    if (!(v = PyObject_CallMethod(mainScene, "keyDown", "iu#i", key, &character, 1, modifiers)))
#else
    if (!(v = PyObject_CallMethod(mainScene, "keyDown", "ici", key, key, modifiers)))
#endif
        PyErr_Print();
    else
        Py_DECREF(v);
}

void callKeyUp(int key, unsigned short character, int modifiers)
{
    PyObject *main_module = PyImport_AddModule("__main__");
    PyObject *global_dict = PyModule_GetDict(main_module);
    PyObject *mainScene = PyDict_GetItemString(global_dict, "mainScene");
    PyObject *v;
#ifdef __WIN32__
    if (!(v = PyObject_CallMethod(mainScene, "keyUp", "iu#i", key, &character, 1, modifiers)))
#else
    if (!(v = PyObject_CallMethod(mainScene, "keyUp", "ici", key, key, modifiers)))
#endif
        PyErr_Print();
    else
        Py_DECREF(v);
}

void callReloadTextures()
{
    PyObject *main_module = PyImport_AddModule("__main__");
    PyObject *global_dict = PyModule_GetDict(main_module);
    PyObject *mainScene = PyDict_GetItemString(global_dict, "mainScene");
    PyObject *v;
    if (!(v = PyObject_CallMethod(mainScene, "reloadTextures", "")))
        PyErr_Print();
    else
        Py_DECREF(v);
}

/** \brief Re-initialise the scene contained in G.world.
 *  \param n an int specifying the number of objects in the list of objects that will replace the objects currently in G.world.
 *
 *  This function frees up the memory currently being used to hold G.world.
 *  It then reinitializes G.world to make it ready to take the new list of objects.
 *
 */
void initscene(int n)
{
    if (G.world != NULL)
    {
        int k;
        for (k = 0; k < G.nObjs; k++)
        {
            free(G.world[k].trigs);
            free(G.world[k].verts);
            free(G.world[k].norms);
            free(G.world[k].UVs);
            free(G.world[k].colors);
            free(G.world[k].colors2);
            free(G.world[k].textString);
        }
        free(G.world);

    }
    G.nObjs = n;
    G.world = objVector(G.nObjs);
}

/** \brief Adds a 3D object into G.world.
 *  \param objIndex an int containing the index of the 3D object (used to index the G.world array).
 *  \param locX a float specifying the x coordinate of the object.
 *  \param locY a float specifying the y coordinate of the object.
 *  \param locZ a float specifying the z coordinate of the object.
 *  \param numVerts an int specifying the number of vertices in the object.
 *  \param numTrigs an int specifying the number of triangular faces in the object.
 *
 *  This function adds a 3D object into the G.world array.
 */
void addObject(int objIndex, float locX, float locY,float locZ,
               int numVerts, int numTrigs)
{
    if (objIndex < G.nObjs)
    {
        G.world[objIndex].verts = makeFloatArray(numVerts*3);
        G.world[objIndex].norms = makeFloatArray(numVerts*3);
        G.world[objIndex].colors = makeUCharArray(numVerts*3);
        G.world[objIndex].colors2 = makeUCharArray(numVerts*4);
        G.world[objIndex].UVs = makeFloatArray(numVerts*2);

        G.world[objIndex].nVerts = numVerts;

        G.world[objIndex].trigs = makeIntArray(numTrigs * 3);
        G.world[objIndex].nNorms = numVerts*3;
        G.world[objIndex].nTrigs = numTrigs;
        G.world[objIndex].nColors = numVerts*3;
        G.world[objIndex].nColors2 = numVerts*4;
        G.world[objIndex].location[0] = locX;
        G.world[objIndex].location[1] = locY;
        G.world[objIndex].location[2] = locZ;
        G.world[objIndex].isVisible = 1;
        G.world[objIndex].isPickable = 1;
        G.world[objIndex].rotation[0] = 0.0;
        G.world[objIndex].rotation[1] = 0.0;
        G.world[objIndex].rotation[2] = 0.0;
        G.world[objIndex].scale[0] = 1.0;
        G.world[objIndex].scale[1] = 1.0;
        G.world[objIndex].scale[2] = 1.0;
        G.world[objIndex].inMovableCamera = 1;
        G.world[objIndex].textString = NULL;
        G.world[objIndex].texture = 0;
        G.world[objIndex].shadeless = 0;

    }
}

void setClearColor(float r, float g, float b, float a)
{
  G.clearColor[0] = r;
  G.clearColor[1] = g;
  G.clearColor[2] = b;
  G.clearColor[3] = a;
}

/** \brief Sets a single coordinate value (x, y or z) for a vertex in G.world.
 *  \param objIndex an int containing the index of the 3D object that contains this vertex.
 *  \param vIdx an int indexing the vertex coordinate component to update.
 *  \param x a float specifying the X component of the value to be assigned to this vertex coordinate
 *           in the G.world array.
 *  \param y a float specifying the Y component of the value to be assigned to this vertex coordinate
 *           in the G.world array.
 *  \param z a float specifying the Z component of the value to be assigned to this vertex coordinate
 *           in the G.world array.
 *
 *  This function sets the value of a G.world coordinate component (x, y or z).
 *  This function is called indirectly by the setVertCoord Python wrapper.
 *  The Python wrapper specifies a list of the three coordinates, but this list is split up into 3
 *  separate calls to this function by the mh_setVertCoord function in main.c.
 */
int setVertCoo(int objIndex, int vIdx, float x, float y, float z)
{
    if (!G.world)
        return 1;

    if (objIndex < 0 || objIndex >= G.nObjs)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", objIndex, G.nObjs);
        return 0;
    }

    if (vIdx < 0 || vIdx >= G.world[objIndex].nVerts)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", vIdx, G.world[objIndex].nVerts);
        return 0;
    }

    G.world[objIndex].verts[vIdx * 3] = x;
    G.world[objIndex].verts[vIdx * 3 + 1] = y;
    G.world[objIndex].verts[vIdx * 3 + 2] = z;
    return 1;
}

/** \brief Sets a single normal component value (x, y or z) for a vertex in G.world.
 *  \param objIndex an int containing the index of the 3D object that contains this vertex.
 *  \param nIdx an int indexing the vertex normal component to update.
 *  \param x a float specifying the X component of the value to be assigned to this normal
 *           in the G.world array.
 *  \param y a float specifying the Y component of the value to be assigned to this normal
 *           in the G.world array.
 *  \param z a float specifying the Z component of the value to be assigned to this normal
 *           in the G.world array.
 *
 *  This function sets the value of a G.world normal component (x, y or z).
 *  This function is called indirectly by the setNormCoord Python wrapper.
 *  The Python wrapper specifies a list of the three components, but this list is split up into 3
 *  separate calls to this function by the mh_setNormCoord function in main.c.
 */
int setNormCoo(int objIndex, int nIdx, float x, float y, float z)
{
    if (!G.world)
        return 1;

    if (objIndex < 0 || objIndex >= G.nObjs)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", objIndex, G.nObjs);
        return 0;
    }

    if (nIdx < 0 || nIdx >= G.world[objIndex].nVerts)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", nIdx, G.world[objIndex].nVerts);
        return 0;
    }

    G.world[objIndex].norms[nIdx * 3] = x;
    G.world[objIndex].norms[nIdx * 3 + 1] = y;
    G.world[objIndex].norms[nIdx * 3 + 2] = z;
    return 1;
}

/** \brief Sets a single UV component value (U or V) for a vertex in G.world.
 *  \param objIndex an int containing the index of the 3D object that contains this vertex.
 *  \param nIdx an int indexing the vertex UV component to update.
 *  \param u a float specifying the value to be assigned to the U component of the UV mapping data
 *         associated with the specified vertex in the G.world array.
 *  \param v a float specifying the value to be assigned to the V component of the UV mapping data
 *         associated with the specified vertex in the G.world array.
 *
 *  This function sets the value of a G.world UV component (U or V).
 *  This function is called indirectly by the setUVCoord Python wrapper.
 *  The Python wrapper specifies a list of the two components, but this list is split up into 2
 *  separate calls to this function by the mh_setUVCoord function in main.c.
 */
int setUVCoo(int objIndex, int nIdx, float u, float v)
{
    if (!G.world)
        return 1;

    if (objIndex < 0 || objIndex >= G.nObjs)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", objIndex, G.nObjs);
        return 0;
    }

    if (nIdx < 0 || nIdx >= G.world[objIndex].nVerts)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", nIdx, G.world[objIndex].nVerts);
        return 0;
    }

    G.world[objIndex].UVs[nIdx * 2] = u;
    G.world[objIndex].UVs[nIdx * 2 + 1] = v;
    return 1;
}

/** \brief Sets a single color component value (R, G or B) for a vertex in G.world.
 *  \param objIndex an int containing the index of the 3D object that contains this vertex.
 *  \param nIdx an int indexing the vertex color component to update.
 *  \param r an unsigned char (an integer value from 0-255) specifying the Red channel 
 *         component to be assigned to this color component.
 *  \param g an unsigned char (an integer value from 0-255) specifying the Green channel
 *         component to be assigned to this color component.
 *  \param b an unsigned char (an integer value from 0-255) specifying the Blue channel
 *         component to be assigned to this color component.
 *
 *  This function sets the value of a G.world color component (R, G or B).
 *  This function is called by the mh_setColorCoord function in main.c which
 *  splits a list of the three color components into 3 separate calls to this function.
 *
 */
int setColorIDComponent(int objIndex, int nIdx, unsigned char r, unsigned char g, unsigned char b)
{
    if (!G.world)
        return 1;

    if (objIndex < 0 || objIndex >= G.nObjs)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", objIndex, G.nObjs);
        return 0;
    }

    if (nIdx < 0 || nIdx >= G.world[objIndex].nVerts)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", nIdx, G.world[objIndex].nVerts);
        return 0;
    }

    G.world[objIndex].colors[nIdx * 3] = r;
    G.world[objIndex].colors[nIdx * 3 + 1] = g;
    G.world[objIndex].colors[nIdx * 3 + 2] = b;
    return 1;
}

/** \brief Sets a single color component value (R, G, B or A) for a vertex in G.world.
 *  \param objIndex an int containing the index of the 3D object that contains this vertex.
 *  \param nIdx an int indexing the vertex color component to update.
 *  \param r an unsigned char (an integer value from 0-255) specifying the Red channel 
 *         component to be assigned to this color component in the G.world array.
 *  \param g an unsigned char (an integer value from 0-255) specifying the Green channel
 *         component to be assigned to this color component in the G.world array.
 *  \param b an unsigned char (an integer value from 0-255) specifying the Blue channel
 *         component to be assigned to this color component in the G.world array.
 *  \param a an unsigned char (an integer value from 0-255) specifying the Alpha channel
 *         component to be assigned to this color component in the G.world array.
 *
 *  This function sets the value of a G.world color component (R, G, B or A).
 */
int setColorComponent(int objIndex, int nIdx, unsigned char r, unsigned char g, unsigned char b, unsigned char a)
{
    if (!G.world)
        return 1;

    if (objIndex < 0 || objIndex >= G.nObjs)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", objIndex, G.nObjs);
        return 0;
    }

    if (nIdx < 0 || nIdx >= G.world[objIndex].nVerts)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", nIdx, G.world[objIndex].nVerts);
        return 0;
    }

    G.world[objIndex].colors2[nIdx * 4] = r;
    G.world[objIndex].colors2[nIdx * 4 + 1] = g;
    G.world[objIndex].colors2[nIdx * 4 + 2] = b;
    G.world[objIndex].colors2[nIdx * 4 + 3] = a;
    return 1;
}


/** \brief Sets a visibility flag for this object in G.world.
 *  \param objIndex an int containing the index of the 3D object that contains this face.
 *  \param visibility an int used as a flag to indicate whether this object is visible or not.
 *
 *  This function sets the visibility flag for this G.world object.
 *  This function is called by the setVisibility Python function via the mh_setVisibility function in main.c.
 */
int setVisibility (int objIndex, int visibility)
{
    if (!G.world)
        return 1;

    if (objIndex < 0 || objIndex >= G.nObjs)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", objIndex, G.nObjs);
        return 0;
    }

    G.world[objIndex].isVisible = visibility;
    return 1;
}

/** \brief Sets a pickable flag for this object in G.world.
 *  \param objIndex an int containing the index of the 3D object that contains this face.
 *  \param pickable an int used as a flag to indicate whether this object is pickable or not.
 *
 *  This function sets the pickable flag for this G.world object.
 *  This function is called by the setPickable Python function via the mh_setPickable function in main.c.
 */
int setPickable(int objIndex, int pickable)
{
    if (!G.world)
        return 1;

    if (objIndex < 0 || objIndex >= G.nObjs)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", objIndex, G.nObjs);
        return 0;
    }

    G.world[objIndex].isPickable = pickable;
    return 1;
}

/** \brief Sets a text string for this object in G.world.
 *  \param objIndex an int containing the index of the 3D object.
 *  \param objText an char pointer to a string of text.
 *
 *  This function sets a text string for this G.world object.
 *  This function is called by the setText Python method on the Object3D
 *  class via the mh_setText function in main.c.
 */
int setText(int objIndex, const char *objText)
{
    if (!G.world)
        return 1;

    if (objIndex < 0 || objIndex >= G.nObjs)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", objIndex, G.nObjs);
        return 0;
    }

    free(G.world[objIndex].textString);
    G.world[objIndex].textString = strdup(objText);
    return 1;
}

/** \brief Sets the camera mode for this object in G.world (fixed or movable).
 *  \param objIndex an int containing the index of the 3D object.
 *  \param camMode an int indicating the camera mode.
 *
 *  This function sets the camera mode for this G.world object.
 *
 *  The 3D engine has two camera modes (both perspective modes).
 *  The first is moved by the mouse, while the second is fixed.
 *  The first is generally used to model 3D objects (human, clothes,
 *  etc...), while the second is used for the 3D GUI.
 *
 *  This function is called by the setCameraProjection Python function
 *  via the mh_setCameraMode function in main.c.
 */
int setCamMode(int objIndex, int camMode)
{
    if (!G.world)
        return 1;

    if (objIndex < 0 || objIndex >= G.nObjs)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", objIndex, G.nObjs);
        return 0;
    }

    G.world[objIndex].inMovableCamera = camMode;
    return 1;
}


/** \brief Sets the location of a 3D object into G.world.
 *  \param objIndex an int containing the index of the 3D object (used to index the G.world array).
 *  \param locX a float specifying the x coordinate of the object.
 *  \param locY a float specifying the y coordinate of the object.
 *  \param locZ a float specifying the z coordinate of the object.
 *
 *  This function sets the location of a 3D object into the G.world array.
 */
int setObjLoc(int objIndex, float locX, float locY, float locZ)
{
    if (!G.world)
        return 1;

    if (objIndex < 0 || objIndex >= G.nObjs)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", objIndex, G.nObjs);
        return 0;
    }

    G.world[objIndex].location[0] = locX;
    G.world[objIndex].location[1] = locY;
    G.world[objIndex].location[2] = locZ;
    return 1;
}


/** \brief Set hasTexture attribute.
 *  \param objIndex an int containing the index of the 3D object (used to index the G.world array).
 *  \param texture an unsigned integer indicating the texture to assigne to the texture attribute
           of the specified object.
 *
 *  This function assigns a texture to a 3D object.
 */
int setObjTexture(int objIndex, unsigned int texture)
{
    if (!G.world)
        return 1;

    if (objIndex < 0 || objIndex >= G.nObjs)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", objIndex, G.nObjs);
        return 0;
    }

    G.world[objIndex].texture = texture;
    return 1;
}

/** \brief Set shadeless attribute.
 *  \param objIndex an int containing the index of the 3D object (used to index the G.world array).
 *  \param value an int flag: 1 = the obj is affected by lights; 0 = the obj is not affected by lights.
 *
 *  This function sets the shadeless attribute of a 3D object in the G.world array.
 */
int setShadeless(int objIndex, int value)
{
    if (!G.world)
        return 1;

    if (objIndex < 0 || objIndex >= G.nObjs)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", objIndex, G.nObjs);
        return 0;
    }

    G.world[objIndex].shadeless = value;
    return 1;
}

/** \brief Sets the orientation of a 3D object into G.world.
 *  \param objIndex an int containing the index of the 3D object (used to index the G.world array).
 *  \param rotX a float specifying the rotation around the x-axis required to achieve the required orientation.
 *  \param rotY a float specifying the rotation around the y-axis required to achieve the required orientatio.
 *  \param rotZ a float specifying the rotation around the z-axis required to achieve the required orientatio.
 *
 *  This function sets the orientation of a 3D object into the G.world array.
 */
int setObjRot(int objIndex, float rotX, float rotY, float rotZ)
{
    if (!G.world)
        return 1;

    if (objIndex < 0 || objIndex >= G.nObjs)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", objIndex, G.nObjs);
        return 0;
    }

    G.world[objIndex].rotation[0] = rotX;
    G.world[objIndex].rotation[1] = rotY;
    G.world[objIndex].rotation[2] = rotZ;
    return 1;
}

/** \brief Sets the scale factor used to define the size of a 3D object into G.world.
 *  \param objIndex an int containing the index of the 3D object (used to index the G.world array).
 *  \param sizeX a float specifying the scale along the x-axis required to achieve the required size.
 *  \param sizeY a float specifying the scale along the Y-axis required to achieve the required size.
 *  \param sizeZ a float specifying the scale along the Z-axis required to achieve the required size.
 *
 *  This function sets the scale factor used to define the size of a 3D object into the G.world array.
 */
int setObjScale(int objIndex, float sizeX, float sizeY, float sizeZ)
{
    if (!G.world)
        return 1;

    if (objIndex < 0 || objIndex >= G.nObjs)
    {
        PyErr_Format(PyExc_IndexError, "index out of range, %i is not between 0 and %i", objIndex, G.nObjs);
        return 0;
    }

    G.world[objIndex].scale[0] = sizeX;
    G.world[objIndex].scale[1] = sizeY;
    G.world[objIndex].scale[2] = sizeZ;
    return 1;
}

/** \brief Creates an array of n floats and returns a pointer to that array.
 *  \param n an int indicating the number of floats to add into the array.
 *
 *  This function creates an array of n floats each containing a value of 1.0 and returns a pointer to that array.
 */
float *makeFloatArray(int n)
{
    float *iptr;
    int i;
    iptr = (float *)malloc(n * sizeof(float));
    if (iptr == NULL)
    {
        printf ("Out of memory!\n");
    }
    for (i = 0; i < n; i++)
    {
        iptr[i] = 1.0;
    }
    return iptr;
}

/** \brief Creates an array of n characters and returns a pointer to that array.
 *  \param n an int indicating the number of characters to add into the array.
 *
 *  This function creates an array of n characters set to high values and returns a pointer to that array.
 */
unsigned char *makeUCharArray(int n)
{
    unsigned char *iptr;
    int i;
    iptr = (unsigned char *)malloc(n * sizeof(unsigned char));
    if (iptr == NULL)
    {
        printf ("Out of memory!\n");
    }
    for (i = 0; i < n; i++)
    {
        iptr[i] = 255;
    }
    return iptr;
}

/** \brief Creates an array of n integers and returns a pointer to that array.
 *  \param n an int indicating the number of integers to add into the array.
 *
 *  This function creates an array of n integers set to '-1' and returns a pointer to that array.
 */
int *makeIntArray(int n)
{
    int *iptr;
    int i;
    iptr = (int *)malloc(n * sizeof(int));
    if (iptr == NULL)
    {
        printf ("Out of memory!\n");
    }
    for (i = 0; i < n; i++)
    {
        iptr[i] = -1;
    }
    return iptr;
}

/** \brief Creates an array of n object3D objects and returns a pointer to that array.
 *  \param n an int indicating the number of objects to add into the array.
 *
 *  This function creates an array of n object3D objects and returns a pointer to that array.
 */
OBJARRAY objVector(int n)
{
    struct object3D * iptr;
    iptr = (struct object3D*)calloc(n, sizeof(struct object3D));
    if (iptr == NULL)
    {
        printf ("Out of memory!\n");
    }
    return iptr;
}




