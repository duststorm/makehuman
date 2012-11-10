#OS X 10.6/7
rm -rf os-x/build
rm -f makehuman-nightly-osx_10.6+.zip
export PATH=/Applications/Xcode.app/Contents/Developer/usr/bin:$PATH
svn update
make -f Makefile.osx clean
make -f Makefile.osx nightlybuild
pushd os-x/build/NightlyBuild
zip -9 -r ../../../makehuman-nightly-osx.zip Makehuman.app
popd
#exit
#OS X 10.5
rm -rf os-x/build
rm -f makehuman-nightly-osx_10.5.zip
OLDPATH=$PATH
export PATH=/Users/gogii/MH/XCode3/usr/bin:$PATH
svn update
make -f Makefile.osx clean
make -f Makefile.osx nightlybuild_10.5
pushd os-x/build/NightlyBuild_10.5Universal
zip -9 -r ../../../makehuman-nightly-osx_10.5.zip Makehuman.app
popd
export PATH=$OLDPATH
#upload
rsync -av makehuman-nightly-osx.zip netjunki@ssh.tuxfamily.org:makehuman/makehuman-repository/nightly/makehuman-nightly-osx.zip
rsync -av makehuman-nightly-osx_10.5.zip netjunki@ssh.tuxfamily.org:makehuman/makehuman-repository/nightly/makehuman-nightly-osx_10.5.zip
