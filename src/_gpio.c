#include <Python.h>

#include <rc_usefulincludes.h>
#include <roboticscape.h>

static char module_docstring[] =
  "This module provides an interface for gpio.";

static PyObject *gpioError;

// initialization
static PyObject *gpio_initialize(PyObject *self, PyObject *args, PyObject *kwargs);

// export functions
static PyObject *gpio_export(PyObject *self, PyObject *args);
static PyObject *gpio_unexport(PyObject *self, PyObject *args);

// set and get functions
static PyObject *gpio_set_dir(PyObject *self, PyObject *args);
static PyObject *gpio_set_edge(PyObject *self, PyObject *args);
static PyObject *gpio_set_value(PyObject *self, PyObject *args);
static PyObject *gpio_get_value(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
  {"initialize",
   (PyCFunction)gpio_initialize,
   METH_VARARGS | METH_KEYWORDS,
   "initialize gpios"}
  ,
  {"export",
   (PyCFunction)gpio_export,
   METH_VARARGS,
   "export gpio pin"}
  ,
  {"unexport",
   (PyCFunction)gpio_unexport,
   METH_VARARGS,
   "unexport gpio pin"}
  ,
  {"set_dir",
   (PyCFunction)gpio_set_dir,
   METH_VARARGS,
   "set gpio direction"}
  ,
  {"set_edge",
   (PyCFunction)gpio_set_edge,
   METH_VARARGS,
   "set gpio edge detection property"}
  ,
  {"set_value",
   (PyCFunction)gpio_set_value,
   METH_VARARGS,
   "set gpio value"}
  ,
  {"get_value",
   (PyCFunction)gpio_get_value,
   METH_VARARGS,
   "get gpio value"}
  ,
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "_gpio",   /* name of module */
  module_docstring, /* module documentation, may be NULL */
  -1,       /* size of per-interpreter state of the module,
	       or -1 if the module keeps state in global variables. */
   module_methods
};

/* auxiliary function */

static int gpio_initialized_flag = 0; // initialized flag
static int rc_initialized_flag = 0;      // cape initialized flag

static
int gpio_initialize_gpio(void) {

  printf("initialize_gpio::1\n");

  // Already initialized?
  if (gpio_initialized_flag)
    return 0;

  printf("initialize_gpio::2\n");

  // Cape initialized?
  if (!rc_initialized_flag) {

    printf("initialize_gpio::3\n");

    if(rc_initialize()){
      PyErr_SetString(gpioError, "Failed to initialize ROBOTICS CAPE");
      return -1;
    }
    rc_initialized_flag = 1;
  }

  // set flag
  gpio_initialized_flag = 1;
  
  return 0;
}

/* python functions */

PyMODINIT_FUNC PyInit__gpio(void)
{
  PyObject *m;

  /* create module */
  m = PyModule_Create(&module);
  if (m == NULL)
    return NULL;

  /* create exception */
  gpioError = PyErr_NewException("gpio.error", NULL, NULL);
  Py_INCREF(gpioError);
  PyModule_AddObject(m, "error", gpioError);

  return m;
}

static
PyObject *gpio_initialize(PyObject *self,
			  PyObject *args,
			  PyObject *kwargs)
{

  /* Initialize gpio */
  gpio_initialized_flag = 0;
  if(gpio_initialize_gpio())
    return NULL;

  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}


static
PyObject *gpio_export(PyObject *self,
		      PyObject *args)
{

  /* initialize */
  if (gpio_initialize_gpio())
    return NULL;

  /* parse arguments */
  int gpio;
  if (!PyArg_ParseTuple(args, "I", &gpio)) {
    PyErr_SetString(gpioError, "Invalid arguments");
    return NULL;
  }

  /* export gpio */
  if (!rc_gpio_export(gpio)) {
    PyErr_SetString(gpioError, "Failed to export gpio");
    return NULL;
  }
    
  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *gpio_unexport(PyObject *self,
		      PyObject *args)
{

  /* initialize */
  if (gpio_initialize_gpio())
    return NULL;

  /* parse arguments */
  int gpio;
  if (!PyArg_ParseTuple(args, "I", &gpio)) {
    PyErr_SetString(gpioError, "Invalid arguments");
    return NULL;
  }

  /* export gpio */
  if (!rc_gpio_unexport(gpio)) {
    PyErr_SetString(gpioError, "Failed to unexport gpio");
    return NULL;
  }
    
  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *gpio_set_dir(PyObject *self,
		       PyObject *args)
{

  /* initialize */
  if (gpio_initialize_gpio())
    return NULL;

  /* parse arguments */
  int gpio, dir = OUTPUT_PIN;
  if (!PyArg_ParseTuple(args, "I|i", &gpio, &dir)) {
    PyErr_SetString(gpioError, "Invalid arguments");
    return NULL;
  }

  /* export gpio */
  if (!rc_gpio_set_dir(gpio, dir)) {
    PyErr_SetString(gpioError, "Failed to set gpio direction");
    return NULL;
  }
    
  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *gpio_set_edge(PyObject *self,
		       PyObject *args)
{

  /* initialize */
  if (gpio_initialize_gpio())
    return NULL;

  /* parse arguments */
  int gpio, edge = EDGE_RISING;
  if (!PyArg_ParseTuple(args, "I|i", &gpio, &edge)) {
    PyErr_SetString(gpioError, "Invalid arguments");
    return NULL;
  }

  /* export gpio */
  if (!rc_gpio_set_edge(gpio, edge)) {
    PyErr_SetString(gpioError, "Failed to set gpio edge");
    return NULL;
  }
    
  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *gpio_set_value(PyObject *self,
			 PyObject *args)
{

  printf("set_value::1\n");
  
  /* initialize */
  if (gpio_initialize_gpio())
    return NULL;

  printf("set_value::2\n");
  
  /* parse arguments */
  int gpio, value = 0;
  if (!PyArg_ParseTuple(args, "I|i", &gpio, &value)) {
    PyErr_SetString(gpioError, "Invalid arguments");
    return NULL;
  }

  printf("set_value::3 %u %d\n", gpio, value);

  
  /* export gpio */
  if (!rc_gpio_set_value(gpio, value)) {
    PyErr_SetString(gpioError, "Failed to set gpio value");
    return NULL;
  }
    
  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("");

  return ret;
}

static
PyObject *gpio_get_value(PyObject *self,
			 PyObject *args)
{

  /* initialize */
  if (gpio_initialize_gpio())
    return NULL;

  /* parse arguments */
  int gpio;
  if (!PyArg_ParseTuple(args, "I", &gpio)) {
    PyErr_SetString(gpioError, "Invalid arguments");
    return NULL;
  }

  /* get gpio value */
  int value = rc_gpio_get_value(gpio);
    
  /* Build the output tuple */
  PyObject *ret = Py_BuildValue("i", value);

  return ret;
}
