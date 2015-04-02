# encoding: UTF-8

"""Physics Applications Library"""

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"

import chanfinder
import common

__version__ = "0.0.1"

__all__= [__version__]

__all__.extend(chanfinder.__all__)
__all__.extend(common.__all__)

# If true, load configuration files automatically from default locations.
AUTO_CONFIG=True
