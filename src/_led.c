#include <Python.h>

#include <rc_usefulincludes.h>
#include <roboticscape.h>

static char module_docstring[] =
  "This module provides an interface for the LEDs.";

static PyObject *ledError;

// led functions
static PyObject *led_set(PyObject *self, PyObject *args);
static PyObject *led_get(PyObject *self, PyObject *args);
static PyObject *led_blink(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
  {"set",
   (PyCFunction)led_set,
   METH_VARARGS,
   "set led"}
  ,
  {"get",
   (PyCFunction)led_get,
   METH_VARARGS,
   "get led"}
  ,
  {"blink",
   (PyCFunction)led_blink,
   METH_VARARGS,
   "blink led"}
  ,
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "led",   /* name of module */
  module_docstring, /* module documentation, may be NULL */
  -1,       /* size of per-interpreter state of the module,
	       or -1 if the module keeps state in global variables. */
  module_methods
};

/* python functions */

PyMODINIT_FUNC PyInit_led(void)
{
  PyObject *m;
  
  /* create module */
  m = PyModule_Create(&module);
  if (m == NULL)
    return NULL;

  /* create exception */
  ledError = PyErr_NewException("led.error", NULL, NULL);
  Py_INCREF(ledError);
  PyModule_AddObject(m, "error", ledError);

  /* initialize cape */
  if (rc_get_state() == UNINITIALIZED) {
    // printf("* * * led: WILL CALL INIT * * *\n");
    if(rc_initialize())
      return NULL;
  }
  
  return m;
}

static
PyObject *led_set(PyObject *self,
		  PyObject *args)
{
  
  /* parse arguments */
  int led, state;
  if (!PyArg_ParseTuple(args, "Ii", &led, &state)) {
    PyErr_SetString(ledError, "Invalid argument");
    return NULL;
  }

  /* set led */
  if (rc_set_led(led, state) < 0) {
    PyErr_SetString(ledError, "Failed");
    return NULL;
  }
    
  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *led_get(PyObject *self,
		  PyObject *args)
{
  
  /* parse arguments */
  int led;
  if (!PyArg_ParseTuple(args, "I", &led)) {
    PyErr_SetString(ledError, "Invalid argument");
    return NULL;
  }
  
  /* set led */
  int state = rc_get_led(led);
  if (state < 0) {
    PyErr_SetString(ledError, "Failed");
    return NULL;
  }
  
  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("i", state);
  
  return ret;
}

static
PyObject *led_blink(PyObject *self,
		    PyObject *args)
{
  
  /* parse arguments */
  int led;
  float hz, period;
  if (!PyArg_ParseTuple(args, "Iff", &led, &hz, &period)) {
    PyErr_SetString(ledError, "Invalid argument");
    return NULL;
  }

  /* blink led */
  if (!rc_blink_led(led, hz, period)) {
    PyErr_SetString(ledError, "Failed");
    return NULL;
  }
    
  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}
