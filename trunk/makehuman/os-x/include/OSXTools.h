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
     <td>MakeHuman Team 2001-2011                        </td></tr>
 <tr><td>Licensing:                                      </td>
     <td>GPL3 (see also
         http://makehuman.wiki.sourceforge.net/Licensing)</td></tr>
 <tr><td>Coding Standards:                               </td>
     <td>See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards
                                                         </td></tr>
 </table>

 */

#ifdef __cplusplus
extern "C"
{
#endif // #ifdef __cplusplus

    /** Adjust the working dir in order to relocate to the application resources directory.
      *
      * \param inAppAbsPath the location to the Applications executeable (inclusive path).
      *        This is commonly argv[0] of main().
      *
      * \return 0 for success, -1 for failure.
      *
      * \author Hans-Peter Dusel <hdusel@tangerine-soft.de>
      */
    int osx_adjustWorkingDir(const char* inAppAbsPath);

    /** Adjusts the environment in order to work with all supported Ray Tracers.
      *
      * \return 0 for success, -1 for failure.
      *
      * \author Hans-Peter Dusel <hdusel@tangerine-soft.de>
      */
    int osx_adjustRenderEnvironment();

    /** Get the path property of a given key. All properties are set in the user preferences.
     * The actual path value will be stored into a string array which has to be hand over as
     * well its storage size in bytes. If the string will not fit into the buffer then nothing
     * will be copied and a return value of -1 will be returned.

     * @note In order to determine the minimal buffer which will be needed to store a particular
     * value you may call this function with the \p storage set to <tt>NULL</tt>.
     * In this case this call just returns the needed size (inclusive the NUL character)
     * to store the path.
     *
     * The type String determines which path property should be get. It has the meaning as follow:
     *
     * <table border="1">
     * <tr><th>param <tt>inTypeStr</tt></th><th>Meaning</th><th>Default</th></tr>
     * <tr><td>"exports"</td><td>Gets the path location for Exports.</td><td><tt>${USER}/Documents/MakeHuman/exports/</tt></td></tr>
     * <tr><td>"models"</td><td>Gets the path location for Models.</td><td><tt>${USER}/Documents/MakeHuman/models/</tt></td></tr>
     * <tr><td>"grab"</td><td>Gets the path location for Screenshots (grabs).</td><td><tt>${USER}/Desktop/</tt></td></tr>
     * <tr><td>"render"</td><td>Gets the path location for Renderman ouput.</td><td><tt>${USER}/Documents/MakeHuman/renderman/</tt></td></tr>
     * <tr><td>""</td><td>Gets the path location for MH Documents.</td><td><tt>${USER}/Documents/MakeHuman/</tt></td></tr>
     * </table>
     *
     * \param inTypeStr The type according the table above.
     * \param storage The storage the Value according \p inTypeStr will be stored.
     *                This may be NULL. In this case this function just returns the number of bytes
     *                (inclusive the NUL Byte) for \p sizeOfStorage to store this value.
     * \param sizeOfStorge The size of \p stoarge in bytes. If the string will not
     *                     fit into the buffer then nothing will be copied and a return value
     *                     of -1 will be returned.
     * \return The actual size of the bytes copied into storage (inclusive the
     *         NUL byte) or -1 if a path for the requestend Key in \p inTypeStr does not
     *         exists or -2 if \p sizeOfStorge is less than the storage actually needed.
     */
    const int getPathForTypedString(const char* inTypeStr, char * const storage, int sizeOfStorge);

    /** Checks if the main window is the active one, which means that it has the focus:
     * \return true if the main window has the focus.
     */
    int isMainWindowActive();

    /** Checks if the system consists of at least Python 3.x. If not then
     * challenge the user to download the latest Pyton version by a dialog.
     */
    void challengePythonUpdate();

    /** Checks if the system is \b exactly running on OS X "Leopard" (OS X 10.5.x).
     * \return true if the system is "Leopard" (OS X 10.5.x), false if not.
     *
     * \see isRunningOnSnowLeopard()
     * \see isRunningOnLion()
     * \see isRunningOnSnowLeopardAndAbove()
     * \return 1 if true 0 if false;
     */
    int isRunningOnLeopard();

    /** Checks if the system is \b exactly running on OS X "Snow Leopard" (OS X 10.6.x).
     * \return true if the system is "Snow Leopard" (OS X 10.6.x), false if not.
     *
     * \see isRunningOnLeopard()
     * \see isRunningOnLion()
     * \see isRunningOnSnowLeopardAndAbove()
     * \return 1 if true 0 if false;
     */
    int isRunningOnSnowLeopard();

    /** Checks if the system is \b exactly running on OS X "Lion" (OS X 10.7.x).
     * \return true if the system is "Lion" (OS X 10.7.x), false if not.
     *
     * \see isRunningOnLeopard()
     * \see isRunningOnSnowLeopard()
     * \see isRunningOnSnowLeopardAndAbove()
     * \return 1 if true 0 if false;
     */
    int isRunningOnLion();

    /** Checks if the system is running on SnowLeopard (or above).
     * \return true if the system is "Snow Leopard" (OS X 10.6.x) or greater, false
     * if it below (e.g. "Leopard", "Tiger", Panther ...)
     *
     * \see isRunningOnLeopard()
     * \see isRunningOnSnowLeopard()
     * \see isRunningOnLion()
     * \return 1 if true 0 if false;
     */
    int isRunningOnSnowLeopardAndAbove();

#ifdef __cplusplus
}
#endif // #ifdef __cplusplus

#endif // _OSXTools_H_
