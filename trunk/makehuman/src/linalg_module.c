#ifdef __APPLE__ /* On OS X use cblas for matrix funcs... */
#   include <Python/Python.h>
#	include <Accelerate/Accelerate.h>

#   include <sys/param.h> // For MIN, MAX
#   ifndef min
#       define min MIN
#   endif
#   ifndef max
#       define max MAX
#   endif

#else // ! __APPLE__

#   include <Python.h>

#   ifdef min
#       undef min
#   endif
#   ifdef max
#       undef max
#   endif

#   include <dgemm.h>
#   include <dgesvd.h>
#   include <dgetrf.h>
#   include <dgesvx.h>

#endif /* #ifdef __APPLE__ */

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
  int dim;
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
  dim = min(i,j);
  u = (double*)malloc(i*i*sizeof(double));
  s = (double*)malloc(dim*sizeof(double));
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

//lu factorization : A= P*L*U
static PyObject* mh_dgetrf(PyObject *self, PyObject *args)
{
  PyObject *_a, *_result;
  double *a;
  int i,j;
  long info = 0;
  int dim = 0;
  
  if (!PyArg_ParseTuple(args, "Oii", &_a, &i, &j))
    return NULL;
  
  // need to be freed in the end
  a = PyObj2DoublePtr(_a, i*j);
  if (a==NULL)
    return NULL;
  
  dim = min(i,j);
  dgetrf_((long*)&i, (long*)&j, a, (long*)&i, (long*)&dim, &info);
  _result = double2PyObj(a, i, j);
 
  free(a);
  
  return Py_BuildValue("O", _result);
}

// solving system of linear equations
// Reference: http://www.netlib.org/lapack/double/dgesvx.f
static PyObject* mh_dgesvx(PyObject *self, PyObject *args)
{
  PyObject *_a, *_b, *_x;
  double *a, *b, *af, *r, *c, *x, *ferr, *berr, *work; //s = singular  values of m sorted by s(i)>s(i+1) 
  long *p;
  long *iwork;
  int i;
  double rcond;
  int rhs = 1;
  long info = 0;
  char fact[] = "E"; //matrix will be equilibrated then factored
  char trans[] = "T"; //be careful when using lapack and blas methods even if the parameters have the same value they should be sent with different pointers
  char equed[] = "B";
  
  if (!PyArg_ParseTuple(args, "OOi", &_a, &_b, &i))
    return NULL;
  
  // need to be freed in the end
  a = PyObj2DoublePtr(_a, i*i);
  if (a==NULL)
    return NULL;
  b = PyObj2DoublePtr(_b, i);
  if (b==NULL)
    return NULL;
   
  //outputs:
  //af = 0;

  af = (double*)malloc(i*i*sizeof(double));
  //r = 0;
  r = (double*)malloc(i*sizeof(double));

  //c = 0;

  c = (double*)malloc(i*sizeof(double));
  //x = 0;

  x = (double*)malloc(i*sizeof(double));
  //ferr = 0;

  ferr = (double*)malloc(sizeof(double));
  //berr = 0;
  berr = (double*)malloc(sizeof(double));

  //work = 0;

  work = (double*)malloc(4*i*sizeof(double));
  //p = 0;

  p = (long*)malloc(i*sizeof(long));
  iwork = (long*)malloc(i*sizeof(long));

  dgesvx_(fact, trans, (long*)&i, (long*)&rhs, a, (long*)&i, af, (long*)&i, p, equed, r, c, b, (long*)&i, x, (long*)&i, (double*)&rcond, ferr, berr, work, iwork, &info);
  
  _x = double2PyObj(x, 1, i);
  

  free(iwork); free(p); free(work); free(berr); free(ferr); free(x); free(c);

  free(r); free(af); free(b); free(a);


  return Py_BuildValue("O", _x);
}

static PyMethodDef EmbMethods[] =
{
    {"mmmul", mh_dgemm, METH_VARARGS, ""},
    {"svd", mh_dgesvd, METH_VARARGS, ""},
    {"lu", mh_dgetrf, METH_VARARGS, ""},
    {"svx", mh_dgesvx, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initlinalg_module(void)
{
    (void) Py_InitModule("linalg_module", EmbMethods);
}
