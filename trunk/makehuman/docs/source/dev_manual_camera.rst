
.. highlight:: python
   :linenothreshold: 5

.. _the_camera:

The camera
===========

When your plugin allows editing a certain part of the model, it’s often good to focus the camera on that region. There are two camera’s used in MakeHuman, accessible from the application class as modelCamera and guiCamera. 

The camera which we are interested in is the modelCamera. The application class itself is accessible in every GUI control as app. A camera has the following properties:

* fovAngle: The field of view angle.
* nearPlane: The near clipping plane.
* farPlane: The far clipping plane.
* projection: The projection type, 0 for orthogonal, 1 for perspective.
* stereoMode: The stereo mode, 0 for no stereo, 1 for toein, 2 for offaxis.
* eyeSeparation: The eye separation.
* eyeX, eyeY, eyeZ: The position of the eye.
* focusX, focusY, focusZ: The position of the focus.
* upX, upY, upZ: The up vector.

The properties you’ll use to position the camera are the eye and focus position. The Application class has a few methods for camera presets, like setFaceCamera to focus on the face. We’ll look at what this method does to better understand how to position the camera: first we get the currently selected human (yes, we do anticipate having more than one human in the scene).

::

    human = self.scene3d.selectedHuman

Next we get the vertices which belong to the head by facegroup names.

::

    headNames = [group.name for group in human.meshData.facesGroups if ("head" in
        group.name or "jaw" in group.name)]
    self.headVertices, self.headFaces = human.meshData.getVerticesAndFacesForGroups(
        headNames)

We calculate the center of these vertices as this will become our focus point at which we will look at.

::

    center = centroid([v.co for v in self.headVertices])

Now we are ready to set the eye and focus positions. We set the focus to the center position, and the eye a bit to the back.

::

    self.modelCamera.eyeX = center[0]
    self.modelCamera.eyeY = center[1]
    self.modelCamera.eyeZ = 10
    self.modelCamera.focusX = center[0]
    self.modelCamera.focusY = center[1]
    self.modelCamera.focusZ = 0

finally we reset the human’s position and rotation so that our calculations are as simple as the ones above.

::

    human.setPosition([0.0, 0.0, 0.0])
    human.setRotation([0.0, 0.0, 0.0])

If we would allow the human to be translated and rotated, we would need to take this transformation into account, as above we calculated the center of the untransformed mesh.
