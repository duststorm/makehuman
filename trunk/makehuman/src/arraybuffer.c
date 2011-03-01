/** \file core.c
 *  \brief ArrayBuffer and typed array views.

 <table>
 <tr><td>Project Name:                                   </td>
     <td><b>MakeHuman</b>                                </td></tr>
 <tr><td>Product Home Page:                              </td>
     <td>http://www.makehuman.org/                       </td></tr>
 <tr><td>Google Home Page:                               </td>
     <td>http://code.google.com/p/makehuman/             </td></tr>
 <tr><td>Authors:                                        </td>
     <td>Marc Flerackers                                 </td></tr>
 <tr><td>Copyright(c):                                   </td>
     <td>MakeHuman Team 2001-2011                        </td></tr>
 <tr><td>Licensing:                                      </td>
     <td>GPL3 (see also
         http://sites.google.com/site/makehumandocs/licensing</td></tr>
 <tr><td>Coding Standards:                               </td>
     <td>See http://sites.google.com/site/makehumandocs/developers-guide#TOC-Coding-Style
                                                         </td></tr>
 </table>

 This module contains the ArrayBuffer object and its typed array views.

 */

#ifdef _DEBUG
#undef _DEBUG
#include <Python.h>
#define _DEBUG
#else
#include <Python.h>
#endif
#ifdef __APPLE__
#include <Python/structmember.h>
#else
#include <structmember.h>
#endif

#include "arraybuffer.h"

// ArrayBuffer attributes directly accessed by Python
static PyMemberDef ArrayBuffer_members[] =
{
    {"byteLength", T_INT, offsetof(ArrayBuffer, byteLength), READONLY , "Read-only property. The length of the ArrayBuffer in bytes, as fixed at construction time."},
    {NULL}  /* Sentinel */
};

void ArrayBuffer_dealloc(ArrayBuffer *self);
PyObject *ArrayBuffer_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
int ArrayBuffer_init(ArrayBuffer *self, PyObject *args, PyObject *kwds);

// ArrayBuffer type definition
PyTypeObject ArrayBufferType =
{
    PyObject_HEAD_INIT(NULL)
    0,                                        // ob_size
    "mh.ArrayBuffer",                         // tp_name
    sizeof(ArrayBuffer),                      // tp_basicsize
    0,                                        // tp_itemsize
    (destructor)ArrayBuffer_dealloc,          // tp_dealloc
    0,                                        // tp_print
    0,                                        // tp_getattr
    0,                                        // tp_setattr
    0,                                        // tp_compare
    0,                                        // tp_repr
    0,                                        // tp_as_number
    0,                                        // tp_as_sequence
    0,                                        // tp_as_mapping
    0,                                        // tp_hash
    0,                                        // tp_call
    0,                                        // tp_str
    0,                                        // tp_getattro
    0,                                        // tp_setattro
    0,                                        // tp_as_buffer
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, // tp_flags
    "ArrayBuffer object",                     // tp_doc
    0,		                                    // tp_traverse
    0,		                                    // tp_clear
    0,		                                    // tp_richcompare
    0,		                                    // tp_weaklistoffset
    0,		                                    // tp_iter
    0,		                                    // tp_iternext
    0,                                        // tp_methods
    ArrayBuffer_members,                      // tp_members
    0,                                        // tp_getset
    0,                                        // tp_base
    0,                                        // tp_dict
    0,                                        // tp_descr_get
    0,                                        // tp_descr_set
    0,                                        // tp_dictoffset
    (initproc)ArrayBuffer_init,               // tp_init
    0,                                        // tp_alloc
    ArrayBuffer_new,                          // tp_new
};

void ArrayBuffer_dealloc(ArrayBuffer *self)
{
    // Free our data
    free(self->data);

    // Free Python data
    self->ob_type->tp_free((ArrayBuffer*)self);
}

PyObject *ArrayBuffer_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    // Alloc Python data
    ArrayBuffer *self = (ArrayBuffer*)type->tp_alloc(type, 0);

    // Init our data
    if (self)
    {
        self->byteLength = 0;
        self->data = NULL;
    }

    return (PyObject*)self;
}

int ArrayBuffer_init(ArrayBuffer *self, PyObject *args, PyObject *kwds)
{
    int byteLength;

    if (!PyArg_ParseTuple(args, "i", &byteLength))
        return -1;

    self->byteLength = byteLength;
    self->data = malloc(byteLength);
    memset(self->data, 0, byteLength);

    return 0;
}

void RegisterArrayBuffer(PyObject *module)
{
  if (PyType_Ready(&ArrayBufferType) < 0)
    return;

  Py_INCREF(&ArrayBufferType);
  PyModule_AddObject(module, "ArrayBuffer", (PyObject*)&ArrayBufferType);
}

// ArrayBufferView
typedef void(*Py2C)(void *, PyObject*);
typedef PyObject*(*C2Py)(void *);

typedef struct _ArrayBufferViewType
{
  PyTypeObject type;
  int BYTES_PER_ELEMENT;
  Py2C py2c;
  C2Py c2py;

} ArrayBufferViewType;

// ArrayBufferView as sequence
Py_ssize_t ArrayBufferView_length(ArrayBufferView *self)
{
  return self->length;
}

PyObject *ArrayBufferView_item(ArrayBufferView *self, Py_ssize_t i)
{
  ArrayBufferViewType *type = (ArrayBufferViewType*)self->ob_type;
  char *data = (char*)self->buffer->data + self->byteOffset + i * type->BYTES_PER_ELEMENT;

  if (i >= self->length)
  {
      PyErr_Format(PyExc_IndexError, "element index out of range");
      return NULL;
  }

  return (*type->c2py)(data);
}

int ArrayBufferView_ass_item(ArrayBufferView *self, Py_ssize_t i, PyObject *value)
{
  ArrayBufferViewType *type = (ArrayBufferViewType*)self->ob_type;
  char *data = (char*)self->buffer->data + self->byteOffset + i * type->BYTES_PER_ELEMENT;

  if (i >= self->length)
  {
    PyErr_Format(PyExc_IndexError, "element index out of range");
    return -1;
  }

  (*type->py2c)(data, value);
  return 0;
}

void ArrayBufferView_dealloc(ArrayBufferView *self);
PyObject *ArrayBufferView_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
int ArrayBufferView_init(ArrayBufferView *self, PyObject *args, PyObject *kwds);

static PySequenceMethods ArrayBufferView_as_sequence = {
  (lenfunc)ArrayBufferView_length,            // sq_length
  0,                                          // sq_concat
  0,                                          // sq_repeat
  (ssizeargfunc)ArrayBufferView_item,         // sq_item
  0,                                          // sq_slice
  (ssizeobjargproc)ArrayBufferView_ass_item,  // sq_ass_item
  0,                                          // sq_ass_slice
  0,                                          // sq_contains
  0,                                          // sq_inplace_concat
  0,                                          // sq_inplace_repeat
};

// ArrayBufferView attributes directly accessed by Python
static PyMemberDef ArrayBufferView_members[] =
{
  {"buffer", T_OBJECT_EX, offsetof(ArrayBufferView, buffer), READONLY , "Read-only property. The ArrayBuffer that this ArrayBufferView references."},
  {"byteOffset", T_INT, offsetof(ArrayBufferView, byteOffset), READONLY , "Read-only property. The offset of this ArrayBufferView from the start of its ArrayBuffer, in bytes, as fixed at construction time."},
  {"byteLength", T_INT, offsetof(ArrayBufferView, byteLength), READONLY , "Read-only property. The length of the ArrayBufferView in bytes, as fixed at construction time."},
  {"length", T_INT, offsetof(ArrayBufferView, length), READONLY, "The length of the TypedArray in elements, as fixed at construction time."},
  {NULL}  /* Sentinel */
};

PyObject *ArrayBufferView_BYTES_PER_ELEMENT(ArrayBufferView *self, void *closure)
{
  return PyInt_FromLong(((ArrayBufferViewType*)self->ob_type)->BYTES_PER_ELEMENT);
}

// ArrayBufferView attributes indirectly accessed by Python
static PyGetSetDef ArrayBufferView_getset[] =
{
  {"BYTES_PER_ELEMENT", (getter)ArrayBufferView_BYTES_PER_ELEMENT, (setter)NULL, "The size in bytes of each element in the array.", NULL},
  {NULL}
};

void ArrayBufferView_dealloc(ArrayBufferView *self)
{
  // Free our data
  if (self->buffer)
      Py_DECREF(self->buffer);

  // Free Python data
  self->ob_type->tp_free((ArrayBufferView*)self);
}

PyObject *ArrayBufferView_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
  // Alloc Python data
  ArrayBufferView *self = (ArrayBufferView*)type->tp_alloc(type, 0);

  // Init our data
  if (self)
  {
      self->buffer = 0;
      self->byteOffset = 0;
      self->byteLength = 0;
      self->length = 0;
  }

  return (PyObject*)self;
}

int ArrayBufferView_init(ArrayBufferView *self, PyObject *args, PyObject *kwds)
{
  PyObject *firstObject;
  int byteOffset = 0;
  int byteLength = -1;

  if (!PyArg_ParseTuple(args, "O|ii", &firstObject, &byteOffset, &byteLength))
      return -1;

  // ArrayBufferView(length)
  if (PyInt_Check(firstObject))
  {
      int length = PyInt_AsLong(firstObject);
      self->buffer = PyObject_New(ArrayBuffer, &ArrayBufferType);
      self->buffer->byteLength = length * ((ArrayBufferViewType*)self->ob_type)->BYTES_PER_ELEMENT;
      self->buffer->data = malloc(self->buffer->byteLength);
      memset(self->buffer->data, 0, self->buffer->byteLength);
      self->byteLength = self->buffer->byteLength;
      self->length = length;
  }
  // ArrayBufferView(arrayBufferView)
  else if (firstObject->ob_type == self->ob_type)
  {
      ArrayBufferView *other = (ArrayBufferView*)firstObject;
      self->buffer = other->buffer;
      Py_INCREF(self->buffer);
      self->byteOffset = other->byteOffset;
      self->byteLength = other->byteLength;
      self->length = other->length;
  }
  // ArrayBufferView(arrayBuffer, byteOffset, byteLength)
  else if (PyObject_TypeCheck(firstObject, &ArrayBufferType))
  {
      self->buffer = (ArrayBuffer*)firstObject;
      Py_INCREF(self->buffer);
      if (byteLength == -1)
          byteLength = self->buffer->byteLength - byteOffset;
      self->byteOffset = byteOffset;
      self->byteLength = byteLength;
      self->length = byteLength / ((ArrayBufferViewType*)self->ob_type)->BYTES_PER_ELEMENT;
  }
  // ArrayBufferView(list)
  else if (PySequence_Check(firstObject))
  {
      int size = (int)PySequence_Size(firstObject);
      int i;
      ArrayBufferViewType *type = (ArrayBufferViewType*)self->ob_type;

      self->buffer = PyObject_New(ArrayBuffer, &ArrayBufferType);
      self->buffer->byteLength = size * type->BYTES_PER_ELEMENT;
      self->buffer->data = malloc(self->buffer->byteLength);
    
      for (i = 0; i < size; i++)
          type->py2c((char*)self->buffer->data + i * type->BYTES_PER_ELEMENT, PySequence_ITEM(firstObject, i));

      self->byteOffset = 0;
      self->byteLength = self->buffer->byteLength;
      self->length = size;
  }

  return 0;
}

typedef struct _TypedArrayViewInfo
{
    const char *name;
    int BYTES_PER_ELEMENT;
    Py2C py2c;
    C2Py c2py;
} TypedArrayViewInfo;

void RegisterTypedArrayView(PyObject *module, TypedArrayViewInfo *info)
{
  ArrayBufferViewType *type = (ArrayBufferViewType*)malloc(sizeof(ArrayBufferViewType));
  memset((void*)type, 0, sizeof(ArrayBufferViewType));

  type->type.tp_name = info->name;
  type->type.tp_basicsize = sizeof(ArrayBufferView);
  type->type.tp_dealloc = (destructor)ArrayBufferView_dealloc;
  type->type.tp_as_sequence = &ArrayBufferView_as_sequence;
  type->type.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
  type->type.tp_doc = info->name;
  type->type.tp_members = ArrayBufferView_members;
  type->type.tp_getset = ArrayBufferView_getset;
  type->type.tp_init = (initproc)ArrayBufferView_init;
  type->type.tp_new = ArrayBufferView_new;
  type->BYTES_PER_ELEMENT = info->BYTES_PER_ELEMENT;
  type->py2c = info->py2c;
  type->c2py = info->c2py;

  if (PyType_Ready((PyTypeObject*)type) < 0)
    return;

  Py_INCREF(type);
  PyModule_AddObject(module, info->name, (PyObject*)type);
}

void PyToUint8(void *data, PyObject *object)
{
  *(unsigned char*)data = (unsigned char)PyInt_AsLong(object);
}

PyObject *Uint8ToPy(void *data)
{
  return PyInt_FromLong(*(unsigned char*)data);
}

TypedArrayViewInfo Uint8ArrayInfo =
{
  "Uint8Array",
  sizeof(unsigned char),
  &PyToUint8,
  &Uint8ToPy
};

void PyToUint16(void *data, PyObject *object)
{
  *(unsigned short*)data = (unsigned short)PyInt_AsLong(object);
}

PyObject *Uint16ToPy(void *data)
{
  return PyInt_FromLong(*(unsigned short*)data);
}

TypedArrayViewInfo Uint16ArrayInfo =
{
  "Uint16Array",
  sizeof(unsigned short),
  &PyToUint16,
  &Uint16ToPy
};

void PyToUint32(void *data, PyObject *object)
{
  *(unsigned int*)data = (unsigned int)PyInt_AsLong(object);
}

PyObject *Uint32ToPy(void *data)
{
  return PyInt_FromLong(*(unsigned int*)data);
}

TypedArrayViewInfo Uint32ArrayInfo =
{
  "Uint32Array",
  sizeof(unsigned int),
  &PyToUint32,
  &Uint32ToPy
};

void PyToFloat32(void *data, PyObject *object)
{
  *(float*)data = (float)PyFloat_AsDouble(object);
}

PyObject *Float32ToPy(void *data)
{
  return PyFloat_FromDouble(*(float*)data);
}

TypedArrayViewInfo Float32ArrayInfo =
{
    "Float32Array",
    sizeof(float),
    &PyToFloat32,
    &Float32ToPy
};

void PyToFloat64(void *data, PyObject *object)
{
  *(double*)data = PyFloat_AsDouble(object);
}

PyObject *Float64ToPy(void *data)
{
  return PyFloat_FromDouble(*(double*)data);
}

TypedArrayViewInfo Float64ArrayInfo =
{
  "Float64Array",
  sizeof(double),
  &PyToFloat64,
  &Float64ToPy
};

void RegisterTypedArrayViews(PyObject *module)
{
  RegisterTypedArrayView(module, &Uint8ArrayInfo);
  RegisterTypedArrayView(module, &Uint16ArrayInfo);
  RegisterTypedArrayView(module, &Uint32ArrayInfo);
  RegisterTypedArrayView(module, &Float32ArrayInfo);
  RegisterTypedArrayView(module, &Float64ArrayInfo);
}
