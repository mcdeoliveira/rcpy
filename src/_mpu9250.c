#include <Python.h>

#include <rc_usefulincludes.h>
#include <roboticscape.h>

static char module_docstring[] =
  "This module provides an interface for mpu9250.";

static PyObject *mpu9250Error;

// initialization
static PyObject *mpu9250_initialize(PyObject *self,
				    PyObject *args,
				    PyObject *kwargs);
static PyObject *mpu9250_power_off(PyObject *self);
static PyObject *mpu9250_get(PyObject *self);

// one-shot sampling mode functions
static PyObject *mpu9250_read_accel_data(PyObject *self);
static PyObject *mpu9250_read_gyro_data(PyObject *self);
static PyObject *mpu9250_read_mag_data(PyObject *self);
static PyObject *mpu9250_read_imu_temp(PyObject *self);

// read dmp
static PyObject *mpu9250_read(PyObject *self);

/* // other */
/* static PyObject *mpu9250_calibrate_gyro_routine(PyObject *self, PyObject *args); */
/* static PyObject *mpu9250_calibrate_mag_routine(PyObject *self, PyObject *args); */
/* static PyObject *mpu9250_is_gyro_calibrated(PyObject *self, PyObject *args); */
/* static PyObject *mpu9250_is_mag_calibrated(PyObject *self, PyObject *args); */

static PyMethodDef module_methods[] = {
  {"initialize",
   (PyCFunction)mpu9250_initialize,
   METH_VARARGS | METH_KEYWORDS,
   "initialize imu"}
  ,
  {"power_off",
   (PyCFunction)mpu9250_power_off,
   METH_NOARGS,
   "power off imu"}
  ,
  {"get",
   (PyCFunction)mpu9250_get,
   METH_NOARGS,
   "get imu conf"}
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
  {"read",
   (PyCFunction)mpu9250_read,
   METH_NOARGS,
   "read imu"}
  ,
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "_mpu9250",   /* name of module */
  module_docstring, /* module documentation, may be NULL */
  -1,       /* size of per-interpreter state of the module,
	       or -1 if the module keeps state in global variables. */
   module_methods
};

/* auxiliary function */

static int imu_enable_dmp = 0;       // enable dmp
static int imu_enable_fusion = 0;    // enable fusion
static rc_imu_config_t imu_conf;     // imu configuration
static rc_imu_data_t imu_data;       // imu data

/* python functions */

PyMODINIT_FUNC PyInit__mpu9250(void)
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
  
  /* initialize cape */
  if (rc_get_state() == UNINITIALIZED) {
    printf("* * * mpu9250: WILL CALL INIT * * *\n");
    if(rc_initialize())
      return NULL;
  }

  /* set default parameters for imu */
  imu_conf = rc_default_imu_config();
  
  return m;
}


static
PyObject *mpu9250_initialize(PyObject *self,
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
    "enable_dmp",             /* int */
    "enable_fusion",          /* int */
    NULL
  };
  
  PyObject *ret;

  /* Parse parameters */
  if (! PyArg_ParseTupleAndKeywords(args, kwargs, "|iiiiiifiiiii", kwlist,
				    &imu_conf.accel_fsr,              /* rc_accel_fsr_t (int) */
				    &imu_conf.gyro_fsr,               /* rc_gyro_fsr_t (int) */
				    &imu_conf.accel_dlpf,             /* rc_accel_dlpf_t (int) */
				    &imu_conf.gyro_dlpf,              /* rc_gyro_dlpf_t (int) */
				    &imu_conf.enable_magnetometer,    /* int */
				    &imu_conf.orientation,            /* rc_imu_orientation_t (int) */
				    &imu_conf.compass_time_constant,  /* float */
				    &imu_conf.dmp_interrupt_priority, /* int */
				    &imu_conf.dmp_sample_rate,        /* int */
				    &imu_conf.show_warnings,          /* int */ 
				    &imu_enable_dmp,                  /* int */
				    &imu_enable_fusion                /* int */ )) {
    PyErr_SetString(mpu9250Error, "Failed to initialize IMU");
    return NULL;
  }

  /* Initialize imu */

  // To dmp or not to dmp?
  if (imu_enable_dmp) {

    // initialize imu + dmp
    if(rc_initialize_imu_dmp(&imu_data, imu_conf)){
      PyErr_SetString(mpu9250Error, "Failed to initialize IMU");
      return NULL;
    }

  }
  else {
    if(rc_initialize_imu(&imu_data, imu_conf)){
      PyErr_SetString(mpu9250Error, "Failed to initialize IMU");
      return NULL;
    }
  }

  /* Build the output tuple */
  ret = Py_BuildValue("");

  return ret;
}

static
PyObject *mpu9250_power_off(PyObject *self)
{

  /* power off imu */
  if (rc_power_off_imu()) {
    PyErr_SetString(mpu9250Error, "Failed to power off IMU");
    return NULL;
  }
  
  /* Build the output tuple */
  PyObject *ret = 
    Py_BuildValue("");

  return ret;
}

static
PyObject *mpu9250_get(PyObject *self)
{

  /* Build the output tuple */
  PyObject *ret = 
    Py_BuildValue("{sisisisisisfsisisOsOsOsO}",
		  "accel_fsr",
		  imu_conf.accel_fsr,
		  "gyro_fsr",
		  imu_conf.gyro_fsr,
		  "accel_dlpf",
		  imu_conf.accel_dlpf,
		  "gyro_dlpf",
		  imu_conf.gyro_dlpf,
		  "orientation",
		  imu_conf.orientation,
		  "compass_time_constant",
		  imu_conf.compass_time_constant,
		  "dmp_interrupt_priority",
		  imu_conf.dmp_interrupt_priority,
		  "dmp_sample_rate",
		  imu_conf.dmp_sample_rate,
		  "enable_magnetometer",
		  imu_conf.enable_magnetometer ? Py_True : Py_False,
		  "show_warnings",
		  imu_conf.show_warnings ? Py_True : Py_False,
		  "enable_dmp",
		  imu_enable_dmp ? Py_True : Py_False,
		  "enable_fusion",
		  imu_enable_fusion ? Py_True : Py_False);
  
  return ret;
}

static
PyObject *mpu9250_read_accel_data(PyObject *self)
{

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

static
PyObject *mpu9250_read(PyObject *self)
{

  /* read data */
  if (imu_enable_dmp) {

    /* from dmp  */
    
    // aquires mutex
    pthread_mutex_lock( &rc_imu_read_mutex );

    // waits until a measurement is available
    pthread_cond_wait( &rc_imu_read_condition, &rc_imu_read_mutex );

  } else {

    /* or from registers */

    if (rc_read_accel_data(&imu_data)<0) {
      PyErr_SetString(mpu9250Error, "Failed to read IMU");
      return NULL;
    }
    
    if (rc_read_gyro_data(&imu_data)<0) {
      PyErr_SetString(mpu9250Error, "Failed to read IMU");
      return NULL;
    }

    if (imu_conf.enable_magnetometer) {
      if (rc_read_mag_data(&imu_data)<0) {
	PyErr_SetString(mpu9250Error, "Failed to read magnetometer data");
	return NULL;
      }
    }
    
    if (rc_read_imu_temp(&imu_data)<0) {
      PyErr_SetString(mpu9250Error, "Failed to read IMU");
      return NULL;
    }

  }
    
  /* Build the output tuple */
  PyObject *ret;

  if (imu_conf.enable_magnetometer) {

    if (imu_enable_fusion) {

      ret = Py_BuildValue("{s(fff)s(fff)s(fff)s(ffff)s(fff)sf}",
			  "accel",
			  imu_data.accel[0],
			  imu_data.accel[1],
			  imu_data.accel[2],
			  "gyro",
			  imu_data.gyro[0],
			  imu_data.gyro[1],
			  imu_data.gyro[2],
			  "mag",
			  imu_data.mag[0],
			  imu_data.mag[1],
			  imu_data.mag[2],
			  "quat",
			  imu_data.fused_quat[0],
			  imu_data.fused_quat[1],
			  imu_data.fused_quat[2],
			  imu_data.fused_quat[3],
			  "tb",
			  imu_data.fused_TaitBryan[TB_PITCH_X],
			  imu_data.fused_TaitBryan[TB_ROLL_Y],
			  imu_data.fused_TaitBryan[TB_YAW_Z],
			  "head",
			  imu_data.compass_heading);
      
    } else {

      ret = Py_BuildValue("{s(fff)s(fff)s(fff)s(ffff)s(fff)sf}",
			  "accel",
			  imu_data.accel[0],
			  imu_data.accel[1],
			  imu_data.accel[2],
			  "gyro",
			  imu_data.gyro[0],
			  imu_data.gyro[1],
			  imu_data.gyro[2],
			  "mag",
			  imu_data.mag[0],
			  imu_data.mag[1],
			  imu_data.mag[2],
			  "quat",
			  imu_data.dmp_quat[0],
			  imu_data.dmp_quat[1],
			  imu_data.dmp_quat[2],
			  imu_data.dmp_quat[3],
			  "tb",
			  imu_data.dmp_TaitBryan[TB_PITCH_X],
			  imu_data.dmp_TaitBryan[TB_ROLL_Y],
			  imu_data.dmp_TaitBryan[TB_YAW_Z],
			  "head",
			  imu_data.compass_heading_raw);

    }
  
  } else {

    ret = Py_BuildValue("{s(fff)s(fff)s(ffff)s(fff)}",
			"accel",
			imu_data.accel[0],
			imu_data.accel[1],
			imu_data.accel[2],
			"gyro",
			imu_data.gyro[0],
			imu_data.gyro[1],
			imu_data.gyro[2],
			"quat",
			imu_data.dmp_quat[0],
			imu_data.dmp_quat[1],
			imu_data.dmp_quat[2],
			imu_data.dmp_quat[3],
			"tb",
			imu_data.dmp_TaitBryan[TB_PITCH_X],
			imu_data.dmp_TaitBryan[TB_ROLL_Y],
			imu_data.dmp_TaitBryan[TB_YAW_Z]);
    
  }

  /* release mutex */
  if (imu_enable_dmp) {
    
    // releases mutex
    pthread_mutex_unlock( &rc_imu_read_mutex );
    
  }

  return ret;
}
