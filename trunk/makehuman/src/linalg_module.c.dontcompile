#include <Python.h>
//#include <linalg_module.h>
#undef min
#undef max
#include <dgemm.h>
#include <dgemv.h>

//includes lapack...
//note that the returned double should be freed
static double* PyObj2DoublePtr(PyObject *dP, int seqlen)
{
    PyObject* dSeq;
    double *dC;
    //int seqlen;
    int i;
    
    // get one argument as a sequence 
    if(!PyArg_ParseTuple(dP, "O", &dSeq))
        return dC;
    dSeq = PySequence_Fast(dSeq, "argument must be iterable");
    if(!dSeq)
        return dC;
 
    // prepare data as an array of doubles 
    //*seqlen = PySequence_Fast_GET_SIZE(seq);
    dC = malloc(seqlen*sizeof(double));
    if(!dC) 
    {
        Py_DECREF(dSeq);
        //return PyErr_NoMemory( );
        return dC;
    }

    for(i=0; i < seqlen; i++) 
    {
        PyObject *fitem;
        PyObject *item = PySequence_Fast_GET_ITEM(dP, i);
        if(!item) 
        {
            Py_DECREF(dSeq);
            free(dC);
            return dC;
        }
        fitem = PyNumber_Float(item);
        if(!fitem) 
        {
            Py_DECREF(dSeq);
            free(dC);
            PyErr_SetString(PyExc_TypeError, "all items must be numbers");
            return dC;
        }
        dC[i] = PyFloat_AS_DOUBLE(fitem);
        Py_DECREF(fitem);
    }

    Py_DECREF(dSeq);
    return dC;
}

//matrix multiplication:  m . n = result, m is an ixj matrix and n is a jxk matrix
static PyObject* mh_dgemm(PyObject *self, PyObject *args)
{
  PyObject *_m, *_n, *_result;
  double *m, *n, *result; 
  int i,j,k, index, resultLen;

  if (!PyArg_ParseTuple(args, "OOiii", &_m, &_n, &i, &j, &k))
    return NULL;
  
  // need to be freed in the end
  m = PyObj2DoublePtr(_m, i*j);
  if (m==NULL)
    return NULL;
  
  // need to be freed in the end
  n = PyObj2DoublePtr(_n, j*k);
  if (n==NULL)
    return NULL;
  
  // do something with m and n
  resultLen = i*k;
  _result = PyList_New(resultLen);
  // need to be freed in the end
  result = malloc(resultLen*sizeof(double));
    
  //convert to python list
  if (!dgemm_("N", "B", i, k, j, 1, m, i, n, j, 0, result, i))
  {
    for (index = 0; index< resultLen; index++)
    {
      PyObject *item; 
      item = Py_BuildValue("d", result[index]);
      PyList_SetItem(_result, index, item);
    }
  }
  
  free(result);
  free(n);
  free(m);
  // return flat matrix list
  return _result;
}

/*
static PyObject* mh_dgesvd(PyObject *self, PyObject *args)
{
  PyObject *_m;
  int i,j;
  if (!PyArg_ParseTuple(args, "Oii", &_m, &i, &j))
    return NULL;
  
  // need to be freed in the end
  double *m = PyObj2DoublePtr(_m, i*j);
  if (m==NULL)
    return NULL;
    
  // do something with m and n
  int resultLen = i*k;
  PyObject *_result = PyList_New(resultLen);
  double result = malloc(resultLen*sizeof(double));
  int check = dgemm("N", "B", i, k, j, 1, m, i, n, j, 0, result, i);
    
  //convert to python list
  if (check != 0)
  {
    for (int index = 0; index< resultLen; index++)
    {
      PyObject *item = Py_BuildValue("d", result[index]);
      PyList_SetItem(_result, index, item)
    }
  }
  
  //@todo: free m, n and result
  free(m);
  free(result);
  // return flat matrix list
  return _result;
}
*/

static PyMethodDef EmbMethods[] =
{
    {"mmmul", mh_dgemm, METH_VARARGS, ""},
    //{"mvmul", mh_dgemv, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}
};