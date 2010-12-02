
#!/bin/bash

for file in toconvert/*
do
       if [ -f "$file" ]; then
               python topology_translator.py --tofit baseNew.obj --mold baseOld.obj --target $file --datafile morph.data
       fi
done
