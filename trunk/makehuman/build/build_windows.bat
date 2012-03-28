rem Set up environment variables necessary for M$ tools
call "C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\bin\vcvars32.bat"

rem Assume build directories as per docs on drupal site
cd c:\mh-build\makehuman

rem update to latest SVN version
svn update

rem Build initial exe
call c:\python27\scons.bat

rem Build installation file and put it in c:\mh-build\dist
del c:\mh-build\dist\makehuman-nightly-win32.exe
call c:\python27\scons.bat dist
move makehuman-nightly-win32.exe c:\mh-build\dist

rem cleanup
rmdir /s /q dist

rem upload (comment/remove the following line if you are building only for yourself)
pscp -i c:\mh-build\private.ppk c:\mh-build\dist\makehuman-nightly-win32.exe joepal1976@ssh.tuxfamily.org:makehuman/makehuman-repository/nightly/
