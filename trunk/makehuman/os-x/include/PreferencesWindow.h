//
//  PreferencesWindow.h
//  MakeHuman
//
//  Created by hdusel on 15.08.09.
//  Copyright 2009 Tangerine-Software. All rights reserved.
//

#import <Cocoa/Cocoa.h>

@class SUUpdater;

@interface PreferencesWindow : NSPanel 
{
    IBOutlet SUUpdater    *mUpdater;
    IBOutlet NSButton     *mAutoUpdateCM;
    IBOutlet NSTextField  *mLastUpdated;

@private    
    NSToolbar *mToolbar;

}
-(IBAction)actionCheckNow:(id)inSender;
-(IBAction)actionAutoUpdateCheck:(id)inSender;
@end
