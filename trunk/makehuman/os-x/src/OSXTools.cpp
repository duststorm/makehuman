/*
 *  Copyright (C) 2009 MakeHuman Project
 *
 *  This program is free software; you  can  redistribute  it  and/or
 *  modify  it  under  the terms of the GNU General Public License as
 *  published by the Free Software Foundation; either  version  2  of
 *  the License, or (at your option) any later version.
 *
 *  This  program  is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the  implied  warranty  of
 *  MERCHANTABILITY  or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 *  General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software Foun-
 *  dation, Inc., 59 Temple Place, Suite 330, Boston,  MA  02111-1307
 *  USA
 *  
 *  File   : OSXTools.cpp
 *  Project: MakeHuman <info@makehuman.org>, http://www.makehuman.org/
 *  App    : makehuman
 *  Author : Hans-Peter Dusel <hdusel@tangerine-soft.de>
 *
 *  For individual developers look into the AUTHORS file.
 *   
 */

#include <libgen.h>
#include <stdlib.h>
#include <unistd.h>
#include <cstring>
#include <cassert>
#include <string>
#include "OSXTools.h"

// Adjust the working dir in order to relocate to the application resources directory.
int adjustWorkingDir(const char* inAppAbsPath)
{
    /* Redirect the current working dir into the applications package resource directory because
     * the dirs 'data', '3dobjs' mh_core' and 'mh_plugins' are located there. 
     */

    // Get the apps exec location which is 'MHPhoenix.app/Contents/MacOS'
    char *tmp_currwd = dirname((char*)inAppAbsPath);

    /* Now this path is supposed to bechanged to the 'Resources' directory be appending
     * '/../Resources/' which actually makes 'MakeHuman.app/Contents/MacOS/../Resources/' 
     */ 
    int len1 = strlen(tmp_currwd); // Remember the length of the canonical path for 'MakeHuman.app/Contents/MacOS'
    const char *appStr="/../Resources/"; // The recources are reside here.
    int len = len1 + strlen(appStr) + 1; // calcualte the absolute name of the path (including NUL byte)

    char *currwd = (char*)malloc(len); // allocate the memory.
    assert(NULL != currwd);

    if (NULL != currwd)
    {
        // Append the strings
        strcpy(currwd, tmp_currwd);
        strcpy(&currwd[len1], appStr);

        chdir(currwd); // And change the current working dir to this path
        free(currwd);  // Release the memory again
        return 0; // indicate success
    }
    return -1; // indicate failure
}

/** Gets the value of a particular Environment variable as a string.
  *
  * \param inEnvVarName The name of the Environment variable to get the value from.
  * \param outValue     A pointer to a string which is supposed to be the target for the content 
  *                     of the env var. This can be NULL if you just want to check if the given 
  *                     environment variable existst.
  *
  * \return 0 for success, -1 for failure (if the requested env var does not exists).
  *
  * \see setEnvVar(const std::string&, const std::string&)
  *
  * \author Hans-Peter Dusel <hdusel@tangerine-soft.de>
  */
static int getEnvVar(const std::string& inEnvVarName, std::string* outValue)
{
    const char *envVar = getenv(inEnvVarName.c_str());
    if (NULL == envVar)
    {
        return -1; // indicate "error"
    }
    
    if (NULL != outValue)
    {
        *outValue = envVar;
    }
    return 0; // success
}

/** Sets the value of a particular Environment variable as a string. 
  * The Env-Var is set disregard whether the given environment variable already exists.
  *
  * \param inEnvVarName The name of the Environment variable to set the value to.
  * \param inValue      The actual value (as a string) which has to be assigned to inEnvVarName.
  *
  * \return 0 for success, -1 for failure.
  *
  * \see getEnvVar(const std::string&, std::string*)
  *
  * \author Hans-Peter Dusel <hdusel@tangerine-soft.de>
  */
static int setEnvVar(const std::string& inEnvVarName, const std::string& inValue)
{
    int rc = ::setenv(inEnvVarName.c_str(), inValue.c_str(), 1);
    return (0 == rc) ? 0 : -1;
}

int adjustRenderEnvironment()
{
    std::string path;
    int rc = getEnvVar("PATH", &path);
    if (0 != rc)
    {    
        return -1; // error    
    }

    // -----------------------------------------------------------------
    // Adjust Aqsis
    const std::string kPathAqsis    = "/Applications/Aqsis.app/Contents/";
    path.append(":" + kPathAqsis + "MacOS/");
    rc = setEnvVar("AQSIS_DISPLAY_PATH", kPathAqsis + "Resources/lib/");
    if (0 != rc)
    {
        return -1; // error    
    }

    // -----------------------------------------------------------------
    // Adjust Pixie
    const std::string kPathPixie    = "/Library/Pixie/";
    path.append(":" + kPathPixie + "bin/");

    // -----------------------------------------------------------------
    // Adjust 3Delight
    const std::string kPath3Delight = "/Applications/Graphics/3Delight-8.5.0/";
    path.append(":" + kPath3Delight + "bin/");
    rc = setEnvVar("DELIGHT", kPath3Delight);
    if (0 != rc)
    {    
        return -1; // error    
    }


    rc = setEnvVar("PATH", path.c_str());
    if (0 != rc)
    {    
        return -1; // error    
    }
    return 0; // success
}
