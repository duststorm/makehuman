//
//  UpdatePreferences.h
//  MakeHuman
//
//  Created by hdusel on 16.08.09.
//  Copyright 2009 Tangerine-Software. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import "NSPreferences.h"

@class SUUpdater;

@interface UpdatePreferences : NSPreferencesModule 
{
    IBOutlet SUUpdater    *mUpdater;
    IBOutlet NSButton     *mAutoUpdateCM;
    IBOutlet NSTextField  *mLastUpdated;
}
-(IBAction)actionCheckNow:(id)inSender;
-(IBAction)actionAutoUpdateCheck:(id)inSender;

@end
