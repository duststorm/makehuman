#undef min
#undef max
#include <Python.h>

#ifdef __APPLE__ /* On OS X use cblas for matrix funcs... */
#	include <Accelerate/Accelerate.h>
#	define min(a,b) (((a) < (b)) ? (a) : (b))
#	define max(a,b) (((a) > (b)) ? (a) : (b))
#else
#	include <dgemm.h>
#	include <dgesvd.h>
#endif

//includes lapack...
PyObject *double2PyObj(double* d, int i, int j)
{
    int index;
    int resultLen =  i*j;
    PyObject *_result = PyList_New(resultLen);
    if (!_result)
      return NULL;
    for (index = 0; index < resultLen; index++)
    {
      
      PyObject *item = PyFloat_FromDouble(d[index]);
      if (!item)
      {
        Py_DECREF(_result);
        return NULL;
      }
      PyList_SET_ITEM(_result, index, item);
    }

    return _result;
}

//note that the returned double should be freed
double* PyObj2DoublePtr(PyObject *dSeq, int seqlen)
{
    //PyObject* dSeq;
    double *dC;
    //int seqlen;
    int i;
    
    dSeq = PySequence_Fast(dSeq, "argument must be iterable");
    if(!dSeq)
        return NULL;
 
    // prepare data as an array of doubles 
    //*seqlen = PySequence_Fast_GET_SIZE(seq);
    dC = (double*)malloc(seqlen*sizeof(double));
    if(!dC) 
    {
        Py_DECREF(dSeq);
        //return PyErr_NoMemory( );
        return NULL;
    }

    for(i=0; i < seqlen; i++) 
    {
        PyObject *fitem;
        PyObject *item = PySequence_Fast_GET_ITEM(dSeq, i);
        if(!item) 
        {
            Py_DECREF(dSeq);
            free(dC);
            return NULL;
        }
        fitem = PyNumber_Float(item);
        if(!fitem) 
        {
            Py_DECREF(dSeq);
            free(dC);
            PyErr_SetString(PyExc_TypeError, "all items must be numbers");
            return NULL;
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
  int i,j,k;
  double alpha = 1;
  double beta = 0;
  char a[] = "T"; //Transpose because blas is column-major and mh is row-major
  char b[] = "T"; //be careful when using lapack and blas methods even if the parameters have the same value they should be sent with different pointers

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
      
  result = (double*)malloc(i*k*sizeof(double));
  dgemm_(a, b, (long*)&i, (long*)&k, (long*)&j, &alpha, m, (long*)&i, n, (long*)&j, &beta, result, (long*)&i);
  _result = double2PyObj(result, j, k);
  
  free(result); free(n); free(m);

  return _result;
}

//svd:  m = u*s*vt (vt is the transposed matrix of v)
static PyObject* mh_dgesvd(PyObject *self, PyObject *args)
{
#if __APPLE__
  int dims;
#endif	
  PyObject *_m, *_u, *_s, *_vt;
  double *m, *s, *u, *vt, *work; //s = singular values of m sorted by s(i)>s(i+1) 
  int i,j;
  long lwork = -1;
  long info = 0;
  char a[] = "A"; //returns all the rows of U and V (full svd)
  char b[] = "A"; //be careful when using lapack and blas methods even if the parameters have the same value they should be sent with different pointers
  
  if (!PyArg_ParseTuple(args, "Oii", &_m, &i, &j))
    return NULL;
  
  // need to be freed in the end
  m = PyObj2DoublePtr(_m, i*j);
  if (m==NULL)
    return NULL;
  
  // do something with m
    
  //free in the end
  dims = min(i,j);
  u = (double*)malloc(i*i*sizeof(double));
  s = (double*)malloc(dims*sizeof(double));
  vt = (double*)malloc(j*j*sizeof(double));
  lwork = 5*(i+j);
  work = (double*)malloc(lwork*sizeof(double));

  dgesvd_(a, b, (long*)&i, (long*)&j, m, (long*)&i, s, u, (long*)&i, vt, (long*)&j, work, &lwork, &info);
  _u = double2PyObj(u, i, i);
  _vt = double2PyObj(vt, j, j);
  _s = double2PyObj(s, i, j);
 
  
  free(work); free(vt); free(s); free(u); free(m);

  return Py_BuildValue("[O,O,O]", _u, _s, _vt);
}

static PyMethodDef EmbMethods[] =
{
    {"mmmul", mh_dgemm, METH_VARARGS, ""},
    {"svd", mh_dgesvd, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initlinalg(void)
{
    (void) Py_InitModule("linalg", EmbMethods);
}
