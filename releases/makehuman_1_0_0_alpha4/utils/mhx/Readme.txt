MHX - MakeHuman to Blender eXchange

The purpose of these scripts is to transfer information from MakeHuman to Blender 
and back. To achieve this goal we export to a custom format called MHX (MakeHuman 
eXchange), which can then be imported into Blender.

The MHX format is described in the document "MHX format.txt".

This is version 0.2. It is not compatible with the previous versions.

The weighting and morphs can be modified in the file makehuman/utils/mhx/mhxbase.blend 
and exported to a new mhxbase.mhx. 


Changes since version 0.1:

1. The MHX syntax has been revised, and it is now separated from semantics.

2. The MHX semantics has been greately expanded to cover most python-accessible parts
of Blender. One can export a Blender file with mhx_export.py and import it back with
mhx_import.py, and most features are intact. Some of the limitations are apparently
due to bugs in Blender's python interface.

3. The option for rotating the mesh and rig 90 degrees has been removed. It became to
difficult to maintain it with the new functionality.

4. The imported file may either be merged with the existing scene, or completely replace it.

5. The rigging and shape keys have not been changed. This will be done when the new mesh
is available.



Preparations:

Copy mhx_import.py and mhx_export.py from the makehuman/utils/mhx folder to your Blender
scripts folder. The variable TexDir at the beginning of mhx_import.py may be modified to 
point to your texture directory. 

VERY IMPORTANT: Load pydrivers.py into your Blender file before importing the mhx file.
Otherwise the shape keys will not work.


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
4. Shape keys.
5. Replace scene or merge with scene.
6. Default texture directory.

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




