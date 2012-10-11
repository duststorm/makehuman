/** \file SDL_syswm.h
 *  \brief This file is supposed to wrap the Mac OS X Framework include for SDL.
 
 <table>
 <tr><td>Project Name:                                   </td>
 <td><b>MakeHuman</b>                                </td></tr>
 <tr><td>Product Home Page:                              </td>
 <td>http://www.makehuman.org/                       </td></tr>
 <tr><td>SourceForge Home Page:                          </td>
 <td>http://sourceforge.net/projects/makehuman/      </td></tr>
 <tr><td>Authors:                                        </td>
 <td>Paolo Colombo, Simone Re, Marc Flerackers </td></tr>
 <tr><td>Author of this file:                             </td>
 <td>Hans-Peter Dusel &lt;<a href='mailto:hdusel@tangerine-soft.de'>hdusel@tangerine-soft.de</a>&gt;</td></tr>
 <tr><td>Copyright(c):                                   </td>
 <td>MakeHuman Team 2001-2010                        </td></tr>
 <tr><td>Licensing:                                      </td>
 <td>GPL3 (see also
 http://makehuman.wiki.sourceforge.net/Licensing)</td></tr>
 <tr><td>Coding Standards:                               </td>
 <td>See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards
 </td></tr>
 </table>
 
 This file is supposed to wrap the Mac OS X Framework include for SDL 
 (Simple DirectMedia Layer) libraries. 
 
 Hence it is meaningful to be included for a build for OS-X only! 
 */

#pragma once

#ifndef __APPLE__
  #error "This Header is supposed to be used to build the project for OS-X only!"
#endif
#include <SDL/SDL_syswm.h>
