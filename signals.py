from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------

from sdas.core.client.SDASClient import SDASClient
from sdas.core.SDAStime import TimeStamp

client = SDASClient('baco.ipfn.tecnico.ulisboa.pt', 8888)

def get_data(shot, channel):
    info = client.getData(channel, '0x0000', shot)
    data = info[0].getData()
    t0 = TimeStamp(tstamp=info[0]['events'][0]['tstamp']).getTimeInMicros()
    t1 = info[0].getTStart().getTimeInMicros()
    t2 = info[0].getTEnd().getTimeInMicros()
    dt = float(t2-t1)/float(len(data))
    time = np.arange(t1-t0, t2-t0, dt, dtype=data.dtype)*1e-6
    return data, time

# -------------------------------------------------------------------------

channels = [# top camera
            'MARTE_NODE_IVO3.DataCollection.Channel_000',
            'MARTE_NODE_IVO3.DataCollection.Channel_001',
            'MARTE_NODE_IVO3.DataCollection.Channel_002',
            'MARTE_NODE_IVO3.DataCollection.Channel_003',
            'MARTE_NODE_IVO3.DataCollection.Channel_004',
            'MARTE_NODE_IVO3.DataCollection.Channel_005',
            'MARTE_NODE_IVO3.DataCollection.Channel_006',
            'MARTE_NODE_IVO3.DataCollection.Channel_007',
            'MARTE_NODE_IVO3.DataCollection.Channel_178',
            'MARTE_NODE_IVO3.DataCollection.Channel_179',
            'MARTE_NODE_IVO3.DataCollection.Channel_180',
            'MARTE_NODE_IVO3.DataCollection.Channel_181',
            'MARTE_NODE_IVO3.DataCollection.Channel_182',
            'MARTE_NODE_IVO3.DataCollection.Channel_183',
            'MARTE_NODE_IVO3.DataCollection.Channel_184',
            'MARTE_NODE_IVO3.DataCollection.Channel_185',
            # front camera
            'MARTE_NODE_IVO3.DataCollection.Channel_008',
            'MARTE_NODE_IVO3.DataCollection.Channel_009',
            'MARTE_NODE_IVO3.DataCollection.Channel_010',
            'MARTE_NODE_IVO3.DataCollection.Channel_011',
            'MARTE_NODE_IVO3.DataCollection.Channel_012',
            'MARTE_NODE_IVO3.DataCollection.Channel_013',
            'MARTE_NODE_IVO3.DataCollection.Channel_014',
            'MARTE_NODE_IVO3.DataCollection.Channel_015',
            'MARTE_NODE_IVO3.DataCollection.Channel_186',
            'MARTE_NODE_IVO3.DataCollection.Channel_187',
            'MARTE_NODE_IVO3.DataCollection.Channel_188',
            'MARTE_NODE_IVO3.DataCollection.Channel_189',
            'MARTE_NODE_IVO3.DataCollection.Channel_190',
            'MARTE_NODE_IVO3.DataCollection.Channel_191',
            'MARTE_NODE_IVO3.DataCollection.Channel_192',
            'MARTE_NODE_IVO3.DataCollection.Channel_193',
            # bottom camera
            'MARTE_NODE_IVO3.DataCollection.Channel_016',
            'MARTE_NODE_IVO3.DataCollection.Channel_017',
            'MARTE_NODE_IVO3.DataCollection.Channel_018',
            'MARTE_NODE_IVO3.DataCollection.Channel_019',
            'MARTE_NODE_IVO3.DataCollection.Channel_020',
            'MARTE_NODE_IVO3.DataCollection.Channel_021',
            'MARTE_NODE_IVO3.DataCollection.Channel_022',
            'MARTE_NODE_IVO3.DataCollection.Channel_023',
            'MARTE_NODE_IVO3.DataCollection.Channel_194',
            'MARTE_NODE_IVO3.DataCollection.Channel_195',
            'MARTE_NODE_IVO3.DataCollection.Channel_196',
            'MARTE_NODE_IVO3.DataCollection.Channel_197',
            'MARTE_NODE_IVO3.DataCollection.Channel_198',
            'MARTE_NODE_IVO3.DataCollection.Channel_199',
            'MARTE_NODE_IVO3.DataCollection.Channel_200',
            'MARTE_NODE_IVO3.DataCollection.Channel_201']

# -------------------------------------------------------------------------

def get_signals(shot):

    signals_data = []
    signals_time = []

    for channel in channels:

        print('channel:', channel, end=' ')
        data, time = get_data(shot, channel)
        print(data.shape, data.dtype)

        signals_data.append(data)
        signals_time.append(time)

    signals_data = np.array(signals_data)
    signals_time = np.array(signals_time)
    
    return signals_data, signals_time

# -------------------------------------------------------------------------

def plot_signals(signals_data, signals_time):
    
    n = signals_data.shape[0] // 3

    for (k, channel) in enumerate(channels):
        
        data = signals_data[k]
        time = signals_time[k]

        plt.plot(time, data, label='channel %s' % channel.split('_')[-1])
        
        if k == 1*n-1:
            plt.title('signals (top camera)')
            plt.xlabel('t (s)')
            plt.legend()
            plt.show()

        if k == 2*n-1:
            plt.title('signals (front camera)')
            plt.xlabel('t (s)')
            plt.legend()
            plt.show()

        if k == 3*n-1:
            plt.title('signals (bottom camera)')
            plt.xlabel('t (s)')
            plt.legend()
            plt.show()
