#include <Python.h>

#include <rc/encoder_eqep.h>
#include <rc/encoder_pru.h>

static char module_docstring[] =
  "This module provides an interface for encoder.";

static PyObject *encoderError;

// one-shot sampling mode functions
static PyObject *encoder_read(PyObject *self, PyObject *args);
static PyObject *encoder_set(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
  {"get",
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
  "_encoder",   /* name of module */
  module_docstring, /* module documentation, may be NULL */
  -1,       /* size of per-interpreter state of the module,
	       or -1 if the module keeps state in global variables. */
   module_methods
};

/* python functions */

PyMODINIT_FUNC PyInit__encoder(void)
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

  /* initialize encoders */
  /* remember to call rc_encoder_eqep_cleanup() later */
  if(rc_encoder_eqep_init())
    return NULL;
  // this may fail if not root or someone broke PRU again
  // continue anyway if it fails, encoder 4 just won't work
  // remember to call rc_encoder_pru_cleanup() later
  if(rc_encoder_pru_init()==-1){}

  return m;
}

static
PyObject *encoder_read(PyObject *self,
		       PyObject *args)
{

  /* parse arguments */
  int channel;
  if (!PyArg_ParseTuple(args, "i", &channel)) {
    PyErr_SetString(encoderError, "Invalid arguments");
    return NULL;
  }

  int count;

  /* read encoder */
  if(channel==4) count=rc_encoder_pru_read();
  else count=rc_encoder_eqep_read(channel);

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("i", count);

  return ret;
}

static
PyObject *encoder_set(PyObject *self,
		      PyObject *args)
{

  /* parse arguments */
  int channel, count = 0;
  if (!PyArg_ParseTuple(args, "i|i", &channel, &count)) {
    PyErr_SetString(encoderError, "Invalid arguments");
    return NULL;
  }

  /* set encoder */
  if(channel==4) count=rc_encoder_pru_write(count);
  else count=rc_encoder_eqep_write(channel, count);

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}
