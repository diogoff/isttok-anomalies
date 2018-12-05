from __future__ import print_function

# -------------------------------------------------------------------------

from cameras import *

cameras = get_cameras()

print(cameras)

plot_cameras(cameras)

# -------------------------------------------------------------------------

from projections import *

n_rows = 15
n_cols = 15

projections = get_projections(cameras, n_rows, n_cols)

print('projections:', projections.shape, projections.dtype)

plot_projections(projections)

# -------------------------------------------------------------------------

from signals import *

shot = 44747

signals_data, signals_time = get_signals(shot)

print('signals_data:', signals_data.shape, signals_data.dtype)
print('signals_time:', signals_time.shape, signals_time.dtype)

plot_signals(signals_data, signals_time)

# -------------------------------------------------------------------------

from tomo import *

tomo, tomo_t = get_tomo(projections, signals_data, signals_time)

print('tomo:', tomo.shape, tomo.dtype)
print('tomo_t:', tomo_t.shape, tomo_t.dtype)

plot_tomo(shot, tomo, tomo_t)
