IF( COMMAND CMAKE_MINIMUM_REQUIRED )
        CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
ENDIF( COMMAND CMAKE_MINIMUM_REQUIRED )

####################################################################################
# The name of the project
####################################################################################
PROJECT(FontTransFixer)
####################################################################################
# Target OS specific flags.
####################################################################################
IF(NOT APPLE)
    MESSAGE(FATAL_ERROR "This app is for Mac OS X only!")
ENDIF(APPLE)

# Flags for universal build.
SET(CMAKE_OSX_ARCHITECTURES ppc;i386)

# Determine the SDK the source has to build for.
SET(OSX_SDK 10.5)
SET(DEVELOPER_BASEDIR "/Developer3")

SET(CMAKE_OSX_SYSROOT "${DEVELOPER_BASEDIR}/SDKs/MacOSX${OSX_SDK}.sdk")
SET(CMAKE_CXX_COMPILER ${DEVELOPER_BASEDIR}/usr/bin/g++-4.2)

FIND_LIBRARY(COCOA Cocoa)
MARK_AS_ADVANCED (COCOA)
SET(EXTRA_LIBS ${COCOA})

####################################################################################
# Make sure the compiler can find include files from our project.
####################################################################################
INCLUDE_DIRECTORIES (${PROJECT_SOURCE_DIR}/src)

####################################################################################
# The executeable(s) to build to.
####################################################################################
ADD_EXECUTABLE(fontTransFixer src/main.mm)
TARGET_LINK_LIBRARIES(fontTransFixer ${EXTRA_LIBS})

SET_TARGET_PROPERTIES(fontTransFixer PROPERTIES LINK_FLAGS -mmacosx-version-min=${OSX_SDK})

# INSTALL(TARGETS fontTransFixer DESTINATION /usr/bin)
