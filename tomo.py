from __future__ import print_function

import numpy as np
from skimage.draw import ellipse
import matplotlib.pyplot as plt
import matplotlib.animation as ani

# -------------------------------------------------------------------------

def get_tomo(projections, signals_data, signals_time):
   
    P = projections.reshape((projections.shape[0], -1))
    print('P:', P.shape, P.dtype)

    n_rows = projections.shape[1]
    n_cols = projections.shape[2]

    Dh = np.eye(n_rows*n_cols) - np.roll(np.eye(n_rows*n_cols), 1, axis=1)
    Dv = np.eye(n_rows*n_cols) - np.roll(np.eye(n_rows*n_cols), n_cols, axis=1)

    print('Dh:', Dh.shape, Dh.dtype)
    print('Dv:', Dv.shape, Dv.dtype)

    ii, jj = ellipse(n_rows//2, n_cols//2, n_rows//2, n_cols//2)
    mask = np.ones((n_rows, n_cols))
    mask[ii,jj] = 0.

    Io = np.eye(n_rows*n_cols) * mask.flatten()

    print('Io:', Io.shape, Io.dtype)

    Pt = np.transpose(P)
    PtP = np.dot(Pt, P)

    DtDh = np.dot(np.transpose(Dh), Dh)
    DtDv = np.dot(np.transpose(Dv), Dv)
    ItIo = np.dot(np.transpose(Io), Io)

    alpha = 1e5

    inv = np.linalg.inv(PtP + alpha*DtDh + alpha*DtDv + alpha*ItIo)

    M = np.dot(inv, Pt)

    dt = 0.0001

    tomo = []
    tomo_t = np.arange(0., signals_time[0,-1], dt)

    for t in tomo_t:
        i = np.argmin(np.fabs(signals_time[0] - t))
        f = signals_data[:,i].reshape((-1, 1))
        g = np.dot(M, f)
        tomo.append(g.reshape((n_rows, n_cols)))

    tomo = np.array(tomo)
    
    return tomo, tomo_t

# -------------------------------------------------------------------------

def plot_tomo(shot, tomo, tomo_t):

    fontsize = 'small'
    
    digits = np.max([len(('%g' % t).split('.')[-1]) for t in tomo_t])

    xmin = -100
    xmax = +100
    ymin = -100
    ymax = +100

    vmin = 0.
    vmax = np.max(tomo)

    im = plt.imshow(tomo[0],
                    vmin=vmin, vmax=vmax,
                    extent=[xmin, xmax, ymin, ymax],
                    interpolation='bicubic',
                    animated=True)

    fig = plt.gcf()
    ax = plt.gca()

    title = 'ISTTOK shot #%d t=%.*fs' % (shot, digits, tomo_t[0])
    ax.set_title(title, fontsize=fontsize)
    ax.tick_params(labelsize=fontsize)
    ax.set_xlabel('x (mm)', fontsize=fontsize)
    ax.set_ylabel('y (mm)', fontsize=fontsize)
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

    plt.setp(ax.spines.values(), linewidth=0.1)
    plt.tight_layout()

    def animate(k):
        title = 'ISTTOK shot #%d t=%.*fs' % (shot, digits, tomo_t[k])
        ax.set_title(title, fontsize=fontsize)
        im.set_data(tomo[k])

    animation = ani.FuncAnimation(fig, animate, frames=range(tomo.shape[0]))

    fname = '%d.mp4' % shot
    print('Writing:', fname)
    animation.save(fname, fps=30, extra_args=['-vcodec', 'libx264'])
