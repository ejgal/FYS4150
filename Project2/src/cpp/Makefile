GPP= g++ -Wall
LIB= -larmadillo -llapack -lblas

main:	linalg.o main.cpp
	${GPP} -o main main.cpp linalg.o ${LIB}

linalg.o:	linalg.cpp
	${GPP} -c linalg.cpp ${LIB}


test: linalg.o test.cpp
	${GPP} -o test test.cpp linalg.o ${LIB}
