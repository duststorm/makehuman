This is an utity to be used for:

1) Fit mesh1 obj to the morphed (loading a target file) mesh2 and then save a mesh1 target.
2) Fit mesh1 obj to mesh2 obj and then save a mesh1 target.

Examples.

a) Build a "diff.data" file, that link the mesh1.obj vertices to mesh2.obj vertices:

python topology_translator.py --build --tofit mesh1.obj --mold mesh2.obj --datafile diff.data

b) Convert test.target from mesh2 topology to mesh1 topology, using the diff.data
The target is automatically saved in convert/test.target (it use the same name of the original)

python topology_translator.py --tofit baseNew.obj --mold baseOld.obj --target test.target --datafile diff.data

c) Create a target for mesh1.obj topology, using an obj mesh2.obj as reference.
The target is automatically saved in convert/mesh1.obj.target

python topology_translator.py  --tofit mesh1.obj --mold mesh2.obj --datafile diff.data

d) For debug only. Save a the subdivided version of an obj.

python topology_translator.py --testobj mesh1.obj

