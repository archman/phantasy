# encoding: UTF-8

"""Utilities for FRIB specific data formats, etc."""

import xlf

def read_xlf(xlfpath):
    """
    Convenience method for reading FRIB Expanded Lattice File.
    """

    factory = xlf.AccelFactory(xlfpath)

    return factory.create()
