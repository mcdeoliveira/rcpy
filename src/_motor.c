#include <Python.h>

#include <rc/motor.h>

static char module_docstring[] =
  "This module provides an interface for motor.";

static PyObject *motorError;

// one-shot sampling mode functions
static PyObject *motor_enable(PyObject *self);
static PyObject *motor_disable(PyObject *self);
static PyObject *motor_set(PyObject *self, PyObject *args);
static PyObject *motor_set_free_spin(PyObject *self, PyObject *args);
static PyObject *motor_set_brake(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
  {"enable",
   (PyCFunction)motor_enable,
   METH_NOARGS,
   "enables motors"}
  ,
  {"disable",
   (PyCFunction)motor_disable,
   METH_NOARGS,
   "disable motors"}
  ,
  {"set",
   (PyCFunction)motor_set,
   METH_VARARGS,
   "set motor"}
  ,
  {"set_free_spin",
   (PyCFunction)motor_set_free_spin,
   METH_VARARGS,
   "set motor to spin freely"}
  ,
  {"set_brake",
   (PyCFunction)motor_set_brake,
   METH_VARARGS,
   "set motor to break"}
  ,
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "_motor",   /* name of module */
  module_docstring, /* module documentation, may be NULL */
  -1,       /* size of per-interpreter state of the module,
	       or -1 if the module keeps state in global variables. */
   module_methods
};

/* python functions */

PyMODINIT_FUNC PyInit__motor(void)
{
  PyObject *m;

  /* create module */
  m = PyModule_Create(&module);
  if (m == NULL)
    return NULL;

  /* create exception */
  motorError = PyErr_NewException("motor.error", NULL, NULL);
  Py_INCREF(motorError);
  PyModule_AddObject(m, "error", motorError);

  /* initialize cape */
  if(rc_motor_init()!=0){
    return NULL;
  }

  return m;
}

static
PyObject *motor_enable(PyObject *self)
{

  /* enable motor */
  if (rc_motor_standby(0)<0) {
    PyErr_SetString(motorError, "Failed to enable motors");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *motor_disable(PyObject *self)
{

  /* enable motor */
  if (rc_motor_standby(1)<0) {
    PyErr_SetString(motorError, "Failed to disable motors");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *motor_set(PyObject *self,
		    PyObject *args)
{

  /* parse arguments */
  int motor;
  float duty;
  if (!PyArg_ParseTuple(args, "if", &motor, &duty)) {
    PyErr_SetString(motorError, "Invalid arguments");
    return NULL;
  }

  /* set motor */
  if (rc_motor_set(motor, duty)<0) {
    PyErr_SetString(motorError, "Failed to set motor");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *motor_set_free_spin(PyObject *self,
			      PyObject *args)
{

  /* parse arguments */
  int motor;
  if (!PyArg_ParseTuple(args, "i", &motor)) {
    PyErr_SetString(motorError, "Invalid arguments");
    return NULL;
  }

  /* set motor */
  if (rc_motor_free_spin(motor)<0) {
    PyErr_SetString(motorError, "Failed to set motor free spin");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *motor_set_brake(PyObject *self,
			  PyObject *args)
{

  /* parse arguments */
  int motor;
  if (!PyArg_ParseTuple(args, "i", &motor)) {
    PyErr_SetString(motorError, "Invalid arguments");
    return NULL;
  }

  /* set motor */
  if (rc_motor_brake(motor)<0) {
    PyErr_SetString(motorError, "Failed to brake motor");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}
