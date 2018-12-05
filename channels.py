from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------

from sdas.core.client.SDASClient import SDASClient
from sdas.core.SDAStime import TimeStamp

client = SDASClient('baco.ipfn.tecnico.ulisboa.pt', 8888)

channels = dict()

for item in client.searchParametersByName(''):
    name = item['descriptorUID']['name']
    uniqueID = item['descriptorUID']['uniqueID']
    if uniqueID.startswith('MARTE_NODE_IVO3'):
        if name.startswith('ADC_tomography'):
            if name.split('_')[2] in ['top', 'bottom', 'outer']:
                channels[name] = uniqueID

def sort_key(name):
    cameras = ['top', 'outer', 'bottom']
    parts = name.split('_')
    camera = cameras.index(parts[2])
    detector = int(parts[-1])
    return (camera, detector)

names = sorted(channels.keys(), key=sort_key)

for name in names:
    print(name, ':', channels[name])
