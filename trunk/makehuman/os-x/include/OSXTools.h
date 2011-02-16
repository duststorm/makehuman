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

    /** Adjust the working dir in order to relocate to the application resources directory.
      *
      * \param inAppAbsPath the location to the Applications executeable (inclusive path). This is commonly argv[0] of main().
      *
      * \return 0 for success, -1 for failure.
      *
      * \author Hans-Peter Dusel <hdusel@tangerine-soft.de>
      */
    int adjustWorkingDir(const char* inAppAbsPath);

    /** Gets the path location for Exports. This is usually set by the User Preferences and points to
     * ${USER}/Documents/MakeHuman/exports/ per default.
     *
     * \param inAppAbsPath the location to the Applications executeable (inclusive path). This is commonly argv[0] of main().
     *
     * \return The path to which all exports should be placed to.
     *
     * \see getDocumentsPath()
     * \see getModelPath()
     * \see getGrabPath()
     * \see getRenderPath()
     */
    const char* getExportPath();

    /** Gets the path location for Models. This is usually set by the User Preferences and points to
     * ${USER}/Documents/MakeHuman/models/ per default.
     *
     * \return The path to which all exports should be placed to.
     *
     * \see getDocumentsPath()
     * \see getExportPath()
     * \see getGrabPath()
     * \see getRenderPath()
     */
    const char* getModelPath();

    /** Gets the path location for Screenshots (grabs). This is usually set by the User Preferences and points to
     * ${USER}/Desktop/ per default.
     *
     * \return The path to which all exports should be placed to.
     *
     * \see getDocumentsPath()
     * \see getExportPath()
     * \see getModelPath()
     * \see getRenderPath()
     */
    const char* getGrabPath();

    /** Gets the path location for Renderman ouput. This is usually set by the User Preferences and points to
     * ${USER}/Documents/MakeHuman/renderman per default.
     *
     * \return The path to which all exports should be placed to.
     *
     * \see getDocumentsPath()
     * \see getExportPath()
     * \see getModelPath()
     * \see getGrabPath()
     */
    const char* getRenderPath();
    
    /** Adjusts the environment in order to work with all supported Ray Tracers.
      *
      * \return 0 for success, -1 for failure.
      *
      * \author Hans-Peter Dusel <hdusel@tangerine-soft.de>
      */
    int adjustRenderEnvironment();

    /** Gets the path location for MH Documents. This is usually set by the User Preferences and points to
     * ${USER}/Documents/MakeHuman per default.
     *
     * \return The path to which all user documents for makehuman should be placed to.
     *
     * \see getExportPath()
     * \see getModelPath()
     * \see getGrabPath()
     * \see getRenderPath()
     */
    const char* getDocumentsPath();
#ifdef __cplusplus
}
#endif // #ifdef __cplusplus

#endif // _OSXTools_H_
