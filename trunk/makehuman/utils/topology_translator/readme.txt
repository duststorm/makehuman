This is an utity to be used for:

1) Convert target done for a mesh1 topology to a target for mesh2 topology.
2) Use a mesh2 with arbitrary topology to save a target for mesh1 topology.

Examples.

a) Build a link.dat file, that link the mesh1.obj vertices to mesh2.obj vertices:

python topology_translator.py --build -m mesh1.obj -M mesh2.obj -d link.dat

b) Convert test.target from mesh1 topology to mesh2 topology, using the link.dat
The target is automatically saved in convert/test.target (it use the same name of the original)

python topology_translator.py -m mesh1.obj -M mesh2.obj -t test.target -d link.dat

c) Create a target for mesh1.obj topology, using an obj mesh2.obj as reference.
The target is automatically saved in convert/mesh1.obj.target

python topology_translator.py  -m mesh1.obj -M mesh2.obj -d link.dat



