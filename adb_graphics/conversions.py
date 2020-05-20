'''
This module contains functions for converting the units of a field. The
interface requires a single atmospheric field in a Numpy array, and returns the
converted values as output.
'''

import numpy as np

def k_to_c(field: np.ndarray) -> np.ndarray:

    ''' Conversion from Kelvin to Celsius '''

    return np.asarray(field) - 273.15

def k_to_f(field: np.ndarray) -> np.ndarray:

    ''' Conversion from Kelvin to Farenheit '''

    return (np.asarray(field) - 273.15) * 9/5 + 32

def m_to_dm(field: np.ndarray) -> np.ndarray:

    ''' Conversion from meters to decameters '''

    return np.asarray(field) / 10.

def ms_to_kt(field: np.ndarray) -> np.ndarray:

    ''' Conversion from m s-1 to knots '''

    return np.asarray(field) * 1.9438

def pa_to_hpa(field: np.ndarray) -> np.ndarray:

    ''' Conversion from Pascals to hectopascals '''

    return np.asarray(field) / 100.

def vvel_scale(field: np.ndarray) -> np.ndarray:

    ''' Scale vertical velocity for plotting  '''

    return np.asarray(field) * -10

def vort_scale(field: np.ndarray) -> np.ndarray:

    ''' Scale vorticity for plotting  '''

    return np.asarray(field) / 1E-05
