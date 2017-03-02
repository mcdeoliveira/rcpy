#include <Python.h>

#include <rc_usefulincludes.h>
#include <roboticscape.h>

static char module_docstring[] =
  "This module provides an interface for mpu9250.";

static PyObject *mpu9250Error;

static PyObject *mpu9250_read_accel_data(PyObject *self, PyObject *args);
static PyObject *mpu9250_read_gyro_data(PyObject *self, PyObject *args);
static PyObject *mpu9250_read_mag_data(PyObject *self, PyObject *args);
static PyObject *mpu9250_read_imu_temp(PyObject *self, PyObject *args);
static PyObject *mpu9250_power_off_imu(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
  {"read_accel_data",
   mpu9250_read_accel_data,
   METH_VARARGS,
   "read accelerometer"},
  {"read_gyro_data",
   mpu9250_read_gyro_data,
   METH_VARARGS,
   "read gyroscope"},
  {"read_mag_data",
   mpu9250_read_mag_data,
   METH_VARARGS,
   "read magnetometer"},
  {"read_imu_temp",
   mpu9250_read_imu_temp,
   METH_VARARGS,
   "read temperature"},
  {"power_off_imu",
   mpu9250_power_off_imu,
   METH_VARARGS,
   "power off imu"},
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "mpu9250",   /* name of module */
  module_docstring, /* module documentation, may be NULL */
  -1,       /* size of per-interpreter state of the module,
	       or -1 if the module keeps state in global variables. */
   module_methods
};

static int mpu9250_initialize(void);

static int flag_initialized = 0;
static rc_imu_data_t data; //struct to hold new data

static
int mpu9250_initialize(void) {

  printf("*> Initializing IMU...\n");

  rc_imu_config_t conf = rc_default_imu_config();
  conf.enable_magnetometer=1;
  
  if(rc_initialize_imu(&data, conf)){
    PyErr_SetString(mpu9250Error, "Failed to initialize IMU");
    return -1;
  }

  flag_initialized = 1;
  
  return 0;
}

PyMODINIT_FUNC PyInit_mpu9250(void)
{
  PyObject *m;

  /* create module */
  m = PyModule_Create(&module);
  if (m == NULL)
    return NULL;

  /* create exception */
  mpu9250Error = PyErr_NewException("mpu9250.error", NULL, NULL);
  Py_INCREF(mpu9250Error);
  PyModule_AddObject(m, "error", mpu9250Error);
  
  return m;
}

static
PyObject *mpu9250_read_accel_data(PyObject *self, PyObject *args)
{

  /* initialize */
  if (!flag_initialized && mpu9250_initialize())
    return NULL;

  /* read data */
  if (rc_read_accel_data(&data)<0) {
    PyErr_SetString(mpu9250Error, "Failed to read IMU");
    return NULL;
  }
  
  /* Build the output tuple */
  PyObject *ret = 
    Py_BuildValue("(fff)", 
		  data.accel[0],
		  data.accel[1],
		  data.accel[2]);

  return ret;
}

static
PyObject *mpu9250_read_gyro_data(PyObject *self, PyObject *args)
{

  /* initialize */
  if (!flag_initialized && mpu9250_initialize())
    return NULL;

  /* read data */
  if (rc_read_gyro_data(&data)<0) {
    PyErr_SetString(mpu9250Error, "Failed to read IMU");
    return NULL;
  }
  
  /* Build the output tuple */
  PyObject *ret = 
    Py_BuildValue("(fff)", 
		  data.gyro[0],
		  data.gyro[1],
		  data.gyro[2]);

  return ret;
}

static
PyObject *mpu9250_read_mag_data(PyObject *self, PyObject *args)
{

  /* initialize */
  if (!flag_initialized && mpu9250_initialize())
    return NULL;

  /* read data */
  if (rc_read_mag_data(&data)<0) {
    PyErr_SetString(mpu9250Error, "Failed to read IMU");
    return NULL;
  }
  
  /* Build the output tuple */
  PyObject *ret = 
    Py_BuildValue("(fff)", 
		  data.mag[0],
		  data.mag[1],
		  data.mag[2]);

  return ret;
}

static
PyObject *mpu9250_read_imu_temp(PyObject *self, PyObject *args)
{

  /* initialize */
  if (!flag_initialized && mpu9250_initialize())
    return NULL;

  /* read data */
  if (rc_read_imu_temp(&data)<0) {
    PyErr_SetString(mpu9250Error, "Failed to read IMU");
    return NULL;
  }
  
  /* Build the output tuple */
  PyObject *ret = 
    Py_BuildValue("f", data.temp);

  return ret;
}

static
PyObject *mpu9250_power_off_imu(PyObject *self, PyObject *args)
{

  printf("*> Powering off IMU...\n");
    
  /* power off imu */
  if (rc_power_off_imu()) {
    PyErr_SetString(mpu9250Error, "Failed to power off IMU");
    return NULL;
  }
  
  flag_initialized = 0;

  /* Build the output tuple */
  PyObject *ret = 
    Py_BuildValue("");

  return ret;
}
