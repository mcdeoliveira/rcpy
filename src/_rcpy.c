#include <Python.h>

#include <rc_usefulincludes.h>
#include <roboticscape.h>

/* initialization */
static PyObject *rcpyError;
static PyObject *rcpy_initialize(PyObject *self);
static PyObject *rcpy_cleanup(PyObject *self);
static PyObject *rcpy_get_state(PyObject *self);
static PyObject *rcpy_set_state(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
  {"initialize",
   (PyCFunction)rcpy_initialize,
   METH_NOARGS,
   "Initialize robotics cape"}
  ,
  {"cleanup",
   (PyCFunction)rcpy_cleanup,
   METH_NOARGS,
   "Clean up robotics cape"}
  ,
  {"get_state",
   (PyCFunction)rcpy_get_state,
   METH_NOARGS,
   "Get robotics cape state"}
  ,
  {"set_state",
   (PyCFunction)rcpy_set_state,
   METH_VARARGS,
   "Set robotics cape state"}
  ,
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "_rcpy",
  "This module provides an interface to the robotics cape",
  -1,
   module_methods
};

/* python functions */

PyMODINIT_FUNC PyInit__rcpy(void)
{
  PyObject *m;

  /* create module */
  m = PyModule_Create(&module);
  if (m == NULL)
    return NULL;

  /* create exception */
  rcpyError = PyErr_NewException("rcpy.error", NULL, NULL);
  Py_INCREF(rcpyError);
  PyModule_AddObject(m, "error", rcpyError);
  
  return m;
}

static
PyObject *rcpy_initialize(PyObject *self)
{

  /* initialize cape */
  if(rc_initialize()){
    PyErr_SetString(rcpyError, "Failed to initialize cape");
    return NULL;
  }

  /* disable default signal handler */
  rc_disable_signal_handler();

  /* a python signal handler will be installed by rc.__init__ */
  
  /* return None */
  return Py_BuildValue("");
}

static
PyObject *rcpy_cleanup(PyObject *self)
{

  /* clean up cape */
  if (rc_cleanup()) {
    PyErr_SetString(rcpyError, "Failed to clean up cape");
    return NULL;
  }
  
  /* return None */
  return Py_BuildValue("");
}

static
PyObject *rcpy_get_state(PyObject *self)
{
  /* return cape state */
  return Py_BuildValue("i", rc_get_state());
}

static
PyObject *rcpy_set_state(PyObject *self, PyObject *args)
{

  /* parse arguments */
  int state;
  if (!PyArg_ParseTuple(args, "i", &state)) {
    PyErr_SetString(rcpyError, "Invalid argument");
    return NULL;
  }
  
  /* set up cape state */
  if (rc_set_state(state)) {
    PyErr_SetString(rcpyError, "Failed to set up cape state");
    return NULL;
  }
  
  /* return None */
  return Py_BuildValue("");
}
