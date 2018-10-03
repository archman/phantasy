# -*- coding: utf-8 -*-

import numpy as np
import json
from collections import OrderedDict
from .data_templates import SHEET_TEMPLATES

try:
    basestring
except NameError:
    basestring = str


class ScanDataModel(object):
    """Standardize the scan output data.

    Parameters
    ----------
    data : array
        Numpy array with the shape of `(t, h, w)`, e.g.
        `t` is iteration number, `h` is shot number, `w` is scan dimension.
    """
    def __init__(self, data=None):
       self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, z):
        """Every time data is updated, the shape, std array and mean array
        will be updated.
        """
        self._data = z
        self.t, self.h, self.w = self.shape
        self._std = self._data.std(axis=1)
        self._avg = self._data.mean(axis=1)

    @property
    def shape(self):
        return self._data.shape

    def get_xerr(self, **kws):
        if kws == {}:
            return self._std[:, 0]
        else:
            return self._data.std(axis=1, **kws)[:, 0]

    def get_yerr(self, **kws):
        if kws == {}:
            return self._std[:, 1]
        else:
            return self._data.std(axis=1, **kws)[:, 1]

    def get_xavg(self):
        return self._avg[:, 0]

    def get_yavg(self):
        return self._avg[:, 1]


class DataSheetBase(OrderedDict):
    def __init__(self, path=None):
        super(DataSheetBase, self).__init__()
        if isinstance(path, basestring):
            with open(path, "r") as fp:
                self.read(fp)

    def read(self, fp):
        """How to read the data sheet from file-like stream defined by *fp*.
        """
        raise NotImplementedError

    def write(self, path=None):
        """How to write the data sheet to file defined by *path*.
        """
        raise NotImplementedError

    def __deepcopy__(self, memo):
        s = DataSheetBase()
        s.update(deepcopy(list(self.items()), memo))
        return s

    def load_template(self, template):
        """Load template dict.

        Parameters
        ----------
        template : str
            Name of sheet template, all valid names could be returned from
            :method:`~DataSheetBase.template_names()`.
        """
        temp_sheet_dict = SHEET_TEMPLATES[template]
        self.update(temp_sheet_dict)

    @staticmethod
    def template_names():
        """Return list of all valid sheet template names.
        """
        return list(SHEET_TEMPLATES.keys())


class JSONDataSheet(DataSheetBase):
    """Save/Open JSON formated data sheet.
    """
    def __init__(self, path=None):
        super(JSONDataSheet, self).__init__(path)

        # load 'Quad Scan' template
        self.load_template('Quad Scan')

    def read(self, fp):
        self.update(json.load(fp, object_pairs_hook=OrderedDict))

    def write(self, path):
        with open(path, 'w') as fp:
            json.dump(self, fp, indent=2, sort_keys=True)

