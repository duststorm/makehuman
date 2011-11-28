
.. highlight:: python
   :linenothreshold: 5


.. _opengl_notes:

################
OpenGL Notes
################

Most of the 3D mesh handling functionality is delivered using OpenGL embedded within the C application code. OpenGL is a 3D graphics library that enables a 3D world to be defined, with a camera, objects, lights, textures etc. 

It then enables that 3D world to be visualised as a 2D representation that can be displayed on a computer screen and provides functions to enable an application (in response to user input) to navigate around the scene.

********
Basics
********

OpenGL takes a 3D scene and draws it into a 2D viewing area on your screen known as the viewport.

OpenGL can project the scene onto the viewport in a variety of different ways, but the most common are:

* Perspective projection, as you would get if you could place a camera in the scene
* Orthographic projection, as a draftsman may contstruct technical drawings such as plans and elevations.

MakeHuman only uses Perspective projection.

***************************
Projection Transformation 
***************************

You tell OpenGL how to project 3D objects onto the 2D viewport by defining a projection transformation, which indicates whether you wish to use perspective or orthographic projection (or an alternative projection pattern) and specifies other projection settings.

This can be imagined as being comparable to specifying the characteristics of a camera (field of view, aspect ratio etc.) where an orthographic projection is equivalent to a camera at an infinite distance. 

The main difference being that with OpenGL you can change the settings between drawing different objects, which is a bit like taking a photo, changing the lens and moving the camera, then taking another photo without winding the film on.

MakeHuman sets a perspective projection using the function gluPerspective(fovAngle,aspectRatio,near,far) where:

* fovAngle: is the vertical field of view angle (45 degrees)
* aspectRatio: is the viewport width divided by the viewport height which, by default, is 800/600 (4/3)
* near: is the distance to the centre of the viewing plane (0.1)
* far: is the distance to the centre of the rear clippling plane (100)

*************************
Modelview Transformation 
*************************

For OpenGL to know what to display in the viewport it also needs to know where the camera is relative to the 3D model. For this you need to define a modelview which defines the position and orientation of the camera and the position and orientation of objects that go to make up the model inside a virtual 3D world. 

You do this by moving through and around the 3D world and by creating objects relative to your current position. OpenGL keeps track of your current position and orientation in the 3D world by recording the modelview transformation.

Both the projection transformation and the modelview transformation are stored internally in 4x4 transformation matrices. You can modify these matrices by calling functions that apply direct transformations (translations and rotations) or by calling functions that calculate transformations (e.g. the gluPerspective function outlined above). 

To apply transformations you need to first make one of these matrices the current matrix. Subsequent transformations are applied cumulatively to the current matrix. The glMatrixMode function is used to set the current matrix mode:

* glMatrixMode(GL_PROJECTION) makes the projection transformation the current matrix so that projection settings can be applied, such as the Field of View angle and Aspect Ratio.
* glMatrixMode(GL_MODELVIEW) makes the modelview transformation matrix the current matrix so that subsequent translations and rotations move the current location through the 3D world.

************************************
Resetting a transformation matrix
************************************

Matrix transformations that you apply are applied cumulatively. It is therefore often necessary to reset the matrix to its default 'no transformation' state so that you can apply a fresh set of transformations. OpenGL uses the transformation and modelview matrices to transform coordinates by performing a matrix multiplication. If you multiply by an identity matrix then the result is the same as the thing you started with, so to reset one of these matrices to an initial state where the transformation has no effect you can simply load the identity matrix using the function glLoadIdentity(). This loads the identity matrix into whichever transformation matrix is currently active, resetting it to the default 'no transformation' state.

*************
Coordinates
*************

OpenGL world space coordinates are unitless, so 2 units can represent milimeters, inches or light years. Interpretation of world space coordinates is up to the application. OpenGL uses a right handed coordinate system, so, if you are looking at the origin with the +X axis stretching away to the right and the +Y axis pointing straight up, the +Z axis will be heading out of the screen straight towards you and the -Z axis will be dissapearing away from you into the distance.

MakeHuman uses the default OpenGL modelview camera settings which are equivalent to invoking gluLookAt(0,0,0, 0,0,-1, 0,1,0). This places the camera at the origin, looking straight into the model along the -Z axis with the +Y axis pointing straight up. This means that a 2 unit wide and 2 unit high object centred at <0,0,-1> will roughly fill the viewport, as will a 4x4 object at twice the distance from the viewpoint.

*****************
Drawing objects
*****************

MakeHuman contains multiple objects. The Humanoid object is the main object, but it is surrounded by a set of control objects. Each object is constructed using triangular faces. The position and orientation of each face is defined relative to the object of which it is a part. 

The positions and orientations of the vertices and normals of the faces are defined relative to the face they're on. The sequence in which face vertices are defined is significant in OpenGL. If the face is viewed from the front, the sequence of points runs counter clockwise. 

If the face is viewed from the back the points run clockwise. Faces viewed from behind may be invisible or may have a different color/texture defined to the front face.
The glPushMatrix and glPopMatrix functions can be used to store away a copy of a matrix that can subsequently restored. MakeHuman uses this before and after drawing each object to store a copy of the modelview matrix and restore it.
