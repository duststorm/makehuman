/*   SDLMain.m - main entry point for our Cocoa-ized SDL app
       Initial Version: Darrell Walisser <dwaliss1@purdue.edu>
       Non-NIB-Code & other changes: Max Horn <max@quendi.de>

    Feel free to customize this file to suit your needs
*/

#import <Cocoa/Cocoa.h>

#ifdef __cplusplus
extern "C" {
#endif
    const char* osx_getExportPath();
    const char* osx_getModelPath();
    const char* osx_getGrabPath();
    const char* osx_getRenderPath();
    const char* osx_getDocumentsPath();
#ifdef __cplusplus
}
#endif

@interface SDLMain : NSObject
{
    bool licenseWindowVisible;

    IBOutlet NSPanel *mAboutPanel;
    IBOutlet NSPanel *mLicensePanel;
    IBOutlet NSPanel *mAcknowlegmentPanel;
    IBOutlet NSPanel *mPreferencesPanel;
    IBOutlet NSUserDefaultsController *mUserDefaults;
}

@property (assign) bool licenseWindowVisible;

-(IBAction)helpFileMHUsersGuide:(id)inSender;
-(IBAction)helpFileMHQuickStart:(id)inSender;

-(IBAction)helpFileMHDevelMHProto:(id)inSender;

-(IBAction)helpURLMHVisitHome:(id)inSender;
-(IBAction)helpURLMHVisitForum:(id)inSender;
-(IBAction)helpURLMHDocuments:(id)inSender;
-(IBAction)helpURLMHArtists:(id)inSender;
-(IBAction)helpURLMHSoftwareDownload:(id)inSender;

-(IBAction)helpURLAqsisHome:(id)inSender;
-(IBAction)helpURLAqsisWiki:(id)inSender;

-(IBAction)helpURLPixieHome:(id)inSender;
-(IBAction)helpURLPixieWiki:(id)inSender;
-(IBAction)helpURLPixieInstall:(id)inSender;

-(IBAction)helpURL3DelightHome:(id)inSender;
-(IBAction)helpURL3DelighWiki:(id)inSender;


-(IBAction)showAbout:(id)inSender;
-(IBAction)showAcknowledgments:(id)inSender;
-(IBAction)showPreferences:(id)inSender;
-(IBAction)showLicensing:(id)inSender;

@end
