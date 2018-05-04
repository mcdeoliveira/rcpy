/* Contributed by BrendanSimon */

#include <Python.h>

#include <rc/adc.h>

static char module_docstring[] =
  "This module provides an interface for the ADC (Analog Digital Converter).";

static PyObject *adcError;

// adc functions
static PyObject *adc_get_raw(PyObject *self, PyObject *args);
static PyObject *adc_get_voltage(PyObject *self, PyObject *args);
static PyObject *adc_get_dc_jack_voltage(PyObject *self, PyObject *args);
static PyObject *adc_get_battery_voltage(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
  {"get_raw",
   (PyCFunction)adc_get_raw,
   METH_VARARGS,
   "get adc raw value"}
  ,
  {"get_voltage",
   (PyCFunction)adc_get_voltage,
   METH_VARARGS,
   "get adc voltage"}
  ,
  {"get_dc_jack_voltage",
   (PyCFunction)adc_get_dc_jack_voltage,
   METH_VARARGS,
   "get DC jack voltage"}
  ,
  {"get_battery_voltage",
   (PyCFunction)adc_get_battery_voltage,
   METH_VARARGS,
   "get battery voltage"}
  ,
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "_adc",   /* name of module */
  module_docstring, /* module documentation, may be NULL */
  -1,       /* size of per-interpreter state of the module,
	       or -1 if the module keeps state in global variables. */
   module_methods
};

/* python functions */

PyMODINIT_FUNC PyInit__adc(void)
{
  PyObject *m;

  /* create module */
  m = PyModule_Create(&module);
  if (m == NULL)
    return NULL;

  /* create exception */
  adcError = PyErr_NewException("adc.error", NULL, NULL);
  Py_INCREF(adcError);
  PyModule_AddObject(m, "error", adcError);

  /* initialize cape */
  if(rc_adc_init() != 0){
      return NULL;
  }

  return m;
}

static
PyObject *adc_get_raw(PyObject *self,
			PyObject *args)
{
  /* parse arguments */
  unsigned channel;
  if (!PyArg_ParseTuple(args, "I", &channel)) {
    PyErr_SetString(adcError, "Invalid arguments");
    return NULL;
  }

  /* get adc value */
  int value;
  if ((value = rc_adc_read_raw((int)channel)) < 0) {
    PyErr_SetString(adcError, "Failed to get adc raw value");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("i", value);

  return ret;
}

static
PyObject *adc_get_voltage(PyObject *self,
			PyObject *args)
{
  /* parse arguments */
  unsigned channel;
  if (!PyArg_ParseTuple(args, "I", &channel)) {
    PyErr_SetString(adcError, "Invalid arguments");
    return NULL;
  }

  /* get adc voltage */
  float voltage;
  if ((voltage = rc_adc_read_volt((int)channel)) < 0) {
    PyErr_SetString(adcError, "Failed to get adc voltage");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("f", voltage);

  return ret;
}

static
PyObject *adc_get_dc_jack_voltage(PyObject *self,
			PyObject *args)
{
  /* parse arguments */

  /* get dc jack voltage */
  float voltage;
  if ((voltage = rc_adc_dc_jack()) < 0) {
    PyErr_SetString(adcError, "Failed to get DC jack voltage");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("f", voltage);

  return ret;
}

static
PyObject *adc_get_battery_voltage(PyObject *self,
			PyObject *args)
{
  /* parse arguments */

  /* get dc jack voltage */
  float voltage;
  if ((voltage = rc_adc_batt()) < 0) {
    PyErr_SetString(adcError, "Failed to get battery voltage");
    return NULL;
  }

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("f", voltage);

  return ret;
}

