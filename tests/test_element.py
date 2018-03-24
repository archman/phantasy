#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test Element.

Tong Zhang <zhangt@frib.msu.edu>
2017-05-23 10:49:33 AM EDT
"""

import unittest
import os
import json

from phantasy import MachinePortal
from phantasy import CaElement

curdir = os.path.dirname(__file__)

TEST_MACH = 'FRIB_FLAME'
TEST_CA = 'TEST_CA'
TEST_CA_1 = 'TEST_CA_1'


class TestElement(unittest.TestCase):
    def setUp(self):
        self.config_dir = os.path.join(curdir, 'config')
        mpath = os.path.join(self.config_dir, TEST_MACH)
        mp = MachinePortal(machine=mpath, segment='LINAC')
        self.mp = mp
        self.machine = mpath

    def tearDown(self):
        pass

    def test_init_with_default(self):
        elem = CaElement()
        self.assertEqual(elem.active, True)
        self.assertEqual(elem.family, None)
        self.assertEqual(elem.name, None)
        self.assertEqual(elem.index, -1)
        self.assertEqual(elem.length, 0.0)
        self.assertEqual(elem.sb, float('inf'))
        self.assertEqual(elem.se, float('inf'))
        self.assertEqual(elem.virtual, False)
        self.assertEqual(elem.fields, list())
        self.assertEqual(elem.tags, dict())
        self.assertEqual(elem.group, set())

    def test_init_with_data_dict(self):
        with open(os.path.join(curdir, 'data/pv_record.json'), 'r') as f:
            pv_record = json.load(f)
        pv_name = pv_record['pv_name']
        pv_props = pv_record['pv_props']
        pv_tags = pv_record['pv_tags']
        elem = CaElement(pv_data=pv_record)
        self.assertEqual(elem.name, pv_props['name'])
        self.assertEqual(elem.index, int(pv_props['index']))
        self.assertEqual(elem.length, float(pv_props['length']))
        self.assertEqual(elem.active, True)
        self.assertEqual(elem.family, pv_props['family'])
        self.assertEqual(elem.sb, float(pv_props['sb']))
        self.assertEqual(elem.se, float(pv_props['se']))
        self.assertEqual(elem.group, {pv_props['family']})
        self.assertEqual(elem.pv(), [pv_name])
        self.assertEqual(elem.tags[pv_name], set(pv_tags))

    def test_init_with_data_list(self):
        with open(os.path.join(curdir, 'data/pv_record.json'), 'r') as f:
            pv_record = json.load(f)
        pv_name = pv_record['pv_name']
        pv_props = pv_record['pv_props']
        pv_tags = pv_record['pv_tags']
        elem = CaElement(pv_data=[pv_name, pv_props, pv_tags])
        self.assertEqual(elem.name, pv_props['name'])
        self.assertEqual(elem.index, int(pv_props['index']))
        self.assertEqual(elem.length, float(pv_props['length']))
        self.assertEqual(elem.active, True)
        self.assertEqual(elem.family, pv_props['family'])
        self.assertEqual(elem.sb, float(pv_props['sb']))
        self.assertEqual(elem.se, float(pv_props['se']))
        self.assertEqual(elem.group, {pv_props['family']})
        self.assertEqual(elem.pv(), [pv_name])
        self.assertEqual(elem.tags[pv_name], set(pv_tags))

    def test_init_with_data_props(self):
        with open(os.path.join(curdir, 'data/pv_record.json'), 'r') as f:
            pv_record = json.load(f)
        pv_props = pv_record['pv_props']
        elem = CaElement(**pv_props)
        self.assertEqual(elem.name, pv_props['name'])
        self.assertEqual(elem.index, int(pv_props['index']))
        self.assertEqual(elem.length, float(pv_props['length']))
        self.assertEqual(elem.active, True)
        self.assertEqual(elem.family, pv_props['family'])
        self.assertEqual(elem.sb, float(pv_props['sb']))
        self.assertEqual(elem.se, float(pv_props['se']))
        self.assertEqual(elem.group, {pv_props['family']})


class TestCaElement(unittest.TestCase):
    def setUp(self):
        self.config_dir = os.path.join(curdir, 'config')
        mpath = os.path.join(self.config_dir, TEST_CA)
        mp = MachinePortal(machine=mpath)
        self.mp = mp

    def tearDown(self):
        pass

    def test_channel_props(self):
        """Set channel properties to elem*..."""
        lat = self.mp.work_lattice_conf
        elem0 = lat[0]
        for k in ('name', 'family', 'index', 'se', 'length', 'sb'):
            self.assertEqual(hasattr(elem0, k), True)
        for k in ('phy_type', 'phy_name', 'machine'):
            self.assertEqual(hasattr(elem0, k), False)

    def test_channel_props_1(self):
        """Set channel properties to elem*, physics*..."""
        mpath = os.path.join(self.config_dir, TEST_CA_1)
        mp = MachinePortal(mpath)
        lat = mp.work_lattice_conf
        elem0 = lat[0]
        for k in ('name', 'family', 'index', 'se', 'length', 'sb',
                  'phy_type', 'phy_name'):
            self.assertEqual(hasattr(elem0, k), True)
        for k in ('machine',):
            self.assertEqual(hasattr(elem0, k), False)
