from __future__ import print_function

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString

# -------------------------------------------------------------------------

def get_cameras():

    t_pinhole_x = 5.
    t_pinhole_y = 97.

    f_pinhole_x = 109.
    f_pinhole_y = 0.
    
    b_pinhole_x = 0.    # to be translated by 5. after rotation (see below)
    b_pinhole_y = -102.

    n = 16          # number of detectors per camera
    width = 0.75    # detector width
    space = 0.20    # space between detectors
    dist = 9.0      # distance from pinhole to camera
    
    size = n*width + (n-1)*space        # camera full size
    step = width + space                # distance between adjacent detectors
    
    t_detector_x = t_pinhole_x - size/2. + width/2. + np.arange(n)*step
    t_detector_y = (t_pinhole_y + dist) * np.ones(n)

    f_detector_x = (f_pinhole_x + dist) * np.ones(n)
    f_detector_y = f_pinhole_y + size/2. - width/2. - np.arange(n)*step

    dist = 13.0     # different for bottom camera

    b_detector_x = b_pinhole_x + size/2. - width/2. - np.arange(n)*step
    b_detector_y = (b_pinhole_y - dist) * np.ones(n)

    # bottom camera rotation

    theta = np.radians(7.5)
    
    # rotate pinhole
    
    b_pinhole_x_rotated = b_pinhole_x*np.cos(theta) - b_pinhole_y*np.sin(theta)
    b_pinhole_y_rotated = b_pinhole_x*np.sin(theta) + b_pinhole_y*np.cos(theta)

    b_pinhole_x = b_pinhole_x_rotated + 5.      # translation by 5. is here
    b_pinhole_y = b_pinhole_y_rotated

    # rotate detectors

    b_detector_x_rotated = b_detector_x*np.cos(theta) - b_detector_y*np.sin(theta)
    b_detector_y_rotated = b_detector_x*np.sin(theta) + b_detector_y*np.cos(theta)
    
    b_detector_x = b_detector_x_rotated + 5.    # translation by 5. is here
    b_detector_y = b_detector_y_rotated
    
    coords = []

    for i in range(n):
        x0 = t_detector_x[i]
        y0 = t_detector_y[i]
        x1 = t_pinhole_x
        y1 = t_pinhole_y
        m = (y1-y0)/(x1-x0)
        b = (y0*x1-y1*x0)/(x1-x0)
        y2 = -100.
        x2 = (y2-b)/m
        line = LineString([(x0, y0), (x2, y2)])
        circle = Point(0., 0.).buffer(100.).boundary
        segment = line.difference(circle)[1]
        x0, y0 = segment.coords[0]
        x1, y1 = segment.coords[1]
        coords.append(['top', x0, y0, x1, y1])

    for i in range(n):
        x0 = f_detector_x[i]
        y0 = f_detector_y[i]
        x1 = f_pinhole_x
        y1 = f_pinhole_y
        m = (y1-y0)/(x1-x0)
        b = (y0*x1-y1*x0)/(x1-x0)
        x2 = -100.
        y2 = m*x2+b
        line = LineString([(x0, y0), (x2, y2)])
        circle = Point(0., 0.).buffer(100.).boundary
        segment = line.difference(circle)[1]
        x0, y0 = segment.coords[0]
        x1, y1 = segment.coords[1]
        coords.append(['front', x0, y0, x1, y1])

    for i in range(n):
        x0 = b_detector_x[i]
        y0 = b_detector_y[i]
        x1 = b_pinhole_x
        y1 = b_pinhole_y
        m = (y1-y0)/(x1-x0)
        b = (y0*x1-y1*x0)/(x1-x0)
        y2 = 100.
        x2 = (y2-b)/m
        line = LineString([(x0, y0), (x2, y2)])
        circle = Point(0., 0.).buffer(100.).boundary
        segment = line.difference(circle)[1]
        x0, y0 = segment.coords[0]
        x1, y1 = segment.coords[1]
        coords.append(['bottom', x0, y0, x1, y1])

    cameras = pd.DataFrame(coords, columns=['camera', 'x0', 'y0', 'x1', 'y1'])

    return cameras

# -------------------------------------------------------------------------

def plot_cameras(cameras):
    
    for (i, row) in enumerate(cameras.itertuples()):
        if row.camera == 'top':
            color = 'darkturquoise'
        elif row.camera == 'front':
            color = 'limegreen'
        elif row.camera == 'bottom':
            color = 'orange'
        plt.plot([row.x0, row.x1], [row.y0, row.y1], color)

    circle = plt.Circle((0., 0.), 100., color='k', fill=False)
    plt.gca().add_artist(circle)

    plt.plot(0., 0., 'k+')

    plt.gca().set_aspect('equal')

    plt.xlabel('x (mm)')
    plt.ylabel('y (mm)')

    plt.title('cameras')

    plt.show()
