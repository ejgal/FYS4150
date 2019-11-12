import matplotlib.pyplot as plt

# Directory settings
DATADIR = '../data/'
FIGDIR = '../figures/'

# Plot settings
colwidth = 418.25368
width = colwidth / 72.27
height = width / 1.618
figsize = [width, height]
fontsize = 16
ticksize = 10
DPI = 100
plt.rc('font', family='serif', serif='Times')
plt.rc('figure', autolayout=True)
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=ticksize)
plt.rc('ytick', labelsize=ticksize)
plt.rc('axes', labelsize=fontsize)
plt.rc('figure', figsize=[width, height])
plt.rc('figure', dpi=DPI)
