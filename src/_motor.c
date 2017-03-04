#include <Python.h>

#include <rc_usefulincludes.h>
#include <roboticscape.h>

static char module_docstring[] =
  "This module provides an interface for motor.";

static PyObject *motorError;

// initialization
static PyObject *motor_initialize(PyObject *self, PyObject *args, PyObject *kwargs);

// one-shot sampling mode functions
static PyObject *motor_enable(PyObject *self);
static PyObject *motor_disable(PyObject *self);
static PyObject *motor_set(PyObject *self, PyObject *args);
static PyObject *motor_free_spin(PyObject *self, PyObject *args);
static PyObject *motor_brake(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
  {"initialize",
   (PyCFunction)motor_initialize,
   METH_VARARGS | METH_KEYWORDS,
   "initialize motors"}
  ,
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
  {"free_spin",
   (PyCFunction)motor_free_spin,
   METH_VARARGS,
   "set motor to spin freely"}
  ,
  {"brake",
   (PyCFunction)motor_brake,
   METH_VARARGS,
   "set motor to break"}
  ,
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "motor",   /* name of module */
  module_docstring, /* module documentation, may be NULL */
  -1,       /* size of per-interpreter state of the module,
	       or -1 if the module keeps state in global variables. */
   module_methods
};

/* auxiliary function */

static int motor_initialized_flag = 0; // initialized flag
static int rc_initialized_flag = 0;      // cape initialized flag

static
int motor_initialize_motor(void) {

  // Already initialized?
  if (motor_initialized_flag)
    return 0;

  // Cape initialized?
  if (!rc_initialized_flag) {
    if(rc_initialize()){
      PyErr_SetString(motorError, "Failed to initialize ROBOTICS CAPE");
      return -1;
    }
    rc_initialized_flag = 1;
  }

  // set flag
  motor_initialized_flag = 1;
  
  return 0;
}

/* python functions */

PyMODINIT_FUNC PyInit_motor(void)
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

  return m;
}

static
PyObject *motor_initialize(PyObject *self,
			     PyObject *args,
			     PyObject *kwargs)
{

  /* Initialize motor */
  motor_initialized_flag = 0;
  if(motor_initialize_motor())
    return NULL;

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *motor_enable(PyObject *self)
{

  /* initialize */
  if (motor_initialize_motor())
    return NULL;

  /* enable motor */
  if (rc_enable_motors()<0) {
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

  /* initialize */
  if (motor_initialize_motor())
    return NULL;

  /* enable motor */
  if (rc_disable_motors()<0) {
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

  /* initialize */
  if (motor_initialize_motor())
    return NULL;

  /* parse arguments */
  int motor;
  float duty;
  if (!PyArg_ParseTuple(args, "if", &motor, &duty)) {
    PyErr_SetString(motorError, "Invalid arguments");
    return NULL;
  }

  /* set motor */
  if (rc_set_motor(motor, duty)<0) {
    PyErr_SetString(motorError, "Failed to set motor");
    return NULL;
  }
  
  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *motor_free_spin(PyObject *self,
			  PyObject *args)
{

  /* initialize */
  if (motor_initialize_motor())
    return NULL;

  /* parse arguments */
  int motor;
  if (!PyArg_ParseTuple(args, "i", &motor)) {
    PyErr_SetString(motorError, "Invalid arguments");
    return NULL;
  }

  /* set motor */
  if (rc_set_motor_free_spin(motor)<0) {
    PyErr_SetString(motorError, "Failed to set motor free spin");
    return NULL;
  }
  
  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *motor_brake(PyObject *self,
		      PyObject *args)
{

  /* initialize */
  if (motor_initialize_motor())
    return NULL;

  /* parse arguments */
  int motor;
  if (!PyArg_ParseTuple(args, "i", &motor)) {
    PyErr_SetString(motorError, "Invalid arguments");
    return NULL;
  }

  /* set motor */
  if (rc_set_motor_brake(motor)<0) {
    PyErr_SetString(motorError, "Failed to brake motor");
    return NULL;
  }
  
  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}
