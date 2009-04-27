/*
 *  Copyright (C) 2008  MakeHuman Project
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
 *  File   : MouseEventTrap.m
 *  Project: MakeHuman <info@makehuman.org>, http://www.makehuman.org/
 *  App    : makehuman
 *  Author : Hans-Peter Dusel <hdusel@tangerine-soft.de>
 *
 *  For individual developers look into the AUTHORS file.
 *   
 */

#import <libgen.h>
#import "MouseEventTrap.h"
#import <Cocoa/Cocoa.h>
#import <GLUT/GLUT.h>

typedef void (*MouseFuncCB)(int button, int state, int x, int y);
typedef void (*MouseWheelCB)(int wheel_number, int direction, int x, int y);


static MouseFuncCB  sOSXMouseFuncWrapper;
static MouseWheelCB sOSXMouseWheelWrapper;

/* This is a Hack in order to trap Mouswheel-Events which are posted into the 
   GLUTWindow object */
@interface MHOpenGLWindow : NSWindow
@end // @interface MHOpenGLWindow : NSWindow

// Adjust the working dir in order to relocate to the application resources directory.
int adjustWorkingDir(const char* inAppAbsPath)
{
    /* Redirect the current working dir into the applications package resource directory because
     * the dirs 'data', '3dobjs' mh_core' and 'mh_plugins' are located there. 
     */

    // Get the apps exec location which is 'MHPhoenix.app/Contents/MacOS'
    char *tmp_currwd = dirname(inAppAbsPath);

    /* Now this path is supposed to bechanged to the 'Resources' directory be appending
     * '/../Resources/' which actually makes 'MHPhoenix.app/Contents/MacOS/../Resources/' 
     */ 
    int len1 = strlen(tmp_currwd); // Remember the length of the canonical path for 'MHPhoenix.app/Contents/MacOS'
    const char *appStr="/../Resources/"; // The recources are reside here.
    int len = len1 + strlen(appStr) + 1; // calcualte the absolute name of the path (including NUL byte)

    char *currwd = malloc(len); // allocate the memory.
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

/* ========================================================================== */
/**
 */
/* ========================================================================== */
@implementation MHOpenGLWindow

- (void)sendEvent:(NSEvent *)theEvent
{
    if ([theEvent type] == NSScrollWheel)
    {
        float dirY = [theEvent deltaY];

        // Mighty Mouse ?
        float dirX = [theEvent deltaX];

        if ((dirY > 0.0001f) && (dirY <= 1.f)) {
            dirY = 1.0f;
        } else if ((dirY < 0.0001f) && (dirY >= -1.f)) {
            dirY = -1.0f;
        }

        if ((dirX > 0.0001f) && (dirX <= 1.f)) {
            dirX = 1.0f;
        } else if ((dirX < 0.0001f) && (dirX >= -1.f)) {
            dirX = -1.0f;
        }
        
        if (sOSXMouseFuncWrapper != NULL)
        {
            int x=0;
            int y=0;
            int i;
            if (dirY != 0.0f)
            {
                int emuButton = (dirY > 0.0f) ? GLUT_WHEEL_UP : GLUT_WHEEL_DOWN;
                float n = abs((float)dirY);
                for (i=0; i<n; ++i)
                {
                    sOSXMouseFuncWrapper(emuButton, GLUT_UP, x, y);
                }
            }

            if (dirX != 0.0f)
            {
                int emuButton = (dirX > 0.0f) ? GLUT_WHEEL_RIGHT : GLUT_WHEEL_LEFT;
                float n = abs((float)dirX);
                for (i=0; i<n; ++i)
                {
                    sOSXMouseFuncWrapper(emuButton, GLUT_UP, x, y);
                }
            }
        }

        if (sOSXMouseWheelWrapper != NULL)
        {
//            int direction = (dirY > 0) ? 1 : -1;
            int direction = (int)dirY;
            sOSXMouseWheelWrapper(0, direction, (int)dirX, (int)dirY);
        }
    }
    [super sendEvent:theEvent];
}

@end // @implementation MHOpenGLWindow


/* ========================================================================== */
/**
 */
/* ========================================================================== */
void initMouseScrollWheelTrap()
{
    [MHOpenGLWindow poseAsClass:[NSWindow class]];
}

void glutMouseWheelFuncOSX(void (*func)(int wheel_number, int direction, int x, int y))
{
    sOSXMouseWheelWrapper = func;
}

void glutMouseFuncOSX(void (*func)(int button, int state, int x, int y))
{
    sOSXMouseFuncWrapper = func;
    glutMouseFunc(func);
}
