import matplotlib.pyplot as plt
colwidth = 418.25368
width = colwidth / 72.27
# width = 3.487
height = width / 1.618
figsize = [width, height]
fontsize = 10
plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=fontsize)
plt.rc('ytick', labelsize=fontsize)
plt.rc('axes', labelsize=fontsize)
plt.rc('figure', figsize=[width, height])
plt.rc('figure', dpi=900)
