//
//  main.m
//  FontTransFixer
//
//  Created by Dusel Hans-Peter on 04.02.12.
//  Copyright (c) 2012 Tangerine Software. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import <libgen.h>

@interface MHImageConverter : NSObject
+ (BOOL)convertImageFromFile:(NSString*)inFilename toPath:(NSString*)targetPath;
+ (void)convertImageFilesWithinDirectory:(NSString*)inSourcePath toPath:(NSString*)targetPath;
@end

@implementation MHImageConverter
+ (BOOL)convertImageFromFile:(NSString*)inFilename toPath:(NSString*)targetPath
{
    BOOL rc = FALSE; // assume error per default

    NSImage * image = [[NSImage alloc] initByReferencingFile:inFilename];
    if ( image )
    {
        NSArray *reps = [image representations];

        NSBitmapImageRep* imageRep = nil;

        for (NSImageRep* rep in reps)
        {
            if ([rep isKindOfClass:[NSBitmapImageRep class]])
            {
                imageRep = (NSBitmapImageRep*)rep;
                break;
            }
        }

        if ( imageRep )
        {
            const NSSize imageSize([image size]);

            const int  bitsPerSample(8);
            const bool hasAlpha = YES;
            const int  samplesPerPixel( hasAlpha ? 2 : 1);
            const int  bitsPerPixel(samplesPerPixel * bitsPerSample);
            const int  bytesPerRow((bitsPerPixel * (int)imageSize.width)>> 3);

            NSBitmapImageRep *targetBitmap = [[NSBitmapImageRep alloc]
                                              initWithBitmapDataPlanes:nil
                                              pixelsWide:imageSize.width
                                              pixelsHigh:imageSize.height
                                              bitsPerSample:bitsPerSample
                                              samplesPerPixel:samplesPerPixel
                                              hasAlpha:hasAlpha
                                              isPlanar:NO
                                              colorSpaceName:NSDeviceWhiteColorSpace
                                              bitmapFormat:0
                                              bytesPerRow:bytesPerRow
                                              bitsPerPixel:0];

            if (targetBitmap)
            {
                struct gray_t {uint8_t v;};
                struct grayA_t {uint8_t v, a;};

                const uint8_t * srcDataPtr = [imageRep bitmapData];
                uint8_t * dstDataPtr = [targetBitmap bitmapData];

                const size_t srcBytesPerLine([imageRep bytesPerRow]);
                const size_t dstBytesPerLine([targetBitmap bytesPerRow]);

                for (int y=0; y != imageSize.height; ++y)
                {
                    const gray_t  *srcPixelPtr((gray_t*)srcDataPtr);
                    grayA_t *dstPixelPtr((grayA_t*)dstDataPtr);

                    for (int x=0; x != imageSize.width; ++x)
                    {
                        dstPixelPtr[x].a = srcPixelPtr[x].v;

#if USE_PREMULTIPLIED_ALPHA_VALUES
                        dstPixelPtr[x].v = (((uint16_t)srcPixelPtr[x].v) * dstPixelPtr[x].a) / 255;
#else
                        dstPixelPtr[x].v = srcPixelPtr[x].v;
#endif
                    }
                    srcDataPtr+=srcBytesPerLine;
                    dstDataPtr+=dstBytesPerLine;
                }

                NSData *pngImageData = [targetBitmap representationUsingType:NSPNGFileType properties:nil];

                NSString *fileName = [inFilename lastPathComponent];

                const BOOL success ( [pngImageData writeToFile:[NSString stringWithFormat:@"%@/%@", targetPath, fileName] atomically:NO]);

                [targetBitmap release];

                rc = success;
            }
        }
        [image release];
    }

    return rc;
}

+ (void)convertImageFilesWithinDirectory:(NSString*)inSourcePath toPath:(NSString*)targetPath
{
    NSFileManager* fileManager = [NSFileManager defaultManager];

    NSArray *paths = [fileManager contentsOfDirectoryAtPath:inSourcePath error:nil];
    for(NSString *compPath in paths)
    {
        if ([compPath hasSuffix:@".png"])
        {
            NSString *fileToLoad([NSString stringWithFormat:@"%@/%@", inSourcePath, compPath]);
            printf("Converting '%s' to '%s'... ", [fileToLoad UTF8String], [targetPath UTF8String]);
            const BOOL success([MHImageConverter convertImageFromFile:fileToLoad toPath:targetPath]);
            printf(" %s\n", success ? "[SUCCESS]" : "[FAILED]");
        }
    }
}
@end // @implementation MHImageConverter

static void usage(const char* inBasename)
{
    fprintf(stderr, "*** Error using %s!\n", inBasename);
    fprintf(stderr, "*** Usage %s source_path dest_path\n\n", inBasename);

    fprintf(stderr, "%s is a tool which converts a bunch of grayscale png images which\n"
                    "does not consist of an alpha channel to grayscale png image with\n"
                    "alpha channel!\n\n", inBasename);

    fprintf(stderr, "Hereby %s scans the contents of source_path and processes all\n"
                    "files whose file ending is '.png'. Each of it will be stored within\n"
                    "the subdir 'dest_path'.\n", inBasename);
}

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        usage(::basename(argv[0]));
        return EXIT_FAILURE;
    }

    NSApplicationLoad();
    NSAutoreleasePool *pool = [NSAutoreleasePool new];

    [MHImageConverter convertImageFilesWithinDirectory:[NSString stringWithUTF8String:argv[1]]
                                                toPath:[NSString stringWithUTF8String:argv[2]]];
    [pool release];

    return EXIT_SUCCESS;
}
