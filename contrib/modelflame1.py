#!/usr/bin/python
# -*- coding: utf-8 -*-

""" This example is created for demonstrating the general procedure
of modeling accelerator physics by FLAME code, the lattice file used
here is specifically designed for FRIB.


Tong Zhang <zhangt@frib.msu.edu>

2016-11-30 10:35:09 AM EST
"""

from flame import Machine
from phyapps import flameutils
import matplotlib.pyplot as plt


# create FLAME machine
latfile = "test.lat"
m = Machine(open(latfile, 'r'))

# create MachineStates object
ms = flameutils.MachineStates(machine=m)
# adjust the attributes of ms
#ms.ref_IonEk = 1e7

# create ModelFlame object
fm = flameutils.ModelFlame()
# setup machine and state
fm.mstates, fm.machine = ms, m

# setup observers and run flame model
obs = fm.get_index_by_type(type='bpm')['bpm']
r,s = fm.run(monitor=obs)

# get data of intereset from running results
data = fm.collect_data(r, pos=True, x0_env=True, y0_env=True, ref_IonEk=True)

# plot figure
plt.plot(data['pos'], data['ref_IonEk'])
#plt.plot(data['pos'], data['x0_env'], 'r', lw=2, label='x')
#plt.plot(data['pos'], data['y0_env'], 'b', lw=2, label='y')
#plt.legend()
#plt.xlabel('z [m]')
#plt.ylabel('Envelope [mm]')
plt.show()
