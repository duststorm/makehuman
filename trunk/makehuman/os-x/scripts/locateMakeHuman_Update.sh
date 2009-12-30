#!/bin/sh
# -------------------------------------------------------------------------
# This script is supposed to compensate a bug which was live till 
# MakeHuman1.0alpha4
#
# In MakeHuman prior Version 1.0alpha4 the custom dirs 'export' and 'models' 
# reside within the app bundle.
# So this script is supposed to move these directorys into the target directory 
# ~/Documents/MakeHuman/ because this is the default target beginning with 
# MakeHuman V 1.0 alpha4
#
# This script must be run *before* the installation of the MakeHuman app 
# package will start! 
#

# The base directory of the (old) MakeHuman installation
MH_BASE="/Applications/MakeHuman.app"

# The directory of the resources which (probably) contains the old models / exports
MH_RES_BASE=${MH_BASE}"/Contents/Resources/"

# The destination to which models nd exports dirs has to be moved to.
MH_DOCS_BASE=${HOME}"/Documents/MakeHuman"

MH_EXPORTS=${MH_RES_BASE}"exports/"
MH_MODELS=${MH_RES_BASE}"models/"

# Create the new MakeHuman Directory
mkdir -p ${MH_DOCS_BASE}

# Move the exports...
if [ -e ${MH_EXPORTS} ]; then 
    echo ${MH_EXPORTS}
    mkdir -p ~/Documents/MakeHuman/exports
    cp -r ${MH_EXPORTS}* ${MH_DOCS_BASE}/exports/
    rm -rf ${MH_EXPORTS}
fi

# Move the models...
if [ -e ${MH_MODELS} ]; then 
    mkdir -p ~/Documents/MakeHuman/models
    cp -r ${MH_MODELS}* ${MH_DOCS_BASE}/models/
    rm -rf ${MH_MODELS}
fi

# ...and set the permissions to grant users access.
chown -R ${USER}:${USER} ${MH_DOCS_BASE}

#finally erase the old app
rm -rf ${MAKEHUMAN_BASE}
