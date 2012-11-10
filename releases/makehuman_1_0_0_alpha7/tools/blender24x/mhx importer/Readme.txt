MHX - MakeHuman to Blender eXchange

The purpose of these scripts is to transfer information from MakeHuman to Blender 
and back. To achieve this goal we export to a custom format called MHX (MakeHuman 
eXchange), which can then be imported into Blender.

The MHX format is described in the document "MHX format.txt".

This is version 0.3. It is not compatible with the previous versions.



Preparations:

Copy mhx_import.py and mhx_export.py from the makehuman/importers/mhx/blender249 folder 
to your Blender scripts folder. 

The import script only works with Blender 2.49b. In earlier versions there is a bug in 
Blender's python API which makes the script crash (one can not access a bone display object 
from python). A version for Blender 2.5x will come later.

Load the pydrivers.py into a text editor window in Blender before importing the mhx file. 
Otherwise the shape keys will not work. The file should only be loaded into Blender, not 
executed.


Usage:

Run MakeHuman as usual and export your mesh. If you gave it the name foo, the makehuman/export
folder will now contain a file called foo.mhx, in addition to the usual foo.obj, foo.obj.mtl,
and foo.bvh. If you have copied mhx_import.py to your scripts folder, the menu File > Import
should now have the option "MakeHuman eXchange (.mhx)". If the choice is not there, you can
load mhx_import.py in your text window instead. You will now be prompted with the MHX
importer's user interface. First there are some choices to be made:

1. Enable FK/IK switch
2. Arm IK or FK (if FK/IK switch not enabled).
3. Leg IK or FK (if FK/IK switch not enabled).
4. Finger IK or FK.
5. Facial shape keys.
6. Body shape keys, to preserve volume.
7. Replace scene or merge with scene.
8. Default texture directory. 
9. Rotate the character 90 degrees to make the head point up (Z up convention).
10. Use display objects for bones.

Pressing "Load MHX" will now allow you to select the MHX file in the MH export directory.
Hopefully the rigged and weighted mesh is now loaded into Blender. As a final step, you need
to make the armature modifier real and uncheck envelopes (I haven't figured out how to do that
in python).


Bone layers:
The bones are separated into different bone layers to unclutter the view for the animator:

1. All control bones for FK.
2. Torso
3. Arm IK
4. Arm FK
5. Leg IK
6. Leg FK
7. Hand IK
8. Hand FK

9. Panel
10. Indiviual toes.
11. Head

18. Root bone.
19. All deform bones.
20. Hidden helper bones.


Vertex weighting:

The vertex weighting is not very good, but at least the character can open his/her mouth. And
unlike OBJ/BVH import, the mesh and the rig appear at the same place. To improve the weighting,
edit the file base.blend, which contains the rigged base mesh, and use the script mhx_export.py
to export to mhxbase.mhx (again, you need to edit the file to reflect the location of MakeHuman
on your machine). I didn't put a lot of effort into this export-from-Blender script, but it
gets the vertex weighting right, which is what matters at this time.


Some links where aspects of MHX import are discussed:

Generalities: 			http://makehuman.blogspot.com/2009/11/blender-export-with-mhx-format.html
Shape keys: 			http://makehuman.blogspot.com/2009/11/bones-that-bend.html
Z up: 				http://makehuman.blogspot.com/2009/11/z-up-last-week-i-have-struggled-with.html
FK/IK switch: 			http://makehuman.blogspot.com/2009/12/fkik-switch.html
Problems with FK/IK switch:	http://makehuman.blogspot.com/2010/01/problems-with-fkik-switch.html



Known issues:

1. IK does not work terribly well, especially for the fingers.

2. FK/IK switching does not update in real time. Therefore it is also possible to 
choose between FK/IK at load time.

3. The Blender import script does not always register. It does not show up in Blender's 
import menu on my Linux machine, but it works nicely under Windows (XP).

4. On Linux (or at least Ubuntu), Blender does not recognize the texture images in tif
format. Workaround: convert the textures to png and make the corresponding changes in the
file makehuman/data/3dobjs/mxhbase.mhx. There are three lines starting with the word
"filename". This problem does not appear under Windows.

5. The artistic quality of the shape keys is poor. They will be replaced once the proper pose
engine is in place.





