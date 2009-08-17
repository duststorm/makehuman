#ifndef _OSXTools_H_
#define _OSXTools_H_
/** \file OSXTools.h
 *  \brief Header file for several functions to adapt the project for Mac OS-X.
 
 <table>  
 <tr><td>Project Name:                                   </td>
     <td><b>MakeHuman</b>                                </td></tr>
 <tr><td>Product Home Page:                              </td>
     <td>http://www.makehuman.org/                       </td></tr>
 <tr><td>SourceForge Home Page:                          </td>
     <td>http://sourceforge.net/projects/makehuman/      </td></tr>
 <tr><td>Authors:                                        </td>
     <td>Hans-Peter Dusel <hdusel@tangerine-soft.de>     </td></tr>                                     
 <tr><td>Copyright(c):                                   </td>
     <td>MakeHuman Team 2001-2008                        </td></tr>
 <tr><td>Licensing:                                      </td>
     <td>GPL3 (see also 
         http://makehuman.wiki.sourceforge.net/Licensing)</td></tr>
 <tr><td>Coding Standards:                               </td>
     <td>See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards
                                                         </td></tr>
 </table>
 
 Header file for trapping mouse events on Mac OS-X.
 
 */

/*compatibility with original GLUT*/

#ifdef __cplusplus
extern "C"
{
#endif // #ifdef __cplusplus

    /** Adjust the working dir in order to relocate to the application resources directory 
      * @param inAppAbsPath the location to the Applications executeable (inclusive path). This is commonly argv[0] of main().
      * @return 0 for success, -1 for failure.
      */
    int adjustWorkingDir(const char* inAppAbsPath);

    const char* getExportPath();
    const char* getModelPath();
#ifdef __cplusplus
}
#endif // #ifdef __cplusplus

#endif // _OSXTools_H_
