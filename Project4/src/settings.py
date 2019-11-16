import matplotlib.pyplot as plt
import numpy as np

# Analytical value for critical temperature
analytic = 2/np.log(1+np.sqrt(2))



# Directory settings
DATADIR = '../data/'
FIGDIR = '../figures/'

# Plot settings
colwidth = 418.25368
width = colwidth / 72.27
height = width / 1.618
figsize = [width, height]
fontsize = 12
ticksize = 8
legendsize = 10
DPI = 300


def get_size(columns=2,ratio=False):
    colwidth = 418.25368
    if columns == 1:
        colwidth *= 0.5
    width = colwidth / 72.27
    if not ratio:
        height = width / 1.618
    else:
        height = ratio*width
    return [width, height]




plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)

plt.rc('figure', autolayout=True)
plt.rc('figure', figsize=[width, height])
plt.rc('figure', dpi=DPI)

plt.rc('xtick', labelsize=ticksize)
plt.rc('ytick', labelsize=ticksize)

plt.rc('axes', labelsize=fontsize)
plt.rc('axes', titlesize=fontsize)

plt.rc('legend', fontsize=legendsize)
plt.rc('legend', numpoints=1)
plt.rc('legend', handletextpad=0.3)
