//
//  main.cpp
//  PythonChecker
//
//  Created by Dusel Hans-Peter on 17.01.12.
//  Copyright (c) 2012 Tangerine Software. All rights reserved.
//

#include "Capabilities.h"
#include <AppKit/AppKit.h>
#include <iostream>

/*
 Download overview:
 Python 2.7.2 :
 ============
    http://www.python.org/download/releases/2.7.2/

 Universal Build (PPC + i386) (10.3-10.6) :
    http://www.python.org/ftp/python/2.7.2/python-2.7.2-macosx10.3.dmg
 Intel only (i386 + x86_64) (10.6-10.7)
    http://www.python.org/ftp/python/3.2.2/python-2.7.2-macosx10.6.dmg

 Python 3.2.2 :
 ============
    http://www.python.org/download/releases/3.2.2/

 Universal Build (PPC + i386) (10.3-10.6) :
    http://www.python.org/ftp/python/3.2.2/python-3.2.2-macosx10.3.dmg
 Intel only (i386 + x86_64) (10.6-10.7)
    http://www.python.org/ftp/python/3.2.2/python-3.2.2-macosx10.6.dmg

*/

enum EPythonVersion {ePyUnknown = 0, ePyV272, ePyV332};

static NSString* getDownloadLinkFor(EPythonVersion inPyVersion)
{
    if ( ePyV272 == inPyVersion )
    {
        // If the OS Version is leopard _or_ the cpu arch is ppc then the universal package
        // for OS X 10.3 ... 10.6 is the only proper installation!
        if ( ( isOSXLeopard() ) || ( isArchPPC() ) )
        {
            return @"http://www.python.org/ftp/python/2.7.2/python-2.7.2-macosx10.3.dmg";
        }
        else
        {
            return @"http://www.python.org/ftp/python/2.7.2/python-2.7.2-macosx10.6.dmg";
        }
    }
    else if ( ePyV332 == inPyVersion )
    {
        // If the OS Version is leopard _or_ the cpu arch is ppc then the universal package
        // for OS X 10.3 ... 10.6 is the only proper installation!
        if ( ( isOSXLeopard() ) || ( isArchPPC() ) )
        {
            return @"http://www.python.org/ftp/python/3.2.2/python-3.2.2-macosx10.3.dmg";
        }
        else
        {
            return @"http://www.python.org/ftp/python/3.2.2/python-3.2.2-macosx10.6.dmg";
        }
    }
    else
    {
        return nil;
    }
}

static NSString* getOverviewLinkFor(EPythonVersion inPyVersion)
{
    if ( ePyV272 == inPyVersion )
    {
        return @"http://www.python.org/download/releases/2.7.2/";
    }
    else if ( ePyV332 == inPyVersion )
    {
        return @"http://www.python.org/download/releases/3.2.2/";
    }
    else
    {
        return nil;
    }
}

static bool isPythonInstalled(EPythonVersion inRequiredPyVersion)
{
	switch(inRequiredPyVersion)
	{
		case ePyV272 : 
			return isPyInstalled27();
		case ePyV332 : 
			return isPyInstalled33();
		default:
			return false;
	}
}

static void challengeDownload(EPythonVersion inRequiredPyVersion)
{    
	NSString *messageString = \
	@"This Version of MakeHuman requires Python Vn!\n"
	@"You have installed Vc.\n\n"
	@"In order to install this Version of MakeHuman you have to update to Python Vn first!\n\n"
	@"Now you have the choice either to:\n\n"
	@"   1) Cancel this install process without any further action.\n"
	@"   2) Visit the download page for Python Vn on http://www.python.org.\n"
	@"   3) Let this installer download the right Version of Python Vn\n"
	@"      from http://www.python.org.\n"
	@"      Please don't forget to install this downloaded package afterwards. This Installer will not do that for you!"
	@"\nNote that in any case the installation Process of MakeHuman will be canceled"
	@" until you have finally installed Python Vn!";
	
	NSLog(@"%@", messageString);
	
    const NSInteger result ( NSRunCriticalAlertPanel(@"The required Version of Python is missing!",
													 messageString,
                                                     @"Download", // Default
                                                     @"Cancel installation", // alternate
                                                     @"visit www.python.org" // other
                                                     ));
        //    NSLog(@"response is %d", result);
        // ok:        1
        // alternate: 0
        // other:    -1
    
    switch (result)
    {
        case NSAlertDefaultReturn :
        {
            NSString *dllink = getDownloadLinkFor(inRequiredPyVersion);
            assert(dllink);
            if (dllink)
            {
                NSWorkspace *ws = [NSWorkspace sharedWorkspace];
                assert(ws);
                if (ws)
                {
                    [ws openURL:[NSURL URLWithString:dllink]];
                }
            }
        }
        break;
            
        case NSAlertAlternateReturn :
            break;
            
        case NSAlertOtherReturn :
        {
            NSString *dllink = getOverviewLinkFor(inRequiredPyVersion);
            assert(dllink);
            if (dllink)
            {
                NSWorkspace *ws = [NSWorkspace sharedWorkspace];
                assert(ws);
                if (ws)
                {
                    [ws openURL:[NSURL URLWithString:dllink]];
                }
            }
        }
            break;
    }
}

int main (int argc, const char * argv[])
{
	const EPythonVersion requiredVersion(ePyV272);
//	const EPythonVersion requiredVersion(ePyV332);
	
    NSAutoreleasePool *pool = [NSAutoreleasePool new];
    const BOOL loaded = NSApplicationLoad();
    int rc = EXIT_FAILURE;

	if (loaded)
	{
		if ( isPythonInstalled(requiredVersion) )
		{
			rc = EXIT_SUCCESS;
		}
		else 
		{
			challengeDownload(requiredVersion);
			rc = EXIT_FAILURE;
		}
		
		[pool release];
		
	}
	
    return rc;
}

