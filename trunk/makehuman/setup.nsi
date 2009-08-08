Name Makehuman
OutFile setup.exe
LicenseData license.txt

InstallDir $PROGRAMFILES\Makehuman

Page license
Page directory
Page instfiles

Section "Copy files"

  # Copy root files
  SetOutPath $INSTDIR
  File makehuman.exe
  File mh.pyd
  File *.dll
  File main.py
  File license.txt

  # Copy data files
  SetOutPath $INSTDIR\data
  File /r /x .svn data\3dobjs
  SetOutPath $INSTDIR\data
  File /r /x .svn data\hairs
  SetOutPath $INSTDIR\data
  File /r /x .svn data\povray
  SetOutPath $INSTDIR\data
  File /r /x .svn data\rotations
  
  # Copy shaders
  SetOutPath $INSTDIR\data\shaders\3delight
  File /r /x .svn data\shaders\3delight\*.sl
  SetOutPath $INSTDIR\data\shaders\aqsis
  File /r /x .svn data\shaders\aqsis\*.sl
  SetOutPath $INSTDIR\data\shaders\pixie
  File /r /x .svn data\shaders\pixie\*.sl
  SetOutPath $INSTDIR\data\shaders\renderman
  File /r /x .svn data\shaders\renderman\*.sl
  
  # Copy targets
  SetOutPath $INSTDIR\data\targets\details
  File /r /x .svn data\targets\details\*.target
  SetOutPath $INSTDIR\data\targets\macrodetails
  File /r /x .svn data\targets\macrodetails\*.target
  SetOutPath $INSTDIR\data\targets\microdetails
  File /r /x .svn data\targets\microdetails\*.target
  
  # Copy textures
  SetOutPath $INSTDIR\data\textures
  File /r /x .svn data\textures\*.tif
  
  # Copy themes
  SetOutPath $INSTDIR\data
  File /r /x .svn data\themes
  
  # Copy docs
  SetOutPath $INSTDIR\doc
  File /r /x .svn docs\*.pdf

  # Copy python files
  SetOutPath $INSTDIR\mh_core
  File /r /x .svn mh_core\*.py
  SetOutPath $INSTDIR\mh_plugins
  File /r /x .svn mh_plugins\*.py
  SetOutPath $INSTDIR\pythonmodules
  File /r /x .svn pythonmodules\*.py
  
  CreateDirectory $INSTDIR\models
  CreateDirectory $INSTDIR\exports
  
SectionEnd

Section "Create uninstaller"
  
  WriteUninstaller $INSTDIR\Uninst.exe
  
SectionEnd

Section "Create shortcuts"

  CreateDirectory "$SMPROGRAMS\Makehuman"
  SetOutPath $INSTDIR
  CreateShortCut "$SMPROGRAMS\Makehuman\Makehuman.lnk" "$INSTDIR\makehuman.exe" \
    "" "$INSTDIR\makehuman.exe" 2 SW_SHOWNORMAL ""  "Makehuman"
  CreateShortCut "$SMPROGRAMS\Makehuman\Uninstall.lnk" "$INSTDIR\Uninst.exe" \
    "" "$INSTDIR\Uninst.exe" 2 SW_SHOWNORMAL ""  "Uninstall Makehuman"
    
SectionEnd

Section "Uninstall"

  # Remove Makehuman files
  Delete $INSTDIR\makehuman.exe
  Delete $INSTDIR\mh.pyd
  Delete $INSTDIR\*.dll
  Delete $INSTDIR\main.py
  Delete $INSTDIR\license.txt
  
  # Remove Makehuman data folders
  RMDir /r $INSTDIR\data
  RMDir /r $INSTDIR\docs
  RMDir /r $INSTDIR\mh_core
  RMDir /r $INSTDIR\mh_plugins
  RMDir /r $INSTDIR\pythonmodules
  
  # Remove uninstaller
  Delete $INSTDIR\Uninst.exe
  
  # Remove remaining Makehuman folders if empty
  RMDir $INSTDIR\models
  RMDir $INSTDIR\exports
  RMDir $INSTDIR
  
  # Remove shortcuts
  Delete $SMPROGRAMS\Makehuman\Makehuman.lnk
  Delete $SMPROGRAMS\Makehuman\Uninstall.lnk
  RMDir $SMPROGRAMS\Makehuman
  
SectionEnd
