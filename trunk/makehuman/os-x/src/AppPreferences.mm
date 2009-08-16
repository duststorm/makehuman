//
//  AppPreferences.mm
//  MakeHuman
//
//  Created by hdusel on 15.08.09.
//  Copyright 2009 Tangerine-Software. All rights reserved.
//

#import "AppPreferences.h"
#import "UpdatePreferences.h"

@implementation AppPreferences

- (id)init 
{
    _nsBeginNSPSupport();			// MUST come before [super init]
    self = [super init];
    if (self) 
    {
        [self addPreferenceNamed:NSLocalizedString(@"UpdatePrefsHead", "update preference pane name" ) owner:[UpdatePreferences sharedInstance]];
    }
    return self;
}

// Wo don't use the Buttons "Applay" "Cancel" and "OK"
- (BOOL) usesButtons
{
	return NO;
}

@end // @implementation AppPreferences

