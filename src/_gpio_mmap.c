#include <Python.h>

#include <rc_usefulincludes.h>
#include <roboticscape.h>

static char module_docstring[] =
  "This module provides an interface for gpio_mmap.";

static PyObject *gpio_mmapError;

// set and get functions
static PyObject *gpio_mmap_set(PyObject *self, PyObject *args);
static PyObject *gpio_mmap_get(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
  {"set",
   (PyCFunction)gpio_mmap_set,
   METH_VARARGS,
   "set gpio value"}
  ,
  {"get",
   (PyCFunction)gpio_mmap_get,
   METH_VARARGS,
   "get gpio value (nonblocking)"}
  ,
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "_gpio_mmap",   /* name of module */
  module_docstring, /* module documentation, may be NULL */
  -1,       /* size of per-interpreter state of the module,
	       or -1 if the module keeps state in global variables. */
   module_methods
};

/* python functions */

PyMODINIT_FUNC PyInit__gpio_mmap(void)
{
  PyObject *m;
  
  /* create module */
  m = PyModule_Create(&module);
  if (m == NULL)
    return NULL;

  /* create exception */
  gpio_mmapError = PyErr_NewException("gpio_mmap.error", NULL, NULL);
  Py_INCREF(gpio_mmapError);
  PyModule_AddObject(m, "error", gpio_mmapError);

  /* initialize cape */
  if (rc_get_state() == UNINITIALIZED) {
    // printf("* * * gpio_mmap: WILL CALL INIT * * *\n");
    if(rc_initialize())
      return NULL;
  }
  
  return m;
}

static
PyObject *gpio_mmap_set(PyObject *self,
			PyObject *args)
{

  /* parse arguments */
  int gpio, value = 0;
  if (!PyArg_ParseTuple(args, "I|i", &gpio, &value)) {
    PyErr_SetString(gpio_mmapError, "Invalid arguments");
    return NULL;
  }

  /* set gpio value */
  if (rc_gpio_set_value_mmap(gpio, value) < 0) {
    PyErr_SetString(gpio_mmapError, "Failed to set gpio value");
    return NULL;
  }
    
  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *gpio_mmap_get(PyObject *self,
			PyObject *args)
{

  /* parse arguments */
  int gpio;
  if (!PyArg_ParseTuple(args, "I", &gpio)) {
    PyErr_SetString(gpio_mmapError, "Invalid arguments");
    return NULL;
  }

  /* get gpio_mmap value */
  int value;
  if ((value = rc_gpio_get_value_mmap(gpio)) < 0) {
    PyErr_SetString(gpio_mmapError, "Failed to get gpio value");
    return NULL;
  }
  
  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("i", value);

  return ret;
}

