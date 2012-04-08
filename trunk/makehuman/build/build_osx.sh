rm -rf os-x/build
rm -f makehuman-nightly-osx.zip
make -f Makefile.osx clean
make -f Makefile.osx nightlybuild
pushd os-x/build/NightlyBuild
zip -9 -r ../../../makehuman-nightly-osx.zip Makehuman.app
popd
#upload
