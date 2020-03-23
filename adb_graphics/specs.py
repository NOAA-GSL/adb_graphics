'''
This module sets the specifications for certain atmospheric variables. Typically
this is related to a spec that needs some level of computation, i.e. a set of
colors from a color map.
'''

import abc
from itertools import chain
from functools import lru_cache
from matplotlib import cm
import numpy as np
import yaml


class VarSpec(abc.ABC):

    '''
    Loads a yaml config file with spec settings. Also defines methods for
    declaring more complex specifications for variables based on settings within
    the config file.
    '''

    def __init__(self, config):

        with open(config, 'r') as cfg:
            self.yml = yaml.load(cfg, Loader=yaml.Loader)

    @property
    @abc.abstractmethod
    def clevs(self) -> np.ndarray:

        ''' An abstract method responsible for returning the np.ndarray of contour
        levels for a given field. Numpy arange supports non-integer values. '''

    @property
    @lru_cache()
    def ps_colors(self) -> np.ndarray:

        ''' Default color map for Surface Pressure '''

        grays = cm.get_cmap('Greys', 13)(range(13))
        segments = [[16, 53], [86, 105], [110, 151, 2], [172, 202, 2]]
        ncar = cm.get_cmap('gist_ncar', 200)(list(chain(*[range(*i) for i in segments])))
        return np.concatenate((grays, ncar))

    @property
    @lru_cache()
    def t_colors(self) -> np.ndarray:

        ''' Default color map for Temperature '''

        ncolors = len(self.clevs)
        return cm.get_cmap(self.vspec.get('cmap', 'jet'), ncolors)(range(ncolors))
