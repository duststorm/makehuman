
.. highlight:: python
   :linenothreshold: 5

.. _undoredo:

##########
Undo-redo
##########


One of the first features written was undoredo. Having this from the start saves us a lot of time later as we add this functionality to each kind of model modification immediately. It is important that every modification is undoable, since just one undo able modification would leave the user without the possibility to undo anything. So it’s crucial that if you write a plugin which modifies the model, you also make undo work. 

The Application class has several methods to work with actions. An action is a class with two methods, do and undo. If the action itself does the modification you can use app.do to add it to the undo stack. If you did the modification yourself already during user interaction, you can add the action using app.did. The application won’t call the do method of the action in that case. 

If you want to make your own undoredo buttons, you can use app.undo and app.redo. To illustrate, here is the action we use to change the hair color:

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

The postAction is a handy way to specify a method to keep your GUI in sync with the changes. In this case we update the color control to show the correct color when the user chooses to undo or redo the hair color change.

********
Meshes
********


When writing exporters, subdivision or polygon reducing algorithms it can be useful to know how the mesh is stored in Python (the C side has a different compact but less convenient representation). 

An Object3D has three important lists: object.verts, object.faces and object.faceGroups. The first two lists contain instances of Vertex and Face. The facesGroups contain FaceGroup objects. A FaceGroup specifies the name of the group and the faces that make up the group. A Face references 3 vertices in face.verts. A Vert or vertex holds its coordinates in vert.co and normal in vert.no. If we put all this together, we can write a simple Wavefront object exporter now

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



As you can see, we take the uv values from obj.uvValues. The uv values are referenced in two places, obj.uvValues holds all the uv values of each vertex by index.

Face.uv is a list with the uv values of each vertex of the face. The reason is that while normals are per vertex, uv values are per facevertex, because a vertex can have a different uv depending on which face is drawn.

