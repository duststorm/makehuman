::
:: Utility for copying MH scripts to Blenders addon folder
:: Usage:
:: 
::     copy2blender path\to\addons\folder

echo Copy files to %1

mkdir %1\makeclothes
copy .\utils\makeclothes\*.py %1\makeclothes

mkdir %1\makerig
copy .\utils\makerig\*.py %1\makerig

copy .\utils\maketarget\maketarget_b25x.py %1

mkdir %1\mh_mocap_tool
copy .\importers\mhx\mh_mocap_tool\*.py %1\mh_mocap_tool
mkdir %1\mh_mocap_tool\target_rigs
copy .\importers\mhx\mh_mocap_tool\target_rigs\*.trg %1\mh_mocap_tool\target_rigs

echo All files copied




