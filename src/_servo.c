#include <Python.h>

#include <rc/servo.h>

static char module_docstring[] =
  "This module provides an interface for servo.";

static PyObject *servoError;

// one-shot sampling mode functions
static PyObject *servo_enable(PyObject *self);
static PyObject *servo_disable(PyObject *self);

static PyObject *servo_pulse_us(PyObject *self, PyObject *args);
static PyObject *servo_pulse_us_all(PyObject *self, PyObject *args);

static PyObject *servo_pulse(PyObject *self, PyObject *args);
static PyObject *servo_pulse_all(PyObject *self, PyObject *args);

static PyObject *servo_esc_pulse(PyObject *self, PyObject *args);
static PyObject *servo_esc_pulse_all(PyObject *self, PyObject *args);

static PyObject *servo_oneshot_pulse(PyObject *self, PyObject *args);
static PyObject *servo_oneshot_pulse_all(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
  {"enable",
   (PyCFunction)servo_enable,
   METH_NOARGS,
   "enables servos"}
  ,
  {"disable",
   (PyCFunction)servo_disable,
   METH_NOARGS,
   "disable servos"}
  ,
  {"pulse_us",
   (PyCFunction)servo_pulse_us,
   METH_VARARGS,
   "send servo pulse in us"}
  ,
  {"pulse_us_all",
   (PyCFunction)servo_pulse_us_all,
   METH_VARARGS,
   "send pulse in us to all servos"}
  ,
  {"pulse",
   (PyCFunction)servo_pulse,
   METH_VARARGS,
   "send servo normalized pulse"}
  ,
  {"pulse_all",
   (PyCFunction)servo_pulse_all,
   METH_VARARGS,
   "send normalized pulse to all servos"}
  ,
  {"esc_pulse",
   (PyCFunction)servo_esc_pulse,
   METH_VARARGS,
   "send servo normalized pulse"}
  ,
  {"esc_pulse_all",
   (PyCFunction)servo_esc_pulse_all,
   METH_VARARGS,
   "send normalized pulse to all servos"}
  ,
  {"oneshot_pulse",
   (PyCFunction)servo_oneshot_pulse,
   METH_VARARGS,
   "send servo normalized pulse"}
  ,
  {"oneshot_pulse_all",
   (PyCFunction)servo_oneshot_pulse_all,
   METH_VARARGS,
   "send normalized pulse to all servos"}
  ,
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "_servo",   /* name of module */
  module_docstring, /* module documentation, may be NULL */
  -1,       /* size of per-interpreter state of the module,
	       or -1 if the module keeps state in global variables. */
   module_methods
};

/* python functions */

PyMODINIT_FUNC PyInit__servo(void)
{
  PyObject *m;

  /* create module */
  m = PyModule_Create(&module);
  if (m == NULL)
    return NULL;

  /* create exception */
  servoError = PyErr_NewException("servo.error", NULL, NULL);
  Py_INCREF(servoError);
  PyModule_AddObject(m, "error", servoError);

  /* initialize cape */
  if (rc_servo_init() != 0){
    return NULL;
  }

  return m;
}

static
PyObject *servo_enable(PyObject *self)
{

  /* enable servo */
  if (rc_servo_power_rail_en(1)<0) {
    PyErr_SetString(servoError, "Failed to enable servos");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *servo_disable(PyObject *self)
{

  /* enable servo */
  if (rc_servo_power_rail_en(0)<0) {
    PyErr_SetString(servoError, "Failed to disable servos");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *servo_pulse_us(PyObject *self,
			 PyObject *args)
{

  /* parse arguments */
  int servo;
  float us;
  if (!PyArg_ParseTuple(args, "ii", &servo, &us)) {
    PyErr_SetString(servoError, "Invalid arguments");
    return NULL;
  }

  /* set servo */
  if (rc_servo_send_pulse_us(servo, us)<0) {
    PyErr_SetString(servoError, "Failed to send pulse to servo");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *servo_pulse_us_all(PyObject *self,
			     PyObject *args)
{

  /* parse arguments */
  float us;
  if (!PyArg_ParseTuple(args, "i", &us)) {
    PyErr_SetString(servoError, "Invalid arguments");
    return NULL;
  }

  /* set servo */
  if (rc_servo_send_pulse_us(0, us)<0) {
    PyErr_SetString(servoError, "Failed to send pulse to servo");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *servo_pulse(PyObject *self,
		      PyObject *args)
{

  /* parse arguments */
  int servo;
  float duty;
  if (!PyArg_ParseTuple(args, "if", &servo, &duty)) {
    PyErr_SetString(servoError, "Invalid arguments");
    return NULL;
  }

  /* set servo */
  if (rc_servo_send_pulse_normalized(servo, duty)<0) {
    PyErr_SetString(servoError, "Failed to send normalized pulse to servo");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *servo_pulse_all(PyObject *self,
			  PyObject *args)
{

  /* parse arguments */
  float duty;
  if (!PyArg_ParseTuple(args, "f", &duty)) {
    PyErr_SetString(servoError, "Invalid arguments");
    return NULL;
  }

  /* set servo */
  if (rc_servo_send_pulse_normalized(0,duty)<0) {
    PyErr_SetString(servoError, "Failed to send normalized pulse to servo");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *servo_esc_pulse(PyObject *self,
			  PyObject *args)
{

  /* parse arguments */
  int servo;
  float duty;
  if (!PyArg_ParseTuple(args, "if", &servo, &duty)) {
    PyErr_SetString(servoError, "Invalid arguments");
    return NULL;
  }

  /* set servo */
  if (rc_servo_send_esc_pulse_normalized(servo, duty)<0) {
    PyErr_SetString(servoError, "Failed to send normalized pulse to servo");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *servo_esc_pulse_all(PyObject *self,
			      PyObject *args)
{

  /* parse arguments */
  float duty;
  if (!PyArg_ParseTuple(args, "f", &duty)) {
    PyErr_SetString(servoError, "Invalid arguments");
    return NULL;
  }

  /* set servo */
  if (rc_servo_send_esc_pulse_normalized(0,duty)<0) {
    PyErr_SetString(servoError, "Failed to send normalized pulse to servo");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *servo_oneshot_pulse(PyObject *self,
			      PyObject *args)
{

  /* parse arguments */
  int servo;
  float duty;
  if (!PyArg_ParseTuple(args, "if", &servo, &duty)) {
    PyErr_SetString(servoError, "Invalid arguments");
    return NULL;
  }

  /* set servo */
  if (rc_servo_send_oneshot_pulse_normalized(servo, duty)<0) {
    PyErr_SetString(servoError, "Failed to send normalized pulse to servo");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *servo_oneshot_pulse_all(PyObject *self,
				  PyObject *args)
{

  /* parse arguments */
  float duty;
  if (!PyArg_ParseTuple(args, "f", &duty)) {
    PyErr_SetString(servoError, "Invalid arguments");
    return NULL;
  }

  /* set servo */
  if (rc_servo_send_oneshot_pulse_normalized(0,duty)<0) {
    PyErr_SetString(servoError, "Failed to send normalized pulse to servo");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}
