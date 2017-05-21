#include <Python.h>

#include <rc_usefulincludes.h>
#include <roboticscape.h>

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

  /* initialize cape */
  if (rc_get_state() == UNINITIALIZED) {
    printf("* * * encoder: WILL CALL INIT * * *\n");
    if(rc_initialize())
      return NULL;
  }
  
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
