/** \file core.h
 *  \brief Header file for arraybuffer.c.

 <table>
 <tr><td>Project Name:                                   </td>
     <td><b>MakeHuman</b>                                </td></tr>
 <tr><td>Product Home Page:                              </td>
     <td>http://www.makehuman.org/                       </td></tr>
 <tr><td>SourceForge Home Page:                          </td>
     <td>http://sourceforge.net/projects/makehuman/      </td></tr>
 <tr><td>Authors:                                        </td>
     <td>Marc Flerackers                                 </td></tr>
 <tr><td>Copyright(c):                                   </td>
     <td>MakeHuman Team 2001-2010                        </td></tr>
 <tr><td>Licensing:                                      </td>
     <td>GPL3 (see also
         http://makehuman.wiki.sourceforge.net/Licensing)</td></tr>
 <tr><td>Coding Standards:                               </td>
     <td>See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards
                                                         </td></tr>
 </table>

 Header file for core.c.

 */

#ifndef ARRAYBUFFER_H
#define ARRAYBUFFER_H 1

#ifdef _DEBUG
#undef _DEBUG
#include <Python.h>
#define _DEBUG
#else
#include <Python.h>
#endif

#ifdef __cplusplus
extern "C"
{
#endif

void RegisterArrayBuffer(PyObject *module);

extern PyTypeObject ArrayBufferType;

typedef struct
{
    PyObject_HEAD
    
    unsigned int  byteLength;
    void          *data;

} ArrayBuffer;

void RegisterTypedArrayViews(PyObject *module);

typedef struct
{
    PyObject_HEAD

    ArrayBuffer   *buffer;
    unsigned int  byteOffset;
    unsigned int  byteLength;
    unsigned int  length;

} ArrayBufferView;

#ifdef __cplusplus
}
#endif

#endif // ARRAYBUFFER_H
