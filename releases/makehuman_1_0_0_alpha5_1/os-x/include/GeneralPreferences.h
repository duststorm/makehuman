//
//  GeneralPreferences.h
//  MakeHuman
//
//  Created by hdusel on 16.08.09.
//  Copyright 2009 Tangerine-Software. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import "NSPreferences.h"
        
@class SUUpdater;

@interface GeneralPreferences : NSPreferencesModule 
{
    IBOutlet NSPopUpButton *mModelsPathsPUB;
    IBOutlet NSPopUpButton *mExportsPathsPUB;
    IBOutlet NSPopUpButton *mGrabPathPUB;
    IBOutlet NSPopUpButton *mRenderPathPUB;

@private
    NSImage *mFolderIcon;
}


-(IBAction)actionResetPaths:(id)inSender;
-(IBAction)actionSelectModelPath:(NSPopUpButton*)inSender;
-(IBAction)actionSelectExportPath:(id)inSender;
-(IBAction)actionSelectGrabPath:(id)inSender;
-(IBAction)actionSelectRenderPath:(id)inSender;

+(NSString*)exportPath;
+(NSString*)modelPath;
+(NSString*)grabPath;
+(NSString*)renderPath;

@end
