#Build the data file to convert targets from a no_makehuman.obj to makehuman.obj
#python topology_translator.py --tofit  makehuman.obj --mold no_makehuman.obj --build --datafile diff.data

#Build the datafile to convert targets from baseOld.obj to baseNew.obj
#python topology_translator.py --tofit  baseNew.obj --mold baseOld.obj --build --datafile morph.data

#Convert test.target from baseOld.obj to baseNew.obj
python topology_translator.py --tofit baseNew.obj --mold baseOld.obj --target test.target --datafile morph.data

#make a target fitting base.obj to random1.obj
#python topology_translator.py --tofit base.obj --mold random1.obj --datafile diff.data

#Convert all meshes in the folder called "testfaces" in targets, using as base base.obj. (Note that the mesh used to build diff.data must have the same topology of base.obj)
#python topology_translator.py --tofit base.obj --datafile diff.data --targetbase base.obj --folder testfaces

