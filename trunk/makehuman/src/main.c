/** \file main.c
 *  \brief The main C application file.

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
     <td>MakeHuman Team 2001-2008                        </td></tr>
 <tr><td>Licensing:                                      </td>
     <td>GPL3 (see also
         http://makehuman.wiki.sourceforge.net/Licensing)</td></tr>
 <tr><td>Coding Standards:                               </td>
     <td>See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards
                                                         </td></tr>
 </table>

 This is the main C application file used to run the MakeHuman application.
 A large part of this file is dedicated to providing an integration layer
 between the C core application and the Python GUI control scripts.

 Much of the core C application is used to implement OpenGL library functions
 that are used to control the 3D graphics environment.
 See http://makehuman.wiki.sourceforge.net/DG_Application_Overview for a
 description of how the integration between C and Python works.

 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <SDL.h>

#ifdef _DEBUG
  #undef _DEBUG
  #include <Python.h>
  #define _DEBUG
#else
  #include <Python.h>
#endif

#include "core.h"
#include "glmodule.h"
#ifdef __APPLE__
#include "MouseEventTrap.h"
#endif // __APPLE__

/* Our global struct - all globals must be here */
Global G;

/** \brief Initialize Globals
 *
 *  This function initializes a small number of global settings that define
 *  the initial view of the Humanoid figure that the MakeHuman application
 *  manipulates (e.g. Field of View, Window Dimensions, Rotation Settings etc.).
 */
void initGlobals(void)
{
    G.world = NULL;
    G.nObjs = 0;
    G.fovAngle = 45;
    G.zoom = 60;
    G.rotX = 0;
    G.rotY = 0;
    G.translX = 0;
    G.translY = 0;
    G.windowHeight = 600;
    G.windowWidth = 800;
    G.modifiersKeyState = 0;
    G.millisecTimer = 10;

    G.fontOffset = 0;
    G.pendingUpdate = 0;
    G.pendingTimer = 0;
    G.loop = 1;
    G.fullscreen = 0;
}

/** \brief Get an integer representing the current modifier key settings.
 *
 *  This function returns the current modifier key settings as a Python integer value
 *  (e.g. Whether the Shift or Ctrl keys are currently depressed).
 */
static PyObject* mh_getKeyModifiers(PyObject *self, PyObject *args)
{
    return Py_BuildValue("i", G.modifiersKeyState);
}

/** \brief Get the RGB value of the color that has been picked.
 *
 *  This function returns the color that has been picked as a Python list of 3 integers,
 *  each between 0 and 255, representing an RGB value.
 */
static PyObject* mh_getColorPicked(PyObject *self, PyObject *args)
{
    return Py_BuildValue("[i,i,i]", G.color_picked[0], G.color_picked[1], G.color_picked[2]);
}

/** \brief Get the current camera rotation settings.
 *
 *  This function returns the current camera rotation settings as a Python
 *  list of 2 float values. This is an X and a Y rotation in degrees.
 */
static PyObject* mh_getCameraRotations(PyObject *self, PyObject *args)
{
    return Py_BuildValue("[f,f]", G.rotX,G.rotY);
}

/** \brief Set the current camera rotation settings.
 *
 *  This function sets the current camera rotation settings as 
 *  2 float values. This is an X and a Y rotation in degrees.
 */
static PyObject* mh_setCameraRotations(PyObject *self, PyObject *args)
{
  if (!PyArg_ParseTuple(args, "ff", &G.rotX, &G.rotY))
      return NULL;
  return Py_BuildValue("");
}

/** \brief Get the current camera translation (pan) settings.
 *
 *  This function returns the current camera translation settings as a Python
 *  list of 2 float values. This is an X and a Y translation in ???.
 *  <b>EDITORIAL NOTE. Need to indicate the units used.</b>
 */
static PyObject* mh_getCameraTranslations(PyObject *self, PyObject *args)
{
    return Py_BuildValue("[f,f]", G.translX,G.translY);
}

/** \brief Set the current camera translation (pan) settings.
 *
 *  This function returns the current camera translation settings as
 *  2 float values. This is an X and a Y translation in ???.
 *  <b>EDITORIAL NOTE. Need to indicate the units used.</b>
 */
static PyObject* mh_setCameraTranslations(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, "ff", &G.translX, &G.translY))
        return NULL;
    return Py_BuildValue("");
}

/** \brief Get the current camera zoom setting.
 *
 *  This function returns the current camera zoom setting as a Python
 *  float value.
 *  <b>EDITORIAL NOTE. Need to indicate the units used.</b>
 */
static PyObject* mh_getCameraZoom(PyObject *self, PyObject *args)
{
    return Py_BuildValue("f", G.zoom);
}

/** \brief Set the current camera zoom setting.
 *
 *  This function sets the current camera zoom setting as a Python
 *  float value.
 *  <b>EDITORIAL NOTE. Need to indicate the units used.</b>
 */
static PyObject* mh_setCameraZoom(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, "f", &G.zoom))
        return NULL;
    return Py_BuildValue("");
}

/** \brief Get the current camera settings.
 *
 *  This function returns the current camera settings as a list of 8 Python
 *  float values:
 *  1: Camera Pan X - The camera displacement in the +X direction.
 *  2: Camera Pan Y - The camera displacement in the +Y direction.
 *  3: Camera Zoom (Z) - The camera displacement in the -Z direction.
 *  4: Camera X Rotation - The camera rotation around the X axis in degrees.
 *  5: Camera Y Rotation - The camera rotation around the Y axis in degrees.
 *  6: Camera FOV - The vertical field of view angle in degrees (Y).
 *  7: Window Width - The viewport width in pixels (X).
 *  8: Window Height - The viewport height in pixels (Y).
 *
 *  Note. The camera start position is at the origin pointing straight
 *  ahead along the +Z axis.
 */
static PyObject* mh_getCameraSettings(PyObject *self, PyObject *args)
{
    return Py_BuildValue("[f,f,f,f,f,f,i,i]",
                         G.translX, G.translY, G.zoom,
                         G.rotX, G.rotY,
                         G.fovAngle,
                         G.windowHeight, G.windowWidth);
}

/** \brief Get the current mouse x, y cursor position on the screen, in pixels.
 *  This function retrieves the x and y mouse position in screen
 *  coordinates returning two integer values to the Python code.
 */
static PyObject* mh_getMousePos2D(PyObject *self, PyObject *args)
{
    int x, y;
    SDL_GetMouseState(&x, &y);
    return Py_BuildValue("[i,i]", x, y);
}

/** \brief Get the current mouse x, y, z cursor position in the 3D scene.
 *  This function retrieves the x, y and z mouse position in screen
 *  coordinates returning three float values to the Python code.
 */
static PyObject* mh_getMousePos3D(PyObject *self, PyObject *args)
{
    return Py_BuildValue("[d,d,d]", G.mouse3DX, G.mouse3DY, G.mouse3DZ);
}

/** \brief Get the current mouse x, y, z cursor position in the 3D GUI.
 *  This function retrieves the x, y and z mouse position in GUI
 *  coordinates returning three float values to the Python code.
 */
static PyObject* mh_getMousePosGUI(PyObject *self, PyObject *args)
{
    return Py_BuildValue("[d,d,d]", G.mouseGUIX, G.mouseGUIY, G.mouseGUIZ);
}

static PyObject* mh_convertToScreen(PyObject *self, PyObject *args)
{
    double world[3];
    double screen[3];
    int camera;
    if (!PyArg_ParseTuple(args, "dddi", screen, screen + 1, screen + 2, &camera))
        return NULL;
    else
    {
        mhConvertToScreen(screen, world, camera);
        return Py_BuildValue("[d,d,d]", world[0], world[1], world[2]);
    }
}

static PyObject* mh_convertToWorld2D(PyObject *self, PyObject *args)
{
    double screen[2];
    double world[3];
    int camera;
    if (!PyArg_ParseTuple(args, "ddi", screen, screen + 1, &camera))
        return NULL;
    else
    {
        mhConvertToWorld2D(screen, world, camera);
        return Py_BuildValue("[d,d,d]", world[0], world[1], world[2]);
    }
}

static PyObject* mh_convertToWorld3D(PyObject *self, PyObject *args)
{
    double screen[3];
    double world[3];
    int camera;
    if (!PyArg_ParseTuple(args, "dddi", screen, screen + 1, screen + 2, &camera))
        return NULL;
    else
    {
        mhConvertToWorld3D(screen, world, camera);
        return Py_BuildValue("[d,d,d]", world[0], world[1], world[2]);
    }
}

/** \brief Get the current window (viewport) width and height in pixels.
 *  This function retrieves the current width and height of the drawable area
 *  within the MakeHuman window in pixels (the viewport size).
 */
static PyObject* mh_getWindowSize(PyObject *self, PyObject *args)
{
    return Py_BuildValue("[i,i]", G.windowWidth, G.windowHeight);
}

/** \brief Start the GUI window at application launch.
 *
 *  This function constitutes part of the application initiation processing.
 *  It passes through the instruction to create the SDL window.
 *  It returns a null value.
 */
static PyObject* mh_startWindow(PyObject *self, PyObject *args)
{
    int useTimer = 0;
    if (!PyArg_ParseTuple(args, "i", &useTimer))
        return NULL;
    else
    {
        mhCreateWindow(useTimer);
    }
    return Py_BuildValue("");
}

/** \brief Start the event loop at application launch.
 *
 *  This function constitutes part of the application initiation processing.
 *  It passes through the instruction to launch the main event loop which
 *  will control the GUI environment until the termination of the
 *  application.
 *  It returns a null value.
 */
static PyObject* mh_startEventLoop(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ""))
        return NULL;
    else
    {
        mhEventLoop();
    }
    return Py_BuildValue("");
}

/** \brief End the GUI application.
 *
 *  This function constitutes part of the application termination processing.
 *  It passes through the instruction to exit from the main event loop which
 *  controls the GUI environment.
 *  It returns a null value.
 */
static PyObject* mh_shutDown(PyObject *self, PyObject *args)
{
    mhShutDown();
    return Py_BuildValue("");
}

/** \brief Redraws the scene in the GUI window.
 *
 *  This function passes through the instruction to the SDL module to redraw the
 *  main application GUI window. Drawing asynchronous will queue an update,
 *  drawing synchronous will render immediately.
 *  It returns a null value.
 */
static PyObject* mh_redraw(PyObject *self, PyObject *args)
{
    int async;
    if (!PyArg_ParseTuple(args, "i", &async))
        return NULL;
    if (async)
        mhQueueUpdate();
    else
        mhDraw();
    return Py_BuildValue("");
}

/** \brief Sets the fullscreen state of the GUI window.
 *
 *  This function passes through the instruction to the SDL module to set the
 *  fullscreen state of the main application GUI window.
 *  It returns a null value.
 */
static PyObject* mh_setFullscreen(PyObject *self, PyObject *args)
{
    int fullscreen;
    if (!PyArg_ParseTuple(args, "i", &fullscreen))
        return NULL;
    mhSetFullscreen(fullscreen);
    return Py_BuildValue("");
}

/** \brief Initialize the scene in the GUI window.
 *
 *  This function passes through the instruction to the core.c module to reinitialize
 *  the set of objects stored in G.world by freeing memory from all objects previously
 *  recorded and creating an array of an appropriate size to take the new object list.
 *
 *  It returns a null value.
 */
static PyObject* mh_init3DScene(PyObject *self, PyObject *args)
{
    int n;
    if (!PyArg_ParseTuple(args, "i", &n))
        return NULL;
    else
    {
        initscene(n);
    }
    return Py_BuildValue("");
}

/** \brief Add an object into the scene.
 *
 *  This function adds the object specified into the scene at the specified location.
 *  It returns a null value.
 */
static PyObject* mh_addObj(PyObject *self, PyObject *args)
{
    int objIdx, vertexbufferSize;
    float objX,objY,objZ;
    PyObject *indexBuffer;

    if (!PyArg_ParseTuple(args, "ifffiO", &objIdx, &objX,
                          &objY, &objZ, &vertexbufferSize, &indexBuffer) || !PyList_Check(indexBuffer))
        return NULL;
    else
    {
        PyObject *iterator = PyObject_GetIter(indexBuffer);
        PyObject *item;
        int index = 0;

        addObject(objIdx, objX, objY, objZ, vertexbufferSize, (int)PyList_Size(indexBuffer) / 3);

        for (item = PyIter_Next(iterator); item; item = PyIter_Next(iterator))
        {
            G.world[objIdx].trigs[index++] = PyInt_AsLong(item);
            Py_DECREF(item);
        }

        Py_DECREF(iterator);
    }
    return Py_BuildValue("");
}

/** \brief Set coordinates, normal and color information for the 3 vertices of a face.
 *
 *  This function passes the coordinates, normal and color information for the 3 vertices
 *  of a face into OpenGL.
 *  It returns a null value.
 */
static PyObject* mh_setAllCoord(PyObject *self, PyObject *args)
{
    float vert[3];
    float norm[3];
    unsigned char color[3];
    unsigned char color2[4];
    int objIdx, index, colorIdx;

    if (!PyArg_ParseTuple(args, "iii(fff)(fff)(BBB)(BBBB)",  &objIdx, &index, &colorIdx, &vert[0], &vert[1], &vert[2], &norm[0], &norm[1], &norm[2], &color[0], &color[1], &color[2], &color2[0], &color2[1], &color2[2],&color2[3]))
        return NULL;
    else if (!setVertCoo(objIdx, index, vert[0], vert[1], vert[2]) ||
             !setNormCoo(objIdx, index, norm[0], norm[1], norm[2]) ||
             !setColorIDComponent(objIdx, index, color[0], color[1], color[2]) ||
             !setColorComponent(objIdx, colorIdx, color2[0], color2[1], color2[2], color2[3]))
        return NULL;
    else
        return Py_BuildValue("");
}

/** \brief Set the coordinates of a specified vertex.
 *
 *  This function passes the x, y and z coordinates for a specifed vertex
 *  into OpenGL.
 *  It returns a null value.
 */
static PyObject* mh_setVertCoord(PyObject *self, PyObject *args)
{
    float vert[3];
    int objIdx, index;

    if (!PyArg_ParseTuple(args, "ii(fff)",  &objIdx, &index, &vert[0], &vert[1], &vert[2]))
        return NULL;
    else if (!setVertCoo(objIdx, index, vert[0], vert[1], vert[2]))
        return NULL;
    else
        return Py_BuildValue("");
}

/** \brief Set the normal of a specified vertex.
 *
 *  This function passes the x, y and z coordinates of a normal vector for a specifed vertex
 *  into OpenGL.
 *  It returns a null value.
 */
static PyObject* mh_setNormCoord(PyObject *self, PyObject *args)
{
    float norm[3];
    int objIdx, index;

    if (!PyArg_ParseTuple(args, "ii(fff)",  &objIdx, &index, &norm[0], &norm[1], &norm[2]))
        return NULL;
    else if (!setNormCoo(objIdx, index, norm[0], norm[1], norm[2]))
        return NULL;
    else
        return Py_BuildValue("");
}

/** \brief Set the UV coordinates of a specified vertex.
 *
 *  This function passes the UV coordinates of a specifed vertex
 *  into OpenGL.
 *  It returns a null value.
 */
static PyObject* mh_setUVCoord(PyObject *self, PyObject *args)
{
    int objIdx,index;
    float uv[2];
    if (!PyArg_ParseTuple(args, "ii(ff)", &objIdx, &index, &uv[0], &uv[1]))
        return NULL;
    else if (!setUVCoo(objIdx, index, uv[0], uv[1]))
        return NULL;
    else
        return Py_BuildValue("");
}

/** \brief Set the color of a specified vertex.
 *
 *  This function passes the 3 components (RGB) of a color of a specifed vertex
 *  into OpenGL.
 *  It returns a null value.
 *
 *  <b>EDITORIAL NOTE: mh_setColorCoord doesn't seem to be called from anywhere.</b>
 */
static PyObject* mh_setColorCoord(PyObject *self, PyObject *args)
{
    unsigned char color[3];
    int objIdx, index;

    if (!PyArg_ParseTuple(args, "ii(BBB)",  &objIdx, &index, &color[0], &color[1], &color[2]))
        return NULL;
    else if (!setColorIDComponent(objIdx, index, color[0], color[1], color[2]))
        return NULL;
    else
        return Py_BuildValue("");
}

/** \brief Set the color and alpha channel of a specified vertex.
 *
 *  This function passes the 4 components (RGBA) of a color of a specifed vertex
 *  into OpenGL.
 *  It returns a null value.
 */
static PyObject* mh_setColorCoord2(PyObject *self, PyObject *args)
{
    unsigned char color[4];
    int objIdx, index;

    if (!PyArg_ParseTuple(args, "ii(BBBB)",  &objIdx, &index, &color[0], &color[1], &color[2], &color[3]))
        return NULL;
    else if (!setColorComponent(objIdx, index, color[0], color[1], color[2], color[3]))
        return NULL;
    else
        return Py_BuildValue("");
}

/** \brief Set the camera mode.
 *
 *  This function passes the camera mode
 *  into OpenGL.
 *  It returns a null value.
 */
static PyObject* mh_setCameraMode(PyObject *self, PyObject *args)
{
    int objIdx, cameraMode;
    if (!PyArg_ParseTuple(args, "ii", &objIdx, &cameraMode))
        return NULL;
    else if (!setCamMode(objIdx, cameraMode))
        return NULL;
    else
        return Py_BuildValue("");
}

/** \brief Set the texture attribute.
 *
 *  This function passes the texture
 *  into OpenGL.
 *  It returns a null value.
 */
static PyObject* mh_setObjTexture(PyObject *self, PyObject *args)
{
    int objIdx, texture;
    if (!PyArg_ParseTuple(args, "ii", &objIdx, &texture))
        return NULL;
    else if (!setObjTexture(objIdx, texture))
        return NULL;
    else
        return Py_BuildValue("");
}

/** \brief Set the useLights attribute.
 *
 *  This function passes the useLights
 *  into OpenGL.
 *  It returns a null value.
 */
static PyObject* mh_setShadeless(PyObject *self, PyObject *args)
{
    int objIdx, shadelessFlag;
    if (!PyArg_ParseTuple(args, "ii", &objIdx, &shadelessFlag))
        return NULL;
    else if (!setShadeless(objIdx, shadelessFlag))
        return NULL;
    else
        return Py_BuildValue("");
}

/** \brief Set the object location.
 *
 *  This function passes the location of a specified object
 *  into OpenGL.
 *  It returns a null value.
 */
static PyObject* mh_setObjLocation(PyObject *self, PyObject *args)
{
    int objIdx;
    float locX,locY,locZ;
    if (!PyArg_ParseTuple(args, "ifff", &objIdx, &locX, &locY, &locZ))
        return NULL;
    else if (!setObjLoc(objIdx, locX, locY, locZ))
        return NULL;
    else
        return Py_BuildValue("");
}

/** \brief Set the object orientation.
 *
 *  This function passes the orientation of a specified object
 *  into OpenGL.
 *  It returns a null value.
 */
static PyObject* mh_setObjRotation(PyObject *self, PyObject *args)
{
    int objIdx;
    float rotX,rotY,rotZ;
    if (!PyArg_ParseTuple(args, "ifff", &objIdx, &rotX, &rotY, &rotZ))
        return NULL;
    else if (!setObjRot(objIdx, rotX, rotY, rotZ))
        return NULL;
    else
        return Py_BuildValue("");
}

/** \brief Set the object scale factors.
 *
 *  This function passes the x, y and z scale factors of a specified object
 *  into OpenGL.
 *  It returns a null value.
 */
static PyObject* mh_setObjScale(PyObject *self, PyObject *args)
{
    int objIdx;
    float sizeX,sizeY,sizeZ;
    if (!PyArg_ParseTuple(args, "ifff", &objIdx, &sizeX, &sizeY, &sizeZ))
        return NULL;
    else if (!setObjScale(objIdx, sizeX, sizeY, sizeZ))
        return NULL;
    else
        return Py_BuildValue("");
}

/** \brief Set the visibility of an object.
 *
 *  This function sets the visibility of a specified object by passing it
 *  into OpenGL.
 *  It returns a null value.
 */
static PyObject* mh_setVisibility(PyObject *self, PyObject *args)
{
    int objIdx;
    int visib;
    if (!PyArg_ParseTuple(args, "ii", &objIdx, &visib))
        return NULL;
    else if (!setVisibility(objIdx, visib))
        return NULL;
    else
        return Py_BuildValue("");
}

/** \brief Set text of an object.
 *
 *  This function passes the text describing the specified object
 *  into OpenGL.
 *  It returns a null value.
 */
static PyObject* mh_setText(PyObject *self, PyObject *args)
{
    int objIdx;
    char *objText;
    if (!PyArg_ParseTuple(args, "is", &objIdx, &objText))
        return NULL;
    else if (!setText(objIdx, objText))
        return NULL;
    else
        return Py_BuildValue("");
}

/** \brief Load texture of an object from file.
 *
 *  This function passes a string containing the file system path to a texture file
 *  into OpenGL.
 *  The texture from this file is applied to the specified object.
 *  It returns a null value.
 */
static PyObject* mh_LoadTexture(PyObject *self, PyObject *args)
{
    int texture;
    char *filename;
    if (!PyArg_ParseTuple(args, "si", &filename, &texture))
        return NULL;
    else if (!(texture = mhLoadTexture(filename, texture)))
        return NULL;
    else
        return Py_BuildValue("i", texture);
}

static PyObject* mh_GrabScreen(PyObject *self, PyObject *args)
{
    int x, y, width, height;
    char *filename;
    if (!PyArg_ParseTuple(args, "iiiis", &x, &y, &width, &height, &filename))
        return NULL;
    else if (!mhGrabScreen(x, y, width, height, filename))
      return NULL;
    else
        return Py_BuildValue("");
}

/** \brief Set millisec attribute for timer func.
 *
 *  This function passes the delay function to the SDL timer
 *  It returns a null value.
 */
static PyObject* mh_setTimeTimer(PyObject *self, PyObject *args)
{
    int milliseconds;
    if (!PyArg_ParseTuple(args, "i", &milliseconds))
        return NULL;
    else
    {
        G.millisecTimer = milliseconds;
    }
    return Py_BuildValue("");
}

/** \brief Defines a set of functions as an array that can be passed into the Py_InitModule function.
 *
 *  This array declaration is used to list a set of functions that can be called from Python.
 *  The array is passed into the Py_InitModule function when it is used to dynamically
 *  initialize the 'mh' moduleas.
 */

static PyMethodDef EmbMethods[] =
{
    {"setTimeTimer", mh_setTimeTimer, METH_VARARGS, ""},
    {"getMousePosGUI", mh_getMousePosGUI, METH_VARARGS, ""},
    {"getMousePos3D", mh_getMousePos3D, METH_VARARGS, ""},
    {"getWindowSize", mh_getWindowSize, METH_VARARGS, ""},
    {"getMousePos2D", mh_getMousePos2D, METH_VARARGS, ""},
    {"convertToScreen", mh_convertToScreen, METH_VARARGS, ""},
    {"convertToWorld2D", mh_convertToWorld2D, METH_VARARGS, ""},
    {"convertToWorld3D", mh_convertToWorld3D, METH_VARARGS, ""},
    {"setShadeless", mh_setShadeless, METH_VARARGS, ""},
    {"setObjTexture", mh_setObjTexture, METH_VARARGS, ""},
    {"getKeyModifiers", mh_getKeyModifiers, METH_VARARGS, ""},
    {"getCameraRotations", mh_getCameraRotations, METH_VARARGS, ""},
    {"setCameraRotations", mh_setCameraRotations, METH_VARARGS, ""},
    {"getCameraTranslations", mh_getCameraTranslations, METH_VARARGS, ""},
    {"setCameraTranslations", mh_setCameraTranslations, METH_VARARGS, ""},
    {"getCameraZoom", mh_getCameraZoom, METH_VARARGS, ""},
    {"setCameraZoom", mh_setCameraZoom, METH_VARARGS, ""},
    {"getCameraSettings", mh_getCameraSettings, METH_VARARGS, ""},
    {"setText", mh_setText, METH_VARARGS, ""},
    {"setVisibility", mh_setVisibility, METH_VARARGS, ""},
    {"getColorPicked", mh_getColorPicked, METH_VARARGS, ""},
    {"setColorCoord", mh_setColorCoord, METH_VARARGS, ""},
    {"setColorCoord2", mh_setColorCoord2, METH_VARARGS, ""},
    {"init3DScene", mh_init3DScene, METH_VARARGS, ""},
    {"redraw", mh_redraw, METH_VARARGS, ""},
    {"setFullscreen", mh_setFullscreen, METH_VARARGS, ""},
    {"addObj", mh_addObj, METH_VARARGS, ""},
    {"setVertCoord", mh_setVertCoord, METH_VARARGS, ""},
    {"setNormCoord", mh_setNormCoord, METH_VARARGS, ""},
    {"setUVCoord", mh_setUVCoord, METH_VARARGS, ""},
    {"setCameraMode", mh_setCameraMode, METH_VARARGS, ""},
    {"setObjLocation", mh_setObjLocation, METH_VARARGS, ""},
    {"setObjRotation", mh_setObjRotation, METH_VARARGS, ""},
    {"setObjScale", mh_setObjScale, METH_VARARGS, ""},
    {"LoadTexture", mh_LoadTexture, METH_VARARGS, ""},
    {"grabScreen", mh_GrabScreen, METH_VARARGS, ""},
    {"startWindow", mh_startWindow, METH_VARARGS, ""},
    {"startEventLoop", mh_startEventLoop, METH_VARARGS, ""},
    {"shutDown", mh_shutDown, METH_VARARGS, ""},
    {"setAllCoord", mh_setAllCoord, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}
};

/** \brief The main function initializes the MakeHuman application.
 *
 *  This function sets up the integration layer between Python and the
 *  C core application then runs the 'main' Python module to start
 *  up the MakeHuman application.
 *
 *  When the user quits the application, the SDL loop
 *  controlling user interaction with the MakeHuman GUI is terminated
 *  by the mhShutDown function from glmodule.c which issues a system exit.
 *  This function traps the exit condition and displays a goodbye message
 *  into the message window before releasing the memory used by the
 *  global variables and ending.
 *
 *  This function returns a '1'.
 */
int main(int argc, char *argv[])
{
    // Need to declare variables before other statements
    char str[80];
    int index, err;

    initGlobals(); /* initialize all our globals */

#ifdef __APPLE__ /* Since Mac OS uses app bundles all data reside in this resource bundle too. */
    strcpy(str, "execfile(\"main.py\")");
    adjustWorkingDir(argv[0]);
    // Initialize the Mouse trap code in order to gain access the mouse scroll wheel...
    initMouseScrollWheelTrap();
#else
    if (argc >= 2 && strlen(argv[1]) < 68)
    {
        sprintf(str, "execfile(\"%s\")", argv[1]);
    }
    else
    {
        strcpy(str, "execfile(\"main.py\")");
    }
#endif

    Py_SetProgramName(argv[0]);
    Py_Initialize();

    if (!Py_IsInitialized())
    {
        printf("Could not initialize Python\n");
        exit(1);
    }

    PySys_SetArgv(argc, argv);
    Py_InitModule("mh", EmbMethods);

#if defined(__GNUC__) && defined(__WIN32__)
    PyRun_SimpleString("import sys\nfo = open(\"python_out.txt\", \"w\")\nsys.stdout = fo");
    PyRun_SimpleString("import sys\nfe = open(\"python_err.txt\", \"w\")\nsys.stderr = fe");
    err = PyRun_SimpleString("execfile(\"main.py\")");
    PyRun_SimpleString("fo.close()");
    PyRun_SimpleString("fe.close()");
#else
    err = PyRun_SimpleString("execfile(\"main.py\")");
#endif

    if (err != 0)
    {
        printf("Could not run main Python script\n");
        getc(stdin);
        exit(1);
    }

    Py_Finalize();
    /*getc(stdin); just to stop the exit*/

    printf("number of objects %i\n",G.nObjs);
    for (index = 0; index < G.nObjs; index++)
    {
        printf("index %i\n", index);
        printf("number of triangles %i\n", G.world[index].nTrigs);
        printf("number of vertices %i\n", G.world[index].nVerts);
        free(G.world[index].trigs);
        free(G.world[index].verts);
        free(G.world[index].norms);
        free(G.world[index].colors);
        free(G.world[index].colors2);
        free(G.world[index].UVs);
        free(G.world[index].textString);
    }
    free(G.world);
    return 1;
}

// The following comment block is used by Doxygen to populate the main page

/** \mainpage MakeHuman - 'C' Documentation

\section intro Introduction
MakeHuman&copy; is a free interactive modelling tool for creating custom 3D human characters. These characters can be modelled very quickly and can then be exported and used with many other modelling and rendering programs to incorporate realistic human figures into computer generated images and animations. Features that make this software unique include the tetra-parametric GUI&copy; and the Natural Pose System&copy;, for advanced muscular simulation.

The home page for MakeHuman&copy; is at http://www.makehuman.org/ . The MakeHuman project is an open source project hosted on sourceforge at http://sourceforge.net/projects/makehuman/ and documented on a Wiki at http://makehuman.wiki.sourceforge.net/.

The program uses a small (but crucial) C core to support MakeHuman application functionality written in Python. These pages document the C source code that forms the core of the MakeHuman application. The Python API is documented at http://makehuman.sourceforge.net/API/ .

The C code uses OpenGL to manage the 3D graphics environment and SDL to control user interaction with the main GUI window. The C code passes events up to the Python code and provides functions to the Python code to enable it to interact with the 3D environment. The C source is contained in 4 key files and their header files (see the 'Files' tab for the full list):

<center>
<table>
<tr>
  <td class="indexkey">src/<a class="el" href="main_8c.html">main.c</a> <a href="main_8c-source.html">[code]</a></td>
  <td class="indexvalue">The main C application file </td>
</tr><tr>
  <td class="indexkey">src/<a class="el" href="glmodule_8c.html">glmodule.c</a> <a href="glmodule_8c-source.html">[code]</a></td>
  <td class="indexvalue">This module integrates with OpenGL functionality </td>
</tr><tr>
  <td class="indexkey">src/<a class="el" href="core_8c.html">core.c</a> <a href="core_8c-source.html">[code]</a></td>
  <td class="indexvalue">Integration layer between the C core and Python functions </td>
</tr>
</table>
</center>

\section startup Application Startup
When MakeHuman is launched, the C code from the 'main' function in main.c is run which dynamically creates the Python module 'mh'.
This module contains a series of embedded integration functions that map through to the other C functions in main.c, connecting the C application with the Python front-end by providing Python functions that call C functions.

For example, the "getCameraRotations" function is created as an embedded Python function on the 'mh' module that calls the C function "mh_getCameraRotations" (defined in the file main.c). This returns camera rotation angles as Python values based upon settings stored in C global variables.

Having created the 'mh' module in memory the 'main' C function loads the 'main.py' module. This displays a splash screen and a progress bar as it loads the initial 3D humanoid model (the neutral base object) and adds the various GUI sections into the scene. It creates the main toolbar that enables the user to switch between different GUI modes and defines functions to 
perform that switch for all active buttons. Active buttons are connected to these functions by being registered to receive events.
 
At the end of the initiation process the splash screen is hidden and Modelling mode is activated. The 'startEventLoop' method on the main Scene3D object is invoked to call the OpenGL/SDL C functions that manage the low-level event loop. 

This Python module responds to high-level GUI toolbar events to switch between different GUI modes, but otherwise events are handled by GUI mode specific Python modules.

\section events GUI Events
SDL manages all low-level events and mhEventLoop calls C functions to handle these events. The C functions mostly pass through the events to the corresponding Python functions that have been registered against the Scene3D object. This is handled by core.c which contains a series of C functions that call Python functions using the PyRun_SimpleString function. Some Python functions need to make calls back to the OpenGL C code to perform processing such as redraws before returning control to the C code.

Whether implemented within the C handler or bubbled up to Python, the handler performs an action and ends, returning control to mhEventLoop.


\section close Application Close
Keyboard and mouse events that are configured to end the application bubble up to the Python handlers in main.py which call mh_shutDown in main.c which in turn calls mhShutDown in glmodule.c. This issues a system exit(0) to end the SDL application loop. The exit is intercepted to enable cleanup to be performed and control to be passed back through the main function in the main.c file which issues a 'goodbye' message and exits.


*/


