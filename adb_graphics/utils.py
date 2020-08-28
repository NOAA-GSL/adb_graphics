'''
A set of generic utilities available to all the adb_graphics components.
'''

import argparse
import datetime as dt
import functools
import importlib as il
from math import atan2, degrees
import os
import sys
import time

import numpy as np

def fhr_list(args):

    '''
    Given an argparse list argument, return the sequence of forecast hours to
    process.

    The length of the list will determine what forecast hours are returned:

      Length = 1:   A single fhr is to be processed
      Length = 2:   A sequence of start, stop with increment 1
      Length = 3:   A sequence of start, stop, increment
      Length > 3:   List as is

    argparse should provide a list of at least one item (nargs='+').

    Must ensure that the list contains integers.
    '''

    args = args if isinstance(args, list) else [args]
    arg_len = len(args)
    if arg_len in (2, 3):
        return list(range(*args))

    return args

def from_datetime(date):
    ''' Return a string like YYYYMMDDHH given a datetime object. '''
    return dt.datetime.strftime(date, '%Y%m%d%H')

def get_func(val: str):

    '''
    Given an input string, val, returns the corresponding callable function.
    This function is borrowed from stackoverflow.com response to "Python: YAML
    dictionary of functions: how to load without converting to strings."
    '''

    if '.' in val:
        module_name, fun_name = val.rsplit('.', 1)
    else:
        module_name = '__main__'
        fun_name = val

    mod_spec = il.util.find_spec(module_name, package='adb_graphics')
    if mod_spec is None:
        mod_spec = il.util.find_spec('.' + module_name, package='adb_graphics')

    try:
        __import__(mod_spec.name)
    except ImportError as exc:
        print(f'Could not load {module_name} while trying to locate function in get_func')
        raise exc
    module = sys.modules[mod_spec.name]
    fun = getattr(module, fun_name)
    return fun


# pylint: disable=invalid-name, too-many-locals
def label_line(ax, label, segment, **kwargs):

    '''
    Label a single line with line2D label data.

    Input:

    Input:

      ax        the SkewT object axis
      label     label to be used for the current line
      segment   a list (array) of values for the current line

    Key Word Arguments

      align     optional bool to enable the rotation of the label to line angle
      end       the end of the line at which to put the label. 'bottom' or 'top'
      offset    index to use for the "end" of the array

      Any kwargs accepted by matplotlib's text box.
    '''

    # Strip non-text-box key word arguments and set default if they don't exist
    align = kwargs.pop('align', True)
    end = kwargs.pop('end', 'bottom')
    offset = kwargs.pop('offset', 0)

    # Label location
    if end == 'bottom':
        x, y = segment[0 + offset, :]
        ip = 1 + offset
    elif end == 'top':
        x, y = segment[-1 - offset, :]
        ip = -1 - offset

    if align:
        #Compute the slope
        dx = segment[ip, 0] - segment[ip-1, 0]
        dy = segment[ip, 1] - segment[ip-1, 1]
        ang = degrees(atan2(dy, dx))

        #Transform to screen co-ordinates
        pt = np.array([x, y]).reshape((1, 2))
        trans_angle = ax.transData.transform_angles(np.array((ang, )), pt)[0]

        if end == 'top':
            trans_angle -= 180

    else:
        trans_angle = 0

    #Set a bunch of keyword arguments
    if ('horizontalalignment' not in kwargs) and ('ha' not in kwargs):
        kwargs['ha'] = 'center'

    if ('verticalalignment' not in kwargs) and ('va' not in kwargs):
        kwargs['va'] = 'center'

    if 'backgroundcolor' not in kwargs:
        kwargs['backgroundcolor'] = ax.get_facecolor()

    if 'clip_on' not in kwargs:
        kwargs['clip_on'] = True

    if 'fontsize' not in kwargs:
        kwargs['fontsize'] = 'larger'

    if 'fontweight' not in kwargs:
        kwargs['fontweight'] = 'bold'

    # Larger value (e.g., 2.0) to move box in front of other diagram elements
    if 'zorder' not in kwargs:
        kwargs['zorder'] = 1.50

    # Place the text box label on the line.
    ax.text(x, y, label, rotation=trans_angle, **kwargs)

def label_lines(ax, lines, labels, offset=0, **kwargs):

    '''
    Plots labels on a set of lines from SkewT.

    Input:

      ax      the SkewT object axis
      lines   the SkewT object special lines
      labels  list of labels to be used
      offset  index to use for the "end" of the array

    Key Word Arguments

      color   line color

      Along with any other kwargs accepted by matplotlib's text box.
    '''

    if 'color' not in kwargs:
        kwargs['color'] = lines.get_color()[0]

    for i, line in enumerate(lines.get_segments()):
        label = int(labels[i])
        label_line(ax, label, line, align=True, offset=offset, **kwargs)

def old_enough(age, file_path):

    '''
    Helper function to test the age of a file.

    Input:

      age         desired age in minutes
      file_path   full path to file to check

    Output:

      bool    whether the file is at least age minutes old
    '''

    file_time = dt.datetime.fromtimestamp(os.path.getctime(file_path))
    max_age = dt.datetime.now() - dt.timedelta(minutes=age)

    return file_time < max_age

def path_exists(path: str):

    ''' Checks whether a file exists, and returns the path if it does. '''

    if not os.path.exists(path):
        msg = f'{path} does not exist!'
        raise argparse.ArgumentTypeError(msg)

    return path

def timer(func):

    ''' Decorator function that provides an elapsed time for a method. '''

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")
        return value
    return wrapper_timer

def to_datetime(string):
    ''' Return a datetime object give a string like YYYYMMDDHH. '''

    return dt.datetime.strptime(string, '%Y%m%d%H')
