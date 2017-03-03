#include <Python.h>

#include <rc_usefulincludes.h>
#include <roboticscape.h>

static char module_docstring[] =
  "This module provides an interface for encoder.";

static PyObject *encoderError;

// initialization
static PyObject *encoder_initialize(PyObject *self, PyObject *args, PyObject *kwargs);

// one-shot sampling mode functions
static PyObject *encoder_read(PyObject *self, PyObject *args);
static PyObject *encoder_set(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
  {"initialize",
   (PyCFunction)encoder_initialize,
   METH_VARARGS | METH_KEYWORDS,
   "initialize encoders"}
  ,
  {"read",
   (PyCFunction)encoder_read,
   METH_VARARGS,
   "read encoder"}
  ,
  {"set",
   (PyCFunction)encoder_set,
   METH_VARARGS,
   "set encoder"}
  ,
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "encoder",   /* name of module */
  module_docstring, /* module documentation, may be NULL */
  -1,       /* size of per-interpreter state of the module,
	       or -1 if the module keeps state in global variables. */
   module_methods
};

/* auxiliary function */

static int encoder_enable_eqep4 = 1;     // eqep4 configuration
static int encoder_initialized_flag = 0; // initialized flag
static int rc_initialized_flag = 0;      // cape initialized flag

static
int encoder_initialize_encoder(void) {

  // Already initialized?
  if (encoder_initialized_flag)
    return 0;

  // Cape initialized?
  if (!rc_initialized_flag) {
    if(rc_initialize()){
      PyErr_SetString(encoderError, "Failed to initialize ROBOTICS CAPE");
      return -1;
    }
    rc_initialized_flag = 1;
  }

  // set flag
  encoder_initialized_flag = 1;
  
  return 0;
}

/* python functions */

PyMODINIT_FUNC PyInit_encoder(void)
{
  PyObject *m;

  /* create module */
  m = PyModule_Create(&module);
  if (m == NULL)
    return NULL;

  /* create exception */
  encoderError = PyErr_NewException("encoder.error", NULL, NULL);
  Py_INCREF(encoderError);
  PyModule_AddObject(m, "error", encoderError);

  // Make sure the GIL has been created since we need to acquire it in our
  // callback to safely call into the python application.
  if (! PyEval_ThreadsInitialized()) {
    PyEval_InitThreads();
  }
  
  return m;
}

static
PyObject *encoder_initialize(PyObject *self,
			     PyObject *args,
			     PyObject *kwargs)
{

  static char *kwlist[] = {
    "enable_eqep4",    /* int */
    NULL
  };
  
  PyObject *ret;

  /* Parse parameters */
  if (! PyArg_ParseTupleAndKeywords(args, kwargs, "|i", kwlist,
				    &encoder_enable_eqep4 /* int */ )) {
    PyErr_SetString(encoderError, "Failed to initialize encoder");
    return NULL;
  }

  /* Initialize encoder */
  encoder_initialized_flag = 0;
  if(encoder_initialize_encoder())
    return NULL;

  /* Build the output tuple */
  ret = Py_BuildValue("");

  return ret;
}


static
PyObject *encoder_read(PyObject *self,
		       PyObject *args)
{

  /* initialize */
  if (encoder_initialize_encoder())
    return NULL;

  /* parse arguments */
  int channel;
  if (!PyArg_ParseTuple(args, "i", &channel)) {
    PyErr_SetString(encoderError, "Invalid arguments");
    return NULL;
  }

  /* read encoder */
  int count = rc_get_encoder_pos(channel);
  
  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("i", count);

  return ret;
}

static
PyObject *encoder_set(PyObject *self,
		      PyObject *args)
{

  /* initialize */
  if (encoder_initialize_encoder())
    return NULL;

  /* parse arguments */
  int channel, count = 0;
  if (!PyArg_ParseTuple(args, "i|i", &channel, &count)) {
    PyErr_SetString(encoderError, "Invalid arguments");
    return NULL;
  }

  /* set encoder */
  rc_set_encoder_pos(channel, count);
  
  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}
