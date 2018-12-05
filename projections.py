from __future__ import print_function

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import MultiLineString, LineString

# -------------------------------------------------------------------------

x_min = -100.
x_max = +100.

y_min = -100.
y_max = +100.

# -------------------------------------------------------------------------

def get_projections(cameras, n_rows, n_cols):

    x_grid = np.linspace(x_min, x_max, num=n_cols+1)
    y_grid = np.linspace(y_min, y_max, num=n_rows+1)

    grid = []

    for x in x_grid:
        grid.append([(x, y_min), (x, y_max)])

    for y in y_grid:
        grid.append([(x_min, y), (x_max, y)])

    grid = MultiLineString(grid)

    projections = []

    for row in cameras.itertuples():
        line = LineString([(row.x0, row.y0), (row.x1, row.y1)])
        projection = np.zeros((n_rows, n_cols))
        for segment in line.difference(grid):
            xx, yy = segment.xy
            x = np.mean(xx)
            y = np.mean(yy)
            j = int((x-x_min)/(x_max-x_min)*n_cols)
            i = int((y_max-y)/(y_max-y_min)*n_rows)
            projection[i,j] = segment.length
        projections.append(projection)
        
    projections = np.array(projections)

    return projections

# -------------------------------------------------------------------------

def plot_projections(projections):
    
    n_rows = projections.shape[1]
    n_cols = projections.shape[2]

    vmin = 0.
    vmax = np.sqrt(((x_max-x_min)/n_cols)**2 + ((y_max-y_min)/n_rows)**2)
    
    k = 0
    for camera in ['top', 'front', 'bottom']:

        ni = 4
        nj = 4

        figsize = (2*nj, 2*ni)
        fig, ax = plt.subplots(ni, nj, figsize=figsize)

        for i in range(ni):
            for j in range(nj):
                ax[i,j].imshow(projections[k], vmin=vmin, vmax=vmax)
                ax[i,j].set_axis_off()
                k += 1

        fig.suptitle('projections (%s camera)' % camera)
        plt.show()
