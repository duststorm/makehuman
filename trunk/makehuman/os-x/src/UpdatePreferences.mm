//
//  UpdatePreferences.mm
//  MakeHuman
//
//  Created by hdusel on 16.08.09.
//  Copyright 2009 Tangerine-Software. All rights reserved.
//

#import "UpdatePreferences.h"
#import "Sparkle/SUUpdater.h"

@implementation UpdatePreferences


-(void)awakeFromNib
{

    mUpdater = [[SUUpdater sharedUpdater] retain];
    [mUpdater setDelegate:self];

    BOOL autoCheck = [mUpdater automaticallyChecksForUpdates];
    [mAutoUpdateCM setState:autoCheck ? NSOnState : NSOffState];
    
    [self updateLastUpdateCheckTime];
}

-(IBAction)actionCheckNow:(id)inSender
{
    [mUpdater checkForUpdates:self];
}

-(IBAction)actionAutoUpdateCheck:(id)inSender
{
    BOOL checked = (NSOnState == [inSender state]);
    [mUpdater setAutomaticallyChecksForUpdates:checked];
}

- (BOOL) isResizable
{
	return NO;
}

@end // @implementation UpdatePreferences

@implementation UpdatePreferences (Private)

-(void)updateLastUpdateCheckTime
{
    NSDate *date = [mUpdater lastUpdateCheckDate];
    if (NULL == date)
    {
        [mLastUpdated setStringValue:@"-- (no check performed yet)"];
    }
    else
    {
        NSDateFormatter *formatter = [[NSDateFormatter alloc] 
                                      initWithDateFormat:@"%A, %Y-%m-%d %H:%M:%S" allowNaturalLanguage:NO];
        [mLastUpdated setStringValue:[formatter stringFromDate:date]];
        [formatter release];
    }
}

@end // @implementation UpdatePreferences (Private)

@implementation UpdatePreferences (Delegate)
- (void)updater:(SUUpdater *)updater didFinishLoadingAppcast:(SUAppcast *)appcast
{
    [self updateLastUpdateCheckTime];
}
@end // @implementation UpdatePreferences (Delegate)
