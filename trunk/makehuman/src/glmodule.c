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
     <td>Manuel Bastioni, Paolo Colombo, Simone Re, Marc Flerackers </td></tr>
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
#include <AGL/agl.h>
#include <Fonts.h>
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

typedef SDL_Surface *(*PFN_IMG_LOAD)(const char *);
static void *g_sdlImageHandle = NULL;
static PFN_IMG_LOAD IMG_Load = NULL;

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
void mhFlipSurface(SDL_Surface *surface)
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
unsigned int mhLoadTexture(const char *fname, unsigned int texture)
{
    int mode, components;
    SDL_Surface *surface;

    if (!texture)
        glGenTextures(1, &texture);

    if (!g_sdlImageHandle)
    {
#ifdef __WIN32__
        g_sdlImageHandle = SDL_LoadObject("SDL_image");
#elif __APPLE__
        g_sdlImageHandle = SDL_LoadObject("libSDL_image-1.2.0.dylib");
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

    surface = IMG_Load(fname);

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

    glBindTexture(GL_TEXTURE_2D, texture);

    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP);
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP);
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_LINEAR);
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
    //glTexImage2D(GL_TEXTURE_2D, 0, components, surface->w, surface->h, 0, mode, GL_UNSIGNED_BYTE, surface->pixels);
    gluBuild2DMipmaps(GL_TEXTURE_2D, components, surface->w, surface->h, mode, GL_UNSIGNED_BYTE, surface->pixels);
    glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE);

    SDL_FreeSurface(surface);

    return texture;
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
  int viewport[4];
  SDL_Surface *surface;

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
  glReadPixels(x, viewport[3] - y - height, width, height, GL_RGB, GL_UNSIGNED_BYTE, surface->pixels);
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
void mhKeyDown(int key, unsigned short character)
{
    callKeyDown(key, character);
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
        return G.millisecTimer;

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
    mhGetPickedColor(x, y);

    // Notify python
    callMouseButtonDown(b, x, y);

    // Update screen
    mhQueueUpdate();
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
    SDL_WarpMouse(g_savedx, g_savedy);

    // Calculate 3d positions
    mhGetPickedCoords(x,y);

    // Notify python
    callMouseButtonUp(b, x, y);

    // Update screen
    mhQueueUpdate();
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
    float z;
    int viewport[4];
    glGetIntegerv( GL_VIEWPORT, viewport );

    /*Getting mouse coords in 3D scene, using z value from glReadPixels*/
    mhSceneCameraPosition();/*Applying scene matrix*/
    glGetDoublev( GL_PROJECTION_MATRIX, projection );
    glGetDoublev( GL_MODELVIEW_MATRIX, modelview );
    glReadPixels( x, viewport[3]-y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &z );
    gluUnProject( x, viewport[3]-y, z, modelview,
                  projection, viewport, &G.mouse3DX, &G.mouse3DY, &G.mouse3DZ );

    /*Getting mouse 3D coords on the GUI plane, using a fixed z value.
    Assuming we use a 3D cursor in scene, with coords (x,y,9.5).
    Using glPerspective clip planes near = 0.1 and far = 100,
    the z coord = 9.5 is normalized to 0.800801. So we use this fixed
    precalculated value.
    */
    mhGUICameraPosition();/*Applying GUI matrix*/
    glGetDoublev( GL_PROJECTION_MATRIX, projection );
    glGetDoublev( GL_MODELVIEW_MATRIX, modelview );
    z = 0.800801f;
    gluUnProject( x, viewport[3]-y, z, modelview,
                  projection, viewport, &G.mouseGUIX, &G.mouseGUIY, &G.mouseGUIZ );
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

    // Turn off lighting
    glDisable(GL_LIGHTING);

	// Turn off antialiasing
    glDisable (GL_BLEND);
    glDisable(GL_MULTISAMPLE);

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    // draw the objects in static camera
    mhGUICameraPosition();
    mhDrawMeshes(1, 0);

    // draw the objects in dynamic camera
    mhSceneCameraPosition();
    mhDrawMeshes(1, 1);

    // get color information from frame buffer
    glGetIntegerv(GL_VIEWPORT, viewport);

    /* Reading the unique object color ID */
    glReadPixels(x, viewport[3] - y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE, G.color_picked);

	// Turn on antialiasing
    glEnable (GL_BLEND);
    glEnable(GL_MULTISAMPLE);

    /* restore lighting */
    glEnable(GL_LIGHTING);
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
void mhConvertToScreen(double world[3], double screen[3], int camera)
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

/** \brief Convert screen coordinates to 2D OpenGL world coordinates.
 *  \param screen a list of doubles that will contain the screen coordinates.
 *  \param world a list of doubles containing the 3D OpenGL world coordinates.
 *  \param camera an int indicating the camera mode (1=Scene or 0=GUI).
 *
 *  This function converts screen coordinates to 2D OpenGL world coordinates based upon 
 *  the specified camera setting.
 *
 */
void mhConvertToWorld2D(double screen[2], double world[3], int camera)
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

  glReadPixels(screen[0], viewport[3] - screen[1], 1, 1, GL_DEPTH_COMPONENT, GL_DOUBLE, &z);
  gluUnProject(screen[0], viewport[3] - screen[1], z, modelview, projection, viewport, world, world + 1, world + 2);
}

/** \brief Convert screen coordinates to 3D OpenGL world coordinates.
 *  \param screen a list of doubles that will contain the screen coordinates.
 *  \param world a list of doubles containing the 3D OpenGL world coordinates.
 *  \param camera an int indicating the camera mode (1=Scene or 0=GUI).
 *
 *  This function converts screen coordinates to 3D OpenGL world coordinates based upon 
 *  the specified camera setting.
 *
 */
void mhConvertToWorld3D(double screen[3], double world[3], int camera)
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
}

/** \brief Initialise the drawing space.
 *
 *  This function clears the screen and depth buffer and any previous transformations
 *  to initialize the drawing space.
 */
void mhDrawBegin()
{
    // clear the screen & depth buffer
    glClear(GL_DEPTH_BUFFER_BIT|GL_COLOR_BUFFER_BIT);
}

/** \brief Swap buffers following a redraw.
 *
 *  This function swaps the drawing buffers following a redraw.
 */
void mhDrawEnd()
{
    SDL_GL_SwapBuffers();
}

/** \brief Initialize lights and materials/textures.
 *
 *  This function initializes lights and materials/textures available to a scene.
 */
void OnInit()
{
    /*Lights and materials*/
    float lightPos[] = { -10.99f, 20.0f, 20.0f, 1.0f}; /* Light Position */
    float ambientLight[] = { 0.0f, 0.0f, 0.0f, 1.0f};  /* Ambient Light Values */
    float diffuseLight[] = { .5f, .5f, .5f, 1.0f};     /* Diffuse Light Values */
    float specular[] = {0.5f, .5f, .5f, .5f};          /* Specular Light Values */
    float MatAmb[] = {0.11f, 0.06f, 0.11f, 1.0f};      /* Material - Ambient Values */
    float MatDif[] = {0.2f, 0.6f, 0.9f, 1.0f};         /* Material - Diffuse Values */
    float MatSpc[] = {0.33f, 0.33f, 0.52f, 1.0f};      /* Material - Specular Values */
    float MatShn[] = {50.0f};                          /* Material - Shininess */
    glEnable(GL_DEPTH_TEST);                           /* Hidden surface removal */
    glEnable(GL_CULL_FACE);                            /* Inside face removal */
    glEnable(GL_LIGHTING);                             /* Enable lighting */
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight);
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular);
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos);
    //glLightModeli(GL_LIGHT_MODEL_COLOR_CONTROL, GL_SEPARATE_SPECULAR_COLOR); // If we enable this, we have stronger specular highlights
    glMaterialfv(GL_FRONT, GL_SHININESS, MatShn);      /* Set Material Shininess */
    glMaterialfv(GL_FRONT, GL_AMBIENT, MatAmb);        /* Set Material Ambience */
    glMaterialfv(GL_FRONT, GL_DIFFUSE, MatDif);        /* Set Material Diffuse */
    glMaterialfv(GL_FRONT, GL_SPECULAR, MatSpc);       /* Set Material Specular */
    glMaterialfv(GL_FRONT, GL_SHININESS, MatShn);      /* Set Material Shininess */
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


    /*LINES BELOW ARE JUST TO PRINT USEFUL INFO ABOUT USER MACHINE*/
    /*
    GLint redBits, greenBits, blueBits;
    GLint packSwapBytes, packLSBfirst, unpackSwapBytes, unpackLSBfirst;
    GLint packRowLength, packSkipRows, packSkipPixels, packAlignment;
    GLint unpackRowLength, unpackSkipRows, unpackSkipPixels, unpackAlignment;
    glGetIntegerv (GL_RED_BITS, &redBits);
    glGetIntegerv (GL_GREEN_BITS, &greenBits);
    glGetIntegerv (GL_BLUE_BITS, &blueBits);

    glGetIntegerv (GL_PACK_SWAP_BYTES, &packSwapBytes);
    glGetIntegerv (GL_PACK_LSB_FIRST, &packLSBfirst);
    glGetIntegerv (GL_UNPACK_SWAP_BYTES, &unpackSwapBytes);
    glGetIntegerv (GL_UNPACK_LSB_FIRST, &unpackLSBfirst);

    glGetIntegerv (GL_PACK_ROW_LENGTH, &packRowLength);
    glGetIntegerv (GL_PACK_SKIP_ROWS, &packSkipRows);
    glGetIntegerv (GL_PACK_SKIP_PIXELS, &packSkipPixels);
    glGetIntegerv (GL_PACK_ALIGNMENT, &packAlignment);
    glGetIntegerv (GL_UNPACK_ROW_LENGTH, &unpackRowLength);
    glGetIntegerv (GL_UNPACK_SKIP_ROWS, &unpackSkipRows);
    glGetIntegerv (GL_UNPACK_SKIP_PIXELS, &unpackSkipPixels);
    glGetIntegerv (GL_UNPACK_ALIGNMENT, &unpackAlignment);

    printf("OPENGL INFO\n --------------\n");
    printf("GL_VENDOR: %s\n",(char *)glGetString(GL_VENDOR));
    printf("GL_RENDERER: %s\n" ,(char *)glGetString(GL_RENDERER));
    printf("GL_VERSION: %s\n" ,(char *)glGetString(GL_VERSION));
    //printf("GL_EXTENSIONS: %s\n" ,(char *)glGetString(GL_EXTENSIONS));

    printf("Actual RGB bits used: %i, %i, %i\n",redBits, greenBits, blueBits);
    printf("GL_PACK_SWAP_BYTES: %i\n",packSwapBytes);
    printf("GL_PACK_LSB_FIRST: %i\n",packLSBfirst);
    printf("GL_UNPACK_SWAP_BYTES: %i\n",unpackSwapBytes);
    printf("GL_UNPACK_LSB_FIRST: %i\n",unpackLSBfirst);
    printf("GL_PACK_ROW_LENGTH: %i\n",packRowLength);
    printf("GL_PACK_SKIP_ROWS: %i\n",packSkipRows);
    printf("GL_PACK_SKIP_PIXELS: %i\n",packSkipPixels);
    printf("GL_PACK_ALIGNMENT: %i\n",packAlignment);
    printf("GL_UNPACK_ROW_LENGTH: %i\n",unpackRowLength);
    printf("GL_UNPACK_SKIP_ROWS: %i\n",unpackSkipRows);
    printf("GL_UNPACK_SKIP_PIXELS: %i\n",unpackSkipPixels);
    printf("GL_UNPACK_ALIGNMENT: %i\n",unpackAlignment);
    */

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
#elif __APPLE__
    {
        short fontNum;
        GetFNum("\pHelvetica", &fontNum);
        aglUseFont(aglGetCurrentContext(), fontNum, normal, 12, 0, 256, G.fontOffset);
    }
#else
    {
        Display *dpy = XOpenDisplay(NULL);
        XFontStruct *XFont = XLoadQueryFont(dpy, "-adobe-helvetica-medium-r-normal--12-120-75-75-p-67-iso8859-1");
        glXUseXFont(XFont->fid, 0, 256, G.fontOffset);
        XFreeFont(dpy, XFont);
        XCloseDisplay(dpy);
    }
#endif
}

/** \brief Delete materials/textures when the event loop exits.
 *
 *  This function deletes materials/textures when the event loop is exited.
 */
void OnExit()
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
void mhSceneCameraPosition()
{
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(25, (float)G.windowWidth/G.windowHeight, 0.1, 100);

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
void mhGUICameraPosition()
{
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(G.fovAngle, (float)G.windowWidth/G.windowHeight, 0.1, 100);

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
    int i;
    
    if (!G.world)
      return;

    /*Draw all objects contained by G.world*/
    for (i = 0; i < G.nObjs; i++)
    {
        if (G.world[i].inMovableCamera == cameraType)
        {
            if (G.world[i].isVisible)
            {
                //printf("draw obj n %i\n",G.world[i].nVerts/3);
                /*Transform the current object*/
                glPushMatrix();
                glTranslatef(G.world[i].location[0], G.world[i].location[1], G.world[i].location[2]);
                glRotatef(G.world[i].rotation[0], 1, 0, 0);
                glRotatef(G.world[i].rotation[1], 0, 1, 0);
                glRotatef(G.world[i].rotation[2], 0, 0, 1);
                glScalef(G.world[i].scale[0], G.world[i].scale[1], G.world[i].scale[2]);

                if (G.world[i].texture && !pickMode)
                {
                    glEnable(GL_TEXTURE_2D);
                    /*Bind the texture, that has the same index of object*/

                    glEnableClientState(GL_TEXTURE_COORD_ARRAY);
                    glBindTexture(GL_TEXTURE_2D, G.world[i].texture);

                    glTexCoordPointer(2, GL_FLOAT, 0, G.world[i].UVs);
                }

                /*
                int l;
                for (l = 0; l < G.world[i].nVerts; l++)
                    printf("oggetto %i, vert: %i\n",i,G.world[i].verts[l]);
                */

                /*Fill the array pointers with object mesh data*/
                glVertexPointer(3, GL_FLOAT, 0, G.world[i].verts);
                glNormalPointer(GL_FLOAT, 0, G.world[i].norms);


                /*Because the selection is based on color, the color array can have 2 values*/
                if (pickMode)
                {
                    /*Use color to pick ì*/
                    glColorPointer(3, GL_UNSIGNED_BYTE, 0, G.world[i].colors);
                }
                else
                {
                    /*Use color to draw ì*/
                    glColorPointer(4, GL_UNSIGNED_BYTE, 0, G.world[i].colors2);
                    /*draw text attribute if there is one; because this function
                    restores lighting, it can be used only in non picking mode*/
                    if (G.world[i].textString && G.world[i].textString[0] != '\0')
                        mhDrawText(G.world[i].location[0], G.world[i].location[1], G.world[i].textString);
                }

                /*Disable lighting if the object is shadeless*/
                if (G.world[i].shadeless || pickMode)
                {
                    glDisable(GL_LIGHTING);
                }

                /*draw the mesh*/
                glDrawElements(GL_TRIANGLES, G.world[i].nTrigs * 3, GL_UNSIGNED_INT, G.world[i].trigs);

                /*Enable lighting if the object was shadeless*/
                if (G.world[i].shadeless || pickMode)
                {
                    glEnable(GL_LIGHTING);
                }

                if (G.world[i].texture && !pickMode)
                {
                    glDisable(GL_TEXTURE_2D);
                    glDisableClientState(GL_TEXTURE_COORD_ARRAY);
                }

                glPopMatrix();
            }
        }
    }
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
void mhShutDown()
{
    G.loop = 0;
}

/** \brief Queue an update.
 *
 *  This function places an update event into the event queue if there
 *  isn't one pending already. This makes sure we don't create a "traffic
 *  jam" in the event queue when the system is slow in redrawing
 */
void mhQueueUpdate()
{
    SDL_Event ev;

    if (G.pendingUpdate)
        return;

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
        return;

    G.fullscreen = fullscreen;
    
    if (fullscreen)
    {
      G.windowWidth = g_desktopWidth;
      G.windowHeight = g_desktopHeight;
    }
    else
    {
      G.windowWidth = g_windowWidth;
      G.windowHeight = g_windowHeight;
    }

    if (!g_screen)
        return;
    
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
void mhEventLoop()
{
    SDL_ShowCursor(SDL_DISABLE);

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
                SDL_ShowCursor(SDL_DISABLE);
              }
              else
              {
                SDL_ShowCursor(SDL_ENABLE);
#ifdef __WIN32__
                SDL_WM_GrabInput(SDL_GRAB_OFF);
#endif
              }
            }
            break;
        case SDL_KEYDOWN:
            G.modifiersKeyState = event.key.keysym.mod;
            mhKeyDown(event.key.keysym.sym, event.key.keysym.unicode);
            break;
        case SDL_KEYUP:
            G.modifiersKeyState = event.key.keysym.mod;
            if (event.key.keysym.sym == SDLK_F11 || (event.key.keysym.sym == SDLK_RETURN && event.key.keysym.mod & KMOD_ALT))
                mhSetFullscreen(!G.fullscreen); // Switch fullscreen
            else if (event.key.keysym.sym == SDLK_ESCAPE)
                mhShutDown(); // Exit
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
