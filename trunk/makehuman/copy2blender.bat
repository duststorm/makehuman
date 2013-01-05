::
:: Utility for copying MH scripts to Blenders addon folder
:: Usage:
:: 
::     copy2blender path\to\addons\folder

echo Copy files to %1

copy .\tools\blender26x\mhx_importer\*.py %1

mkdir %1\makeclothes
copy .\tools\blender26x\makeclothes\*.py %1\makeclothes

mkdir %1\makerig
copy .\tools\blender26x\makerig\*.py %1\makerig

copy .\tools\blender26x\maketarget\maketarget.py %1

mkdir %1\mh_mocap_tool
copy .\tools\blender26x\mh_mocap_tool\*.py %1\mh_mocap_tool
mkdir %1\mh_mocap_tool\target_rigs
copy .\tools\blender26x\mh_mocap_tool\target_rigs\*.trg %1\mh_mocap_tool\target_rigs

echo All files copied




