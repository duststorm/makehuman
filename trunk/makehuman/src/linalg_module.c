#include <Python.h>
//#include <linalg_module.h>
#undef min
#undef max
#include <dgemm.h>
#include <dgesvd.h>

//includes lapack...
static void double2PyObj(double* d, PyObject *_result, int i, int j)
{
    int index;
    int resultLen =  i*j;
    _result = PyList_New(resultLen);
    for (index = 0; index < resultLen; index++)
    {
      PyObject *item; 
      item = Py_BuildValue("d", d[index]);
      PyList_SetItem(_result, index, item);
    }
}

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
  int i,j,k, index;
  //int resultLen = i*k;
  //double result[resultLen]; 
  double alpha = 1;
  double beta = 0;

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
      
  //convert to python list
  result = malloc(i*k*sizeof(double));
  if (!dgemm_("N", "B", &i, &k, &j, &alpha, m, &i, n, &j, &beta, result, &i))
      double2PyObj(result, _result, i, k);
  
  free(result);
  free(n);
  free(m);
  // return flat matrix list
  return _result;
}

//svd:  m = u*s*vt (vt is the transposed matrix of v)
static PyObject* mh_dgesvd(PyObject *self, PyObject *args)
{
  PyObject *_m, *_u, *_s, *_vt;
  double *m, *s, *u, *vt, *work; //s = singular values of m sorted by s(i)>s(i+1) 
  int i,j,k, index;
  int lwork = -1;
  int info = 0;
  
  if (!PyArg_ParseTuple(args, "Oii", &_m, &i, &j))
    return NULL;
  
  // need to be freed in the end
  m = PyObj2DoublePtr(_m, i*j);
  if (m==NULL)
    return NULL;
  
  // do something with m
    
  //free in the end
  u = malloc(i*i*sizeof(double));
  s = malloc(i*j*sizeof(double));
  vt = malloc(j*j*sizeof(double));

  if (!dgesvd_("A", "A", &i, &j, m, &i, s, u, &i, vt, &j, work, &lwork, &info))
  {
    double2PyObj(u, _u, i, i);
    double2PyObj(vt, _vt, j, j);
    double2PyObj(s, _s, i, j);
  }
  
  free(vt); free(s); free(u); free(m);

  return Py_BuildValue("[O,O,O]", _u, _s, _vt);
}

static PyMethodDef EmbMethods[] =
{
    {"mmmul", mh_dgemm, METH_VARARGS, ""},
    //{"mvmul", mh_dgemv, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initlinalg(void)
{
    (void) Py_InitModule("linalg", EmbMethods);
}
