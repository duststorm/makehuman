call "C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\bin\vcvars32.bat"
cd c:\mh-build\makehuman
svn update
call c:\python27\scons.bat
call c:\python27\scons.bat dist
pscp -i private.ppk dist\makehuman-nightly-win32.exe joepal1976@ssh.tuxfamily.org:makehuman/makehuman-repository/nightly/
rmdir /s /q dist
