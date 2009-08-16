//
//  PreferencesWindow.mm
//  MakeHuman
//
//  Created by hdusel on 15.08.09.
//  Copyright 2009 Tangerine-Software. All rights reserved.
//

#import "PreferencesWindow.h"
#import "Sparkle/SUUpdater.h"



@interface PreferencesWindow (Private)
-(void)updateLastUpdateCheckTime;
@end // @interface PreferencesWindow (Private)

@implementation PreferencesWindow

NSString *kPreferencesToolbar = @"PreferencesToolbar";
NSString *kTBItemUpdate       = @"TBItem_Update";

- (id)init 
{
    self = [super init];
    if (self) 
    {
        NSLog(@"Init");

    // Initialization code here.
    }
    return self;
}

-(void)awakeFromNib
{
    [mUpdater setDelegate:self];
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


-(void)toolbarAction:(id)inSender
{
}

- (void)makeKeyAndOrderFront:(id)sender
{
    BOOL autoCheck = [mUpdater automaticallyChecksForUpdates];
    [mAutoUpdateCM setState:autoCheck ? NSOnState : NSOffState];

    [self updateLastUpdateCheckTime];

    [super makeKeyAndOrderFront:sender];
}


@end // @implementation PreferencesWindow

@implementation PreferencesWindow (Private)

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
@end // @implementation PreferencesWindow (Private)

@implementation PreferencesWindow (Delegate)
// delegate
- (void)toolbarWillAddItem:(NSNotification *)notification
{
    NSDictionary *dict = [notification userInfo];
    NSToolbarItem *item = [dict objectForKey:@"item"];
    int tag = [item tag];
    if (tag != -1)
    {
        [item setTarget:self];
        [item setAction:@selector(toolbarAction:)];
    }
}

- (void)updater:(SUUpdater *)updater didFinishLoadingAppcast:(SUAppcast *)appcast
{
    [self updateLastUpdateCheckTime];
}
@end // @implementation PreferencesWindow (Delegate)
