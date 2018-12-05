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
    
    theta = np.radians(-82.5)

    b_pinhole_x = 5. + 102.*np.cos(theta)
    b_pinhole_y = 102.*np.sin(theta)

    n = 16          # number of detectors per camera
    size = 0.75     # detector size
    space = 0.2     # space between detectors
    dist = 9.0      # distance from camera to pinhole

    t_detector_x = t_pinhole_x - (n*size + (n-1)*space)/2. + size/2. + np.arange(n)*(size + space)
    t_detector_y = (t_pinhole_y + dist) * np.ones(n)

    f_detector_x = (f_pinhole_x + dist) * np.ones(n)
    f_detector_y = f_pinhole_y + (n*size + (n-1)*space)/2. - size/2. - np.arange(n)*(size + space)

    dist = 13.0      # distance from camera to pinhole (different for the bottom camera)

    b_detector_x = (n*size + (n-1)*space)/2. - size/2. - np.arange(n)*(size + space)
    b_detector_y = - dist * np.ones(n)

    theta = np.radians(7.5)

    b_detector_rotated_x = b_detector_x*np.cos(theta) - b_detector_y*np.sin(theta)
    b_detector_rotated_y = b_detector_x*np.sin(theta) + b_detector_y*np.cos(theta)

    b_detector_x = b_pinhole_x + b_detector_rotated_x
    b_detector_y = b_pinhole_y + b_detector_rotated_y

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
