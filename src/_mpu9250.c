#include <Python.h>

#include <rc_usefulincludes.h>
#include <roboticscape.h>

static char module_docstring[] =
  "This module provides an interface for mpu9250.";

static PyObject *mpu9250Error;

// initialization
static PyObject *mpu9250_initialize_imu(PyObject *self, PyObject *args, PyObject *kwargs);
static PyObject *mpu9250_power_off_imu(PyObject *self);

// one-shot sampling mode functions
static PyObject *mpu9250_read_accel_data(PyObject *self);
static PyObject *mpu9250_read_gyro_data(PyObject *self);
static PyObject *mpu9250_read_mag_data(PyObject *self);
static PyObject *mpu9250_read_imu_temp(PyObject *self);

/* // interrupt-driven sampling mode functions */
/* static PyObject *mpu9250_initialize_imu_dmp(PyObject *self, PyObject *args); */
/* static PyObject *mpu9250_set_imu_interrupt_func(PyObject *self, PyObject *args); */
/* static PyObject *mpu9250_stop_imu_interrupt_func(PyObject *self, PyObject *args); */
/* static PyObject *mpu9250_was_last_imu_read_successful(PyObject *self, PyObject *args); */
/* static PyObject *mpu9250_nanos_since_last_imu_interrupt(PyObject *self, PyObject *args); */

/* // other */
/* static PyObject *mpu9250_calibrate_gyro_routine(PyObject *self, PyObject *args); */
/* static PyObject *mpu9250_calibrate_mag_routine(PyObject *self, PyObject *args); */
/* static PyObject *mpu9250_is_gyro_calibrated(PyObject *self, PyObject *args); */
/* static PyObject *mpu9250_is_mag_calibrated(PyObject *self, PyObject *args); */

static PyMethodDef module_methods[] = {
  {"initialize_imu",
   (PyCFunction)mpu9250_initialize_imu,
   METH_VARARGS | METH_KEYWORDS,
   "initialize imu"}
  ,
  {"power_off_imu",
   (PyCFunction)mpu9250_power_off_imu,
   METH_NOARGS,
   "power off imu"}
  ,
  {"read_accel_data",
   (PyCFunction)mpu9250_read_accel_data,
   METH_NOARGS,
   "read accelerometer"}
  ,
  {"read_gyro_data",
   (PyCFunction)mpu9250_read_gyro_data,
   METH_NOARGS,
   "read gyroscope"}
  ,
  {"read_mag_data",
   (PyCFunction)mpu9250_read_mag_data,
   METH_NOARGS,
   "read magnetometer"}
  ,
  {"read_imu_temp",
   (PyCFunction)mpu9250_read_imu_temp,
   METH_NOARGS,
   "read temperature"}
  ,
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
PyObject *mpu9250_initialize_imu(PyObject *self,
				 PyObject *args,
				 PyObject *kwargs)
{

  PyObject *accel_fsr;
  PyObject *gyro_fsr;
  PyObject *accel_dlpf;
  PyObject *gyro_dlpf;
  PyObject *enable_magnetometer;
  PyObject *imu_orientation;
  PyObject *compass_time_constant;
  PyObject *dmp_interrupt_priority;
  PyObject *dmp_sample_rate;

  static char *kwlist[] = {
    "accel_fsr",
    "gyro_fsr",
    "accel_dlpf",
    "gyro_dlpf",
    "enable_magnetometer",
    "imu_orientation",
    "compass_time_constant",
    "dmp_interrupt_priority",
    "dmp_sample_rate",
    NULL
  };
  
  PyObject *ret;

  printf("*> Initialize IMU...\n");

  accel_fsr = A_FSR_2G; /* Default value. */
  if (! PyArg_ParseTupleAndKeywords(args, kwargs, "i|i|i|", kwlist,
				    &accel_fsr,
				    &gyro_fsr,
				    &accel_dlpf,
				    &gyro_dlpf,
				    &enable_magnetometer,
				    &imu_orientation,
				    &compass_time_constant,
				    &dmp_interrupt_priority,
				    &dmp_sample_rate) ) {
    goto except;
  }
      
  /* power off imu */
  if (rc_power_off_imu()) {
    PyErr_SetString(mpu9250Error, "Failed to power off IMU");
    return NULL;
  }
  
  flag_initialized = 0;

  goto finally;
  
 except:
  
  PyErr_SetString(mpu9250Error, "Failed to power off IMU");

 finally:

  /* Build the output tuple */
  ret = Py_BuildValue("");

  return ret;
}


static
PyObject *mpu9250_power_off_imu(PyObject *self)
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

static
PyObject *mpu9250_read_accel_data(PyObject *self)
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
PyObject *mpu9250_read_gyro_data(PyObject *self)
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
PyObject *mpu9250_read_mag_data(PyObject *self)
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
PyObject *mpu9250_read_imu_temp(PyObject *self)
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
