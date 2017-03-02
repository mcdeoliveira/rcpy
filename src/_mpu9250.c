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

static rc_imu_config_t imu_conf;     // imu configuration
static rc_imu_data_t imu_data;       // imu data
static int imu_initialized_flag = 0; // initialized flag

static
int mpu9250_initialize(void) {

  // Already initialized?
  if (imu_initialized_flag)
    return 0;

  // Initialize
  printf("*> Initializing IMU...\n");

  if(rc_initialize_imu(&imu_data, imu_conf)){
    PyErr_SetString(mpu9250Error, "Failed to initialize IMU");
    return -1;
  }

  // set flag
  imu_initialized_flag = 1;
  
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

  /* set default parameters for imu */
  imu_conf = rc_default_imu_config();
  
  return m;
}


static
PyObject *mpu9250_initialize_imu(PyObject *self,
				 PyObject *args,
				 PyObject *kwargs)
{

  static char *kwlist[] = {
    "accel_fsr",              /* rc_accel_fsr_t (int) */
    "gyro_fsr",               /* rc_gyro_fsr_t (int) */
    "accel_dlpf",             /* rc_accel_dlpf_t (int) */
    "gyro_dlpf",              /* rc_gyro_dlpf_t (int) */
    "enable_magnetometer",    /* int */
    "orientation",            /* rc_imu_orientation_t (int) */
    "compass_time_constant",  /* float */
    "dmp_interrupt_priority", /* int */
    "dmp_sample_rate",        /* int */
    "show_warnings",          /* int */
    NULL
  };
  
  PyObject *ret;

  /* Parse parameters */
  if (! PyArg_ParseTupleAndKeywords(args, kwargs, "|iiiiiifiii", kwlist,
				    &imu_conf.accel_fsr,              /* rc_accel_fsr_t (int) */
				    &imu_conf.gyro_fsr,               /* rc_gyro_fsr_t (int) */
				    &imu_conf.accel_dlpf,             /* rc_accel_dlpf_t (int) */
				    &imu_conf.gyro_dlpf,              /* rc_gyro_dlpf_t (int) */
				    &imu_conf.enable_magnetometer,    /* int */
				    &imu_conf.orientation,            /* rc_imu_orientation_t (int) */
				    &imu_conf.compass_time_constant,  /* float */
				    &imu_conf.dmp_interrupt_priority, /* int */
				    &imu_conf.dmp_sample_rate,        /* int */
				    &imu_conf.show_warnings           /* int */ )) {
    PyErr_SetString(mpu9250Error, "Failed to initialize IMU");
    return NULL;
  }

  /* Initialize imu */
  imu_initialized_flag = 0;
  if(mpu9250_initialize())
    return NULL;

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
  
  imu_initialized_flag = 0;

  /* Build the output tuple */
  PyObject *ret = 
    Py_BuildValue("");

  return ret;
}

static
PyObject *mpu9250_read_accel_data(PyObject *self)
{

  /* initialize */
  if (mpu9250_initialize())
    return NULL;

  /* read data */
  if (rc_read_accel_data(&imu_data)<0) {
    PyErr_SetString(mpu9250Error, "Failed to read IMU");
    return NULL;
  }
  
  /* Build the output tuple */
  PyObject *ret = 
    Py_BuildValue("(fff)", 
		  imu_data.accel[0],
		  imu_data.accel[1],
		  imu_data.accel[2]);

  return ret;
}

static
PyObject *mpu9250_read_gyro_data(PyObject *self)
{

  /* initialize */
  if (mpu9250_initialize())
    return NULL;

  /* read data */
  if (rc_read_gyro_data(&imu_data)<0) {
    PyErr_SetString(mpu9250Error, "Failed to read IMU");
    return NULL;
  }
  
  /* Build the output tuple */
  PyObject *ret = 
    Py_BuildValue("(fff)", 
		  imu_data.gyro[0],
		  imu_data.gyro[1],
		  imu_data.gyro[2]);

  return ret;
}

static
PyObject *mpu9250_read_mag_data(PyObject *self)
{

  /* initialize */
  if (mpu9250_initialize())
    return NULL;

  /* enabled? */
  if (!imu_conf.enable_magnetometer) {
    PyErr_SetString(mpu9250Error, "Magnetometer is disabled");
    return NULL;
  }
  
  /* read data */
  if (rc_read_mag_data(&imu_data)<0) {
    PyErr_SetString(mpu9250Error, "Failed to read magnetometer data");
    return NULL;
  }
  
  /* Build the output tuple */
  PyObject *ret = 
    Py_BuildValue("(fff)", 
		  imu_data.mag[0],
		  imu_data.mag[1],
		  imu_data.mag[2]);

  return ret;
}

static
PyObject *mpu9250_read_imu_temp(PyObject *self)
{

  /* initialize */
  if (mpu9250_initialize())
    return NULL;

  /* read data */
  if (rc_read_imu_temp(&imu_data)<0) {
    PyErr_SetString(mpu9250Error, "Failed to read IMU");
    return NULL;
  }
  
  /* Build the output tuple */
  PyObject *ret = 
    Py_BuildValue("f", imu_data.temp);

  return ret;
}
