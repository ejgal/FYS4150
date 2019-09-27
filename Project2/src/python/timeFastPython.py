
import cythonJacobi
import numbaJacobi


Ns = [100, 120, 150, 180, 200, 220, 250, 275, 300]
runs = 5

with open('../../data/fastpythonRuns.dat','w') as file:
    file.write('n, numba, cython\n')
for i in range(len(Ns)):
#     dataPython[i,0]
    timeCython = cythonJacobi.timeJacobi(Ns[i], runs)[2]
    timeNumba = numbaJacobi.timeJacobi(Ns[i], runs)[2]
    with open('../../data/fastpythonRuns.dat','a') as file:
        for j in range(len(timeNumba)):
            file.write('{},{:.8f},{:.8f} \n'.format(Ns[i],timeNumba[j], timeCython[j]))
