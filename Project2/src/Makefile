GPP= g++ -Wall
LIB= -larmadillo -llapack -lblas

main:	linalg.o test
	${GPP} -o main main.cpp linalg.o ${LIB}

linalg.o:	linalg.cpp
	${GPP} -c linalg.cpp ${LIB}


test: linalg.o
	${GPP} -o test test.cpp linalg.o ${LIB}
