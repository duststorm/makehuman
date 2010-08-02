To build and run on Linux:


make -f Makefile.Linux

./fixall

Transforms all targets in makehuman/data/targets directories and put the new targets in 
makehuman/utils/fixmesh/data/new/targets folder, from where it can be moved to the desired place.

shapes.py

In Blender, either exports all shapekeys (as .target files) and vertgroups (as .vgroup files) to a
given directory; or, imports all target and vgroup files in the directory and apply them to your mesh.

./fixshapes

Transforms all target and vgroup files in the makehuman/data/target/shapes directory (which you put there
with the shapes.py script) to the makehuman/utils/fixmesh/data/new/targets/shapes folder, from where it
can be importet to the new mesh. For fixing a rigged character with shapekeys.


Preparation.

The program requires that the base meshes (both old and new) have materials with the same names. When looking
for the face on which a vert lies, only faces with the appropriate material will be considered. This means that
e.g. the eyelid will never follow an eye face. I applied materials to the old and new meshes in the file
fixmesh/base/new/newbase.blend. Note in particular how the teeth are assigned.

Files to be put into the fixmesh/base directory:

fixmesh/base/old/base.obj
Old base mesh from the distribution. Contains information about the "part_" face groups. The "UTIL_" face groups
are lost.

fixmesh/base/old/base-mat.obj
Old base mesh with special materials applied for separation of disjoint parts. 

fixmesh/base/old/base-mat.obj
New base mesh with special materials applied for separation of disjoint parts. 

Create the directory tree in fixmesh/data/new, if not already there.



Running

Run ./fixall in the fixmesh directory.

All new targets should now appear in the fixmesh/data/new/targets directory. Move it to the makehuman dir.

There also appears a file fixmesh/base/new/grbase.obj, which contains information about the face groups. 

1. Load grbase.obj into Blender with the standard obj importer. Groups as vertgroups, and no rotate -90 deg.

2. Apply texture coordinates.
I failed to do so automatically, and I would have run into problems at seams anyway.

3. Run blendersaveobject.py
Exports the mesh directly to the MH directory. Again the file path must be edited.



Program switches:

-build
Build the weight table and stores it in wtable.txt. The wtable must exist before conversion can take place.

-fgroup
Construct the face groups and save the grouped base mesh to fixmesh/data/new/grbase.obj.

-vgroup name
Convert the file name.vgroup in data/shapes/ to a file with the same filename in fixmesh/data/new/shapes/.

-convert morph
Convert the morph. The old morph must exist in a subdirectory of data/, and the new morph appears
in the same subdirectory of fixmesh/data/old/. The directory tree must exist.

-view morph
Convert a target file to an obj file, which can be viewed in Blender. For debugging.

-detail D
Specifies that not all verts should be listed in the target file, but only those that have moved a minimal distance.
For use with details and microdetails. The minimal distance is D times the minimal distance in the old target. The
default D = 0.7 seems to work.

-verbosity level
Sets the verbosity level. By default, building should be done with verbosity 1 and converting with verbosity 0, but 
it can be set higher to get more info.

-weight W
It is inevitable that some verts, the projection onto all nearby faces fall outside the face, i.e. some weight is
negative. Therefore we allow for weights between -W and 1+W. Should be set as small as possible to avoid misassignment,
but large enough that all verts can be projected onto some face. The default W = 0.2 seems to work well.

-zone Z
Only faces within the zone of a vert will be considered. Must have Z > 1. The default Z = 2.0 seems to work well.

-dir directory
Sets the fixmesh directory. Equals /home/thomas/fixmesh/ by default.

-obj
Generate an obj file in addition to the target file. For debugging and evaluation of the result.



