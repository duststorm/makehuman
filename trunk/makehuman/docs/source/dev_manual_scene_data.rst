.. _scene_data:

.. highlight:: python
   :linenothreshold: 5

Scene data
===========

 A scene is stored as a flat object list, there is no hierarchy and thus no transformations or properties are inherited. This means that if a model wears clothes, the clothes need to undergo the same transform as the model, it is not automatic. Besides the object list, the scene also contains a dictionary of 'false' colors for each object, this enables the system to work out which object the user has clicked on by comparing it with an image generated from the current camera position using these false colors.
 
Object
---------

.. warning::
    Editorial Note: to update

An object is used to represent an object that can appear on the screen. This can be the humanoid object or one of the GUI objects. An object has a name to identify it in the scene. It also holds an index to the corresponding object in the array of C objects. For transformation it holds translation, rotation and scale settings and for the purposes of selection it holds a selection color. The object includes lists of vertices, faces and facegroups to enable it to be rendered. Other object properties which affect the rendering are cameraMode, visibility, texture, hasTexture and shadeless.

Facegroup
----------

Editorial Note: to update
A face group represents a discrete, named group of faces within an object. The facegroup contains a name, a list of faces and the name of the object it belongs to.

Face
-----

.. warning::
    Editorial Note: to update
    
Each face represents an individual triangular face that goes to make up an object. A face has a list of 3 vertices (since it is always a triangle), a normal, its index in the list of faces, the name of the facegroup it belongs to, 3 vertex colors, a selection color and 3 uv coordinates.

Vertex
----------

.. warning::
    Editorial Note: to update
    
    
A vertex represents each vertex of each face of an object. A vertex contains coordinates, a normal, the index of the object this vertex belongs to, a list of indexes of faces and a list of faces which refer to this vertex, a list of corresponding C vertex indices, the index in the verts list of the object this vertex belongs to. 
