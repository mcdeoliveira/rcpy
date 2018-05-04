#include <Python.h>

#include <rc/start_stop.h>

/* initialization */
static PyObject *rcpyError;
static PyObject *rcpy_get_state(PyObject *self);
static PyObject *rcpy_set_state(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
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
  rc_set_state(state);

  /* return None */
  return Py_BuildValue("");
}
