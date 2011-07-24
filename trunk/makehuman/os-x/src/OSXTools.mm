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
 *  File   : OSXTools.mm
 *  Project: MakeHuman <info@makehuman.org>, http://www.makehuman.org/
 *  App    : makehuman
 *  Author : Hans-Peter Dusel <hdusel@tangerine-soft.de>
 *
 *  For individual developers look into the AUTHORS file.
 *
 */

#include "OSXTools.h"
#include <libgen.h>
#include <stdlib.h>
#include <unistd.h>
#include <cstring>
#include <cassert>
#include <string>
#import "GeneralPreferences.h"
#import "AppPreferences.h"

static bool getSystemVersion(SInt32 *major, SInt32 *minor)
{
    return ((0 == ::Gestalt(gestaltSystemVersionMajor, major)) &&
            (0 == ::Gestalt(gestaltSystemVersionMinor, minor)));
}

int isRunningOnLeopard()
{
    SInt32 major, minor;

    if ( !getSystemVersion(&major, &minor) )
    {
        return false;
    }
    return (major == 10 && minor == 5) ? 1 : 0;
}

int isRunningOnSnowLeopard()
{
    SInt32 major, minor;

    if ( !getSystemVersion(&major, &minor) )
    {
        return false;
    }
    return (major == 10 && minor == 6) ? 1 : 0;
}

int isRunningOnLion()
{
    SInt32 major, minor;

    if ( !getSystemVersion(&major, &minor) )
    {
        return false; // no info available
    }
    return (major == 10 && minor == 7) ? 1 : 0;
}

int isRunningOnSnowLeopardAndAbove()
{
    SInt32 major, minor;

    if ( !getSystemVersion(&major, &minor) )
    {
        return false;
    }
    return (major == 10 && minor >= 6) ? 1 : 0;
}

const int getPathForTypedString(const char* inTypeStr, char * const storage, int sizeOfStorge)
{
    std::string pathStr;

    if (0 == strcmp(inTypeStr, "exports"))
    {
        pathStr = [[GeneralPreferences exportPath] UTF8String];
    }
    else if (0 == strcmp(inTypeStr, "models"))
    {
        pathStr = [[GeneralPreferences modelPath] UTF8String];
    }
    else if (0 == strcmp(inTypeStr, "grab"))
    {
        pathStr = [[GeneralPreferences grabPath] UTF8String];
    }
    else if (0 == strcmp(inTypeStr, "render"))
    {
        pathStr = [[GeneralPreferences renderPath] UTF8String];
    }
    else if (0 == strcmp(inTypeStr, ""))
    {
        pathStr = [[GeneralPreferences documentsPath] UTF8String];
    }
    else
    {
        return -1; // not found!
    }

    const size_t bytesNeedToStore(pathStr.length() + 1);
    if ( NULL != storage )
    {
        if (bytesNeedToStore > sizeOfStorge)
        {
            return -2; // Found, but dest buffer is too small!
        }
    }
    strcpy(storage, pathStr.c_str());
    return bytesNeedToStore; // success!
}

// Adjust the working dir in order to relocate to the application resources directory.
int osx_adjustWorkingDir(const char* inAppAbsPath)
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

        int rc = ::chdir(currwd); // And change the current working dir to this path
        assert(0 == rc);
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

int osx_adjustRenderEnvironment()
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
    path.append(":" + kPathAqsis + "Resources/bin/");
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

// Check weather the current focus window is the main window
int isMainWindowActive()
{
    const NSWindow *keyWin  = [NSApp keyWindow];

        // is the key window valid?
    if (keyWin == NULL)
        return false; // No? then The main Window is not the active one.

        // Get the Key Windows title
    const NSString *title = [keyWin title];

        // The MainWindow is active only if the key window is the MainWindow
        // (whose title is "MakeHuman").
    const NSRange range([title rangeOfString:@"MakeHuman"]);
    return range.location == 0 && range.length > 0;
}

void challengePythonUpdate()
{
    /* Perform a version check of the installed Python interpreter.
     * If it is older than 3.x The User will be notified to update it.
     */
    const char* kPythonVersionNumber = Py_GetVersion();
    int major, minor, sub;
    const int rc(::sscanf(kPythonVersionNumber, "%d.%d.%d", &major, &minor, &sub));

    if ((rc == 3) && !((major >= 3) && (minor >= 2)))
    {
        NSString *messageString = [NSString stringWithFormat:
                                   @"Please update to Python 3.x as soon as possible!\n\n"
                                   "Makehuman will use some extended Functionality of Python 3.x in the near future.\n\n"
                                   "You are currently using Python V%d.%d.%d\n\n"
                                   "So please update the Python on your machine as soon as possible!",major, minor, sub];

        const NSInteger rc = NSRunInformationalAlertPanel(@"Alert Message",
                                                          messageString,
                                                          @"Start it anyway!",
                                                          @"Visit the Python Website...",
                                                          @"Download the Python installer...");
        switch(rc)
        {
            case NSAlertDefaultReturn :
                break;

            case NSAlertAlternateReturn :
                [[NSWorkspace sharedWorkspace] openURL:[NSURL URLWithString:@"http://www.python.org/download"]];
                break;

            case NSAlertOtherReturn :
                [[NSWorkspace sharedWorkspace]
                 openURL:[NSURL URLWithString:isRunningOnSnowLeopardAndAbove() ?
                          @"http://www.python.org/ftp/python/3.2/python-3.2-macosx10.6.dmg" :
                          @"http://www.python.org/ftp/python/3.2/python-3.2-macosx10.3.dmg"]];
                break;
        }
        printf("rc is %d\n", rc);
            //        printf("Please update to Python 3.x as soon as possible!\n");
    }
}

#pragma mark -
#pragma mark Extensions for SDLMain

@implementation SDLMain (MenuHandling)

-(void)endSelector:(id)inSender
{
}

-(IBAction)showAbout:(id)inSender
{
    [mAboutPanel makeKeyAndOrderFront:self];
}

-(IBAction)showAcknowledgments:(id)inSender
{
    [mAcknowlegmentPanel makeKeyAndOrderFront:self];
}

-(IBAction)showLicensing:(id)inSender;
{
    [mLicensePanel makeKeyAndOrderFront:self];
}

-(IBAction)showPreferences:(id)inSender
{
	[NSPreferences setDefaultPreferencesClass: [AppPreferences class]];
	[[NSPreferences sharedPreferences] showPreferencesPanel];
}

+(void)openFile:(NSString*)fileName
{
    NSString *s = NSLocalizedStringFromTable(fileName, @"HelpLinks", @"");
    [[NSWorkspace sharedWorkspace] openFile:s];
}

+(void)openURL:(NSString*)urlName
{
    NSString *s = NSLocalizedStringFromTable(urlName, @"HelpLinks", @"");
    [[NSWorkspace sharedWorkspace] openURL:[NSURL URLWithString:s]];
}

-(IBAction)helpFileMHUsersGuide:(id)inSender        {[SDLMain openURL:@"FileMHUsersGuide"];}

-(IBAction)helpFileMHDevelMHProto:(id)inSender      {[SDLMain openFile:@"FileDevelMHProto"];}

-(IBAction)helpURLMHVisitHome:(id)inSender          {[SDLMain openURL:@"URLMHHome"];}
-(IBAction)helpURLMHVisitForum:(id)inSender         {[SDLMain openURL:@"URLMHForum"];}
-(IBAction)helpURLMHDocuments:(id)inSender          {[SDLMain openURL:@"URLMHDocuments"];}
-(IBAction)helpURLMHArtists:(id)inSender            {[SDLMain openURL:@"URLMHArtists"];}
-(IBAction)helpURLMHSoftwareDownload:(id)inSender   {[SDLMain openURL:@"URLMHUpdate"];}

-(IBAction)helpURLAqsisHome:(id)inSender            {[SDLMain openURL:@"URLAqsisHome"];}
-(IBAction)helpURLAqsisWiki:(id)inSender            {[SDLMain openURL:@"URLAqsisWiki"];}

-(IBAction)helpURLPixieHome:(id)inSender            {[SDLMain openURL:@"URLPixieHome"];}
-(IBAction)helpURLPixieWiki:(id)inSender            {[SDLMain openURL:@"URLPixieWiki"];}
-(IBAction)helpURLPixieInstall:(id)inSender         {[SDLMain openURL:@"URLPixieInstall"];}

-(IBAction)helpURL3DelightHome:(id)inSender         {[SDLMain openURL:@"URL3DelightHome"];}
-(IBAction)helpURL3DelighWiki:(id)inSender          {[SDLMain openURL:@"URL3DelightWiki"];}
@end // @implementation SDLMain

