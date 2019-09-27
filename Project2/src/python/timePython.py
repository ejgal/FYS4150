
import cythonJacobi
import numbaJacobi
import pythonJacobi


Ns = [5,10,20,25,30,40,50,60,70, 80]
runs = 5

with open('../../data/pythonRuns.dat','w') as file:
    file.write('n,python, cython, numba\n')
for i in range(len(Ns)):
#     dataPython[i,0]
    timePython = pythonJacobi.timeJacobi(Ns[i], runs)[2]
    timeNumba = numbaJacobi.timeJacobi(Ns[i], runs)[2]
    timeCython = cythonJacobi.timeJacobi(Ns[i], runs)[2]
    with open('../../data/pythonRuns.dat','a') as file:
        for j in range(len(timePython)):
            file.write('{},{:.8f},{:.8f},{:.8f} \n'.format(Ns[i],timePython[j],timeNumba[j], timeCython[j]))
