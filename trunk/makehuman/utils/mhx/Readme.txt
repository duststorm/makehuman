MHX - MakeHuman to Blender eXchange

The purpose of these scripts is to transfer information from MakeHuman to Blender, and to some
extent back. To achieve this goal we export to a custom format called MHX (MakeHuman eXchange),
which can then be imported into Blender. The format is described in the document 
"MHX format.txt".

This is version 0.1. It is not compatible with the previous, unnumbered version.

New features:

1. There is a (minimal) user interface. Files are now selected by a file selector 
instead of being hardcoded.

2. The script can be registered with Blender. Just copy mhx_import.py to your Blender
scripts follow, and it should appear in the File > Import meny as "MakeHuman (.mhx)".

3. There is an option for rotating the mesh and rig 90 degrees, to get the head up.

4. The rig has been completely remade. It has the following new features.

	a. Arm FK and IK.

	b. Leg FK and IK, with an inverse foot setup.

	c. Finger FK and IK, a la Bassam Kurdali.

	d. Gaze bone for eye tracking.

	e. Bone layers.

	f. Display objects for bones

5. The mesh has a number of shape keys for morphing. Since the morphs were made on the base
mesh, they will work more or less well depending on how much the character deviates from the 
base mesh. 

The shape keys can be turned off, to reduce load time and file size. This should be done if
you plan on modifying the mesh, e.g. to add clothes, since that will ruin the shape keys
anyway.

The weighting and morphs can be modified in the file base03.blend and exported to a new 
mhxbase.mhx. 



Preparations:

* Copy mhx_import.py to your Blender scripts folder. The variable TexDir at the end of
this file should be modified to point to your texture directory.

* Copy mhxbase.mhx to makehuman/data/3dobjs

* Copy mh2mhx.py and mhxbones.py to makehuman/mh_plugins

* Edit the files guifiles.py and guimodelling.py in the makehuman/mh_plugins directory.
Everywhere where there is a reference to mh2obj (there are two places in each file), add an
analogous statement for mh2mhx. Thus, in guifiles.py,

change line 33 from:
import files3d, animation3d, gui3d, events3d, os, mh2obj, mh2bvh
to:
import files3d, animation3d, gui3d, events3d, os, mh2obj, mh2bvh, mh2mhx

and after line 170:
      mh2obj.exportObj(self.app.scene3d.selectedHuman.meshData, "exports/" + filename + ".obj")
add the line:
      mh2mhx.exportMhx(self.app.scene3d.selectedHuman.meshData, "exports/" + filename + ".mhx")

There are two analogous patches to be made in guimodelling.py.


Usage:

Run MakeHuman as usual and export your mesh. If you gave it the name foo, the makehuman/export
folder will now contain a file called foo.mhx, in addition to the usual foo.obj, foo.obj.mtl,
and foo.bvh. If you have copied mhx_import.py to your scripts folder, the menu File > Import
should now have the option "MakeHuman eXchange (.mhx)". If the choice is not there, you can
load mhx_import.py in your text window instead. You will now be prompted with the MHX
importer's user interface. First there are some choices to be made:

1. Arm IK or FK.
2. Leg IK or FK.
3. Finger IK or FK.
4. Rotate mesh and rig 90 degrees.

Pressing "Load MHX" will now allow you to select the MHX file in the MH export directory.
Hopefully the rigged and weighted mesh is now loaded into Blender. As a final step, you need
to make the armature modifier real and uncheck envelopes (I haven't figured out how to do that
in python).


Bone layers:
The bones are separated into different bone layers to unclutter the view for the animator:

1. All deform bones.
2. Torso
3. Arm IK
4. Arm FK
5. Leg IK
6. Leg FK
7. Hand IK
8. Hand FK

9. Root bone
10. Indiviual toes.
11. Head

16. Hidden helper bones.


Vertex weighting:

The vertex weighting is not very good, but at least the character can open his/her mouth. And
unlike OBJ/BVH import, the mesh and the rig appear at the same place. To improve the weighting,
edit the file base.blend, which contains the rigged base mesh, and use the script mhx_export.py
to export to mhxbase.mhx (again, you need to edit the file to reflect the location of MakeHuman
on your machine). I didn't put a lot of effort into this export-from-Blender script, but it
gets the vertex weighting right, which is what matters at this time.


Known issues:

IK does not work terribly well, especially for the fingers.

One can choose between FK/IK at load time. It should be driven by bone instead,
but I have not figured out how to implement driven constraint influence from a Python
script. If somebody has done that, I would be interested to see a code example.

Also shape keys should be driven by bones.

Display objects should be in wireframe, but I haven't figured out how to press the W button 
from python. Also, only the outline should be shown.

The Blender import script did not register on my Linux machine, but it works nicely under
Windows (XP).


