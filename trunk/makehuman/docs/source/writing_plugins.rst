.. _writing_plugins:

.. highlight:: python
   :linenothreshold: 5

***************
Writing plugins
***************

.. _plugins:

Plugins
=========


Makehuman has a simple plugin framework which makes it easy to add and remove
features. At startup, MakeHuman now looks for .py files in the plugins folder which are
not starting with an underscore (which makes it easier to disable unwanted plugins).
It loads them one by one and calls the load entry point passing a reference to the
application. The plugin can use this reference to add the necessary GUI widgets or
code to the application.
The rules for plugins are very simple:

* A plugin is a .py file in the plugins folder with a load entry point.
* A plugin only imports core files.

The reason a plugin cannot import other plugins is that it would make it difficult to
know which files belong to which plugin. We still need to define a convention for
shared files beyond the core MakeHuman files. To get started look at example.py or
any of the other plugins to see how you can create your own feature in MakeHuman.

.. _gui:

GUI
====

The GUI in MakeHuman is still far from finished. Since the first alpha there have been
many changes already and many other will come. This is because when features are
added or modified, we can run out of space, or start to see things differently. Some
times we experiment to see how a modifier can be manipulated in a different way. For
example in the details and microdetails we chose to have tools manipulating the model
directly instead of using sliders. Another idea for the macrodetails was a multidimensional
slider, like a radar chart which would replace all five sliders. It is impossible to
pour the GUI into into its final form while we are still adding functionality and getting
new ideas. However don’t let the lack of guidelines stop you from adding a GUI to
your own plugins. The current GUI API is very usable, and gets more mature every day.
The layout at the moment is a two level tab control. The tabs at the top represent
categories, like modeling, files, rendering. The ones at the bottom are the tasks
in the current category and refine the more broad category in macrodetail, detail and
microdetail modeling, or saving, loading and exporting. So when creating your plugin,
the first thought should be "In which category does it belong?". From experience we
know that it can be a though question to answer. Sometimes the only answer is adding
a new category. This is what we initially did for measurement for example

::

    def load(app):
        category = gui3d.Category(app, "Measurement")

Next you probably want your own task to implement your feature. While it’s possible
to attach functionality to an instance of gui3d.Task, it’s often easier to derive your
own class. When you create an instance of your class, you pass the parent of your task,
which can either be an existing category

::

    def load(app):
        taskview = HairPropertiesTaskView(app.categories["Modelling"])

or the new one which you added.

::

    def load(app):
        category = gui3d.Category(app, "Measurement")
        taskview = MeasurementTaskView(category)


In your derived task you will then add the necessary controls to let the user interact.
A good place to see how to use the different controls is the example plugin. You will
see that even if you don’t add any controls, the model is already visible. This is because
the model is attached to the root of the GUI tree. In the onShow event of your task you
might want to reset the camera position, like we do in the save task, or hide the model,
like we do in the load task. Just don’t forget to reset the state when your task gets
hidden in onHide.

.. _morph_targets:

Morph targets
==============

Whatever your plugin does, there’s a big chance that it will modify the model. As
many of you probably know, MakeHuman doesn’t work mathematically or procedural,
but artistically. This means that you don’t just drag vertices when moving a part
of the body, but you actually apply a morph made by an artist. There are different
kind of morphs targets which are applied in different ways. Macro targets, which
are the most complex internally, are ironically the easiest to use: human.setGender,
human.setAge, human.setWeight and human.setMuscle can be used to change the cor
responding macro features. Height was originally not there, so you had to make the
modifier yourself. We will look at that in a moment. Detail and micro detail targets
both come in pairs. For example one target to move a body part to the left, and another
target to move the same body part to the right. Therefore you should never apply both
targets at the same time. This means that when you apply one, and later you want to
apply the other, you need to remove the first. While you could use human.setDetail to
this, it is easier to use the Modifier class which does all of the needed logic behind the
the method modifier.setValue, it has an accompanying modifier.getValue which has the
reverse logic. To use it, you create a modifier passing the two opposite targets:

::

    modifier = humanmodifier.Modifier(
        "data/targets/macrodetails/universalstaturedwarf.target",
        "data/targets/macrodetails/universalstaturegiant.target")
    modifier.setValue(human, 0.0)

A value between 1.0 and 0.0 will use the dwarf target, while a value between 0.0
and 1.0 will use the giant target. Using 0.0 will remove both targets. While using a
modifier also applies the target, to keep changes interactive other targets are not reapplied
and normals are not recalculated. Once you have made the necessary changes,
you commit them using human.applyAllTargets. Which does exactly what it says. It
applies all the targets one by one and additionally recalculates the normals. Reapplying
all targets minimizes the size of mathematical error in the final model.

.. _undoredo:

Undo-redo
=========


One of the first features written was undoredo. Having this from the start saves us
a lot of time later as we add this functionality to each kind of model modification
immediately. It is important that every modification is undoable, since just one undo
able modification would leave the user without the possibility to undo anything. So it’s
crucial that if you write a plugin which modifies the model, you also make undo work.
The Application class has several methods to work with actions. An action is a class
with two methods, do and undo. If the action itself does the modification you can use
app.do to add it to the undo stack. If you did the modification yourself already during
user interaction, you can add the action using app.did. The application won’t call the
do method of the action in that case. If you want to make your own undoredo buttons,
you can use app.undo and app.redo. To illustrate, here is the action we use to change
the hair color:

::

    class Action:
        def __init__(self, human, before, after, postAction = None):
            self.name = "Change hair color"
            self.human = human
            self.before = before
            self.after = after
            self.postAction = postAction

        def do(self):
            self.human.hairColor = self.after
            if self.postAction:
                self.postAction()
            return True

        def undo(self):
            self.human.hairColor = self.before
            if self.postAction:
                self.postAction()
            return True

The postAction is a handy way to specify a method to keep your GUI in sync with
the changes. In this case we update the color control to show the correct color when
the user chooses to undo or redo the hair color change.

.. _meshes:

Meshes
======


When writing exporters, subdivision or polygon reducing algorithms it can be useful
to know how the mesh is stored in Python (the C side has a different compact but
less convenient representation). An Object3D has three important lists: object.verts,
object.faces and object.faceGroups. The first two lists contain instances of Vertex and
Face. The facesGroups contain FaceGroup objects. A FaceGroup specifies the name
of the group and the faces that make up the group. A Face references 3 vertices in
face.verts. A Vert or vertex holds its coordinates in vert.co and normal in vert.no. If we
put all this together, we can write a simple Wavefront object exporter now

::


    f = open(filename,'w')
    for v in obj.verts:
        f.write("v %f %f %f\n" %tuple(v.co))

    for uv in obj.uvValues:
        f.write("vt %f %f\n" %tuple(uv))

    for g in obj.faceGroups:
        f.write("g %s\n" %(g.name))
        for fc in g.faces:
            f.write("f")
            for v in fc.verts:
                f.write(" %i/%i/%i " %(v.idx + 1, fc.uv[i] + 1, v.idx + 1))
    f.close()



As you can see, we take the uv values from obj.uvValues. The uv values are referenced
in two places, obj.uvValues holds all the uv values of each vertex by index.
Face.uv is a list with the uv values of each vertex of the face. The reason is that while
normals are per vertex, uv values are per facevertex, because a vertex can have a different
uv depending on which face is drawn.

.. _the_camera:

The camera
===========

When your plugin allows editing a certain part of the model, it’s often good to focus
the camera on that region. There are two camera’s used in MakeHuman, accessible
from the application class as modelCamera and guiCamera. The camera which we are
interested in is the modelCamera. The application class itself is accessible in every
GUI control as app. A camera has the following properties:

    * fovAngle: The field of view angle.
    * nearPlane: The near clipping plane.
    * farPlane: The far clipping plane.
    * projection: The projection type, 0 for orthogonal, 1 for perspective.
    * stereoMode: The stereo mode, 0 for no stereo, 1 for toein, 2 for offaxis.
    * eyeSeparation: The eye separation.
    * eyeX, eyeY, eyeZ: The position of the eye.
    * focusX, focusY, focusZ: The position of the focus.
    * upX, upY, upZ: The up vector.

The properties you’ll use to position the camera are the eye and focus position. The
Application class has a few methods for camera presets, like setFaceCamera to focus
on the face. We’ll look at what this method does to better understand how to position
the camera:
first we get the currently selected human (yes, we do anticipate having more than
one human in the scene).

::

    human = self.scene3d.selectedHuman

Next we get the vertices which belong to the head by facegroup names.

::

    headNames = [group.name for group in human.meshData.facesGroups if ("head" in
        group.name or "jaw" in group.name)]
    self.headVertices, self.headFaces = human.meshData.getVerticesAndFacesForGroups(
        headNames)

We calculate the center of these vertices as this will become our focus point at
which we will look at.

::

    center = centroid([v.co for v in self.headVertices])

Now we are ready to set the eye and focus positions. We set the focus to the center
position, and the eye a bit to the back.

::

    self.modelCamera.eyeX = center[0]
    self.modelCamera.eyeY = center[1]
    self.modelCamera.eyeZ = 10
    self.modelCamera.focusX = center[0]
    self.modelCamera.focusY = center[1]
    self.modelCamera.focusZ = 0

finally we reset the human’s position and rotation so that our calculations are as
simple as the ones above.

::

    human.setPosition([0.0, 0.0, 0.0])
    human.setRotation([0.0, 0.0, 0.0])

If we would allow the human to be translated and rotated, we would need to take
this transformation into account, as above we calculated the center of the untransformed mesh.

.. _gui_controls:

GUI controls
============

Whether you are writing an exporter, modeling feature or mesh algorithm, sooner or
later you will need to add some controls in order to interact with the user. MakeHuman
has a lot of the usual controls which you find in in other GUI toolkits:

    * Button: A regular push button.
    * ToggleButton: A button which has two states, selected and deselected, clicking the button toggles between the states. Used for making an on/off choice.
    * CheckBox: A togglebutton, but with a check box look.
    * RadioButton: A button which is part of a group, clicking one of the buttons selects it and deselects the others. Used for a multiple choice.
    * Slider: Used to select a value from a discrete or continous range.
    * TextEdit: A one line text field.
    * TextView: A label.
    * GroupBox: Used to group a few controls together under a title.

.. _layout_guidelines:

Layout guidelines
=================

To have a consistent look, it is important that all tasks use the same layout practices.
GroupBoxes on the left side have x=10. The first GroupBox starts at y=80. Controls start
25 pixels lower, and after the last control there are 6 extra pixels (besides the
4 pixels spacing from the last control). So the total height of a GroupBox is 25+con
tent+6. Sliders start at x=10 and are 128 pixels wide, so there is no border left or right.
Buttons start at x=18 and are 112 wide, so there are 8 pixels of border on each side. Between
controls there are 4 pixels. Sliders are 32 pixels high and Buttons are 20 pixels
high. This means that the space to the next control for a Slider is 36, and for a Button
24. So the height of a GroupBox can be calculated as 25+36*sliders+24*buttons+6.
Between GroupBoxes there are 10 pixels.

When creating a GUI, many of these rules are followed automatically. Controls have default styles assigned
which take care of the margin, padding and size of the control. When using GroupBoxes, a BoxLayout will
automatically place the controls in rows or columns. Only on a higher level, namely placing the GroupBoxes
themselves, some custom positioning has to be done, as well as when reacting to screen resizing.

Labels only have the first letter capitalized, unless there is an acronym that needs
to be in uppercase.

.. _Asynchronous:

Asynchronous calls and animation
================================

When doing lengthy operations it is important not to block the GUI from redrawing.
Since everything runs in one thread, it is easy to block the event loop in your plugin.
There are 4 ways to avoid this, depending on the need.
If no user interaction is needed, a progressbar can be used. A progressbar uses
the redrawNow() method of the application. This redraws the screen outside the event
loop. Instead of creating your own progressbar, it is advised to use the progress method,
which uses the global progressbar. Calling progress with a value greater than zero
shows the progressbar, a value of zero hides it.

::

    inc = 1.0 / n
    value = inc
    for i in xrange(n):
        # Shows the progressbar the first time
        self.app.progress(value)
        ...
        value += inc
    # Hides the progressbar
    self.app.progress(0)

If user interaction is desired during the operation, either asynchronous calls, a timer
or a thread can be used.
Asynchronous calls are used when a lengthy operation can be split in several units.
It is used for example in the startup procedure as well as for the plugin loading loop.
The mh.callAsync(method) queues the calling of method in the event loop, so it will
be called when the event gets processed. In case different methods need to be called
after each other, as in the startup procedure, callAsync is used to call the next method.

::

    def method1(self):
        ...
        mh.callAsync(self.method2)

In case of the plugin loading loop, it calls the same method until it is done.

::

    def method(self):
        if continue :
            mh.callAsync(self.method)


This is not to be used for animations, as it takes very little time between calling
callAsync and the event loop calling the method. Calling time.sleep(dt) to avoid this
should not be done as it blocks the main thread. For animations use timers instead. An
example of this can be found in the BvhPlayer plugin. The method mh.addTimer(interval,
method) adds a timer which calls the given method every interval milliseconds.
It returns a value to be used by removeTimer to stop the timer.

::

    def play(self):
        self.timer = mh.addTimer(33, self.nextFrame)

    def pause(self):
        mh.removeTimer(self.timer)

    def nextframe(self):
        ...

If a lengthy operation includes blocking on sockets or pipes, it is advised to use a
python thread. However this has been shown to be problematic on Linux. To get around the problems
on linux you should not access any makehuman structures from within your thread,
but use mh.callAsync to call the methods from the main thread. See the clock
plugin example for example code on how to use threads correctly.




















